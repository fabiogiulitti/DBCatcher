from tkinter.tix import Tree
from typing import Optional
from PyQt6.QtCore import Qt,QModelIndex

class TreeNode():

    def __init__(self, display_value=None, parent=None) -> None:
        self._index = None
        self._internal_data = {Qt.ItemDataRole.DisplayRole.value: display_value}
        self._parent = parent
        self._childrens = []
        self._deep = parent._deep+1 if parent else 0


    @property
    def parent(self):
        return self._parent
    
    @parent.setter
    def parent(self, parent):
        self._parent = parent

    @property
    def childrens(self):
        return self._childrens
    
    @childrens.setter
    def childrens(self, childrens: list):
        self._childrens = childrens

    @property
    def index(self):
        return self._index
    
    @index.setter
    def index(self, index: QModelIndex):
        self._index = index

    def getData(self, role: Qt.ItemDataRole):
        return self._internal_data.get(role.value, None)

    def setData(self, role: Qt.ItemDataRole, value):
        self._internal_data[role.value] = value

    def getUserData(self):
        return self._internal_data[Qt.ItemDataRole.UserRole]

    def setUserData(self, value):
        self._internal_data[Qt.ItemDataRole.UserRole] = value

    def addItem(self, item):
        self._childrens.append(item)
        
    def clearItems(self):
        self._childrens.clear()


    def getRow(self):
        if self.parent is None:
            return 0
        return self.parent.childrens.index(self)
