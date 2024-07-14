from cProfile import label
from enum import Enum

from widgets.model.viewtypeenum import ViewTypeEnum


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
    MONGODB = ('MongoDB', ViewTypeEnum.JSON)
    POSTGRESQL = ('PostgreSQL', ViewTypeEnum.TABULAR)
    ORACLE = ('Oracle', ViewTypeEnum.TABULAR)
    MYSQL = ('MySql', ViewTypeEnum.TABULAR)

    def __init__(self, label, view) -> None:
        self.label = label
        self.view = view


    @classmethod
    def fromLabel(cls, label):
        for item in cls:
            if item.label == label:
                return item
        raise ValueError(f"{label=} not found in {cls.__name__}")

