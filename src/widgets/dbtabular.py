from PyQt6.QtWidgets import QTableView, QWidget
from PyQt6.QtWidgets import QTextEdit, QSizePolicy
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt
from core.driver.abstractdataresponse import AbstractDataResponse
from core.manager import executeCntAction
from widgets.ContentData import ContentData
from core.ActonTypeEnum import ActionTypeEnum, ObjectTypeEnum


class DbTabular(QTableView):

    def __init__(self, parent: QWidget, queryTxt) -> None:
        super().__init__(parent)
        self._queryTxt = queryTxt
        self.setTabKeyNavigation(False)

    def refreshData(self, data):
        self.setModel(data.results)
        self._metaData = data.metaData
        self._queryTxt.setText(data.query)
        self._queryTxt.setMetaData(data.metaData)

    def keyPressEvent(self, event):
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier and event.key() == Qt.Key.Key_PageDown:
            ctx = self._metaData
            ctx['action_type'] = ActionTypeEnum.NEXT_PAGE
            ctx['action_obj'] = ObjectTypeEnum.TABULAR
            response: AbstractDataResponse = executeCntAction(ctx)
            if response is not None:
                result = response.toTabular()
                self.refreshData(result)
        elif event.modifiers() == Qt.KeyboardModifier.ControlModifier and  event.key() == Qt.Key.Key_PageUp:
            ctx = self._metaData
            ctx['action_type'] = ActionTypeEnum.PREVIOUS_PAGE
            ctx['action_obj'] = ObjectTypeEnum.TABULAR
            response: AbstractDataResponse = executeCntAction(ctx)
            if response != None:
                result = response.toTabular()
                self.refreshData(result)
        super().keyPressEvent(event)

    