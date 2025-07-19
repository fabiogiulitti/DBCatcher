from typing import Optional
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from main.core.manager import executeTreeNav
from main.core.treepath import Node
from main.core.config.ConfigManager import retrieveConnections
from main.widgets.utils import createItem

class ModelManager:

    def __init__(self, model: QStandardItemModel) -> None:
         self._model = model

    @staticmethod
    def createBaseModel():
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['Connections'])
        root_item: Optional[QStandardItem] = model.invisibleRootItem()
        assert root_item
        root_item.appendRows(addConnections())
        manager = ModelManager(model)
        return manager
    
    def getModel(self):
         return self._model


    def expandModel(self, index):
        item = self._model.itemFromIndex(index)
        assert item
        data = index.model().itemData(index)
        node: Node = executeTreeNav(data[257])
        addNodes(item,node)

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

