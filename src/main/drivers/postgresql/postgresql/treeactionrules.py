from ast import List
from importlib import metadata
import inspect
from platform import node
from core.ActonTypeEnum import ActionTypeEnum
from core.driver.abstractdataresponse import AbstractDataResponse
from core.treepath import ItemAction, TreePath,make_session_id, references
from json import dumps
from widgets.ContentData import ContentData, ContentDataModel
from core.driver.abstractdriver import AbstractTreeAction
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
            
            conn = connect(ctx['connectionURI'])
            references[id] = {'connection_uri' : ctx['connectionURI']}
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
        connectionURI = references[id]['connection_uri']
        dsn = extensions.make_dsn(connectionURI, dbname = ctx['path'][0])
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
    def retrieveObjHolding(self, ctx: dict):
        return (['tables','views'],ctx['sessionID'])


    @TreePath(node_type_in='schema_obj_hold', node_type_out='tables', holder_type='tables')
    def retrieveTables(self, ctx: dict):
        objType = getattr(self.retrieveTables, 'holder_type')
        return self.retrieveDbObjects(ctx, objType)

    @TreePath(node_type_in='schema_obj_hold', node_type_out='views', holder_type='views')
    def retrieveViews(self, ctx: dict):
        objType = getattr(self.retrieveViews, 'holder_type')
        return self.retrieveDbObjects(ctx, objType)
    
    def retrieveDbObjects(self, ctx, objType):
        id = ctx['sessionID']
        schema = ctx['path'][-2]
        
        conn = references[id]['client']
        cur = conn.cursor()
        cur.execute(f"""
            SELECT table_name
            FROM information_schema.{objType}
            WHERE table_schema = '{schema}'
        """)

        tables = cur.fetchall()
        result = map(lambda n: n[0], tables)

        return (result, id)
    

    @TreePath(node_type_in='tables', node_type_out='tables_obj_hold')
    def retrieveTabHolding(self, ctx: dict):
        return (['columns','indexes'],ctx['sessionID'])


    @TreePath(node_type_in='tables_obj_hold', node_type_out='columns', holder_type='columns')
    def retrieveColumns(self, ctx: dict):
        objType = getattr(self.retrieveColumns, 'holder_type')
        id = ctx['sessionID']
        tableName = ctx['path'][-2]
        
        conn = references[id]['client']
        cur = conn.cursor()
        cur.execute(f"""
            SELECT column_name, data_type, character_maximum_length
            FROM information_schema.columns
                    where table_name = '{tableName}'
        """)

        columns = cur.fetchall()
        result = map(lambda n: f"{n[0]} {n[1]} {n[2]}", columns)

        return (result, id)
    
    @TreePath(node_type_in='tables_obj_hold', node_type_out='indexes', holder_type='indexes')
    def retrieveIndexes(self, ctx: dict):
        return ["(NOT DEFINED)"],ctx['sessionID']


    @ItemAction(node_type_in='tables', action_type = ActionTypeEnum.CLICK)
    def retrieveFirstRows(self, ctx: dict):
        return getRows(ctx)


def getRows(ctx: dict, curPage: int = 0, dimPage: int = 25):
    id = ctx['sessionID']
    schemaName = ctx['path'][1]
    tabName = ctx['path'][-1]

    conn = references[id]['client']
    skip = curPage * dimPage

    lastPage = getTableCount(dimPage, schemaName, tabName, conn)
    
    cur = conn.cursor()
    query = dedent(f"""
                   SELECT *
                   FROM {schemaName}.{tabName}
                   offset {skip}
                   limit {dimPage}
        """).lstrip()

    cur.execute(query)
    rows = cur.fetchall()
    cols = [desc[0] for desc in cur.description]
    cur.close()
    
    metaData = ctx.copy()
    metaData['cur_page'] = curPage
    metaData['last_page'] = lastPage
    return DataResponse(cols, rows, query, metaData)


def getTableCount(dimPage, schemaName, tabName, conn):
    cur = conn.cursor()
    cur.execute(f"""
                select count(*) as numRecords
                from {schemaName}.{tabName}
            """)
    numRows = cur.fetchone()[0]
    lastPage = numRows / dimPage - 1
    cur.close()
    return lastPage
