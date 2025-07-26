from threading import Thread
from PyQt6.QtWidgets import QTableView, QWidget, QMessageBox
from PyQt6.QtWidgets import QTextEdit, QSizePolicy
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt, QObject, pyqtSignal
from main.core.driver import abstractdataresponse
from main.core.driver.abstractdataresponse import AbstractDataResponse
from main.core.manager import executeCntAction
from main.widgets.ContentData import ContentData
from main.core.ActonTypeEnum import ActionTypeEnum, ObjectTypeEnum
from main.widgets.utils import DBCSignals

class QueryEdit(QTextEdit):

    def __init__(self, parent, dbc_signals: DBCSignals) -> None:
        super().__init__(parent)

        self.setTabChangesFocus(True)
        self._metadata = dict()

        self.dbc_signals = dbc_signals


    def setMetaData(self, metaData: dict):
        self._metadata = metaData

    def keyPressEvent(self, event):
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier and event.key() == Qt.Key.Key_Return:
            ctx = self._metadata
            ctx['action_type'] = ActionTypeEnum.CTRL_ENTER
            ctx['action_obj'] = ObjectTypeEnum.QUERY_EDIT
            ctx['query'] = self.toPlainText()
            self.dbc_signals.executeQueryRequested.emit(ctx)

        super().keyPressEvent(event)

