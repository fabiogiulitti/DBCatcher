from logging import raiseExceptions
import re
from main.core.treepath import ContentAction
from main.core.treepath import references
from main.core.driver.abstractdriver import AbstractDriver
from drivers.postgresql.postgresql.treeactionrules import DataResponse
from main.core.ActonTypeEnum import ActionTypeEnum

class PSQueryActionDef(AbstractDriver):


    def __init__(self) -> None:
        super().__init__()
        methods = [self.__getattribute__(n) for n in self.__dir__() if hasattr(getattr(self, n), 'action_type')]
        for method in methods:
            self._actions[getattr(method, 'action_type')] = method
        

    @ContentAction(action_type=ActionTypeEnum.CTRL_ENTER)
    def _executeQuery(self, ctx: dict):
        return executeQuery(ctx)


def executeQuery(ctx, dim_page=200):
    id = ctx['sessionID']

    conn = references[id]['client']

    try:
        cur = conn.cursor()
        query: str = ctx['query']
        match = re.search(r'\bLIMIT\s+\d+', query, flags=re.IGNORECASE)
        if match:
            dim_page = int(match.group().split(' ')[1])
        else:
            query = f"{query} LIMIT {dim_page}"

        cur.execute(query)
        rows = cur.fetchall()
        cols = [desc[0] for desc in cur.description]
        cur.close()
        metadata = ctx.copy()
        metadata['cur_page'] = 0
        metadata['dim_page'] = dim_page
        metadata['last_page'] = 0
        metadata.pop("tot_result", 0)
        return DataResponse(cols, rows, query, metadata)
    except Exception as e:
        cur.close()
        conn.rollback()
        raise e
