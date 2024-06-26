from uuid import uuid4


rules = {}
actions = {}
contentActions = {}
references = {}

class Node():
    def __init__(self, nodeType, items, session=None):
        self.nodeType = nodeType
        self.items = items
        self.session = session
        self.leaf = False
        
def TreePath(node_type_in: str, node_type_out: str):
    def decorator(func):
        def wrapper(param: dict):
            result,id = func(param)
            node = Node(node_type_out, result,id)
            if node_type_out not in rules:
                node.leaf = True
            return node
            return result;

        setattr(wrapper, TreePath.__name__, True)
        rules[node_type_in] = wrapper
        return wrapper
    return decorator


def make_session_id():
    id = uuid4()
    return id


def ItemAction(node_type_in: str, action_type: str):
    def decorator(func):
        def wrapper(param: dict):
            result = func(param)
            return result;

        setattr(wrapper, ItemAction.__name__, True)
        actions[action_type] = {node_type_in : wrapper}
        return wrapper
    return decorator


def ContentAction(obj_type: str, action_type: str):
    def decorator(func):
        def wrapper(param: dict):
            result = func(param)
            return result;

        setattr(wrapper, ContentAction.__name__, True)
        print(f"action {action_type}, obj {obj_type}")
        contentActions[action_type] = {obj_type : wrapper}
        return wrapper
    return decorator
