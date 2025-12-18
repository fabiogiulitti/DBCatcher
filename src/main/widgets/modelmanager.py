from threading import Thread
from typing import Optional
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6.QtCore import pyqtBoundSignal, pyqtSignal, QObject, QModelIndex, Qt
from main.core.manager import executeTreeNav
from main.core.treepath import Node
from main.core.config.ConfigManager import retrieveConnections
from main.widgets.model import dbc_item_model
from main.widgets.model.dbc_item_model import DBCItemModel
from main.widgets.model.tree_node import TreeNode
from main.widgets.utils import createItem


class ModelManager(QObject):
    node_insertion = pyqtSignal(list, Node)

    def __init__(self, model: DBCItemModel, wrong_action: pyqtBoundSignal) -> None:
         super().__init__()
         self._model = model
         self._wrong_action = wrong_action
         self.node_insertion.connect(self.addNodes)

    @staticmethod
    def createBaseModel(wrong_action: pyqtBoundSignal):
        #model = QStandardItemModel()
        model = DBCItemModel()
        #model.setHorizontalHeaderLabels(['Connections'])
        
        manager = ModelManager(model, wrong_action)
        manager.setupConnectionNodes()
        return manager
    

    @property
    def model(self):
         return self._model


    def expandModel(self, index: QModelIndex):
        item = index.internalPointer()
        assert item
        data = self._model.data(index, Qt.ItemDataRole.UserRole.value)
        #print(data)

        path = []
        while index.isValid():
            path.insert(0, index.row())
            index = index.parent()

        Thread(target=self.expandModelAsync, args=(data, path)).start()

    def expandModelAsync(self, data, path):
        try:
            node: Node = executeTreeNav(data)
            self.node_insertion.emit(path, node)
        except Exception as e:
            self._wrong_action.emit("Error", str(e))


    def collapseModel(self, index):
        node: Optional[TreeNode] = index.internalPointer()
        assert node
        node.clearItems()
        


    def setupConnectionNodes(self):
        connection_items = list()

        root_node = self._model.getRootNode()
        root_index = self._model.createIndex(0, 0, root_node)
        assert root_node

        for connection in retrieveConnections():
            name = connection.name
            type = connection.type
            uri = connection.connection_uri
            host = connection.host
            port = connection.port
            connection_item = TreeNode(f"{name} -> {type.name}")
            connection_item.setUserData({"name": name,
                'levelTag' : 'connections'
                ,'connection_uri' : uri
                ,'host' : host
                ,'port' : port
                ,'type' : type})
            connection_item.parent = root_node
            connection_item.addItem(TreeNode('(LOADING...)')) #Temporary item

            connection_items.append(connection_item)
        #root_item = self._model.invisibleRootItem()
        if 0 < len(connection_items):
            root_node.childrens = connection_items

    def addConnection(self, connection: dict):
        connection_item = TreeNode(f"{connection['name']} -> {connection['type']}")
        connection_item.setUserData({'name' : connection.get('name'),
            'levelTag' : 'connections'
        ,'connection_uri' : connection.get('connection_uri', None)
        ,'host' : connection.get('host', None)
        ,'port' : connection.get('port', None)
        ,'type' : connection['type']})
        connection_item.addItem(QStandardItem('(LOADING...)')) #Temporary item

        root_item = QStandardItem()
        assert root_item
        root_item.appendRow(connection_item)


    def addNodes(self, parent_path: list, node: Node):
        index = self._model.index(parent_path[0], 0)
        for value in parent_path[1:]:
            index = self._model.index(value, 0, index)
        parent: TreeNode = index.internalPointer()
        parent.clearItems()
        new_rows = [createItem(parent, it, node) for it in node.items]
        self.model.beginInsertRows(index, 0, len(new_rows))
        parent.childrens = new_rows
        self.model.endInsertRows()
