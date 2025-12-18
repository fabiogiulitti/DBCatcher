from PyQt6.QtWidgets import QSplitter, QMainWindow
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import  Qt
from main.widgets import menu_bar
from main.widgets.dbtree import DbTreeView
from main.widgets.status_bar import DBCStatusBar
from main.widgets.content_window import ContentWindow
from main.widgets.utils import DBCSignals

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('D B Catcher')

        self.setGeometry(300, 200, 800, 600)
        

        dbc_signals = DBCSignals()
        db_tree = DbTreeView(self, dbc_signals)
        content_win = ContentWindow(self, dbc_signals)
        
        main_split = QSplitter(Qt.Orientation.Horizontal)
        main_split.addWidget(db_tree)
        main_split.addWidget(content_win)
        main_split.setStretchFactor(0, 2)
        main_split.setStretchFactor(1, 2)
        self.setCentralWidget(main_split)

        self.setMenuBar(menu_bar.DBCMenuBar(content_win))

        status_bar = DBCStatusBar(self, dbc_signals)
        self.setStatusBar(status_bar)

        # tab navigation
        self.setTabOrder(db_tree, content_win.content_txt)
        self.setTabOrder(content_win.content_txt, content_win.content_tab)
        self.setTabOrder(content_win.content_tab, content_win.content_tree)
        self.setTabOrder(content_win.content_tree, content_win._first_page_btn)
        self.setTabOrder(content_win._first_page_btn, content_win._prev_page_btn)
        self.setTabOrder(content_win._prev_page_btn, content_win._next_page_btn)
        self.setTabOrder(content_win._next_page_btn, content_win._last_page_btn)
        self.setTabOrder(content_win._last_page_btn, content_win._query_txt)
        self.setTabOrder(content_win._query_txt, content_win._execute_btn)
        
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.GlobalColor.darkGreen)
