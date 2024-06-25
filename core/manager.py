import drivers.mongodb.treeactionrules as treeactionrules
import drivers.mongodb.contentactionrules
from core.treepath import rules
from core.itemaction import actions
from core.contentaction import contentActions

def getNav(ctx: dict):
    return rules[ctx['levelTag']](ctx)


def getAction(ctx: dict):
    return actions['clicked'][ctx['levelTag']](ctx)


def getCntAction(ctx: dict):
    return contentActions[ctx['action_type']][ctx['action_obj']](ctx)
