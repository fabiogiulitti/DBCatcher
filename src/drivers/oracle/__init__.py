# Package definition for Oracle driver

from main.core.driver.dbdriver import AbstractDbDriver
from main.core.ActonTypeEnum import ObjectTypeEnum
from drivers.oracle.contentactionrules import ORActionDef
from drivers.oracle.treeactionrules import ORTreeActions
from drivers.oracle.tabularactionrules import ORTabularActionDef
from drivers.oracle.queryactionrules import ORQueryActionDef


class OracleDriver(AbstractDbDriver):

    def __init__(self) -> None:
        super().__init__()
        self._objects[ObjectTypeEnum.TEXT_AREA] = ORActionDef()
        self._objects[ObjectTypeEnum.DB_TREE] = ORTreeActions()
        self._objects[ObjectTypeEnum.TABULAR] = ORTabularActionDef()
        self._objects[ObjectTypeEnum.QUERY_EDIT] = ORQueryActionDef()
