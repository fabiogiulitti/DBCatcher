# Package definition for PostgreSQL driver

from core.driver.dbdriver import AbstractDbDriver
from core.ActonTypeEnum import ObjectTypeEnum
from drivers.postgresql.contentactionrules import PSActionDef
from drivers.postgresql.treeactionrules import PSTreeActions
from drivers.postgresql.tabularactionrules import PSTabularActionDef


class PostgreSQLDriver(AbstractDbDriver):


    def __init__(self) -> None:
        super().__init__()
        self._objects[ObjectTypeEnum.TEXT_AREA] = PSActionDef()
        self._objects[ObjectTypeEnum.DB_TREE] = PSTreeActions()
        self._objects[ObjectTypeEnum.TABULAR] = PSTabularActionDef()
        

    