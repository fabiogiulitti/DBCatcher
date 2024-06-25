from PyQt5.QtWidgets import QWidget, QHBoxLayout
from widgets.dbcontent import DbContent
import widgets.dbtree as dbtree

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Dive into db')
        mylayout = QHBoxLayout()
        self.setGeometry(200, 200, 600, 400)
        fTree = dbtree.DbTree(self)
        mylayout.addWidget(fTree)
        content = DbContent(self)
        content.setVisible(True)
        fTree.content = content
        self.setTabOrder(fTree, content)
        self.setTabOrder(content, fTree)
        self.setLayout(mylayout)

