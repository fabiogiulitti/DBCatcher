from core.treepath import ContentAction
from core.treepath import references
from core.driver.abstractdriver import AbstractDriver
from drivers.hive.hive.treeactionrules import DataResponse
from core.ActonTypeEnum import ActionTypeEnum
from pyhive import hive

class PSQueryActionDef(AbstractDriver):


    def __init__(self) -> None:
        super().__init__()
        methods = [self.__getattribute__(n) for n in self.__dir__() if hasattr(getattr(self, n), 'action_type')]
        for method in methods:
            self._actions[getattr(method, 'action_type')] = method
        

    @ContentAction(action_type=ActionTypeEnum.CTRL_ENTER)
    def executeQuery(self, ctx: dict):
        id = ctx['sessionID']

        conn = references[id]['client']
    
        cur = conn.cursor()
        query = ctx['query']
        cur.execute(query)
        rows = cur.fetchall()
        cols = [desc[0] for desc in cur.description]
        cur.close()
    
        metaData = ctx.copy()
        return DataResponse(cols, rows, query, metaData)
