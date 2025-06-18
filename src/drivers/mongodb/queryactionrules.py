from textwrap import dedent
from typing import Iterable
from pymongo.cursor import Cursor
from main.core.treepath import ContentAction
from main.core.treepath import references
from main.core.driver.abstractdriver import AbstractDriver
from drivers.mongodb.treeactionrules import MongoDataResponse
from main.core.ActonTypeEnum import ActionTypeEnum


class MongoQueryActionDef(AbstractDriver):


    def __init__(self) -> None:
        super().__init__()
        methods = [self.__getattribute__(n) for n in self.__dir__() if hasattr(getattr(self, n), 'action_type')]
        for method in methods:
            self._actions[getattr(method, 'action_type')] = method
        

    @ContentAction(action_type=ActionTypeEnum.CTRL_ENTER)
    def _executeQuery(self, ctx: dict):
        id = ctx['sessionID']
        dbName = ctx['path'][0]
        colName = ctx['path'][2]
        
        db = references[id][dbName]
        scope = {'cursor': None,
                 'db': db}

        query: str = dedent(ctx['query']).strip()
        #exec('cursor = ' + query)
        exec(f"cursor = {query}", {}, scope)
        cursor = scope['cursor']
        docs = list()
        tot_result = 0
        if isinstance(cursor, Cursor):
            while (doc := next(cursor, None)) is not None and tot_result < 100:
#            for doc in cursor:
                docs.append(doc)
                tot_result += 1
        else:
            docs.append({"countDocuments": cursor})
            tot_result = 1

        metadata = ctx.copy()
        metadata['cur_page'] = 0
        metadata['last_page'] = 0
        metadata.pop("tot_result", 0)
        metadata['dim_page'] = tot_result
        return MongoDataResponse(docs, query, metadata)
