from typing import Optional
from PyQt6.QtWidgets import QSizePolicy, QWidget, QVBoxLayout, QSpacerItem, QLabel, QMessageBox
from main.core.driver.abstractdataresponse import AbstractDataResponse
from main.core.ActonTypeEnum import DriverTypeEnum
from main.widgets.content_tree import ContentTreeView
from main.widgets.dbcontent import ContenTextEdit
from main.widgets.dbtabular import ContentTableView
from main.widgets.queryedit import QueryEdit
from main.core.driver.abstractdataresponse import AbstractDataResponse
from main.widgets.model.viewtypeenum import ViewTypeEnum
from main.widgets.utils import DBCSignals

class ContentWindow(QWidget):
    def __init__(self, parent, dbc_signals: DBCSignals):
        super().__init__(parent)
        self._query_txt = QueryEdit(self)
        cnt_layout = QVBoxLayout()
        cnt_layout.addSpacerItem(QSpacerItem(100, 30, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        cnt_layout.addWidget(QLabel("Query"))
        cnt_layout.addWidget(self._query_txt)

        self.content_txt = ContenTextEdit(self, self._query_txt)
        self.content_txt.setVisible(False)
        self.content_tab = ContentTableView(self, self._query_txt)
        self.content_tab.setVisible(False)
        self.content_tree = ContentTreeView(self, self._query_txt)
        self.content_tree.setVisible(False)
        cnt_layout.addSpacerItem(QSpacerItem(100, 30, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        cnt_layout.addWidget(QLabel("Result data"))
        cnt_layout.addWidget(self.content_txt)
        cnt_layout.setStretchFactor(self._query_txt, 3)
        cnt_layout.setStretchFactor(self.content_txt, 10)
        self.setLayout(cnt_layout)
        self.setVisible(False)

        self.driver_type: Optional[DriverTypeEnum ] = None
        self._response: Optional[AbstractDataResponse] = None

        dbc_signals.table_loaded.connect(self.refresh_content)
        self._dbc_signals = dbc_signals
        self._query_txt.custom_signals.results_updated.connect(self.refresh_content)
        

    def refresh_content(self, response: AbstractDataResponse):
        if response:
            self._response = response
        assert self._response
        metadata: dict = self._response.metadata()
        self.driver_type = metadata['type']
        assert self.driver_type
        try:
            if self.driver_type.selected_view == ViewTypeEnum.JSON:
                data = self._response.toJson()
                self.content_txt.refreshData(data)
                self.content_tab.setVisible(False)
                self.content_tree.setVisible(False)
                self.content_txt.setVisible(True)
            elif self.driver_type.selected_view == ViewTypeEnum.TABULAR:
                data = self._response.toTabular()
                self.content_tab.refreshData(data)
                self.content_txt.setVisible(False)
                self.content_tab.setVisible(True)
                self.content_tree.setVisible(False)
            elif self.driver_type.selected_view == ViewTypeEnum.TREE:
                data = self._response.toTree()
                self.content_tree.refreshData(data)
                self.content_txt.setVisible(False)
                self.content_tab.setVisible(False)
                self.content_tree.setVisible(True)
            self._dbc_signals.status_notify.emit("Results page:", f"{metadata['cur_page']} of {metadata['last_page']}")
    
            self.setVisible(True)
        except Exception as e:
            QMessageBox.information(self, "Error", str(e))
