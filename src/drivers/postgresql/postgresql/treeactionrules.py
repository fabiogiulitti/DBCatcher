import math

from main.core.ActonTypeEnum import ActionTypeEnum
from main.core.driver.abstractdataresponse import AbstractDataResponse, TextResponse
from main.core.treepath import ItemAction, TreePath,make_session_id, references
from json import dumps
from main.core.util.util import AbstractConnectionStrategy, ConnectionProxy
from main.widgets.ContentData import ContentData, ContentDataModel
from main.core.driver.abstractdriver import AbstractTreeAction
from psycopg2 import connect, extensions
from attr import define
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from textwrap import dedent


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
        result = list()
        for row in self._rows:
            result.append(dict(zip(self._cols, row)))
        text = dumps(result, default=str, indent=4)
        return ContentData(text, self._query, self._metaData)
    
    def toTabular(self):
        model = QStandardItemModel(len(self._rows), len(self._cols))
        model.setHorizontalHeaderLabels(self._cols)

        for row in range(len(self._rows)):
            for col in range(len(self._cols)):
                item = QStandardItem(str(self._rows[row][col]))
                item.setEditable(False)
                item.setSelectable(True)
                model.setItem(row, col, item)

        return ContentDataModel(model, self._query, self._metaData)
    

    def toTree(self):
        pass


    def metadata(self):
        return self._metaData


class PSTreeActions(AbstractTreeAction):
    
    def __init__(self) -> None:
        super().__init__()
        methods = [self.__getattribute__(n) for n in self.__dir__() if hasattr(getattr(self, n), 'action_type')]
        for method in methods:
            node_type_in = getattr(method, 'node_type_in')
            sub_actions = self._itemActions.get(node_type_in, {})
            sub_actions[getattr(method, 'action_type')] = method
            self._itemActions[node_type_in] = sub_actions
        methods = [self.__getattribute__(n) for n in self.__dir__() if hasattr(getattr(self, n), 'node_type_out')]
        for method in methods:
            nodeTypeIn = getattr(method, 'node_type_in')
            holderType: str = getattr(method, 'holder_type')
            if holderType != 'default':
                subItem: dict = self._navActions.get(nodeTypeIn, dict())
                subItem[holderType] = method
                self._navActions[nodeTypeIn] = subItem
            else:
                self._navActions[nodeTypeIn] = {'default' : method}

        

    @TreePath(node_type_in='connections', node_type_out='databases')
    def retrieveDatabases(self, ctx: dict):
