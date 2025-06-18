from typing import Optional
from PyQt6.QtWidgets import QTextEdit, QSizePolicy, QMessageBox
from PyQt6.QtGui import QTextOption, QFocusEvent
from PyQt6.QtCore import Qt, pyqtBoundSignal
from main.widgets.ContentData import ContentData
from main.core.ActonTypeEnum import ActionTypeEnum, ObjectTypeEnum

class ContenTextEdit(QTextEdit):
    

    def __init__(self, parent, queryTxt, executeQueryRequested: pyqtBoundSignal):
        super().__init__(parent)
        self._queryTxt = queryTxt
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setAccessibleName("Content view")
        self.setTabChangesFocus(True)
        self.setWordWrapMode(QTextOption.WrapMode.NoWrap)
        self.show()

        self._execute_query_requested: pyqtBoundSignal = executeQueryRequested


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
                self._execute_query_requested.emit(ctx)
            elif event.modifiers() == Qt.KeyboardModifier.ControlModifier and  event.key() == Qt.Key.Key_PageUp:
                ctx = self.metaData
                ctx['action_type'] = ActionTypeEnum.PREVIOUS_PAGE
                ctx['action_obj'] = ObjectTypeEnum.TEXT_AREA
                self._execute_query_requested.emit(ctx)
        except Exception as e:
            QMessageBox.information(self, "Error", str(e))
        super().keyPressEvent(event)

