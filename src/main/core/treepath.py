from uuid import uuid4
from main.core.ActonTypeEnum import ActionTypeEnum
from functools import wraps

drivers = dict()
references = dict()

class Node():
    def __init__(self, nodeType, items, session=None):
        self.nodeType = nodeType
        self.items = items
        self.session = session
        self.leaf = False
        
def TreePath(node_type_in: str, node_type_out: str, holder_type: str = 'default'):
    def decorator(func):
        @wraps(func)
        def wrapper(self, param: dict):
            result,id = func(self, param)
            node = Node(node_type_out, result,id)
            if node_type_out not in self._navActions:
                node.leaf = True
            return node

        setattr(wrapper, "node_type_in", node_type_in)
        setattr(wrapper, "node_type_out", node_type_out)
        setattr(wrapper, "holder_type", holder_type)
        #rules[node_type_in] = wrapper
        return wrapper
    return decorator


def make_session_id():
    id = uuid4()
    return id


def ItemAction(node_type_in: str, action_type: ActionTypeEnum):
    def decorator(func):
        @wraps(func)
        def wrapper(self, param: dict):
            result = func(self, param)
            return result;

        setattr(wrapper, "node_type_in", node_type_in)
        setattr(wrapper, "action_type", action_type)
        return wrapper
    return decorator


def ContentAction(action_type: ActionTypeEnum):
    def decorator(func):
        @wraps(func)
        def wrapper(self, param: dict):
            result = func(self, param)
            return result;

        setattr(wrapper, 'action_type', action_type)
        return wrapper
    return decorator
