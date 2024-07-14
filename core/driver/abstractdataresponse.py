from abc import ABC,abstractmethod
from widgets.ContentData import ContentData


class AbstractDataResponse(ABC):

    @abstractmethod
    def toJson(self) -> ContentData:
        return None

    def toTabular(self):
        pass

    def toTree(self):
        pass

