from PyQt6.QtWidgets import QTreeView, QMessageBox, QWidget
from PyQt6.QtCore import Qt, QModelIndex, pyqtSignal, QObject
from main.core.driver.abstractdataresponse import AbstractDataResponse
from main.core.manager import executeTreeAction
from main.widgets.modelmanager import ModelManager
from main.core.ActonTypeEnum import ActionTypeEnum
from PyQt6.QtGui import QKeyEvent
from threading import Thread

from main.widgets.utils import DBCSignals

class DbTreeView(QTreeView):
    _wrong_action = pyqtSignal(QWidget, str, str)

    def __init__(self, parent, dbc_signals: DBCSignals) -> None:
        super().__init__(parent)
        self.setAccessibleName("Connections")
        self.modelManager = ModelManager.createBaseModel()
        self.setModel(self.modelManager.getModel())
        self.expanded.connect(self.on_item_expanded)
        self.collapsed.connect(self.on_item_collapsed)
        self.show()

        self._wrong_action.connect(QMessageBox.information)
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
            response: AbstractDataResponse = executeTreeAction(ctx)
            if response is not None:
                self._dbc_signals.table_loaded.emit(response)
        except Exception as e:
            self._wrong_action.emit(self, "Error", str(e))
        

    def on_item_expanded(self, index: QModelIndex):
        Thread(target=self.asynch_expand, args=(index,)).start()

    def asynch_expand(self, index: QModelIndex):
        try:
            self.modelManager.expandModel(index)
        except Exception as e:
            self._wrong_action.emit(self, "Error", str(e))

    def on_item_collapsed(self, index: QModelIndex):
        try:
            self.modelManager.collapseModel(index)
        except Exception as e:
            QMessageBox.information(self, "Error", str(e))

