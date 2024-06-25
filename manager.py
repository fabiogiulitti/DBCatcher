import navigationrules
from treepath import rules

def getNav(ctx: str):
    return rules[ctx['levelTag']](ctx)
