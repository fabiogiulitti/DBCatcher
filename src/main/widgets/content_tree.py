from PyQt6.QtWidgets import QWidget, QMenu, QTreeView, QApplication, QMainWindow
from PyQt6.QtGui import QStandardItemModel, QAction, QGuiApplication, QStandardItem
from PyQt6.QtCore import Qt, QAbstractItemModel
import csv
import io
import sys

from main.widgets import mainwindow

class ContentTree(QTreeView):

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.contextMenuEvent
#        self._queryTxt = queryTxt
#        self.setTabKeyNavigation(False)
        self.setModel(self.tempModel())
        

    def refreshData(self, data):
        self.setModel(data.results)
        self._metaData = data.metaData
        self._queryTxt.setText(data.query)
        self._queryTxt.setMetaData(data.metaData)

    # def keyPressEvent(self, event):
    #     if event.modifiers() == Qt.KeyboardModifier.ControlModifier and event.key() == Qt.Key.Key_PageDown:
    #         ctx = self._metaData
    #         ctx['action_type'] = ActionTypeEnum.NEXT_PAGE
    #         ctx['action_obj'] = ObjectTypeEnum.TABULAR
    #         response: AbstractDataResponse = executeCntAction(ctx)
    #         if response is not None:
    #             result = response.toTabular()
    #             self.refreshData(result)
    #     elif event.modifiers() == Qt.KeyboardModifier.ControlModifier and  event.key() == Qt.Key.Key_PageUp:
    #         ctx = self._metaData
    #         ctx['action_type'] = ActionTypeEnum.PREVIOUS_PAGE
    #         ctx['action_obj'] = ObjectTypeEnum.TABULAR
    #         response: AbstractDataResponse = executeCntAction(ctx)
    #         if response != None:
    #             result = response.toTabular()
    #             self.refreshData(result)
    #     super().keyPressEvent(event)

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
            assert cb
            cb.setText(csvStr)


    def tempModel(self):
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['Name', 'Value'])
        rootItem: QStandardItem | None = model.invisibleRootItem()
        assert rootItem
        qsi11 = QStandardItem("eta")
        qsi12 = QStandardItem(11)
        qsi11.appendRow([QStandardItem('citta'), QStandardItem('Rome')])
        qsi12.appendRow([QStandardItem('paese'), QStandardItem('Italy')])
        rootItem.appendRow([qsi11, qsi12])
        return model

class MainWindow(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        self._cw = ContentTree(self)
        self.setCentralWidget(self._cw)
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
