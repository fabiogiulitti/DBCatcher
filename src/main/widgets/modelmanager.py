from typing import Optional
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from main.core.manager import executeTreeNav
from main.core.treepath import Node
from main.core.config.ConfigManager import retrieveConnections
from main.widgets.utils import createItem

class ModelManager:

    def __init__(self) -> None:
         self.model = None

    @staticmethod
    def createBaseModel():
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['Connections'])
        rootItem: QStandardItem = model.invisibleRootItem()
        rootItem.appendRows(addConnections())
        manager = ModelManager()
        manager.model = model
        return manager
    
    def getModel(self):
         return self.model


    def expandModel(self, index):
        item = self.model.itemFromIndex(index)
        data = index.model().itemData(index)
        node: Node = executeTreeNav(data[257])
        addNodes(item,node)

    def collapseModel(self, index):
        item: QStandardItem = self.model.itemFromIndex(index)
        item.removeRows(0, item.rowCount() - 1)
        
def addNodes(parent: QStandardItem, node: Node):
        parent.removeRow(0)
        parent.appendRows(map(lambda i: createItem(parent.data(), i, node), node.items))


def addConnections():
        connectionItems = list()
        for connection in retrieveConnections():
            name = connection.name
            type = connection.type
            uri = connection.connectionURI
            host = connection.host
            port = connection.port
            connectionItem = QStandardItem(f"{name} -> {type.name}")
            connectionItem.setData({'levelTag' : 'connections'
            ,'connectionURI' : uri
            ,'host' : host
            ,'port' : port
            ,'type' : type})
            connectionItem.appendRow(QStandardItem('(LOADING)'))
            connectionItems.append(connectionItem)
        return connectionItems

