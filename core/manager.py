from core.driver.dbdriver import AbstractDbDriver
import core.driver.abstractdriver as car
from drivers.mongodb import MongoDriver

from core.treepath import drivers
from core.ActonTypeEnum import ActionTypeEnum, DriverTypeEnum, ObjectTypeEnum
from drivers.postgresql import PostgreSQLDriver

psd = PostgreSQLDriver()
drivers[DriverTypeEnum.POSTGRESQL.name] = psd
inst = MongoDriver()
drivers[DriverTypeEnum.MONGODB.name] = inst

def executeTreeNav(ctx: dict):
    driver: AbstractDbDriver = drivers[ctx['type']]
    print(driver)
    obj: car.AbstractTreeAction = driver.getObject(ObjectTypeEnum.DB_TREE)
    return obj.executeAction(ctx['levelTag'], ActionTypeEnum.EXPAND, ctx)


def executeTreeAction(ctx: dict):
    driver: AbstractDbDriver = drivers[ctx['type']]
    obj: car.AbstractTreeAction = driver.getObject(ObjectTypeEnum.DB_TREE)
    return obj.executeAction(ctx['levelTag'], ctx['action_type'], ctx)



def executeCntAction(ctx: dict):
    driver: AbstractDbDriver = drivers[ctx['type']]
    obj: car.AbstractDriver = driver.getObject(ctx['action_obj'])
    return obj.executeAction(ctx['action_type'], ctx)

