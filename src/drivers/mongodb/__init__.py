# Package definition for MongoDb driver

from core.driver.dbdriver import AbstractDbDriver
from core.ActonTypeEnum import ObjectTypeEnum
from drivers.mongodb.contentactionrules import MyDriver
from drivers.mongodb.treeactionrules import TreeActions

class MongoDriver(AbstractDbDriver):

    def __init__(self) -> None:
        super().__init__()
        self._objects[ObjectTypeEnum.TEXT_AREA] = MyDriver()
        self._objects[ObjectTypeEnum.DB_TREE] = TreeActions()
        
