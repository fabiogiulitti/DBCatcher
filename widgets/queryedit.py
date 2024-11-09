from PyQt6.QtWidgets import QTableView, QWidget
from PyQt6.QtWidgets import QTextEdit, QSizePolicy
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt
from core.driver.abstractdataresponse import AbstractDataResponse
from core.manager import executeCntAction
from widgets.ContentData import ContentData
from core.ActonTypeEnum import ActionTypeEnum, ObjectTypeEnum


class QueryEdit(QTextEdit):

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setText("db.collection.find()")
        self.setTabChangesFocus(True)
