import drivers.mongodb.AbstractDriver as car
import drivers.mongodb as mdb

from core.treepath import drivers
from core.ActonTypeEnum import DriverTypeEnum, ObjectTypeEnum, ActionTypeEnum

inst = mdb.MongoDriver()
drivers[DriverTypeEnum.MONGODB] = inst

def executeTreeNav(ctx: dict):
    driver: mdb.MongoDriver = drivers[DriverTypeEnum.MONGODB]
    obj: car.AbstractTreeAction = driver.getObject(ObjectTypeEnum.DB_TREE)
    return obj.executeAction(ctx['levelTag'], ActionTypeEnum.EXPAND, ctx)


def executeTreeAction(ctx: dict):
    driver: mdb.MongoDriver = drivers[DriverTypeEnum.MONGODB]
    obj: car.AbstractTreeAction = driver.getObject(ObjectTypeEnum.DB_TREE)
    return obj.executeAction(ctx['levelTag'], ctx['action_type'], ctx)


def executeCntAction(ctx: dict):
    driver: mdb.MongoDriver = drivers[DriverTypeEnum.MONGODB]
    obj: car.AbstractDriver = driver.getObject(ctx['action_obj'])
    return obj.executeAction(ctx['action_type'], ctx)

