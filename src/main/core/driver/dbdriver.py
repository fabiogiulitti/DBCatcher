from core.ActonTypeEnum import ObjectTypeEnum


class AbstractDbDriver:
    def __init__(self) -> None:
        self._objects = dict()

    def getObject(self, objType: ObjectTypeEnum):
        return self._objects[objType]
