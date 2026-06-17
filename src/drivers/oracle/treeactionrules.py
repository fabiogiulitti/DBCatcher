import logging as log
import math
from json import dumps
from textwrap import dedent
from urllib.parse import urlparse

import oracledb
from attr import define
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6.QtCore import Qt

from main.core.ActonTypeEnum import ActionTypeEnum
from main.core.config import crypto_manager
from main.core.driver.abstractdataresponse import AbstractDataResponse, TextResponse
from main.core.driver.abstractdriver import AbstractTreeAction
from main.core.treepath import ItemAction, TreePath, make_session_id, references
from main.core.util.util import AbstractConnectionStrategy, ConnectionProxy
from main.widgets.ContentData import ContentData, ContentDataModel


#log = logging.getLogger()


@define
class DataResponse(AbstractDataResponse):
    _cols: list
    _rows: list
    _query: str
    _metaData: dict

    @property
    def rows(self):
        return self._rows

    def toJson(self):
        result = [dict(zip(self._cols, row)) for row in self._rows]
        text = dumps(result, default=str, indent=4)
        return ContentData(text, self._query, self._metaData)

    def toTabular(self):
        model = QStandardItemModel(len(self._rows), len(self._cols))
        model.setHorizontalHeaderLabels(self._cols)
        print("step 1")
        for r, row in enumerate(self._rows):
            print("step 2")
            for c, value in enumerate(row):
                try:
                    if isinstance(value, (bytes, oracledb.LOB)):
                        item = QStandardItem("[UNMAPPED]")
                    else:
                        item = QStandardItem(str(value))
                except Exception as e:
                    log.error("unmappable value {}", value)
                    raise
                if isinstance(value, (int, float)):
                    item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignCenter)
                elif isinstance(value, bool):
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                else:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignCenter)
                item.setEditable(False)
                item.setSelectable(True)
                
                model.setItem(r, c, item)
        log.info("filled model")
        return ContentDataModel(model, self._query, self._metaData)

    def toTree(self):
        pass

    def metadata(self):
        return self._metaData


