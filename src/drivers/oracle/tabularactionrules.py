from main.core.ActonTypeEnum import ActionTypeEnum
from main.core.driver.abstractdriver import AbstractDriver
from main.core.treepath import ContentAction
from drivers.oracle.treeactionrules import getRows


class ORTabularActionDef(AbstractDriver):

    def __init__(self) -> None:
        super().__init__()
        methods = [self.__getattribute__(n) for n in self.__dir__()
                   if hasattr(getattr(self, n), 'action_type')]
        for method in methods:
            self._actions[getattr(method, 'action_type')] = method

    @ContentAction(action_type=ActionTypeEnum.FIRST_PAGE)
    def _retrieveFirstRows(self, ctx: dict):
        return getRows(ctx, 0)

    @ContentAction(action_type=ActionTypeEnum.NEXT_PAGE)
    def _retrieveMoreRows(self, ctx: dict):
        next_page = ctx['cur_page'] + 1
        if next_page <= ctx['last_page']:
            return getRows(ctx, next_page)
        return None

    @ContentAction(action_type=ActionTypeEnum.PREVIOUS_PAGE)
    def _retrievePreviousRows(self, ctx: dict):
        cur_page = ctx['cur_page']
        if cur_page > 0:
            return getRows(ctx, cur_page=cur_page - 1)
        return None

    @ContentAction(action_type=ActionTypeEnum.LAST_PAGE)
    def _retrieveLastRows(self, ctx: dict):
        return getRows(ctx, ctx['last_page'])
