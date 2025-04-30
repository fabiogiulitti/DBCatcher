from typing import Optional
from PyQt6.QtWidgets import QSizePolicy, QWidget, QVBoxLayout, QSpacerItem, QLabel, QMessageBox
from main.core.driver.abstractdataresponse import AbstractDataResponse
from main.core.ActonTypeEnum import DriverTypeEnum
from main.widgets.dbcontent import DbContent
from main.widgets.dbtabular import DbTabular
from main.widgets.dbtree import DbTreeSignals
from main.widgets.queryedit import QueryEdit
from main.core.driver.abstractdataresponse import AbstractDataResponse
from main.widgets.model.viewtypeenum import ViewTypeEnum

class ContentWin(QWidget):
    def __init__(self, parent, signals: DbTreeSignals):
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
        cntLayout.setStretchFactor(self._queryTxt, 3)
        cntLayout.setStretchFactor(self.contentTxt, 10)
        self.setLayout(cntLayout)
        self.setVisible(False)

        self.driver_type: Optional[DriverTypeEnum ] = None

        signals.table_loaded.connect(self.refresh_content)
        self._queryTxt.custom_signals.results_updated.connect(self.refresh_content)
        

    def refresh_content(self, response: AbstractDataResponse):
        metadata: dict = response.metadata()
        self.driver_type = metadata['type']
        assert self.driver_type
        try:
            if self.driver_type.default_view == ViewTypeEnum.JSON:
                data = response.toJson()
                self.contentTxt.refreshData(data)
                self.contentTab.setVisible(False)
                self.contentTxt.setVisible(True)
            elif self.driver_type.default_view == ViewTypeEnum.TABULAR:
                data = response.toTabular()
                self.contentTab.refreshData(data)
                self.contentTxt.setVisible(False)
                self.contentTab.setVisible(True)

            self.setVisible(True)
        except Exception as e:
            QMessageBox.information(self, "Error", str(e))
