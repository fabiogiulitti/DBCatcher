from PyQt5.QtWidgets import QTreeView, QWidget
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import divemongo
from configyaml import config as conf

class DiveTree(QTreeView):
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