#        id = make_session_id()
        try:
            conn = connect(ctx['connection_uri'])
            id = make_session_id()
            references[id] = {'connection_uri' : ctx['connection_uri']}
            cursor = conn.cursor()
            cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")

            databases = cursor.fetchall()
            result = []
            for db in databases:
                result.append(db[0])

            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Errore durante la connessione a PostgreSQL: {e}")
            raise e

        return (result,id)


    @TreePath(node_type_in='databases', node_type_out='schemas')
    def retrieveSchemas(self, ctx: dict):
        id_server = ctx['sessionID']
        id_db = make_session_id()
        connection_uri = references[id_server]['connection_uri']
        try:
            conn = ConnectionProxy(ConnectionStrategy, connection_uri, ctx['path'][0])
            
            cur = conn.cursor()
            cur.execute("""     
                SELECT schema_name
                FROM information_schema.schemata
            """)

            schemas = cur.fetchall()
            result = map(lambda n: n[0], schemas)
            print(result)
            references[id_db] = {'client' : conn }

            cur.close()

            return (result, id_db)
        except Exception as e:
            print(f"Eccezione {e}")
            cur.close()
            conn.rollback()
            raise e


    @TreePath(node_type_in='schemas', node_type_out='schema_obj_hold')
    def retrieveSchemaHolding(self, ctx: dict):
        return (['tables','views','materialized views','functions','sequences'],ctx['sessionID'])


    @TreePath(node_type_in='schema_obj_hold', node_type_out='tables', holder_type='tables')
    def retrieveTables(self, ctx: dict):
        objType = getattr(self.retrieveTables, 'holder_type')
        return self._retrieveDbObjects(ctx, 'BASE TABLE')

    @TreePath(node_type_in='schema_obj_hold', node_type_out='views', holder_type='views')
    def retrieveViews(self, ctx: dict):
        objType = getattr(self.retrieveViews, 'holder_type')
        return self._retrieveDbObjects(ctx, 'VIEW')
    
    @TreePath(node_type_in='schema_obj_hold', node_type_out='materialized views', holder_type='materialized views')
    def retrieveMaterializedViews(self, ctx: dict):
        id = ctx['sessionID']
        schema = ctx['path'][-2]
        conn = references[id]['client']
        cur = conn.cursor()
        query = f"""
            SELECT matviewname
            FROM pg_catalog.pg_matviews
            WHERE schemaname = '{schema}'
        """

        cur.execute(query)

        mat_views = cur.fetchall()
        result = map(lambda n: n[0], mat_views)

        cur.close()
        return (result, id)
    
    @TreePath(node_type_in='schema_obj_hold', node_type_out='functions', holder_type='functions')
    def retrieveFunctions(self, ctx: dict):
        schema = ctx['path'][-2]

        query = f"""
                SELECT routine_name, routine_type
                FROM information_schema.routines
                where routine_schema = '{schema}'
            """
        
        id = ctx['sessionID']
        conn = references[id]['client']
        try:
            cur = conn.cursor()
            cur.execute(query)

            functions = cur.fetchall()
            result = map(lambda r: f"{r[0]} ({r[1]})", functions)

            cur.close()
            return (result, id)
        except Exception:
            cur.close()
            conn.rollback()
            raise
        
    
    def _retrieveDbObjects(self, ctx, objType):
        id = ctx['sessionID']
        schema = ctx['path'][-2]
        
        conn = references[id]['client']
        cur = conn.cursor()
        query = f"""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = '{schema}'
            AND table_type = '{objType}'
        """
        cur.execute(query)
        tables = cur.fetchall()
        result = map(lambda n: n[0], tables)

        cur.close()

        return (result, id)
    

    @TreePath(node_type_in='tables', node_type_out='tables_obj_hold')
    def retrieveTabHolding(self, ctx: dict):
        return (['columns','indexes'],ctx['sessionID'])


    @TreePath(node_type_in='tables_obj_hold', node_type_out='columns', holder_type='columns')
    def retrieveColumns(self, ctx: dict):
        id = ctx['sessionID']
        schema_name = ctx['path'][-4]
        table_name = ctx['path'][-2]
        
        conn = references[id]['client']
        cur = conn.cursor()
        cur.execute(f"""
            SELECT column_name, data_type, character_maximum_length
            FROM information_schema.columns
                    where table_schema = '{schema_name}'
                    and table_name = '{table_name}'
                    order by ordinal_position
        """)

        columns = cur.fetchall()
        result = map(lambda n: f"{n[0]} {n[1]} {n[2]}", columns)

        cur.close()

        return (result, id)
    
    @TreePath(node_type_in='tables_obj_hold', node_type_out='indexes', holder_type='indexes')
    def retrieveIndexes(self, ctx: dict):
        id = ctx['sessionID']
        schema_name = ctx['path'][-4]
        table_name = ctx['path'][-2]

        conn = references[id]['client']
        cur = conn.cursor()
        query = f"""
            SELECT indexname
            FROM pg_catalog.pg_indexes
            WHERE schemaname = '{schema_name}'
            and tablename = '{table_name}'
        """

        cur.execute(query)

        indexes = cur.fetchall()
        result = map(lambda n: n[0], indexes)

        cur.close()
        return (result, id)


    @ItemAction(node_type_in='tables', action_type = ActionTypeEnum.CLICK)
    def retrieveFirstRowsTable(self, ctx: dict):
        return getRows(ctx)

    @ItemAction(node_type_in='views', action_type = ActionTypeEnum.CLICK)
    def retrieveFirstRowsView(self, ctx: dict):
        return getRows(ctx)
    
    @ItemAction(node_type_in='materialized views', action_type = ActionTypeEnum.CLICK)
    def retrieveFirstRowsMatView(self, ctx: dict):
        return getRows(ctx)
    
    @ItemAction(node_type_in='tables', action_type = ActionTypeEnum.DDL)
    def retrieveTableDDL(self, ctx: dict):
        id = ctx['sessionID']
        try:
            schema_name = ctx['path'][-3]
            table_name = ctx['path'][-1]

            conn = references[id]['client']
            cur = conn.cursor()
            query = f"""
                SELECT column_name, data_type, character_maximum_length, is_nullable, column_default
                FROM information_schema.columns
                WHERE table_schema = '{schema_name}' AND table_name = '{table_name}'
                ORDER BY ordinal_position;
            """
            cur.execute(query)
            columns = cur.fetchall()

            if not columns:
                return f"-- Tabella {schema_name}.{table_name} non trovata."

            ddl = [f'CREATE TABLE {schema_name}."{table_name}" (']
            column_defs = []
            for col in columns:
                col_name, data_type, char_max_len, is_nullable, col_default = col
                col_def = f'    "{col_name}" {data_type}'
                if char_max_len:
                    col_def += f'({char_max_len})'
                if is_nullable == 'NO':
                    col_def += ' NOT NULL'
                if col_default:
                    col_def += f' DEFAULT {col_default}'
                column_defs.append(col_def)
    
            ddl.append(",\n".join(column_defs))
            ddl.append(');')
            result = "\n".join(ddl)
        except Exception:
            cur.close()
            conn.rollback()
            raise
    
        return TextResponse(result, query, ctx)
    
    @ItemAction(node_type_in='views', action_type = ActionTypeEnum.DDL)
    def retrieveViewDDL(self, ctx: dict):
        return self._retrieveDDL(ctx, 'view')

    @ItemAction(node_type_in='materialized views', action_type = ActionTypeEnum.DDL)
    def retrieveMaterializedViewDDL(self, ctx: dict):
        return self._retrieveDDL(ctx, 'materilized view')
    
    @ItemAction(node_type_in='functions', action_type = ActionTypeEnum.DDL)
    def retrieveFunctionDDL(self, ctx: dict):
        id = ctx['sessionID']
        try:
            schema_name = ctx['path'][-3]
            function_name = ctx['path'][-1].split(' ')[0]

            conn = references[id]['client']
            cur = conn.cursor()
            query = f"""
                SELECT pg_get_functiondef(p.oid)
                FROM pg_proc p
                JOIN pg_namespace n ON n.oid = p.pronamespace
                WHERE n.nspname = '{schema_name}' AND p.proname = '{function_name}'
            """
            cur.execute(query) 
            result = cur.fetchone()
            
    
            return TextResponse(result[0], query, ctx)
        except Exception as e:
            cur.close()
            conn.rollback()
            raise

    def _retrieveDDL(self, ctx: dict, view_type):
        id = ctx['sessionID']
        try:
            schema_name = ctx['path'][-3]
            view_name = ctx['path'][-1]

            conn = references[id]['client']
            cur = conn.cursor()
            query = f"SELECT pg_get_viewdef('{schema_name}.{view_name}'::regclass, true);"
        
            cur.execute(query,)
            view_definition = cur.fetchone()[0]
            result = f"CREATE {view_type} {schema_name}.{view_name} AS\n{view_definition};"
            return TextResponse(result, query, ctx)
        except Exception as e:
            cur.close()
            conn.rollback()
            raise


