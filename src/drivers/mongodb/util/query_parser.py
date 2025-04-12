import json
import re

import test


query = "db.product.find({'_id.code':{$eq: '1234'}}).sort({'field': -1}).skip(1(.)0).limit(2).pippo({)}).count()"


class QueryParser():
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(QueryParser, cls).__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        self._col_regex = r"(db\.)?(\w+)(?=\.)"
        self._func_regex = r"\.([a-z_]*)\((.*?)\)(?=\.|$)"

    def parse(self, query: str) -> tuple:
        colName = ''
        functions = []
        end = 0
        col_match = re.match(self._col_regex, query)
        if col_match is not None:
            colName = col_match.group(2)
            end = col_match.end()
        else:
            raise Exception("Collection name not found")
        
        func_matches = re.finditer(self._func_regex, query)
        for func_match in func_matches:
            if 2 != len(func_match.groups()):
                raise Exception("too many values")
            functions.append( (func_match.group(1), convert_if_json(func_match.groups())))
            if end != func_match.start():
                raise Exception(f"Unrecognized text {query[end:func_match.start()]}")
            end = func_match.end()

        if end < len(query):
            raise Exception(f"Unrecognized text {query[end:len(query)]}")
        return (colName, functions)


def convert_if_json(function):
    match function[0]:
        case "find":
            return json.loads(f"[{function[1]}]")
        case "sort":
            sortDict = json.loads(function[1])
            return tuple(sortDict.items())
        case "skip":
            return int(function[1])
        case "limit":
            return int(function[1])
        
    return function[1]