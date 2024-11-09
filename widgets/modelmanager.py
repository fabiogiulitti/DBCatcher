from PyQt6.QtGui import QStandardItem, QStandardItemModel
from core.manager import executeTreeNav
from core.treepath import Node
from core.config.ConfigManager import retrieveConnections
from widgets.utils import createItem

class ModelManager:

    def __init__(self) -> None:
         self.model = None

    @staticmethod
    def createBaseModel():
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['Connections'])
        rootItem = model.invisibleRootItem()
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

        
def addNodes(parent: QStandardItem, node: Node):
        parent.removeRow(0)
        parent.appendRows(map(lambda i: createItem(parent.data(), i, node), node.items))


def addConnections():
        connectionItems = list()
        for connection in retrieveConnections():
            name = connection.name
            type = connection.type
            uri = connection.connectionURI
            connectionItem = QStandardItem(f"{name} -> {type.name}")
            connectionItem.setData({'levelTag' : 'connections'
            ,'connectionURI' : uri
            ,'type' : type})
            connectionItem.appendRow(QStandardItem('(LOADING)'))
            connectionItems.append(connectionItem)
        return connectionItems

