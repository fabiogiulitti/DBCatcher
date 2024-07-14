from json import dumps
from attr import ib, s


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
    
