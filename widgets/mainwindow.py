from PyQt6.QtWidgets import QWidget, QHBoxLayout
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import  Qt
from widgets.dbcontent import DbContent
import widgets.dbtree as dbtree

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Dive into db')
        mylayout = QHBoxLayout()
        self.setGeometry(300, 200, 800, 600)
        fTree = dbtree.DbTree(self)
        mylayout.addWidget(fTree)
        content = DbContent(self)
        content.setVisible(False)
        fTree.content = content
        self.setTabOrder(fTree, content)
        self.setTabOrder(content, fTree)
        self.setLayout(mylayout)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.GlobalColor.darkGreen)
