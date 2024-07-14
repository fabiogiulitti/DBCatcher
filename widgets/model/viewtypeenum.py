from enum import Enum
from json import JSONDecodeError

class ViewTypeEnum(Enum):
    TABULAR = 1
    JSON = 2
    TREE = 3
    