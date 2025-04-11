from PyQt6.QtWidgets import QTableView, QWidget
from PyQt6.QtWidgets import QTextEdit, QSizePolicy
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt
from core.driver.abstractdataresponse import AbstractDataResponse
from core.manager import executeCntAction
from widgets.ContentData import ContentData
#from widgets.contentWin import ContentWin
from core.ActonTypeEnum import ActionTypeEnum, ObjectTypeEnum

class QueryEdit(QTextEdit):

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self._parent = parent
        self.setText("db.collection.find()")
        self.setTabChangesFocus(True)
        self._metaData = dict()

    def setMetaData(self, metaData: dict):
        self._metaData = metaData

    def keyPressEvent(self, event):
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier and event.key() == Qt.Key.Key_Return:
            ctx = self._metaData
            ctx['action_type'] = ActionTypeEnum.CTRL_ENTER
            ctx['action_obj'] = ObjectTypeEnum.QUERY_EDIT
            ctx['query'] = self.toPlainText()
            response: AbstractDataResponse = executeCntAction(ctx)
            if response is not None:
                self._parent.refreshContent(response)
        super().keyPressEvent(event)

    