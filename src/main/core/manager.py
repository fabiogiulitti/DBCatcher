import logging
from typing import Optional
from main.core.driver.dbdriver import AbstractDbDriver
import main.core.driver.abstractdriver as car
from main.core.driver import abstractdataresponse
from drivers.hive import HiveSQLDriver
from drivers.mongodb import MongoDriver

from main.core.treepath import drivers
from main.core.ActonTypeEnum import DriverTypeEnum, ObjectTypeEnum
from drivers.postgresql import PostgreSQLDriver

log = logging.getLogger(__name__)

psd = PostgreSQLDriver()
drivers[DriverTypeEnum.POSTGRESQL.name] = psd
inst = MongoDriver()
drivers[DriverTypeEnum.MONGODB.name] = inst
hvd = HiveSQLDriver()
drivers[DriverTypeEnum.HIVE.name] = hvd

def executeTreeNav(ctx: dict):
    driver: AbstractDbDriver = drivers[ctx['type'].name]
    obj: car.AbstractTreeAction = driver.getObject(ObjectTypeEnum.DB_TREE)
    path = ctx.get("path", [''])
    result = obj.executeNavAction(ctx['levelTag'], path[-1], ctx)
    if not result:
        log.info("Expansion [%s] on tree level [%s] not found", path[-1], ctx['levelTag'])
    return result


def executeTreeAction(ctx: dict) -> Optional[abstractdataresponse.AbstractDataResponse]:
    driver: AbstractDbDriver = drivers[ctx['type'].name]
    obj: car.AbstractTreeAction = driver.getObject(ObjectTypeEnum.DB_TREE)
    result = obj.executeAction(ctx['levelTag'], ctx['action_type'], ctx)
    if not result:
        log.info("Action [%s] on tree level [%s] not found", ctx['action_type'], ctx['levelTag'])
    return result


def executeCntAction(ctx: dict):    
    driver: AbstractDbDriver = drivers[ctx['type'].name]
    obj: car.AbstractDriver = driver.getObject(ctx['action_obj'])
    return obj.executeAction(ctx['action_type'], ctx)

