from PyQt5.QtWidgets import QTreeView, QWidget
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt
import divemongo
from configyaml import config as conf
from widgets.divecontent import DiveContent

class DiveTree(QTreeView):

    content: DiveContent

    def __init__(self, parent: QWidget | None = ...) -> None:
        super().__init__(parent)
        self.setModel(self.createBaseModel())
        self.show()

    def createBaseModel(self):
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['Connections'])
        rootItem = model.invisibleRootItem()
        rootItem.appendRows(self.getConnections())
        return model

    def getConnections(self):
        connectionItems = list()

        for connection in conf.get_value("connections"):
            name = connection['name']
            type = connection['type']
            mongoItem = QStandardItem(f"{name} {type}")
            mongoItem.appendRows(divemongo.create_mongo_model(connection['connectionUri']))
            connectionItems.append(mongoItem)
        return connectionItems

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.content.refreshText("testo di prova")
            event = None
            print("chiamato")
        super().mousePressEvent(event)
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.content.refreshText("testo di prova")
        super().keyPressEvent(event)
