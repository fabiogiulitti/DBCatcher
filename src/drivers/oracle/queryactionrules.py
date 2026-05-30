import re

from main.core.ActonTypeEnum import ActionTypeEnum
from main.core.driver.abstractdriver import AbstractDriver
from main.core.treepath import ContentAction, references
from drivers.oracle.treeactionrules import DataResponse


class ORQueryActionDef(AbstractDriver):

    def __init__(self) -> None:
        super().__init__()
        methods = [self.__getattribute__(n) for n in self.__dir__()
                   if hasattr(getattr(self, n), 'action_type')]
        for method in methods:
            self._actions[getattr(method, 'action_type')] = method

    @ContentAction(action_type=ActionTypeEnum.CTRL_ENTER)
    def _executeQuery(self, ctx: dict):
        return executeQuery(ctx)


def executeQuery(ctx: dict, dim_page: int = 200):
    id = ctx['sessionID']
    conn = references[id]['client']
    cur = conn.cursor()
    try:
        query: str = ctx['query'].rstrip().rstrip(';')
        match_select = re.match(r'\s*SELECT\b', query, flags=re.IGNORECASE)
        match_fetch = re.search(r'\bFETCH\s+(?:FIRST|NEXT)\s+\d+', query, flags=re.IGNORECASE)
        if match_select and not match_fetch:
            query = f"{query} FETCH FIRST {dim_page} ROWS ONLY"
        cur.execute(query)
        if cur.description is None:
            rows = [[cur.rowcount]]
            cols = ["Affected rows"]
        else:
            rows = cur.fetchall()
            cols = [desc[0] for desc in cur.description]
        metadata = ctx.copy()
        metadata['cur_page'] = 0
        metadata['dim_page'] = dim_page
        metadata['last_page'] = 0
        metadata.pop('tot_result', 0)
        return DataResponse(cols, rows, query, metadata)
    finally:
        cur.close()
