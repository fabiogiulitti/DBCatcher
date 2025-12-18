from ast import arg, arguments
from PyQt6.QtCore import QAbstractItemModel, QModelIndex, Qt, QPersistentModelIndex

from main.widgets.model.tree_node import TreeNode


class DBCItemModel(QAbstractItemModel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._root_node = TreeNode()
        self._persistent_indexex = []

    def index(self, row, column, parent=QModelIndex()):
        #print(f"{row} {column}")
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        parent_node = parent.internalPointer() if parent.isValid() else self._root_node
        #print(parent_node._internal_data[0])
        if row < 0 or row >= len(parent_node.childrens):
            return QModelIndex()        
        child = parent_node.childrens[row]
        if child.index:
            new_index = child.index
        else:
            new_index = self.createIndex(row, column, child)
            child.index = new_index
            if child._deep >= 5:
                self._persistent_indexex.append(QPersistentModelIndex(new_index))
                print("aggiunto in persistenza")
        return new_index
    

    def parent(self, index: QModelIndex):
        if not index.isValid():
            return QModelIndex()
        
        node = index.internalPointer()
        parent = node.parent
        if parent is None or parent == self._root_node:
            return QModelIndex()

        
        return parent.index

    def rowCount(self, parent):
        parent_node = parent.internalPointer() if parent.isValid() else self._root_node
        return len(parent_node.childrens)

    def columnCount(self, parent):
        return 1

    def data(self, index, role: int):
        if not index.isValid():
            return None

        node: TreeNode = index.internalPointer()
        return node.getData(Qt.ItemDataRole(role))
    
    def userData(self, index):
        return self.data(index, Qt.ItemDataRole.UserRole.value)
    
    def flags(self, index):
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags
        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
    
    def getRootNode(self):
        return self._root_node