from abc import ABC,abstractmethod
from widgets.ContentData import ContentData


class AbstractDataResponse(ABC):

    @abstractmethod
    def toJson(self) -> ContentData:
        pass

#    @abstractmethod
    def toTabular(self):
        raise NotImplementedError("Unsupported method for this driver")
    
 #   @abstractmethod
    def toTree(self):
        raise NotImplementedError("Unsupported method for this driver")

#    @abstractmethod
    def metadata(self):
        pass

