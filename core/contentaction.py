from core.ActonTypeEnum import  ActonTypeEnum

contentActions = {}
        
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


