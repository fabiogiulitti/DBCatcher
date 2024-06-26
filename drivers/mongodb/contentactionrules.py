from core.treepath import ContentAction
from drivers.mongodb.treeactionrules import getDocuments
from core.ActonTypeEnum import ActonTypeEnum

@ContentAction(obj_type='edit', action_type=ActonTypeEnum.PAGE_DOWN.value)
def retrieveMoreDocuments(ctx: dict):
    nextPage = ctx['cur_page'] + 1
    print(f"vals {nextPage} {ctx['last_page']}")
    if nextPage <= ctx['last_page']:
        return getDocuments(ctx, curPage=nextPage)
    
@ContentAction(obj_type='edit', action_type=ActonTypeEnum.PAGE_UP.value)
def retrievePreviousDocuments(ctx: dict):
    curPage = ctx['cur_page']
    if curPage > 0:
        prevPage = curPage - 1
        return getDocuments(ctx, curPage=prevPage)
    else:
        return None
