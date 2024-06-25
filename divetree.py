from PyQt5.QtWidgets import QWidget, QTreeWidget,QTreeWidgetItem
from PyQt5.QtCore import Qt

class DiveTree(QTreeWidget):
    def __init__(self, parent):
        super().__init__(parent)
#        self.focusPolicy(Qt.FocusPolicy.StrongFocus)
        self.root = QTreeWidgetItem( self, ["root","Connections"])
        self.child1 = QTreeWidgetItem(self.root, ["child","Figlio 1"])
        
    def addChild(self, name):
        QTreeWidgetItem(self,[name,"label"])
