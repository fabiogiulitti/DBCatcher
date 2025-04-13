# Package definition for hive/kyuubi driver

from main.core.driver.dbdriver import AbstractDbDriver
from main.core.ActonTypeEnum import ObjectTypeEnum
from drivers.hive.hive.contentactionrules import PSActionDef
from drivers.hive.hive.treeactionrules import PSTreeActions
from drivers.hive.hive.tabularactionrules import PSTabularActionDef
from drivers.hive.hive.queryactionrules import PSQueryActionDef


class HiveSQLDriver(AbstractDbDriver):


    def __init__(self) -> None:
        super().__init__()
        self._objects[ObjectTypeEnum.TEXT_AREA] = PSActionDef()
        self._objects[ObjectTypeEnum.DB_TREE] = PSTreeActions()
        self._objects[ObjectTypeEnum.TABULAR] = PSTabularActionDef()
        self._objects[ObjectTypeEnum.QUERY_EDIT] = PSQueryActionDef()
        

    