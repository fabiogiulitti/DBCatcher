from enum import Enum


class ActionTypeEnum(Enum):
    EXPAND = 'expand'
    CLICK = 'click'
    NEXT_PAGE = 'next_page'
    PREVIOUS_PAGE = 'previous_page'

class ObjectTypeEnum(Enum):
    TEXT_AREA = 'text_area'
    QUERY_EDIT = 'query_edit'
    DB_TREE = 'db_tree'

class DriverTypeEnum(Enum):
    MONGODB = 'MongoDB'
    POSTGRESQL = 'PostgreSQL'
    ORACLE = 'Oracle'
    MYSQL = 'MySql'

    @classmethod
    def from_value(cls, value):
        for item in cls:
            if item.value == value:
                return item
        raise ValueError(f"{value} not found in {cls.__name__}")

