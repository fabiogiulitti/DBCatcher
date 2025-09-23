import logging
import math
from main.core.ActonTypeEnum import ActionTypeEnum
from main.core.driver.abstractdataresponse import AbstractDataResponse
from main.core.treepath import ItemAction, TreePath,make_session_id, references
from json import dumps
from main.core.util.util import AbstractConnectionStrategy, ConnectionProxy
from main.widgets.ContentData import ContentData, ContentDataModel
from main.core.driver.abstractdriver import AbstractTreeAction
from attr import ib, s
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from textwrap import dedent
from pyhive import hive

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

        
    @TreePath(node_type_in='connections', node_type_out='catalogs')
    def retrieveCatalogs(self, ctx: dict):
        id = make_session_id()
        try:
#            conn = hive.Connection(host=ctx['host'], port=ctx['port'])
            conn = ConnectionProxy(ConnectionStrategy, host=ctx['host'], port=ctx['port'])
            references[id] = {
                'client': conn,
                'host' : ctx['host'],
                'port': ctx['port']
                }

            cursor = conn.cursor()
            cursor.execute("SHOW CATALOGS")
            catalogs = [row[0] for row in cursor.fetchall()]

            result = []
            for cat in catalogs:
                result.append(cat)

            cursor.close()
            print("fine metodo")
        except Exception as e:
            logging.info(f"Errore connetting to Hive-Kyuubi: {ctx} {e}")
            raise e

        return (result, id)


    @TreePath(node_type_in='catalogs', node_type_out='databases')
    def retrieveDatabases(self, ctx: dict):
        id = ctx["sessionID"]
        catalog = ctx['path'][-1]
        try:
            conn = references[id]['client']
    
            cursor = conn.cursor()
            cursor.execute(f"SHOW DATABASES in {catalog}")
            databases = [row[0] for row in cursor.fetchall()]

            result = []
            for db in databases:
                result.append(db)

            cursor.close()
#            conn.close()
        except Exception as e:
            print(f"Errore durante la connessione a Hive-Kyuubi: {e}")

        return (result, id)


    @TreePath(node_type_in='databases', node_type_out='database_obj_hold')
    def retrieveObjHolding(self, ctx: dict):
        return (['tables', 'views', 'indexes', 'procedures'],ctx['sessionID'])


    @TreePath(node_type_in='database_obj_hold', node_type_out='tables')
    def retrieveTables(self, ctx: dict):
        return self.retrieveDbObjects(ctx, 'tables')

#    @TreePath(node_type_in='database_obj_hold', node_type_out='views')
#    def retrieveViews(self, ctx: dict):
#        return self.retrieveDbObjects(ctx, 'tables')
    
    def retrieveDbObjects(self, ctx, objType):
        id = ctx['sessionID']
        database = ctx['path'][-2]

        conn = references[id]['client']
        try:
            cur = conn.cursor()
            cur.execute(f"""
                SHOW {objType} IN {database}
            """)
            tables = cur.fetchall()

            result = list(map(lambda r: r[1], tables))
        except Exception as e:
            print(f"Errore durante la connessione a Hive-Kyuubi: {e}")

        return (result, id)
    

    @TreePath(node_type_in='tables', node_type_out='tables_obj_hold')
    def retrieveTabHolding(self, ctx: dict):
        return (['columns'],ctx['sessionID'])


    @TreePath(node_type_in='tables_obj_hold', node_type_out='columns', holder_type='columns')
    def retrieveColumns(self, ctx: dict):
        id = ctx['sessionID']
        databaseName = ctx['path'][-4]
        tableName = ctx['path'][-2]
        
        conn = references[id]['client']
        cur = conn.cursor()
        cur.execute(f"describe {databaseName}.{tableName}")

        columns = cur.fetchall()
        result = list(map(lambda n: f"{n[0]} {n[1]} {n[2]}", columns))

        return (result, id)
    
    @TreePath(node_type_in='tables_obj_hold', node_type_out='indexes', holder_type='indexes')
    def retrieveIndexes(self, ctx: dict):
        return ["(NOT DEFINED)"],ctx['sessionID']


    @ItemAction(node_type_in='tables', action_type = ActionTypeEnum.CLICK)
    def retrieveFirstRows(self, ctx: dict):
        return getRows(ctx)


def getRows(ctx: dict, cur_page: int = 0, dim_page: int = 50):
    id = ctx['sessionID']
    databaseName = ctx['path'][1]
    tabName = ctx['path'][-1]

    conn = references[id]['client']
#    skip = curPage * dimPage

#    tot_result,last_page = getTableCount(dimPage, databaseName, tabName, conn)
    tot_result,last_page = (None, 0)
    
    cur = conn.cursor()
    references[id]['cursor'] = cur
    query = dedent(f"""
                   SELECT *
                   FROM {databaseName}.{tabName}
                   limit {dim_page}
        """).lstrip()

    cur.execute(query)
    rows = cur.fetchall()
    cols = [desc[0] for desc in cur.description]
    cur.close()
    references[id].pop('cursor')
    
    meta_data = ctx.copy()
    meta_data['cur_page'] = cur_page
    meta_data['dim_page'] = dim_page
    meta_data['last_page'] = last_page
    meta_data['tot_result'] = tot_result
    return DataResponse(cols, rows, query, meta_data)


def getTableCount(dim_page, database_name, tab_name, conn):
    cur = conn.cursor()
    cur.execute(f"""
                select count(*) as numRecords
                from {database_name}.{tab_name}
            """)
    num_rows = cur.fetchone()[0]
    last_page = math.ceil(num_rows / dim_page - 1)
    cur.close()
    return num_rows, last_page


class ConnectionStrategy(AbstractConnectionStrategy[hive.Connection]):
    timeout = 2 #minutes
    close = hive.Connection.close

    @staticmethod
    def connect(params: dict[str, str]):
        host = params['host']

        port = params['port']
        logging.debug(f"Connecting to Hive... {params}")
        connection = hive.Connection(host=host, port=port)
        logging.debug(f"Connected to Hive... {params} {connection.sessionHandle.sessionId}")
        return connection


    @staticmethod
    def isConnected(conn):
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchall()
            return True
        except Exception:
            logging.debug("Hive connection is close")
            return False
