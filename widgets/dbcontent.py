from json import dumps
from PyQt6.QtWidgets import QTextEdit, QSizePolicy
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt
from core.driver.abstractdataresponse import AbstractDataResponse
from core.manager import executeCntAction
from widgets.ContentData import ContentData
from core.ActonTypeEnum import ActionTypeEnum, ObjectTypeEnum

class DbContent(QTextEdit):
    def __init__(self,parent):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setAccessibleDescription("Content view")
        self.setAccessibleName("Content view box")
        self.setTabChangesFocus(True)
        self.show()


    def refreshText(self, text):
        if self.isVisible == False:
            self.setVisible(True)
        self.setText(text)

    def refreshData(self, data: ContentData):
        self.metaData = data.metaData
        self.refreshText(data.results)

    def keyPressEvent(self, event):
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier and event.key() == Qt.Key.Key_PageDown:
            ctx = self.metaData
            ctx['action_type'] = ActionTypeEnum.NEXT_PAGE
            ctx['action_obj'] = ObjectTypeEnum.TEXT_AREA
            response: AbstractDataResponse = executeCntAction(ctx)
            if response is not None:
                result: ContentData = response.toJson()
                self.refreshData(result)
        elif event.modifiers() == Qt.KeyboardModifier.ControlModifier and  event.key() == Qt.Key.Key_PageUp:
            ctx = self.metaData
            ctx['action_type'] = ActionTypeEnum.PREVIOUS_PAGE
            ctx['action_obj'] = ObjectTypeEnum.TEXT_AREA
            response: AbstractDataResponse = executeCntAction(ctx)
            if response != None:
                result: ContentData = response.toJson()
                self.refreshData(result)
        super().keyPressEvent(event)
