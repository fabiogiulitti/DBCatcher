import threading
from main.core.treepath import ContentAction
from main.core.treepath import references
from main.core.driver.abstractdriver import AbstractDriver
from drivers.hive.hive.treeactionrules import DataResponse
from main.core.ActonTypeEnum import ActionTypeEnum
from pyhive import hive
import time
from TCLIService import ttypes

_lock = threading.Lock()

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
            cur: hive.Cursor = conn.cursor()
            references[id]['query_status'] = ttypes.TOperationState.RUNNING_STATE
            query = ctx['query']
            cur.execute(query, async_=True)
            while True:
                status = cur.poll()
                if references[id]['query_status'] == ttypes.TOperationState.CANCELED_STATE:
                    cur.cancel()
                    print("cancelled")
                    return None
                elif status.operationState == ttypes.TOperationState.RUNNING_STATE:
                    print("slip")
                    time.sleep(5)
                elif status.operationState == ttypes.TOperationState.FINISHED_STATE:
                    print("finished")
                    break
                else: #if status.operationState in (ttypes.TOperationState.ERROR_STATE, ttypes.TOperationState.CANCELED_STATE):
                    print(status.operationState)
                    return None

            rows = cur.fetchall()
            cols = [desc[0] for desc in cur.description]
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
        if query_status == ttypes.TOperationState.RUNNING_STATE:
            with _lock:
                references[id]['query_status'] = ttypes.TOperationState.CANCELED_STATE
        metadata = {"query_status": query_status}
        print(references[id]['query_status'])
#            return DataResponse([], [], "", metadata)
        return None
