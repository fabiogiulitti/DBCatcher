from itertools import count
from main.core.ActonTypeEnum import ActionTypeEnum


class AbstractDriver:

    def __init__(self) -> None:
        self._actions = dict()


    def executeAction(self, action_type: ActionTypeEnum, ctx: dict):
        return self._actions[action_type](ctx)


class AbstractTreeAction:

    def __init__(self) -> None:
        self._navActions = dict()
        self._itemActions = dict()

        
    def executeAction(self, node_type_in: str, action_type: ActionTypeEnum, ctx: dict):
        if action_type is ActionTypeEnum.EXPAND:
            return self._navActions[node_type_in](ctx)
        elif action_type is ActionTypeEnum.CLICK and node_type_in in self._itemActions:
            return self._itemActions[node_type_in][action_type](ctx)
        else:
            return None
    
    def executeNavAction(self, nodeTypeIn: str, nodeTypeOut: str, ctx: dict):
        item: dict = self._navActions[nodeTypeIn]
        if len(item) > 1:
            return item[nodeTypeOut](ctx)
        else:
            return item['default'](ctx)
