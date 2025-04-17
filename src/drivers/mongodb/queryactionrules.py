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
        
        query: str = dedent(ctx['query']).strip()
        print(query)
        parser = QueryParser()
        query_elements = parser.parse(query)
        
        col: Collection = db[query_elements[0]]
        col.aggregate
        method = getattr(col, query_elements[1][0][0])
        if "aggregate" == query_elements[1][0][0]:
            cursor: pymongo.cursor.Cursor = method(query_elements[1][0][1])
        else:
            cursor: pymongo.cursor.Cursor = method(*query_elements[1][0][1])

        is_limited = False
        for element in query_elements[1][1:]:
            if "limit" == element[0]:
                is_limited = True
            method = getattr(cursor, element[0])
            cursor = method(element[1])

        docs = list()
        if isinstance(cursor, Iterable):
            if not is_limited and "aggregate" != query_elements[1][0][0]:
                cursor.limit(25)
                query = query + ".limit(25)"
            for doc in cursor:
                docs.append(doc)
        else:
            docs.append({"countDocuments": cursor})

        metaData = ctx.copy()
#        metaData['cur_page'] = curPage
#        metaData['last_page'] = lastPage
        return MongoDataResponse(docs, query, metaData)
