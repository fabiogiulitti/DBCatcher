from PyQt6.QtWidgets import QMenu, QMenuBar
from PyQt6.QtGui import QAction, QActionGroup

from main.core.ActonTypeEnum import DriverTypeEnum
from main.widgets import content_window
from main.widgets.model.viewtypeenum import ViewTypeEnum

class DBCMenuBar(QMenuBar):
    def __init__(self, content_win: content_window.ContentWindow):
        super().__init__()

        self._content_win = content_win

        self.view_menu = self.addMenu("View")
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
            available_views = self._content_win._driver_type.available_views
            self.tree_action.setEnabled(bool(self.tree_action.property("view_mask") & available_views))
            self.tabular_action.setEnabled(self.tabular_action.property("view_mask") & available_views)
            self.json_action.setEnabled(self.json_action.property("view_mask") & available_views)

            if not (self.tree_action.isChecked() or self.tabular_action.isChecked() or self.json_action.isChecked()):
                self.tree_action.setChecked(self.tree_action.property("view_mask") == self._content_win._driver_type.selected_view.value)
                self.tabular_action.setChecked(self.tabular_action.property("view_mask") == self._content_win._driver_type.selected_view.value)
                self.json_action.setChecked(self.json_action.property("view_mask") == self._content_win._driver_type.selected_view.value)


    def actionTriggered(self, action):
        self._content_win._driver_type.setSelectedView(ViewTypeEnum[action.text().upper()])
        self._content_win.refreshContent(None)