def _q(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'


class ORTreeActions(AbstractTreeAction):

    def __init__(self) -> None:
        super().__init__()
        methods = [self.__getattribute__(n) for n in self.__dir__()
                   if hasattr(getattr(self, n), 'action_type')]
        for method in methods:
            node_type_in = getattr(method, 'node_type_in')
            sub_actions = self._itemActions.get(node_type_in, {})
            sub_actions[getattr(method, 'action_type')] = method
            self._itemActions[node_type_in] = sub_actions
        methods = [self.__getattribute__(n) for n in self.__dir__()
                   if hasattr(getattr(self, n), 'node_type_out')]
        for method in methods:
            node_type_in = getattr(method, 'node_type_in')
            holder_type: str = getattr(method, 'holder_type')
            if holder_type != 'default':
                sub_item: dict = self._navActions.get(node_type_in, dict())
                sub_item[holder_type] = method
                self._navActions[node_type_in] = sub_item
            else:
                self._navActions[node_type_in] = {'default': method}

    @TreePath(node_type_in='connections', node_type_out='schemas')
    def retrieveSchemas(self, ctx: dict):
        connection_uri = ctx['connection_uri']
        conn = ConnectionProxy(
            ConnectionStrategy,
        crypto_manager.decrypt(connection_uri),
            None,
            )
        id = make_session_id()
        references[id] = {'client': conn, 'connection_uri': connection_uri}
        try:
            cur = conn.cursor()

            cur.execute("""
                SELECT username
                FROM all_users
                WHERE username IN (SELECT DISTINCT owner FROM all_objects)
                ORDER BY username
            """)
            schemas = [row[0] for row in cur.fetchall()]
            
            return (schemas, id)
        except Exception as e:
            log.error(f"Error during Oracle connection: {e}")
            raise
        finally:
            cur.close()


    @TreePath(node_type_in='schemas', node_type_out='schema_obj_hold')
    def retrieveSchemaHolding(self, ctx: dict):
        return (
            ['tables', 'views', 'materialized views', 'procedures', 'packages', 'sequences'],
            ctx['sessionID'],
        )

    @TreePath(node_type_in='schema_obj_hold', node_type_out='tables', holder_type='tables')
    def retrieveTables(self, ctx: dict):
        return self._listObjects(ctx, """
            SELECT table_name
            FROM all_tables
            WHERE owner = :owner
            ORDER BY table_name
        """)

    @TreePath(node_type_in='schema_obj_hold', node_type_out='views', holder_type='views')
    def retrieveViews(self, ctx: dict):
        return self._listObjects(ctx, """
            SELECT view_name
            FROM all_views
            WHERE owner = :owner
            ORDER BY view_name
        """)

    @TreePath(node_type_in='schema_obj_hold', node_type_out='materialized views', holder_type='materialized views')
    def retrieveMaterializedViews(self, ctx: dict):
        return self._listObjects(ctx, """
            SELECT mview_name
            FROM all_mviews
            WHERE owner = :owner
            ORDER BY mview_name
        """)

    @TreePath(node_type_in='schema_obj_hold', node_type_out='procedures', holder_type='procedures')
    def retrieveProcedures(self, ctx: dict):
        id = ctx['sessionID']
        schema = ctx['path'][-2]
        conn = references[id]['client']
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT object_name, object_type
                FROM all_procedures
                WHERE owner = :owner
                  AND object_type IN ('PROCEDURE', 'FUNCTION')
                  AND procedure_name IS NULL
                ORDER BY object_name
            """, owner=schema)
            rows = cur.fetchall()
            
            return ([f"{name} ({obj_type})" for name, obj_type in rows], id)
        finally:
            cur.close()

    @TreePath(node_type_in='schema_obj_hold', node_type_out='packages', holder_type='packages')
    def retrievePackages(self, ctx: dict):
        return self._listObjects(ctx, """
            SELECT object_name
            FROM all_objects
            WHERE owner = :owner
              AND object_type = 'PACKAGE'
            ORDER BY object_name
        """)

    @TreePath(node_type_in='schema_obj_hold', node_type_out='sequences', holder_type='sequences')
    def retrieveSequences(self, ctx: dict):
        return self._listObjects(ctx, """
            SELECT sequence_name
            FROM all_sequences
            WHERE sequence_owner = :owner
            ORDER BY sequence_name
        """)

    def _listObjects(self, ctx: dict, query: str):
        id = ctx['sessionID']
        schema = ctx['path'][-2]
        conn = references[id]['client']
        try:
            cur = conn.cursor()
            cur.execute(query, owner=schema)
            result = [row[0] for row in cur.fetchall()]
            return (result, id)
        finally:
            cur.close()

    @TreePath(node_type_in='tables', node_type_out='tables_obj_hold')
    def retrieveTabHolding(self, ctx: dict):
        return (['columns', 'indexes'], ctx['sessionID'])

    @TreePath(node_type_in='tables_obj_hold', node_type_out='columns', holder_type='columns')
    def retrieveColumns(self, ctx: dict):
        id = ctx['sessionID']
        schema_name = ctx['path'][-4]
        table_name = ctx['path'][-2]

        conn = references[id]['client']
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT column_name, data_type, data_length
                FROM all_tab_columns
                WHERE owner = :owner
                  AND table_name = :tname
                ORDER BY column_id
            """, owner=schema_name, tname=table_name)
            cols = [f"{n} {t} {ln}" for n, t, ln in cur.fetchall()]
            return (cols, id)
        finally:
            cur.close()

    @TreePath(node_type_in='tables_obj_hold', node_type_out='indexes', holder_type='indexes')
    def retrieveIndexes(self, ctx: dict):
        id = ctx['sessionID']
        schema_name = ctx['path'][-4]
        table_name = ctx['path'][-2]

        conn = references[id]['client']
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT index_name
                FROM all_indexes
                WHERE owner = :owner
                  AND table_name = :tname
                ORDER BY index_name
            """, owner=schema_name, tname=table_name)
            result = [row[0] for row in cur.fetchall()]
            return (result, id)
        finally:
            cur.close()

    @ItemAction(node_type_in='tables', action_type=ActionTypeEnum.CLICK)
    def retrieveFirstRowsTable(self, ctx: dict):
        log.info("retrieve table")
        return getRows(ctx)

    @ItemAction(node_type_in='views', action_type=ActionTypeEnum.CLICK)
    def retrieveFirstRowsView(self, ctx: dict):
        return getRows(ctx)

    @ItemAction(node_type_in='materialized views', action_type=ActionTypeEnum.CLICK)
    def retrieveFirstRowsMatView(self, ctx: dict):
        return getRows(ctx)

    @ItemAction(node_type_in='tables', action_type=ActionTypeEnum.DDL)
    def retrieveTableDDL(self, ctx: dict):
        return self._retrieveDDL(ctx, 'TABLE')

    @ItemAction(node_type_in='views', action_type=ActionTypeEnum.DDL)
    def retrieveViewDDL(self, ctx: dict):
        return self._retrieveDDL(ctx, 'VIEW')

    @ItemAction(node_type_in='materialized views', action_type=ActionTypeEnum.DDL)
    def retrieveMaterializedViewDDL(self, ctx: dict):
        return self._retrieveDDL(ctx, 'MATERIALIZED_VIEW')

    @ItemAction(node_type_in='procedures', action_type=ActionTypeEnum.DDL)
    def retrieveProcedureDDL(self, ctx: dict):
        ctx_copy = ctx.copy()
        ctx_copy['path'] = list(ctx['path'])
        raw = ctx_copy['path'][-1]
        name, obj_type = _split_proc_label(raw)
        ctx_copy['path'][-1] = name
        return self._retrieveDDL(ctx_copy, obj_type)

    @ItemAction(node_type_in='packages', action_type=ActionTypeEnum.DDL)
    def retrievePackageDDL(self, ctx: dict):
        session_id = ctx['sessionID']
        schema_name = ctx['path'][-3]
        package_name = ctx['path'][-1]
        conn = references[session_id]['client']
        query = "SELECT DBMS_METADATA.GET_DDL(:otype, :oname, :owner) FROM dual"
        parts: list[str] = []
        cur = conn.cursor()
        try:
            for otype in ('PACKAGE', 'PACKAGE_BODY'):
                try:
                    cur.execute(query, otype=otype, oname=package_name, owner=schema_name)
                    row = cur.fetchone()
                except oracledb.DatabaseError as e:
                    # PACKAGE_BODY potrebbe non esistere: ORA-31603 / ORA-04043
                    log.info(f"No {otype} for {schema_name}.{package_name}: {e}")
                    continue
                if row is None or row[0] is None:
                    continue
                ddl_value = row[0]
                text = ddl_value.read() if hasattr(ddl_value, 'read') else str(ddl_value)
                parts.append(text.strip())
            if not parts:
                ddl = f"-- DDL non available per {schema_name}.{package_name}"
            else:
                ddl = "\n\n".join(parts)
            return TextResponse(ddl, query, ctx)
        finally:
            cur.close()

    def _retrieveDDL(self, ctx: dict, object_type: str):
        id = ctx['sessionID']
        schema_name = ctx['path'][-3]
        object_name = ctx['path'][-1]
        conn = references[id]['client']
        try:
            cur = conn.cursor()
            query = (
                "SELECT DBMS_METADATA.GET_DDL(:otype, :oname, :owner) FROM dual"
            )
            cur.execute(query, otype=object_type, oname=object_name, owner=schema_name)
            row = cur.fetchone()
            if row is None or row[0] is None:
                ddl = f"-- DDL non available per {schema_name}.{object_name}"
            else:
                ddl_value = row[0]
                ddl = ddl_value.read() if hasattr(ddl_value, 'read') else str(ddl_value)
                ddl = ddl.strip()
            return TextResponse(ddl, query, ctx)
        finally:
            cur.close()


def _split_proc_label(raw: str) -> tuple[str, str]:
    if '(' in raw and raw.endswith(')'):
        name, _, type_part = raw.rpartition(' (')
        return name.strip(), type_part[:-1].strip()
    return raw, 'PROCEDURE'


def getRows(ctx: dict, cur_page: int = 0, dim_page: int = 200):
    id = ctx['sessionID']
    schema_name = ctx['path'][-3]
    tab_name = ctx['path'][-1]
    conn = references[id]['client']
    skip = cur_page * dim_page
    tot_result, last_page = getTableCount(dim_page, schema_name, tab_name, conn)
    cur = conn.cursor()
    try:
        query = dedent(f"""
                SELECT *
                FROM {_q(schema_name)}.{_q(tab_name)}
                OFFSET {skip} ROWS
                FETCH NEXT {dim_page} ROWS ONLY
        """).lstrip()
        cur.execute(query)
        assert cur.description
        cols = [desc[0] for desc in cur.description]
        rows = cur.fetchall()
        query = query.replace("*", ", ".join(cols), 1)
    except Exception as e: 
        log.error("Error in getRows {}", e)
    finally:
        cur.close()

    metadata = ctx.copy()
    metadata['cur_page'] = cur_page
    metadata['last_page'] = last_page
    metadata['dim_page'] = dim_page
    metadata['tot_result'] = tot_result
    return DataResponse(cols, rows, query, metadata)


def getTableCount(dim_page, schema_name, tab_name, conn):
    try:
        cur = conn.cursor()
        query = f"SELECT COUNT(*) FROM {_q(schema_name)}.{_q(tab_name)}"
        cur.execute(query)
        num_rows = cur.fetchone()[0]
        last_page = math.ceil(num_rows / dim_page - 1) if num_rows else 0
    except Exception as e:
        log.error("Error in count {}", e)
    finally:
        cur.close()
    return num_rows, last_page



def replaceBigColumns(cursor, metadata):
    
    if metadata.type in (oracledb.DB_TYPE_BLOB, oracledb.DB_TYPE_CLOB):
        def dimensionReplaceConverter(value):
            return f"[{str(metadata.type.name)}({value.size()} bytes)]"
            
        return cursor.var(metadata.type, arraysize=cursor.arraysize, outconverter=dimensionReplaceConverter)
    elif metadata.type in (oracledb.DB_TYPE_CLOB, 
                         oracledb.DB_TYPE_LONG_RAW):
        
        def dimensionReplaceConverter(value):
            return f"[{str(metadata.type.name)}({len(value)} bytes)]"
            
        return cursor.var(metadata.type, arraysize=cursor.arraysize, outconverter=dimensionReplaceConverter)


class ConnectionStrategy(AbstractConnectionStrategy[oracledb.Connection]):
    timeout = 20  # minutes

    @staticmethod
    def connect(params: dict[str, str]):
        connection_uri = params['connection_uri']
        parsed = urlparse(connection_uri)
        if parsed.scheme not in ('oracle', 'oracledb', 'oracle+thin'):
            raise ValueError(
                f"Unsupported Oracle URI scheme: {parsed.scheme!r}. "
                f"Use oracle://user:password@host:port/service_name"
            )
        host = parsed.hostname or 'localhost'
        port = parsed.port or 1521
        service = (parsed.path or '').lstrip('/')
        if not service:
            raise ValueError(
                "Oracle URI must include the service name (path component): "
                "oracle://user:password@host:port/service_name"
            )
        dsn = f"{host}:{port}/{service}"
        log.debug(f"Connecting to Oracle dsn={dsn} user={parsed.username}")
        connection = oracledb.connect(
            user=parsed.username,
            password=parsed.password,
            dsn=dsn
        )
        connection.outputtypehandler = replaceBigColumns
        return connection

    @staticmethod
    def isConnected(conn: oracledb.Connection) -> bool:
        try:
            return bool(conn) and conn.is_healthy()
        except Exception:
            return False

    @staticmethod
    def close(conn: oracledb.Connection):
        try:
            conn.close()
        except Exception:
            pass
