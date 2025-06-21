import math
from os import path
from sys import exception
import psycopg2
from requests import patch
from main.core.ActonTypeEnum import ActionTypeEnum
from main.core.driver.abstractdataresponse import AbstractDataResponse
from main.core.treepath import ItemAction, TreePath,make_session_id, references
from json import dumps
from main.widgets.ContentData import ContentData, ContentDataModel
from main.core.driver.abstractdriver import AbstractTreeAction
from psycopg2 import connect, extensions
from attr import ib, s
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from textwrap import dedent

@s
class DataResponse(AbstractDataResponse):
    _cols: list = ib()
    _rows: list = ib()
    _query: str = ib()
    _metaData: dict = ib()

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
            self._itemActions[getattr(method, 'node_type_in')] = {getattr(method, 'action_type') : method}
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
        id = make_session_id()

        try:
            
            conn = connect(ctx['connection_uri'])
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

        return (result,id)


    @TreePath(node_type_in='databases', node_type_out='schemas')
    def retrieveSchemas(self, ctx: dict):
        id = ctx['sessionID']
        connection_uri = references[id]['connection_uri']
        dsn = extensions.make_dsn(connection_uri, dbname = ctx['path'][0])
        conn = connect(dsn)

        cur = conn.cursor()
        cur.execute("""     
            SELECT schema_name
            FROM information_schema.schemata
        """)

        schemas = cur.fetchall()
        result = map(lambda n: n[0], schemas)

        references[id]['client'] = conn
        return (result, id)


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
    
    @TreePath(node_type_in='schema_obj_hold', node_type_out='materialized views', holder_type='functions')
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
    
def getRows(ctx: dict, cur_page: int = 0, dim_page: int = 200):
    id = ctx['sessionID']
    schema_name = ctx['path'][1]
    tab_name = ctx['path'][-1]

    conn = references[id]['client']
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
