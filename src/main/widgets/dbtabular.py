from fileinput import filename
import logging
import os
from PyQt6.QtWidgets import QTableView, QWidget, QAbstractItemView, QMenu, QMessageBox
from PyQt6.QtGui import QStandardItemModel, QAction, QGuiApplication
from PyQt6.QtCore import Qt, QAbstractItemModel, QStandardPaths
import oracledb
from drivers.oracle.treeactionrules import FetchTypeEnum
from main.core.driver import abstractbigcolumn
from main.core.driver.abstractdataresponse import AbstractDataResponse
from main.core.manager import executeCntAction
from main.core.ActonTypeEnum import ActionTypeEnum, ObjectTypeEnum
import csv
import io

class ContentTableView(QTableView):

    def __init__(self, parent: QWidget, queryTxt) -> None:
        super().__init__(parent)
        self._queryTxt = queryTxt
        self.setTabKeyNavigation(False)
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectItems)
        self.setDragEnabled(True)
        self.setTabletTracking(True)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)
        
        

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

    def showContextMenu(self, pos):
        menu = QMenu(self)
        widget_pos = self.viewport().mapFromParent(pos)
        index = self.indexAt(widget_pos)
        if index.isValid():# and index.model():
            fetch_info = index.data(Qt.ItemDataRole.UserRole)
            
            if fetch_info:
                if FetchTypeEnum.DOWNLOAD == fetch_info.fetch_type:
                    column_name = index.model().headerData(index.column(), Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole)
                    
                    action_download = QAction("Download", self)
                    action_download.triggered.connect(lambda: self.streamBytes(fetch_info.object, column_name))
                    menu.addAction(action_download)
        action_csv = QAction("Copy to clipboard as csv", self)
        action_csv.triggered.connect(lambda: self.fromModelToJson(self.model()))
        menu.addAction(action_csv)
        menu.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        menu.exec(self.viewport().mapToGlobal(pos))
        menu.setFocus()

    def fromModelToCsv(self, model: QAbstractItemModel | None):
        if isinstance(model, QStandardItemModel):

            out = io.StringIO()
            writer = csv.writer(out)
        
            rows = model.rowCount()
            columns = model.columnCount()
            colWidths = [max([len(str(model.data(model.index(row, col)))) for row in range(rows)] + [len(str(model.headerData(col, Qt.Orientation.Horizontal)))]) for col in range(columns)]

            header = [str(model.headerData(col, Qt.Orientation.Horizontal)).ljust(colWidths[col]) for col in range(columns)]
            writer.writerow(header)
            
            for row in range(rows):
                rowData = []
                for column in range(columns):
                    index = model.index(row, column)
                    item = model.data(index)
                    rowData.append(str(item).ljust(colWidths[column]) if item is not None else "")
                writer.writerow(rowData)

            cb = QGuiApplication.clipboard()
            assert cb
            cb.setText(out.getvalue())

            out.close()

    def streamBytes(self, fetch_info: abstractbigcolumn.AbstractBigColumnFetchInfo, file_name):
        print(fetch_info.type)
        try:
            download_folder =  QStandardPaths.writableLocation(
                QStandardPaths.StandardLocation.DownloadLocation
            )
        
            if not download_folder:
                download_folder = QStandardPaths.writableLocation(
                    QStandardPaths.StandardLocation.HomeLocation
                )

            full_path = os.path.join(download_folder, file_name)
        
            name, estension = os.path.splitext(file_name)
            counter = 1
            while os.path.exists(full_path):
                full_path = os.path.join(download_folder, f"{name} ({counter}){estension}")
                counter += 1

            offset = 1
            chunk_size = 1000
            file_content = fetch_info.read(offset, chunk_size)
            offset += chunk_size
        
            write_mode = 'wb' if isinstance(file_content, bytes) else 'w'
            
            with open(full_path, write_mode) as file_locale:
                
                while(file_content is not  None and len(file_content) > 0):
                    file_locale.write(file_content)
                    offset += chunk_size
                    file_content = fetch_info.read(offset, chunk_size)
        except Exception as e:
            logging.error("Impossible to download the file", e)