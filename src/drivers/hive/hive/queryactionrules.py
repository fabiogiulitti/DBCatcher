from enum import Enum
import threading
from main.core.treepath import ContentAction
from main.core.treepath import references
from main.core.driver.abstractdriver import AbstractDriver
from drivers.hive.hive.treeactionrules import DataResponse
from main.core.ActonTypeEnum import ActionTypeEnum
import time
from impala.hiveserver2 import HiveServer2Cursor

_lock = threading.Lock()

class QueryStatus(Enum):
    RUNNING = 1
    FINISHED = 2
    CANCELED = 3

class PSQueryActionDef(AbstractDriver):


    def __init__(self) -> None:
        super().__init__()
        methods = [self.__getattribute__(n) for n in self.__dir__() if hasattr(getattr(self, n), 'action_type')]
        for method in methods:
            self._actions[getattr(method, 'action_type')] = method
        

    @ContentAction(action_type=ActionTypeEnum.CTRL_ENTER)
    def executeQuery(self, ctx: dict, dim_page=50):
        id = ctx['sessionID']

        conn = references[id]['client']
        try:
            cur: HiveServer2Cursor = conn.cursor()
            cur.status
            references[id]['query_status'] = QueryStatus.RUNNING
            query = ctx['query']
            cur.execute_async(query)
            while True:
                 is_executing = cur.is_executing()
                 if references[id]['query_status'] == QueryStatus.CANCELED:
                     cur.cancel_operation()
                     return None
                 elif is_executing:
                     time.sleep(5)
                 else:
                     references[id]['query_status'] = QueryStatus.FINISHED
                     break

            rows = cur.fetchall()
            cols = [desc[0] for desc in (cur.description or [])]
            cur.close()
            references[id].pop('query_status')
        
            metadata = ctx.copy()
            metadata['cur_page'] = 0
            metadata['dim_page'] = dim_page
            metadata['last_page'] = 0
            metadata.pop('tot_result', 0)
            return DataResponse(cols, rows, query, metadata)
        except Exception as e:
            cur.close()
            references[id].pop('query_status')
            raise e


    @ContentAction(action_type=ActionTypeEnum.CANCEL_QUERY)
    def cancelAction(self, ctx: dict):
        id = ctx['sessionID']
        query_status = references[id]['query_status']
        if query_status == QueryStatus.RUNNING:
            with _lock:
                references[id]['query_status'] = QueryStatus.CANCELED
        metadata = {"query_status": query_status}
#            return DataResponse([], [], "", metadata)
        return None
