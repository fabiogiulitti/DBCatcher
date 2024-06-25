from PyQt6.QtWidgets import QTreeView, QTextEdit
from PyQt6.QtCore import Qt, QModelIndex
from widgets.dbcontent import DbContent
from core.manager import getAction
from widgets.modelmanager import ModelManager

class DbTree(QTreeView):

    def __init__(self, parent: QTreeView, content: QTextEdit | None = ...) -> None:
        super().__init__(parent)
        self.modelManager = ModelManager.createBaseModel()
        self.setModel(self.modelManager.getModel())
        self.expanded.connect(self.on_item_expanded)
        self._content = content
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
            text = getAction(data[257])
            self._content.refreshText(text)
            self._content.setVisible(True)
        super().keyPressEvent(event)
        

    def on_item_expanded(self, index: QModelIndex):
        self.modelManager.expandModel(index)
