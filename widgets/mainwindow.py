from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSplitter, QMainWindow, QLabel, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import  Qt
from widgets.dbcontent import DbContent, QTextEdit
import widgets.dbtree as dbtree
from widgets.statusbar import ContentStatus

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Dive into db')

        self.setGeometry(300, 200, 800, 600)

        cntLayout = QVBoxLayout()
        #cntLayout.setContentsMargins(50, 20, 20, 20)
        
        contentWin = QWidget()
        queryTxt = QTextEdit(contentWin)
        queryTxt.setText("db.collection.find()")
        queryTxt.setTabChangesFocus(True)
        cntLayout.addSpacerItem(QSpacerItem(100, 30, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        cntLayout.addWidget(QLabel("Query"))
        cntLayout.addWidget(queryTxt)
        contentTxt = DbContent(contentWin)
        #contentTxt.setVisible(False)
        cntLayout.addSpacerItem(QSpacerItem(100, 30, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        cntLayout.addWidget(QLabel("Result data"))
        cntLayout.addWidget(contentTxt)
        cntLayout.setStretchFactor(queryTxt, 2)
        cntLayout.setStretchFactor(contentTxt, 11)
        contentWin.setLayout(cntLayout)
        dbTree = dbtree.DbTree(self, contentTxt)
        mainSplit = QSplitter(Qt.Orientation.Horizontal)
        mainSplit.addWidget(dbTree)
        mainSplit.addWidget(contentWin)
        mainSplit.setStretchFactor(0, 1)
        mainSplit.setStretchFactor(1, 3)
        self.setCentralWidget(mainSplit)
        mainStatus = ContentStatus(self)
        mainStatus.addWidget(QLabel("(fixet status label)"))
        self.setStatusBar(mainStatus)
        self.setTabOrder(dbTree, contentTxt)
        self.setTabOrder(contentTxt, queryTxt)
        #self.setTabOrder(queryTxt, dbtree)
        
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.GlobalColor.darkGreen)
