from ast import mod
from typing import Optional
from PyQt6.QtWidgets import QTableView, QWidget, QTextEdit, QSizePolicy, QAbstractItemView, QTableWidget, QMenu, QWidgetAction, QApplication
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QAction, QGuiApplication
from PyQt6.QtCore import Qt, QAbstractItemModel
from main.core.driver.abstractdataresponse import AbstractDataResponse
from main.core.manager import executeCntAction
from main.widgets.ContentData import ContentData
from main.core.ActonTypeEnum import ActionTypeEnum, ObjectTypeEnum
import csv
import io
import sys

class DbTabular(QTableView):

    def __init__(self, parent: QWidget, queryTxt) -> None:
        super().__init__(parent)
        self.contextMenuEvent
        self._queryTxt = queryTxt
        self.setTabKeyNavigation(False)
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectItems)
        self.setDragEnabled(True)
        self.setTabletTracking(True)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        

    def refreshData(self, data):
        self.setModel(data.results)
        self._metaData = data.metaData
        self._queryTxt.setText(data.query)
        self._queryTxt.setMetaData(data.metaData)

    def keyPressEvent(self, event):
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier and event.key() == Qt.Key.Key_PageDown:
            ctx = self._metaData
            ctx['action_type'] = ActionTypeEnum.NEXT_PAGE
            ctx['action_obj'] = ObjectTypeEnum.TABULAR
            response: AbstractDataResponse = executeCntAction(ctx)
            if response is not None:
                result = response.toTabular()
                self.refreshData(result)
        elif event.modifiers() == Qt.KeyboardModifier.ControlModifier and  event.key() == Qt.Key.Key_PageUp:
            ctx = self._metaData
            ctx['action_type'] = ActionTypeEnum.PREVIOUS_PAGE
            ctx['action_obj'] = ObjectTypeEnum.TABULAR
            response: AbstractDataResponse = executeCntAction(ctx)
            if response != None:
                result = response.toTabular()
                self.refreshData(result)
        super().keyPressEvent(event)

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        actionCsv = QAction("Copia in csv", self)
        actionCsv.triggered.connect(lambda: self.fromModelToJson(self.model()))
        menu.addAction(actionCsv)
        menu.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        menu.exec(event.globalPos())
        menu.setFocus()

    def fromModelToJson(self, model: QAbstractItemModel | None):

        if isinstance(model, QStandardItemModel):

            out = io.StringIO()
            writer = csv.writer(out)
        
            rows = model.rowCount()
            columns = model.columnCount()
            colWidths = [max([len(model.data(model.index(row, col))) for row in range(rows)] + [len(str(model.headerData(col, Qt.Orientation.Horizontal)))]) for col in range(columns)]

            header = [str(model.headerData(col, Qt.Orientation.Horizontal)).ljust(colWidths[col]) for col in range(columns)]
            writer.writerow(header)
            
            for row in range(rows):
                rowData = []
                for column in range(columns):
                    index = model.index(row, column)
                    item = model.data(index)
                    rowData.append(str(item).ljust(colWidths[column]) if item else "")
                writer.writerow(rowData)
            csvStr = out.getvalue()
            out.close()

            cb = QGuiApplication.clipboard()
            cb.setText(csvStr)

