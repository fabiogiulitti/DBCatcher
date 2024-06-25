from uuid import uuid4


rules = {}
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


