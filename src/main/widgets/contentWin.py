from json import dumps
from pickle import TRUE
from PyQt6.QtWidgets import QTextEdit, QSizePolicy, QWidget, QVBoxLayout, QSpacerItem, QLabel, QMessageBox
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt
from main.core.driver.abstractdataresponse import AbstractDataResponse
from main.core.manager import executeCntAction
from main.widgets import dbtabular
from main.widgets import queryedit
from main.widgets.ContentData import ContentData
from main.core.ActonTypeEnum import ActionTypeEnum, ObjectTypeEnum
from main.core.ActonTypeEnum import DriverTypeEnum
from main.widgets.dbcontent import DbContent
from main.widgets.dbtabular import DbTabular
from main.widgets.queryedit import QueryEdit
from main.core.driver.abstractdataresponse import AbstractDataResponse
from main.widgets.model import viewtypeenum
from main.widgets.model.viewtypeenum import ViewTypeEnum

class ContentWin(QWidget):
    def __init__(self,parent):
        super().__init__(parent)
        self._queryTxt = QueryEdit(self)
        cntLayout = QVBoxLayout()
        cntLayout.addSpacerItem(QSpacerItem(100, 30, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        cntLayout.addWidget(QLabel("Query"))
        cntLayout.addWidget(self._queryTxt)

        self.contentTxt = DbContent(self, self._queryTxt)
        self.contentTxt.setVisible(False)
        self.contentTab = DbTabular(self, self._queryTxt)
        self.contentTab.setVisible(False)
        cntLayout.addSpacerItem(QSpacerItem(100, 30, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        cntLayout.addWidget(QLabel("Result data"))
        cntLayout.addWidget(self.contentTxt)
        cntLayout.setStretchFactor(self._queryTxt, 2)
        cntLayout.setStretchFactor(self.contentTxt, 11)
        self.setLayout(cntLayout)
        self.setVisible(False)

    def refreshContent(self, response: AbstractDataResponse):
        metadata: dict = response.metadata()
        type: DriverTypeEnum = metadata['type']
        try:
            if type.view == ViewTypeEnum.JSON:
                data = response.toJson()
                self.contentTxt.refreshData(data)
                self.contentTab.setVisible(False)
                self.contentTxt.setVisible(True)
            elif type.view == ViewTypeEnum.TABULAR:
                data = response.toTabular()
                self.contentTab.refreshData(data)
                self.contentTxt.setVisible(False)
                self.contentTab.setVisible(True)

            self.setVisible(True)
        except Exception as e:
            QMessageBox.information(self, "Error", str(e))
