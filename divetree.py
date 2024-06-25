from PyQt5.QtWidgets import QApplication, QTreeView, QWidget
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import divemongo
from config import config

class DiveTree(QTreeView):
    def __init__(self, parent: QWidget | None = ...) -> None:
        super().__init__(parent)
        self.setModel(self.createBaseModel())
        self.show()

    def createBaseModel(self):
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['Connections'])
        model.appendRow(self.getConnections())
        return model

    def getConnections(self):
        name = config['mongodb']['name']
        type = config['mongodb']['type']
        mongoItem = QStandardItem(f"{name} {type}")
        for item in divemongo.create_mongo_model(config['mongodb']['connectionUri']):
            mongoItem.appendRow(item)
        return mongoItem
