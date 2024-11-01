from PyQt6.QtWidgets import QTreeView, QTextEdit, QWidget
from PyQt6.QtCore import Qt, QModelIndex
from core.driver.abstractdataresponse import AbstractDataResponse
from widgets import contentWin
from widgets.ContentData import ContentData
from widgets.dbcontent import DbContent
from core.manager import executeTreeAction
from widgets.modelmanager import ModelManager
from core.ActonTypeEnum import ActionTypeEnum
from widgets.contentWin import ContentWin

class DbTree(QTreeView):

    def __init__(self, parent: QTreeView, content: ContentWin | None = ...) -> None:
        super().__init__(parent)
        self.setAccessibleName("Connections")
        self.modelManager = ModelManager.createBaseModel()
        self.setModel(self.modelManager.getModel())
        self.expanded.connect(self.on_item_expanded)
        self._content: ContentWin = content
        self.show()


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._content.refreshText("testo di prova")
            event = None
        super().mousePressEvent(event)
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            index = self.currentIndex()
            data = index.model().itemData(index)
            ctx = data[257].copy()
            ctx['action_type'] = ActionTypeEnum.CLICK
            response: AbstractDataResponse = executeTreeAction(ctx)
            self._content.refreshContent(response)
        super().keyPressEvent(event)
        

    def on_item_expanded(self, index: QModelIndex):
        self.modelManager.expandModel(index)
