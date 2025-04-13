# Package definition for PostgreSQL driver

from main.core.driver.dbdriver import AbstractDbDriver
from main.core.ActonTypeEnum import ObjectTypeEnum
from drivers.postgresql.postgresql.contentactionrules import PSActionDef
from drivers.postgresql.postgresql.treeactionrules import PSTreeActions
from drivers.postgresql.postgresql.tabularactionrules import PSTabularActionDef
from drivers.postgresql.postgresql.queryactionrules import PSQueryActionDef


class PostgreSQLDriver(AbstractDbDriver):


    def __init__(self) -> None:
        super().__init__()
        self._objects[ObjectTypeEnum.TEXT_AREA] = PSActionDef()
        self._objects[ObjectTypeEnum.DB_TREE] = PSTreeActions()
        self._objects[ObjectTypeEnum.TABULAR] = PSTabularActionDef()
        self._objects[ObjectTypeEnum.QUERY_EDIT] = PSQueryActionDef()
        

    