from json import dumps
from PyQt6.QtWidgets import QTextEdit, QSizePolicy, QMessageBox
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QTextOption
from PyQt6.QtCore import Qt
from main.core.driver.abstractdataresponse import AbstractDataResponse
from main.core.manager import executeCntAction
from main.widgets.ContentData import ContentData
from main.core.ActonTypeEnum import ActionTypeEnum, ObjectTypeEnum

class ContenTextEdit(QTextEdit):
    def __init__(self, parent, queryTxt):
        super().__init__(parent)
        self._queryTxt = queryTxt
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setAccessibleDescription("Content view")
        self.setAccessibleName("Content view box")
        self.setTabChangesFocus(True)
        self.setWordWrapMode(QTextOption.WrapMode.NoWrap)
        self.show()


    def refreshText(self, text):
        if self.isVisible == False:
            self.setVisible(True)
        self.setText(text)

    def refreshData(self, data: ContentData):
        self.metaData = data.metaData
        self.refreshText(data.results)
        self._queryTxt.setText(data.query)
        self._queryTxt.setMetaData(data.metaData)

    def keyPressEvent(self, event):
        try:
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
        except Exception as e:
            QMessageBox.information(self, "Error", str(e))
        super().keyPressEvent(event)
