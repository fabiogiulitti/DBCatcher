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

class QueryEdit(QTextEdit):

    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.setTabChangesFocus(True)
        self._metadata = dict()

        self.custom_signals = QueryEditSignals()
        self.custom_signals.wrong_query.connect(QMessageBox.information)


    def setMetaData(self, metaData: dict):
        self._metadata = metaData

    def keyPressEvent(self, event):
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier and event.key() == Qt.Key.Key_Return:
            ctx = self._metadata
            ctx['action_type'] = ActionTypeEnum.CTRL_ENTER
            ctx['action_obj'] = ObjectTypeEnum.QUERY_EDIT
            ctx['query'] = self.toPlainText()
            thread = Thread(target=self.asynchRefresh, args=(ctx,))
            thread.start()

        super().keyPressEvent(event)

    def asynchRefresh(self, ctx):
        try:
            response: AbstractDataResponse = executeCntAction(ctx)
            if response is not None:
                self.custom_signals.results_updated.emit(response)
        except Exception as e:
            self.custom_signals.wrong_query.emit(self, "Error", str(e))


class QueryEditSignals(QObject):
    results_updated = pyqtSignal(AbstractDataResponse)
    wrong_query = pyqtSignal(QWidget, str, str)
