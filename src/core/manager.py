from core.driver.dbdriver import AbstractDbDriver
import core.driver.abstractdriver as car
from core.driver import abstractdataresponse
from drivers.hive import HiveSQLDriver
from drivers.mongodb import MongoDriver

from core.treepath import drivers
from core.ActonTypeEnum import ActionTypeEnum, DriverTypeEnum, ObjectTypeEnum
from drivers.postgresql import PostgreSQLDriver

psd = HiveSQLDriver()
drivers[DriverTypeEnum.POSTGRESQL.name] = psd
inst = MongoDriver()
drivers[DriverTypeEnum.MONGODB.name] = inst
hvd = HiveSQLDriver()
drivers[DriverTypeEnum.HIVE.name] = hvd

def executeTreeNav(ctx: dict):
    driver: AbstractDbDriver = drivers[ctx['type'].name]
    obj: car.AbstractTreeAction = driver.getObject(ObjectTypeEnum.DB_TREE)
    path = ctx.get("path", [''])
    return obj.executeNavAction(ctx['levelTag'], path[-1], ctx)


def executeTreeAction(ctx: dict) -> abstractdataresponse.AbstractDataResponse:
    driver: AbstractDbDriver = drivers[ctx['type'].name]
    obj: car.AbstractTreeAction = driver.getObject(ObjectTypeEnum.DB_TREE)
    return obj.executeAction(ctx['levelTag'], ctx['action_type'], ctx)



def executeCntAction(ctx: dict):    
    driver: AbstractDbDriver = drivers[ctx['type'].name]
    obj: car.AbstractDriver = driver.getObject(ctx['action_obj'])
    return obj.executeAction(ctx['action_type'], ctx)

