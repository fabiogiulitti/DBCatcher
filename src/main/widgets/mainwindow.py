from PyQt6.QtWidgets import QSplitter, QMainWindow
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import  Qt
from main.widgets import content_menu
from main.widgets.dbtree import DbTree
from main.widgets.statusbar import ContentStatus
from main.widgets.contentWin import ContentWin

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('D B Catcher')

        self.setGeometry(300, 200, 800, 600)
        
        
        dbTree = DbTree(self)
        content_win = ContentWin(self, dbTree.custom_signals)
        main_split = QSplitter(Qt.Orientation.Horizontal)
        main_split.addWidget(dbTree)
        main_split.addWidget(content_win)
        main_split.setStretchFactor(0, 1)
        main_split.setStretchFactor(1, 3)
        self.setCentralWidget(main_split)
        self.setMenuBar(content_menu.ContentMenuBar(content_win))
        mainStatus = ContentStatus(self)
        self.setStatusBar(mainStatus)
        self.setTabOrder(dbTree, content_win.contentTxt)
        self.setTabOrder(content_win.contentTxt, content_win.contentTab)
        self.setTabOrder(content_win.contentTab, content_win._queryTxt)
        
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.GlobalColor.darkGreen)
