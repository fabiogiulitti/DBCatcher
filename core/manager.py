import drivers.mongodb.actionrules as actionrules
from core.treepath import rules
from core.itemaction import actions

def getNav(ctx: str):
    return rules[ctx['levelTag']](ctx)

def getAction(ctx: str):
    return actions['clicked'][ctx['levelTag']](ctx)