def getRows(ctx: dict, cur_page: int = 0, dim_page: int = 200):
    id = ctx['sessionID']
    schema_name = ctx['path'][1]
    tab_name = ctx['path'][-1]

    conn = references[id]['client']
    try:
        skip = cur_page * dim_page

        tot_result,last_page = getTableCount(dim_page, schema_name, tab_name, conn)
        
        cur: extensions.cursor = conn.cursor()
        query = dedent(f"""
                    SELECT *
                    FROM {schema_name}.{tab_name}
                    offset {skip}
                    limit {dim_page}
            """).lstrip()
        
        cur.execute(query)
        
        assert cur.description
        cols = [desc[0] for desc in cur.description]
        rows = cur.fetchall()
        cur.close()
        
        metadata = ctx.copy()
        metadata['cur_page'] = cur_page
        metadata['last_page'] = last_page
        metadata['dim_page'] = dim_page
        metadata['tot_result'] = tot_result
        return DataResponse(cols, rows, query, metadata)
    except Exception as e:
        cur.close()
        conn.rollback()
        raise e


def getTableCount(dimPage, schemaName, tabName, conn):
    cur = conn.cursor()
    cur.execute(f"""
                select count(*) as numRecords
                from {schemaName}.{tabName}
            """)
    num_rows = cur.fetchone()[0]
    last_page = math.ceil(num_rows / dimPage - 1)
    cur.close()
    return num_rows,last_page


class ConnectionStrategy(AbstractConnectionStrategy[extensions.connection]):
    timeout = 5 #minutes
    close = extensions.connection.close
    isCconnected = lambda c: c.closed == 0

    @staticmethod
    def connect(params: dict[str, str]):
        connection_uri = params['connection_uri']
        db_name = params['db_name']
        dsn = extensions.make_dsn(connection_uri, dbname = db_name)
        return connect(dsn)

