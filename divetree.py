from PyQt5.QtWidgets import QApplication, QTreeView, QWidget
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import divemongo

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
        mongoItem = QStandardItem("Localhost Mongo")
        for item in divemongo.create_mongo_model():
            mongoItem.appendRow(item)
        return mongoItem
