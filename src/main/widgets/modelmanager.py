from threading import Thread
from typing import Optional
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6.QtCore import pyqtBoundSignal, pyqtSignal, QModelIndex, QObject
from main.core.manager import executeTreeNav
from main.core.treepath import Node
from main.core.config.ConfigManager import retrieveConnections
from main.widgets.utils import createItem

class ModelManager(QObject):
    node_insertion = pyqtSignal(QStandardItem, Node)

    def __init__(self, model: QStandardItemModel, wrong_action: pyqtBoundSignal) -> None:
         super().__init__()
         self._model = model
         self._wrong_action = wrong_action
         self.node_insertion.connect(addNodes)

    @staticmethod
    def createBaseModel(wrong_action: pyqtBoundSignal):
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['Connections'])
        root_item: Optional[QStandardItem] = model.invisibleRootItem()
        assert root_item
        root_item.appendRows(addConnections())
        manager = ModelManager(model, wrong_action)
        return manager
    
    def getModel(self):
         return self._model


    def expandModel(self, index):
        item = self._model.itemFromIndex(index)
        assert item
        Thread(target=self.expandModelAsync, args=(index, item)).start()

    def expandModelAsync(self, index, item):
        try:
            data = index.model().itemData(index)
            node: Node = executeTreeNav(data[257])
            self.node_insertion.emit(item, node)
        except Exception as e:
            self._wrong_action.emit("Error", str(e))


    def collapseModel(self, index):
        item: Optional[QStandardItem] = self._model.itemFromIndex(index)
        assert item
        item.removeRows(0, item.rowCount() - 1)
        
def addNodes(parent: QStandardItem, node: Node):
        parent.removeRow(0)
        parent.appendRows(map(lambda it: createItem(parent.data(), it, node), node.items))


def addConnections():
        connectionItems = list()
        for connection in retrieveConnections():
            name = connection.name
            type = connection.type
            uri = connection.connection_uri
            host = connection.host
            port = connection.port
            connectionItem = QStandardItem(f"{name} -> {type.name}")
            connectionItem.setData({'levelTag' : 'connections'
            ,'connection_uri' : uri
            ,'host' : host
            ,'port' : port
            ,'type' : type})
            connectionItem.appendRow(QStandardItem('(LOADING...)'))
            connectionItems.append(connectionItem)
        return connectionItems

