actions = {}
        
def ItemAction(node_type_in: str, action_type: str):
    def decorator(func):
        def wrapper(param: dict):
            result = func(param)
            return result;

        setattr(wrapper, ItemAction.__name__, True)
        actions[action_type] = {node_type_in : wrapper}
        return wrapper
    return decorator


