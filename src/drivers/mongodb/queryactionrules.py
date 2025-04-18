import re
import json
from textwrap import dedent
from typing import Collection, Iterable

import pymongo
import pymongo.cursor
from main.core.treepath import ContentAction
from main.core.treepath import references
from main.core.driver.abstractdriver import AbstractDriver
from drivers.mongodb.treeactionrules import MongoDataResponse
from main.core.ActonTypeEnum import ActionTypeEnum
from pymongo.collection import Collection

from drivers.mongodb.util.query_parser import QueryParser

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
        print(cursor)
        docs = list()
        if isinstance(cursor, Iterable):
            for doc in cursor:
                docs.append(doc)
        else:
            docs.append({"countDocuments": cursor})

        metaData = ctx.copy()
#        metaData['cur_page'] = curPage
#        metaData['last_page'] = lastPage
        return MongoDataResponse(docs, query, metaData)
