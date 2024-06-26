from PyQt6.QtGui import QStandardItem, QStandardItemModel
from configyaml import config as conf
from core.manager import executeTreeNav
from core.treepath import Node
from widgets.utils import createItem

class ModelManager:
    

    @staticmethod
    def createBaseModel() -> QStandardItemModel:
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['Connections'])
        rootItem = model.invisibleRootItem()
        rootItem.appendRows(getConnections())
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


def getConnections():
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


