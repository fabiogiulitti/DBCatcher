from uuid import uuid4
from core.ActonTypeEnum import ActionTypeEnum

drivers = dict()
references = dict()

class Node():
    def __init__(self, nodeType, items, session=None):
        self.nodeType = nodeType
        self.items = items
        self.session = session
        self.leaf = False
        
def TreePath(node_type_in: str, node_type_out: str):
    def decorator(func):
        def wrapper(self, param: dict):
            result,id = func(self, param)
            node = Node(node_type_out, result,id)
            if node_type_out not in self._navActions:
                node.leaf = True
            return node
            return result;

        setattr(wrapper, "node_type_in", node_type_in)
        setattr(wrapper, "node_type_out", node_type_out)
        #rules[node_type_in] = wrapper
        return wrapper
    return decorator


def make_session_id():
    id = uuid4()
    return id


def ItemAction(node_type_in: str, action_type: ActionTypeEnum):
    def decorator(func):
        def wrapper(self, param: dict):
            result = func(self, param)
            return result;

        setattr(wrapper, "node_type_in", node_type_in)
        setattr(wrapper, "action_type", action_type)
        #actions[action_type] = {node_type_in : wrapper}
        return wrapper
    return decorator


def ContentAction(action_type: ActionTypeEnum):
    def decorator(func):
        def wrapper(self, param: dict):
            result = func(self, param)
            return result;

        setattr(wrapper, 'action_type', action_type)
        #contentActions[action_type] = {obj_type : wrapper}
        return wrapper
    return decorator
