from core.treepath import ContentAction
from core.driver.abstractdriver import AbstractDriver
from drivers.mongodb.treeactionrules import getDocuments
from core.ActonTypeEnum import ActionTypeEnum
from drivers.postgresql.postgresql.treeactionrules import getRows

class PSTabularActionDef(AbstractDriver):


    def __init__(self) -> None:
        super().__init__()
        methods = [self.__getattribute__(n) for n in self.__dir__() if hasattr(getattr(self, n), 'action_type')]
        for method in methods:
            self._actions[getattr(method, 'action_type')] = method
        

    @ContentAction(action_type=ActionTypeEnum.NEXT_PAGE)
    def _retrieveMoreDocuments(self, ctx: dict):
        nextPage = ctx['cur_page'] + 1
        if nextPage <= ctx['last_page']:
            return getRows(ctx, nextPage)
        
    
    @ContentAction(action_type=ActionTypeEnum.PREVIOUS_PAGE)
    def _retrievePreviousDocuments(self, ctx: dict):
        curPage = ctx['cur_page']
        if curPage > 0:
            prevPage = curPage - 1
            return getRows(ctx, curPage=prevPage)
        else:
            return None

