from attr import ib, s


@s
class ContentData:
    _text: str = ib()
    _metaData: dict = ib()

    @property
    def text(self):
        return self._text

    @property
    def metaData(self):
        return self._metaData