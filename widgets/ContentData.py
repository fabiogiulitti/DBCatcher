from json import dumps
from attr import ib, s
from PyQt6.QtGui import QStandardItemModel, QStandardItem


@s
class ContentData:
    _result: str = ib()
    _metaData: dict = ib()

    @property
    def results(self):
        return self._result

    @property
    def metaData(self):
        return self._metaData
    


@s
class ContentDataModel:
    _result: QStandardItemModel = ib()
    _metaData: dict = ib()

    @property
    def results(self):
        return self._result

    @property
    def metaData(self):
        return self._metaData
    
