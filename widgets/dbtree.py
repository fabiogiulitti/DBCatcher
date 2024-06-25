from PyQt6.QtWidgets import QTreeView
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt, QModelIndex
from core.treepath import Node
from configyaml import config as conf
from widgets.utils import createItem
from widgets.dbcontent import DbContent
from core.manager import getNav,getAction

class DbTree(QTreeView):

    content: DbContent

    def __init__(self, parent: QTreeView | None = ...) -> None:
        super().__init__(parent)
        self.setModel(self.createBaseModel())
        self.expanded.connect(self.on_item_expanded)
        self.show()

    def createBaseModel(self) -> QStandardItemModel:
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['Connections'])
        rootItem = model.invisibleRootItem()
        rootItem.appendRows(self.getConnections())
        return model

    def getConnections(self):
        connectionItems = list()

        for connection in conf.get_value("connections"):
            name = connection['name']
            type = connection['type']
            uri = connection['connectionURI']
            mongoItem = QStandardItem(f"{name} {type}")
            mongoItem.setData({'levelTag' : 'connections'
            ,'connectionURI' : uri})
            mongoItem.appendRow(QStandardItem('(LOADING)'))
            connectionItems.append(mongoItem)
        return connectionItems

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.content.refreshText("testo di prova")
            event = None
        super().mousePressEvent(event)
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            index = self.currentIndex()
            data = index.model().itemData(index)
            text = getAction(data[257])
            self.content.refreshText(text)
            self.content.setVisible(True)
        super().keyPressEvent(event)
        

    def on_item_expanded(self, index: QModelIndex):
        item = self.model().itemFromIndex(index)
        data = index.model().itemData(index)
        node: Node = getNav(data[257])
        self.addNodes(item,node)

    def addNodes(self, parent: QStandardItem, node: Node):
        parent.removeRow(0)
        parent.appendRows(map(lambda i: createItem(parent.data(), i, node), node.items))

