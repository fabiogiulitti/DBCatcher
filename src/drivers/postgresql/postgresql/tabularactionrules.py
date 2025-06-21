from main.core.treepath import ContentAction
from main.core.driver.abstractdriver import AbstractDriver
from drivers.mongodb.treeactionrules import getDocuments
from main.core.ActonTypeEnum import ActionTypeEnum
from drivers.postgresql.postgresql.treeactionrules import getRows

class PSTabularActionDef(AbstractDriver):


    def __init__(self) -> None:
        super().__init__()
        methods = [self.__getattribute__(n) for n in self.__dir__() if hasattr(getattr(self, n), 'action_type')]
        for method in methods:
            self._actions[getattr(method, 'action_type')] = method
        

    @ContentAction(action_type=ActionTypeEnum.FIRST_PAGE)
    def _retrieveFirstDocuments(self, ctx: dict):
        print(ctx)
        return getRows(ctx, 0)
        

    @ContentAction(action_type=ActionTypeEnum.NEXT_PAGE)
    def _retrieveMoreDocuments(self, ctx: dict):
        print(ctx)
        next_page = ctx['cur_page'] + 1
        if next_page <= ctx['last_page']:
            return getRows(ctx, next_page)
        
    
    @ContentAction(action_type=ActionTypeEnum.PREVIOUS_PAGE)
    def _retrievePreviousDocuments(self, ctx: dict):
        print(ctx)
        cur_page = ctx['cur_page']
        if cur_page > 0:
            prev_page = cur_page - 1
            return getRows(ctx, cur_page=prev_page)
        else:
            return None
        

    @ContentAction(action_type=ActionTypeEnum.LAST_PAGE)
    def _retrieveLastDocuments(self, ctx: dict):
        last_page = ctx['last_page']
        return getRows(ctx, last_page)
