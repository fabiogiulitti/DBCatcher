from concurrent.futures import thread
from threading import Thread
from typing import Optional
from PyQt6.QtWidgets import QSizePolicy, QWidget, QVBoxLayout, QSpacerItem, QLabel, QMessageBox, QHBoxLayout, QPushButton
from PyQt6.QtCore import pyqtSignal
from main.core.driver.abstractdataresponse import AbstractDataResponse
from main.core.ActonTypeEnum import ActionTypeEnum, DriverTypeEnum, ObjectTypeEnum
from main.core.manager import executeCntAction
from main.widgets.content_tree import ContentTreeView
from main.widgets.dbcontent import ContenTextEdit
from main.widgets.dbtabular import ContentTableView
from main.widgets.queryedit import QueryEdit
from main.core.driver.abstractdataresponse import AbstractDataResponse
from main.widgets.model.viewtypeenum import ViewTypeEnum
from main.widgets.utils import DBCSignals


class ContentWindow(QWidget):
    wrongQuery = pyqtSignal(QWidget, str, str)

    def __init__(self, parent, dbc_signals: DBCSignals):
        super().__init__(parent)
        # Pagination status
        self._current_page = 1

        self._last_page = 1
        self._query_txt = QueryEdit(self, dbc_signals)
        query_header_layout = QHBoxLayout()
        query_header_layout.addWidget(QLabel("Query"))
        query_header_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self._execute_btn = QPushButton("Execute Query")
        query_header_layout.addWidget(self._execute_btn)

        cnt_layout = QVBoxLayout()
        cnt_layout.addLayout(query_header_layout)
        cnt_layout.addWidget(self._query_txt)

        self.content_txt = ContenTextEdit(self, self._query_txt, dbc_signals.executeQueryRequested)
        self.content_txt.setVisible(False)
        self.content_tab = ContentTableView(self, self._query_txt)
        self.content_tab.setVisible(False)
        self.content_tree = ContentTreeView(self, self._query_txt)
        self.content_tree.execute_query_requested = dbc_signals.executeQueryRequested
        self.content_tree.setVisible(False)
        cnt_layout.addSpacerItem(QSpacerItem(100, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        cnt_layout.addWidget(QLabel("Result data"))
        cnt_layout.addWidget(self.content_txt)
        cnt_layout.addWidget(self.content_tab)
        cnt_layout.addWidget(self.content_tree)
        cnt_layout.setStretchFactor(self._query_txt, 3)
        cnt_layout.setStretchFactor(self.content_txt, 10)
        cnt_layout.setStretchFactor(self.content_tab, 10)
        cnt_layout.setStretchFactor(self.content_tree, 10)

        # Pagination section
        pagination_layout = QHBoxLayout()
        self._first_page_btn = QPushButton("|< First")
        self._prev_page_btn = QPushButton("< Previous")
        self._page_label = QLabel(" --- ")
        self._next_page_btn = QPushButton("Next >")
        self._last_page_btn = QPushButton("Last >|")
        pagination_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        pagination_layout.addWidget(self._first_page_btn)
        pagination_layout.addWidget(self._prev_page_btn)
        pagination_layout.addWidget(self._page_label)
        pagination_layout.addWidget(self._next_page_btn)
        pagination_layout.addWidget(self._last_page_btn)
        pagination_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        cnt_layout.addLayout(pagination_layout)

        self.setLayout(cnt_layout)
        self.setVisible(False)

        self._driver_type: Optional[DriverTypeEnum ] = None
        self._response: Optional[AbstractDataResponse] = None
        self._update_pagination_controls()

        # Signals binding
        dbc_signals.table_loaded.connect(self.refreshContent)
        dbc_signals.results_updated.connect(self.refreshContent)
        self._dbc_signals = dbc_signals
        

        # Signals slots connections
        dbc_signals.executeQueryRequested.connect(lambda ctx: Thread(target=self.executeQuery, args=(ctx,)).start())
        self._execute_btn.clicked.connect(self._on_execute_query)
        self._first_page_btn.clicked.connect(self._on_first_page)
        self._prev_page_btn.clicked.connect(self._on_prev_page)
        self._next_page_btn.clicked.connect(self._on_next_page)
        self._last_page_btn.clicked.connect(self._on_last_page)
        

    def _on_execute_query(self):
        assert self._response
        ctx = self._response.metadata()
        ctx['action_type'] = ActionTypeEnum.CTRL_ENTER
        ctx['action_obj'] = ObjectTypeEnum.QUERY_EDIT
        ctx['query'] = self._query_txt.toPlainText()
        self._dbc_signals.executeQueryRequested.emit(ctx)

    def _on_first_page(self):
        if self._current_page > 0:
            assert self._response
            ctx = self._response.metadata()
            ctx['action_type'] = ActionTypeEnum.FIRST_PAGE
            assert self._driver_type
            if self._driver_type.selected_view == ViewTypeEnum.JSON:
                ctx['action_obj'] = ObjectTypeEnum.TEXT_AREA
            elif self._driver_type.selected_view == ViewTypeEnum.TABULAR:
                ctx['action_obj'] = ObjectTypeEnum.TABULAR
            elif self._driver_type.selected_view == ViewTypeEnum.TREE:
                ctx['action_obj'] = ObjectTypeEnum.TREE

            self.executeQuery(ctx)
            

    def _on_prev_page(self):
        if self._current_page > 0:
            assert self._response
            ctx = self._response.metadata()
            ctx['action_type'] = ActionTypeEnum.PREVIOUS_PAGE
            assert self._driver_type
            if self._driver_type.selected_view == ViewTypeEnum.JSON:
                ctx['action_obj'] = ObjectTypeEnum.TEXT_AREA
            elif self._driver_type.selected_view == ViewTypeEnum.TABULAR:
                ctx['action_obj'] = ObjectTypeEnum.TABULAR
            elif self._driver_type.selected_view == ViewTypeEnum.TREE:
                ctx['action_obj'] = ObjectTypeEnum.TREE

            self.executeQuery(ctx)


    def _on_next_page(self):
        if self._current_page < self._last_page:
            assert self._response
            ctx = self._response.metadata()
            ctx['action_type'] = ActionTypeEnum.NEXT_PAGE
            assert self._driver_type
            if self._driver_type.selected_view == ViewTypeEnum.JSON:
                ctx['action_obj'] = ObjectTypeEnum.TEXT_AREA
            elif self._driver_type.selected_view == ViewTypeEnum.TABULAR:
                ctx['action_obj'] = ObjectTypeEnum.TABULAR
            elif self._driver_type.selected_view == ViewTypeEnum.TREE:
                ctx['action_obj'] = ObjectTypeEnum.TREE

            self.executeQuery(ctx)
            

    def _on_last_page(self):
        if self._current_page < self._last_page:
            assert self._response
            ctx = self._response.metadata()
            ctx['action_type'] = ActionTypeEnum.LAST_PAGE
            assert self._driver_type
            if self._driver_type.selected_view == ViewTypeEnum.JSON:
                ctx['action_obj'] = ObjectTypeEnum.TEXT_AREA
            elif self._driver_type.selected_view == ViewTypeEnum.TABULAR:
                ctx['action_obj'] = ObjectTypeEnum.TABULAR
            elif self._driver_type.selected_view == ViewTypeEnum.TREE:
                ctx['action_obj'] = ObjectTypeEnum.TREE

            self.executeQuery(ctx)
            

    def _update_pagination_controls(self):
        
        is_first_page = self._current_page <= 0
        is_last_page = self._current_page >= self._last_page
        
        self._first_page_btn.setEnabled(not is_first_page)
        self._prev_page_btn.setEnabled(not is_first_page)
        self._next_page_btn.setEnabled(not is_last_page)
        self._last_page_btn.setEnabled(not is_last_page)

    def refreshContent(self, response: AbstractDataResponse):
        if response:
            self._response = response
        assert self._response
        metadata: dict = self._response.metadata()
        self._driver_type = metadata['type']
        assert self._driver_type
        try:
            if self._driver_type.selected_view == ViewTypeEnum.JSON:
                data = self._response.toJson()
                self.content_txt.refreshData(data)
                self.content_tab.setVisible(False)
                self.content_tree.setVisible(False)
                self.content_txt.setVisible(True)
            elif self._driver_type.selected_view == ViewTypeEnum.TABULAR:
                data = self._response.toTabular()
                self.content_tab.refreshData(data)
                self.content_txt.setVisible(False)
                self.content_tab.setVisible(True)
                self.content_tree.setVisible(False)
            elif self._driver_type.selected_view == ViewTypeEnum.TREE:
                data = self._response.toTree()
                self.content_tree.refreshData(data)
                self.content_txt.setVisible(False)
                self.content_tab.setVisible(False)
                self.content_tree.setVisible(True)
            self._dbc_signals.status_notify.emit("Results:", f"{metadata['cur_page']*metadata['dim_page']+1} - {(metadata['cur_page']+1)*metadata['dim_page']} of {metadata.get('tot_result', 'UNKNOWN')}")
    
            self.setVisible(True)
            self._current_page = metadata.get("cur_page", 0)
            self._last_page = metadata.get("last_page", 0)
            self._update_pagination_controls() # Aggiorna i pulsanti dopo aver caricato i dati

        except Exception as e:
            QMessageBox.information(self, "Error", str(e))
            self._current_page = 0
            self._last_page = 0
        self._update_pagination_controls()

    def executeQuery(self, ctx):
        try:
            print("step 0")
            response: AbstractDataResponse = executeCntAction(ctx)
            print("step 1")
            if response is not None:
                print("step 2")
                self._dbc_signals.results_updated.emit(response)
        except Exception as e:
            self.wrongQuery.emit(self, "Error", str(e))
            

        