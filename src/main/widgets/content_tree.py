from typing import Optional
from PyQt6.QtWidgets import QWidget, QMenu, QTreeView, QApplication, QMainWindow, QMessageBox
from PyQt6.QtGui import QStandardItemModel, QAction, QGuiApplication, QStandardItem, QKeyEvent, QFocusEvent
from PyQt6.QtCore import Qt, QAbstractItemModel, pyqtBoundSignal, QEvent
import csv
import io
import sys

from main.core.ActonTypeEnum import ActionTypeEnum, ObjectTypeEnum
from main.widgets import mainwindow

class ContentTreeView(QTreeView):

    def __init__(self, parent, query_txt) -> None:
        super().__init__(parent)
        self._query_txt = query_txt
        self.show()

        self.execute_query_requested: pyqtBoundSignal
        

    def refreshData(self, data):
        self.setModel(data.results)
        self._metaData = data.metaData
        self._query_txt.setText(data.query)
        self._query_txt.setMetaData(data.metaData)

    def keyPressEvent(self, event: QKeyEvent):
        try:
            if event.modifiers() == Qt.KeyboardModifier.ControlModifier and event.key() == Qt.Key.Key_PageDown:
                ctx = self._metaData
                ctx['action_type'] = ActionTypeEnum.NEXT_PAGE
                ctx['action_obj'] = ObjectTypeEnum.TREE
                self.execute_query_requested.emit(ctx)
            elif event.modifiers() == Qt.KeyboardModifier.ControlModifier and  event.key() == Qt.Key.Key_PageUp:
                ctx = self._metaData
                ctx['action_type'] = ActionTypeEnum.PREVIOUS_PAGE
                ctx['action_obj'] = ObjectTypeEnum.TREE
                self.execute_query_requested.emit(ctx)
        except Exception as e:
            QMessageBox.information(self, "Error", str(e))
        super().keyPressEvent(event)

