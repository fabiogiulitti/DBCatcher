from abc import ABC,abstractmethod

from attr import define
from main.widgets.ContentData import ContentData


class AbstractDataResponse(ABC):

    @abstractmethod
    def toJson(self) -> ContentData:
        pass

#    @abstractmethod
    def toTabular(self):
        raise NotImplementedError("Unsupported method for this driver")
    
    @abstractmethod
    def toTree(self):
        pass

#    @abstractmethod
    def metadata(self):
        return dict()


@define
class TextResponse():
    _text: str
    _query: str
    _metadata: dict

    def toPlainText(self) -> ContentData:
        return ContentData(self._text, self._query, self._metadata)
