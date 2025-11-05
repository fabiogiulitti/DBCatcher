from cProfile import label
from enum import Enum
from json import JSONEncoder

from attr import define

from main.widgets.model import viewtypeenum
from main.widgets.model.viewtypeenum import ViewTypeEnum


class ActionTypeEnum(Enum):
    EXPAND = 'expand'
    CLICK = 'click'
    EDIT_CONNECTION = 'edit_connection'
    DDL = 'ddl'
    FIRST_PAGE = 'first_page'
    PREVIOUS_PAGE = 'previous_page'
    NEXT_PAGE = 'next_page'
    LAST_PAGE = 'last_page'
    CTRL_ENTER = 'ctrl_enter'
    EXECUTE = 'execute'
    CANCEL_QUERY = 'cancel_query'


class ObjectTypeEnum(Enum):
    TEXT_AREA = 'text_area'
    QUERY_EDIT = 'query_edit'
    DB_TREE = 'db_tree'
    TABULAR = 'tabular'
    TREE = 'tree'


class DriverTypeEnum(Enum):
    MONGODB = ('MongoDB', ViewTypeEnum.TREE, ViewTypeEnum.JSON.value | ViewTypeEnum.TREE.value, True)
    POSTGRESQL = ('PostgreSQL', ViewTypeEnum.TABULAR, ViewTypeEnum.TABULAR.value, True)
    ORACLE = ('Oracle', ViewTypeEnum.TABULAR, ViewTypeEnum.TABULAR.value, True)
    MYSQL = ('MySql', ViewTypeEnum.TABULAR, ViewTypeEnum.TABULAR.value, True)
    HIVE = ('Hive/Kyuubi', ViewTypeEnum.TABULAR, ViewTypeEnum.TABULAR, False)

    def __init__(self, label, default_view, available_views, connection_uri_enabled: bool) -> None:
        self._label = label
        self._selected_view: ViewTypeEnum = default_view
        self._available_views = available_views
        self._connection_uri_enabled = connection_uri_enabled


    @classmethod
    def fromLabel(cls, label):
        for item in cls:
            if item._label == label:
                return item
        raise ValueError(f"{label=} not found in {cls.__name__}")


    @property
    def label(self):
        return self._label

    @property
    def selectedView(self):
        return self._selected_view

    @selectedView.setter
    def setSelectedView(self, view: ViewTypeEnum):
        self._selected_view = view

    @property
    def availableViews(self):
        return self._available_views

    @property
    def connectionURIEnabled(self):
        return self._connection_uri_enabled
