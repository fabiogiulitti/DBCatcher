from PyQt6.QtWidgets import QMenu, QMenuBar
from PyQt6.QtGui import QAction, QActionGroup, QKeySequence

from main.widgets import content_window
from main.widgets.dbtree import DbTreeView
from main.widgets.model import viewtypeenum
from main.widgets.model.viewtypeenum import ViewTypeEnum

class DBCMenuBar(QMenuBar):
    def __init__(self, content_win: content_window.ContentWindow, db_tree: DbTreeView):
        super().__init__()

        self._content_win = content_win
        self._db_tree = db_tree

        self.file_menu = self.addMenu("&File")
        assert self.file_menu
        self.new_connection_action = QAction("&New connection...", self)
        self.new_connection_action.setShortcut(QKeySequence("Ctrl+N"))
        self.new_connection_action.triggered.connect(lambda: self._db_tree.showConnectionsDialog())
        self.file_menu.addAction(self.new_connection_action)

        self.view_menu = self.addMenu("&View")
        assert self.view_menu

        self.presentation_menu = QMenu("Presentation Mode", self)
        self.view_menu.addMenu(self.presentation_menu)

        action_group = QActionGroup(self.presentation_menu)
        action_group.setExclusive(True)
        self.tree_action = QAction("Tree", self)
        self.tree_action.setCheckable(True)
        self.tree_action.setProperty("view_mask", ViewTypeEnum.TREE.value)
        self.tree_action.setEnabled(False)
        self.tabular_action = QAction("Tabular", self)
        self.tabular_action.setCheckable(True)
        self.tabular_action.setProperty("view_mask", ViewTypeEnum.TABULAR.value)
        self.tabular_action.setEnabled(False)
        self.json_action = QAction("Json", self)
        self.json_action.setCheckable(True)
        self.json_action.setProperty("view_mask", ViewTypeEnum.JSON.value)
        self.json_action.setEnabled(False)
        action_group.addAction(self.tree_action)
        self.presentation_menu.addAction(self.tree_action)
        action_group.addAction(self.tabular_action)
        self.presentation_menu.addAction(self.tabular_action)
        action_group.addAction(self.json_action)
        self.presentation_menu.addAction(self.json_action)

        self.help_menu = self.addMenu("?")

        self.presentation_menu.aboutToShow.connect(self.about_to_show)
        action_group.triggered.connect(self.actionTriggered)

    def about_to_show(self):
        if self._content_win._driver_type is not None:
            available_views = self._content_win._driver_type._available_views
            self.tree_action.setEnabled(bool(self.tree_action.property("view_mask") & available_views))
            self.tabular_action.setEnabled(self.tabular_action.property("view_mask") & available_views)
            self.json_action.setEnabled(self.json_action.property("view_mask") & available_views)

            if not (self.tree_action.isChecked() or self.tabular_action.isChecked() or self.json_action.isChecked()):
                self.tree_action.setChecked(self.tree_action.property("view_mask") == self._content_win._driver_type._selected_view.value)
                self.tabular_action.setChecked(self.tabular_action.property("view_mask") == self._content_win._driver_type._selected_view.value)
                self.json_action.setChecked(self.json_action.property("view_mask") == self._content_win._driver_type._selected_view.value)


    def actionTriggered(self, action):
        assert self._content_win._driver_type
        assert self._content_win.refreshContent
        self._content_win._driver_type.selectedView = ViewTypeEnum[action.text().upper()]
        self._content_win.refreshContent(None)

