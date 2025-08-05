from functools import partial
from pydoc import TextRepr
from typing import Optional
from PyQt6.QtWidgets import QTreeView, QMessageBox, QWidget, QMenu
from PyQt6.QtCore import Qt, QModelIndex, pyqtSignal, QObject, QItemSelectionModel
from main.core.driver.abstractdataresponse import AbstractDataResponse, TextResponse
from main.core.manager import executeDialogAction, executeTreeAction
from main.widgets import dialog
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
        self.setModel(self.modelManager.getModel())
        self.expanded.connect(self.on_item_expanded)
        self.collapsed.connect(self.on_item_collapsed)
        self.show()

        self.wrong_action.connect(partial(QMessageBox.information, self))
        self._dbc_signals = dbc_signals


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
        index = self.currentIndex()
        model = index.model()
        assert model is not None
        data = model.itemData(index)
        ctx = data[257]
        menu = QMenu(self)
        if ctx['levelTag'] == 'connections':
    #        actionCsv.triggered.connect(lambda: self.fromModelToJson(self.model()))
            menu.addAction("New connection...")
            menu.addAction("Edit connection...")
        elif ctx['levelTag'] in ['tables', 'views', 'materialized views', 'functions']:
            action_definition = QAction("Show definition...", self)
            action_definition.triggered.connect(self.showDialog)
            menu.addAction(action_definition)

        if menu.actions():
            menu.focusNextChild()
            menu.exec(event.globalPos())
            
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
                dialog.ModalDialog(self, response.toPlainText().results, self._dbc_signals)
        except Exception as e:
            self.wrong_action.emit("Error", str(e))
