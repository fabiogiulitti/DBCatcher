from enum import Enum
from json import JSONDecodeError

class ViewTypeEnum(Enum):
    TABULAR = 1 << 0
    JSON = 1 << 1
    TREE = 1 << 2
    