from PyQt6.QtWidgets import QTableView, QWidget, QMessageBox
from PyQt6.QtWidgets import QTextEdit, QSizePolicy
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt
from main.core.driver.abstractdataresponse import AbstractDataResponse
from main.core.manager import executeCntAction
from main.widgets.ContentData import ContentData
from main.core.ActonTypeEnum import ActionTypeEnum, ObjectTypeEnum

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
        try:
            if event.modifiers() == Qt.KeyboardModifier.ControlModifier and event.key() == Qt.Key.Key_Return:
                ctx = self._metaData
                ctx['action_type'] = ActionTypeEnum.CTRL_ENTER
                ctx['action_obj'] = ObjectTypeEnum.QUERY_EDIT
                ctx['query'] = self.toPlainText()
                response: AbstractDataResponse = executeCntAction(ctx)
                if response is not None:
                    self._parent.refreshContent(response)
        except Exception as e:
            QMessageBox.information(self, "Error", str(e))

        super().keyPressEvent(event)

    