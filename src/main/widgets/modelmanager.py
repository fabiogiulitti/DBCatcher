from ctypes import sizeof
from threading import Thread
from typing import Optional
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6.QtCore import pyqtBoundSignal, pyqtSignal, QObject
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
        
        manager = ModelManager(model, wrong_action)
        manager.setupConnectionNodes()
        return manager
    

    @property
    def model(self):
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
        


    def setupConnectionNodes(self):
        connection_items = list()
        for connection in retrieveConnections():
            name = connection.name
            type = connection.type
            uri = connection.connection_uri
            host = connection.host
            port = connection.port
            connection_item = QStandardItem(f"{name} -> {type.name}")
            connection_item.setData({"name": name,
                'levelTag' : 'connections'
                ,'connection_uri' : uri
                ,'host' : host
                ,'port' : port
                ,'type' : type})
            connection_item.appendRow(QStandardItem('(LOADING...)')) #Temporary item

            connection_items.append(connection_item)
        root_item = self._model.invisibleRootItem()
        assert root_item
        if 0 < len(connection_items):
            root_item.appendRows(connection_items)
            print("step 4")

    def addConnection(self, connection: dict):
        connection_item = QStandardItem(f"{connection['name']} -> {connection['type']}")
        connection_item.setData({'name' : connection.get('name'),
            'levelTag' : 'connections'
        ,'connection_uri' : connection.get('connection_uri', None)
        ,'host' : connection.get('host', None)
        ,'port' : connection.get('port', None)
        ,'type' : connection['type']})
        connection_item.appendRow(QStandardItem('(LOADING...)')) #Temporary item

        root_item = self._model.invisibleRootItem()
        assert root_item
        root_item.appendRow(connection_item)


def addNodes(parent: QStandardItem, node: Node):
        parent.removeRow(0)
        parent.appendRows(map(lambda it: createItem(parent.data(), it, node), node.items))
