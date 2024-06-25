from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSplitter, QTextEdit, QMainWindow
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import  Qt
from widgets.dbcontent import DbContent
import widgets.dbtree as dbtree
from widgets.statusbar import ContentStatus

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Dive into db')

        self.setGeometry(300, 200, 800, 600)

        contentLayout = QVBoxLayout()
        contentWin = QWidget()
        contentTxt = DbContent(contentWin)
        contentStatus = ContentStatus(self)
        #contentTxt.setVisible(False)
        contentLayout.addWidget(contentTxt)
        #contentLayout.addWidget(contentStatus)
        contentWin.setLayout(contentLayout)
        dbTree = dbtree.DbTree(self, contentTxt)
        mainSplit = QSplitter(Qt.Orientation.Horizontal)
        mainSplit.addWidget(dbTree)
        mainSplit.addWidget(contentWin)
        mainSplit.setStretchFactor(0, 0)
        mainSplit.setStretchFactor(1, 1)
        self.setCentralWidget(mainSplit)
        self.setTabOrder(dbTree, contentTxt)
        self.setTabOrder(contentTxt, dbTree)
        self.setStatusBar(contentStatus)
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.GlobalColor.darkGreen)
