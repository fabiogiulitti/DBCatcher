import drivers.mongodb.treeactionrules as treeactionrules
import drivers.mongodb.contentactionrules
from core.treepath import rules, actions, contentActions

def executeTreeNav(ctx: dict):
    return rules[ctx['levelTag']](ctx)


def executeTreeAction(ctx: dict):
    return actions['clicked'][ctx['levelTag']](ctx)


def executeCntAction(ctx: dict):
    return contentActions[ctx['action_type']][ctx['action_obj']](ctx)
