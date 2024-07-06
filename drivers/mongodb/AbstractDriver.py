from core.ActonTypeEnum import ActionTypeEnum


class AbstractDriver:

    _actions = dict()


    def executeAction(self, action_type: ActionTypeEnum, ctx: dict):
        return self._actions[action_type](ctx)


class AbstractTreeAction:

    _navActions = dict()

    _itemActions = dict()


#    def executeAction(self, node_type_in: str, ctx: dict):
#        return self._navActions[node_type_in](ctx)
        
    def executeAction(self, node_type_in: str, action_type: ActionTypeEnum, ctx: dict):
        if action_type is ActionTypeEnum.EXPAND:
            return self._navActions[node_type_in](ctx)
        else:
            return self._itemActions[node_type_in][action_type](ctx)
    