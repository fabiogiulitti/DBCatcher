from json import dumps
from attr import ib, s
from PyQt6.QtGui import QStandardItemModel, QStandardItem


@s
class ContentData:
    _results: str = ib()
    _query: str = ib()
    _metaData: dict = ib()

    @property
    def results(self):
        return self._results

    @property
    def metaData(self):
        return self._metaData
    
    @property
    def query(self):
        return self._query


@s
class ContentDataModel:
    _result: QStandardItemModel
    _query: str
    _metaData: dict

    @property
    def results(self):
        return self._result

    @property
    def metaData(self):
        return self._metaData
    
    @property
    def query(self):
        return self._query
