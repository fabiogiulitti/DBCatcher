from sys import exception
from tkinter import E
from PyQt6.QtWidgets import QTreeView, QMessageBox
from PyQt6.QtCore import Qt, QModelIndex
from main.core.driver.abstractdataresponse import AbstractDataResponse
from main.core.manager import executeTreeAction
from main.widgets.modelmanager import ModelManager
from main.core.ActonTypeEnum import ActionTypeEnum
from main.widgets.contentWin import ContentWin
from PyQt6.QtGui import QKeyEvent

class DbTree(QTreeView):

    def __init__(self, parent, content: ContentWin) -> None:
        super().__init__(parent)
        self.setAccessibleName("Connections")
        self.modelManager = ModelManager.createBaseModel()
        self.setModel(self.modelManager.getModel())
        self.expanded.connect(self.on_item_expanded)
        self.collapsed.connect(self.on_item_collapsed)
        self._content: ContentWin = content
        self.show()


    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            event = None
        super().mousePressEvent(event)
    
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            try:
                index = self.currentIndex()
                model = index.model()
                assert model is not None
                data = model.itemData(index)
                ctx = data[257].copy()
                ctx['action_type'] = ActionTypeEnum.CLICK
                response: AbstractDataResponse = executeTreeAction(ctx)
                if response is not None:
                    self._content.refreshContent(response)
            except Exception as e:
                QMessageBox.information(self, "Error", str(e))
        super().keyPressEvent(event)
        

    def on_item_expanded(self, index: QModelIndex):
        try:
            self.modelManager.expandModel(index)
        except Exception as e:
            QMessageBox.information(self, "Error", str(e))

    def on_item_collapsed(self, index: QModelIndex):
        try:
            self.modelManager.collapseModel(index)
        except Exception as e:
            QMessageBox.information(self, "Error", str(e))
