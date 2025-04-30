from cProfile import label
from enum import Enum

from main.widgets.model import viewtypeenum
from main.widgets.model.viewtypeenum import ViewTypeEnum


class ActionTypeEnum(Enum):
    EXPAND = 'expand'
    CLICK = 'click'
    NEXT_PAGE = 'next_page'
    PREVIOUS_PAGE = 'previous_page'
    CTRL_ENTER = 'ctrl_enter'


class ObjectTypeEnum(Enum):
    TEXT_AREA = 'text_area'
    QUERY_EDIT = 'query_edit'
    DB_TREE = 'db_tree'
    TABULAR = 'tabular'


class DriverTypeEnum(Enum):
    MONGODB = ('MongoDB', ViewTypeEnum.JSON, ViewTypeEnum.JSON.value | ViewTypeEnum.TREE.value)
    POSTGRESQL = ('PostgreSQL', ViewTypeEnum.TABULAR, ViewTypeEnum.TABULAR.value)
    ORACLE = ('Oracle', ViewTypeEnum.TABULAR, ViewTypeEnum.TABULAR.value)
    MYSQL = ('MySql', ViewTypeEnum.TABULAR, ViewTypeEnum.TABULAR.value)
    HIVE = ('Hive/Kyuubi', ViewTypeEnum.TABULAR, ViewTypeEnum.TABULAR)

    def __init__(self, label, default_view, available_views) -> None:
        self.label = label
        self.default_view: ViewTypeEnum = default_view
        self.available_views = available_views


    @classmethod
    def fromLabel(cls, label):
        for item in cls:
            if item.label == label:
                return item
        raise ValueError(f"{label=} not found in {cls.__name__}")

