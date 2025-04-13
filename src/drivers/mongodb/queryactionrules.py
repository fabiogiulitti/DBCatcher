import re
import json
from typing import Collection

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

        query: str = ctx['query']
        parser = QueryParser()
        query_elements = parser.parse(query)
#        query_elements = query.split('.')
        
        col: Collection = db[query_elements[0]]

        method = getattr(col, query_elements[1][0][0])
        cursor: pymongo.cursor.Cursor = method(*query_elements[1][0][1])
        for element in query_elements[1][1:]:
            method = getattr(cursor, element[0])
            cursor = method(element[1])

        docs = list()
        for doc in cursor:
            docs.append(doc)
 
        metaData = ctx.copy()
#        metaData['cur_page'] = curPage
#        metaData['last_page'] = lastPage
        return MongoDataResponse(docs, query, metaData)
