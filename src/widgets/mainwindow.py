from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSplitter, QMainWindow, QLabel, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import  Qt
from widgets.dbcontent import DbContent, QTextEdit
import widgets.dbtree as dbtree
from widgets.statusbar import ContentStatus
from widgets.contentWin import ContentWin

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Dive into db')

        self.setGeometry(300, 200, 800, 600)
        
        contentWin = ContentWin(self)
        dbTree = dbtree.DbTree(self, contentWin)
        mainSplit = QSplitter(Qt.Orientation.Horizontal)
        mainSplit.addWidget(dbTree)
        mainSplit.addWidget(contentWin)
        mainSplit.setStretchFactor(0, 1)
        mainSplit.setStretchFactor(1, 3)
        self.setCentralWidget(mainSplit)
        mainStatus = ContentStatus(self)
        #mainStatus.addWidget(QLabel("(fixet status label)"))
        self.setStatusBar(mainStatus)
        self.setTabOrder(dbTree, contentWin.contentTxt)
        self.setTabOrder(contentWin.contentTxt, contentWin.contentTab)
        self.setTabOrder(contentWin.contentTab, contentWin._queryTxt)
        
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.GlobalColor.darkGreen)
