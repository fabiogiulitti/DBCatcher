from PyQt5.QtWidgets import QApplication, QTreeView, QWidget
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import divemongo

class DiveTree(QTreeView):
    def __init__(self, parent: QWidget | None = ...) -> None:
        super().__init__(parent)
        self.setModel(divemongo.create_mongo_model())
        self.show()
