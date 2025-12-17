from functools import partial
from typing import Optional
from PyQt6.QtWidgets import QTreeView, QMessageBox, QMenu
from PyQt6.QtCore import Qt, QModelIndex, pyqtSignal
from main.core.driver.abstractdataresponse import AbstractDataResponse, TextResponse
from main.core.manager import executeDialogAction, executeTreeAction
from main.widgets import definition_dialog
from main.widgets.dialog.connection_dialog import ConnectionDialog
from main.widgets.modelmanager import ModelManager
from main.core.ActonTypeEnum import ActionTypeEnum
from PyQt6.QtGui import QKeyEvent, QAction, QContextMenuEvent
from threading import Thread

from main.widgets.utils import DBCSignals

class DbTreeView(QTreeView):
    wrong_action = pyqtSignal(str, str)

    def __init__(self, parent, dbc_signals: DBCSignals) -> None:
        super().__init__(parent)
        self.setAccessibleName("Connections")
        self.modelManager = ModelManager.createBaseModel(self.wrong_action)
        self.setModel(self.modelManager.model)
        self.expanded.connect(self.on_item_expanded)
        self.collapsed.connect(self.on_item_collapsed)
        self.show()

        self.wrong_action.connect(partial(QMessageBox.information, self))
        self._dbc_signals = dbc_signals
        self._dbc_signals.connection_added.connect(self.modelManager.addConnection)


    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            event = None
        super().mousePressEvent(event)
    
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            index = self.currentIndex()
            model = index.model()
            assert model is not None
            data = model.itemData(index)
            ctx = data[257].copy()
            ctx['action_type'] = ActionTypeEnum.CLICK
            Thread(target=self.asynchRefresh, args=(ctx,)).start()

        super().keyPressEvent(event)

    def asynchRefresh(self, ctx):
        try:
            response: Optional[AbstractDataResponse] = executeTreeAction(ctx)
            if response:
                self._dbc_signals.table_loaded.emit(response)
        except Exception as e:
            self.wrong_action.emit("Error", str(e))
        

    def on_item_expanded(self, index: QModelIndex):
        self.modelManager.expandModel(index)

    def on_item_collapsed(self, index: QModelIndex):
        try:
            self.modelManager.collapseModel(index)
        except Exception as e:
            QMessageBox.information(self, "Error", str(e))


    def contextMenuEvent(self, event: QContextMenuEvent):
        menu = QMenu(self)
        index = self.currentIndex()
        if index.internalId() != 0:
            model = index.model()
            assert model
            data = model.itemData(index)
            ctx = data[257]
            
            if ctx['levelTag'] == 'connections':
                new_conn_act_def = QAction("New connection...", self)
                new_conn_act_def.triggered.connect(self.showConnectionsDialog)
                menu.addAction(new_conn_act_def)
                edit_conn_act_def = QAction("Edit connection...", self)
                edit_conn_act_def.triggered.connect(lambda: self.showConnectionsDialog(True))
                menu.addAction(edit_conn_act_def)
            elif ctx['levelTag'] in ['tables', 'views', 'materialized views', 'functions']:
                action_definition = QAction("Show definition...", self)
                action_definition.triggered.connect(self.showDialog)
                menu.addAction(action_definition)
        else:
            new_conn_act_def = QAction("New connection...", self)
            new_conn_act_def.triggered.connect(self.showConnectionsDialog)
            menu.addAction(new_conn_act_def)

        if menu.actions():
            menu.focusNextChild()
            menu.exec(event.globalPos())
            
    def showConnectionsDialog(self, edit=False):
        try:
            if edit:
                index = self.currentIndex()
                model = index.model()
                assert model is not None
                data = model.itemData(index)
                ctx = data[257].copy()
                name = ctx['name']
                ConnectionDialog(self, self._dbc_signals, name)
            else:
                ConnectionDialog(self, self._dbc_signals)
        except Exception as e:
            self.wrong_action.emit("Error", str(e))

    def showDialog(self, ctx):
        try:
            index = self.currentIndex()
            model = index.model()
            assert model is not None
            data = model.itemData(index)
            ctx = data[257].copy()
            ctx['action_type'] = ActionTypeEnum.DDL
            response: Optional[TextResponse] = executeDialogAction(ctx)
            if response:
                definition_dialog.ModalDialog(self, response.toPlainText().results, self._dbc_signals)
        except Exception as e:
            self.wrong_action.emit("Error", str(e))
