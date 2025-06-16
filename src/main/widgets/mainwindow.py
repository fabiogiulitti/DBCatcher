from PyQt6.QtWidgets import QSplitter, QMainWindow
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import  Qt
from main.widgets import menu_bar
from main.widgets.content_tree import ContentTreeView
from main.widgets.dbtree import DbTreeView
from main.widgets.status_bar import DBCStatusBar
from main.widgets.content_window import ContentWindow
from main.widgets.utils import DBCSignals

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('D B Catcher')

        self.setGeometry(300, 200, 800, 600)
        

        signals = DBCSignals()
        db_tree = DbTreeView(self)
        content_win = ContentWindow(self, db_tree.custom_signals)
        main_split = QSplitter(Qt.Orientation.Horizontal)
        main_split.addWidget(db_tree)
        main_split.addWidget(content_win)
        main_split.setStretchFactor(0, 1)
        main_split.setStretchFactor(1, 3)
        self.setCentralWidget(main_split)
        self.setMenuBar(menu_bar.DBCMenuBar(content_win))
        status_bar = DBCStatusBar(self, signals)
        self.setStatusBar(status_bar)
        self.setTabOrder(db_tree, content_win.content_txt)
        self.setTabOrder(content_win.content_txt, content_win.content_tab)
        self.setTabOrder(content_win.content_tab, content_win._query_txt)
        
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.GlobalColor.darkGreen)
