from threading import Thread
from typing import Optional
from PyQt6.QtWidgets import QSizePolicy, QWidget, QVBoxLayout, QSpacerItem, QLabel, QMessageBox, QHBoxLayout, QPushButton
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QKeySequence
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
    wrong_action = pyqtSignal(QWidget, str, str)
    reset_query_buttons = pyqtSignal()

    def __init__(self, parent, dbc_signals: DBCSignals):
        super().__init__(parent)
        # Pagination status
        # self._current_page = 1

        # self._last_page = 1
        query_header_layout = QHBoxLayout()
        query_lbl = QLabel("&Query")
        query_header_layout.addWidget(query_lbl)
        self._query_txt = QueryEdit(self, dbc_signals)
        query_lbl.setBuddy(self._query_txt)
        self._execute_btn = QPushButton("Execute Query")
        self._execute_btn.setShortcut(QKeySequence("Ctrl+Return"))
        self._cancel_btn = QPushButton("Cancel Query")
        self._cancel_btn.setEnabled(False)
        query_bottom_layout = QHBoxLayout()
        query_bottom_layout.addStretch()
        query_bottom_layout.addWidget(self._execute_btn)
        query_bottom_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum))
        query_bottom_layout.addWidget(self._cancel_btn)

        cnt_layout = QVBoxLayout()
        cnt_layout.addLayout(query_header_layout)
        cnt_layout.addWidget(self._query_txt)
        cnt_layout.addLayout(query_bottom_layout)

        self._content_label = QLabel("Result data")
        self._content_label.setVisible(False)
        self._content_txt = ContenTextEdit(self, self._query_txt, dbc_signals.execute_query_requested)
        self._content_txt.setVisible(False)
        self._content_tab = ContentTableView(self, self._query_txt)
        self._content_tab.setVisible(False)
        self._content_tree = ContentTreeView(self, self._query_txt, dbc_signals.execute_query_requested)
        self._content_tree.setVisible(False)
        cnt_layout.addSpacerItem(QSpacerItem(100, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum))
        cnt_layout.addWidget(self._content_label)
        cnt_layout.addWidget(self._content_txt)
        cnt_layout.addWidget(self._content_tab)
        cnt_layout.addWidget(self._content_tree)
        cnt_layout.setStretchFactor(self._query_txt, 3)
        cnt_layout.setStretchFactor(self._content_txt, 10)
        cnt_layout.setStretchFactor(self._content_tab, 10)
        cnt_layout.setStretchFactor(self._content_tree, 10)

        # Pagination section
        self._pagination_container = QWidget()
        pagination_layout = QHBoxLayout()
        self._first_page_btn = QPushButton("|< First")
        self._prev_page_btn = QPushButton("< Previous")
        self._page_label = QLabel(" --- ")
        self._next_page_btn = QPushButton("Next >")
        self._last_page_btn = QPushButton("Last >|")
        pagination_layout.addStretch()
        pagination_layout.addWidget(self._first_page_btn)
        pagination_layout.addWidget(self._prev_page_btn)
        pagination_layout.addWidget(self._page_label)
        pagination_layout.addWidget(self._next_page_btn)
        pagination_layout.addWidget(self._last_page_btn)
        pagination_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum))
        self._pagination_container.setLayout(pagination_layout)
        cnt_layout.addWidget(self._pagination_container)
        
        self.setLayout(cnt_layout)
        self.setVisible(False)

        self._driver_type: Optional[DriverTypeEnum ] = None
        self._response: Optional[AbstractDataResponse] = None
        self._updatePaginationControls(True)

        # Signals binding
        dbc_signals.table_loaded.connect(self.refreshContent)
        dbc_signals.results_updated.connect(self.refreshContent)
        dbc_signals.execute_query_requested.connect(lambda ctx: Thread(target=self.executeAction, args=(ctx,)).start())
        self._dbc_signals = dbc_signals
        self.wrong_action.connect(QMessageBox.information)
        self._execute_btn.clicked.connect(self._on_execute_query)
        self._cancel_btn.clicked.connect(self._on_cancel_query)
        self._first_page_btn.clicked.connect(self._on_first_page)
        self._prev_page_btn.clicked.connect(self._on_prev_page)
        self._next_page_btn.clicked.connect(self._on_next_page)
        self._last_page_btn.clicked.connect(self._on_last_page)
        self.reset_query_buttons.connect(self.resetButtonsForQuery)
        

    def _on_execute_query(self):
        if self._response is not None:
            ctx = self._response.metadata()
            ctx['action_type'] = ActionTypeEnum.CTRL_ENTER
            ctx['action_obj'] = ObjectTypeEnum.QUERY_EDIT
            ctx['query'] = self._query_txt.toPlainText()
            self._dbc_signals.execute_query_requested.emit(ctx)
            self._cancel_btn.setEnabled(True)
            self._execute_btn.setEnabled(False)
            self._updatePaginationControls(True)

    def _on_cancel_query(self):
        if self._response is not None:
            ctx = self._response.metadata()
            ctx['action_type'] = ActionTypeEnum.CANCEL_QUERY
            ctx['action_obj'] = ObjectTypeEnum.QUERY_EDIT
            self.resetButtonsForQuery()
            self._dbc_signals.status_notify.emit("Cancelling query", "")
            self.executeAction(ctx)
            self._dbc_signals.status_notify.emit("Query cancelled", "")

    def resetButtonsForQuery(self):
        self._cancel_btn.setEnabled(False)
        self._execute_btn.setEnabled(True)
        

    def _on_first_page(self):
        if self._current_page > 0:
            assert self._response
            ctx = self._response.metadata()
            ctx['action_type'] = ActionTypeEnum.FIRST_PAGE
            assert self._driver_type
            if self._driver_type._selected_view == ViewTypeEnum.JSON:
                ctx['action_obj'] = ObjectTypeEnum.TEXT_AREA
            elif self._driver_type._selected_view == ViewTypeEnum.TABULAR:
                ctx['action_obj'] = ObjectTypeEnum.TABULAR
            elif self._driver_type._selected_view == ViewTypeEnum.TREE:
                ctx['action_obj'] = ObjectTypeEnum.TREE

            self.executeAction(ctx)
            

    def _on_prev_page(self):
        if self._current_page > 0:
            assert self._response
            ctx = self._response.metadata()
            ctx['action_type'] = ActionTypeEnum.PREVIOUS_PAGE
            assert self._driver_type
            if self._driver_type._selected_view == ViewTypeEnum.JSON:
                ctx['action_obj'] = ObjectTypeEnum.TEXT_AREA
            elif self._driver_type._selected_view == ViewTypeEnum.TABULAR:
                ctx['action_obj'] = ObjectTypeEnum.TABULAR
            elif self._driver_type._selected_view == ViewTypeEnum.TREE:
                ctx['action_obj'] = ObjectTypeEnum.TREE

            self.executeAction(ctx)


    def _on_next_page(self):
        if self._current_page < self._last_page:
            assert self._response
            ctx = self._response.metadata()
            ctx['action_type'] = ActionTypeEnum.NEXT_PAGE
            assert self._driver_type
            if self._driver_type._selected_view == ViewTypeEnum.JSON:
                ctx['action_obj'] = ObjectTypeEnum.TEXT_AREA
            elif self._driver_type._selected_view == ViewTypeEnum.TABULAR:
                ctx['action_obj'] = ObjectTypeEnum.TABULAR
            elif self._driver_type._selected_view == ViewTypeEnum.TREE:
                ctx['action_obj'] = ObjectTypeEnum.TREE

            self.executeAction(ctx)
            

    def _on_last_page(self):
        if self._current_page < self._last_page:
            assert self._response
            ctx = self._response.metadata()
            ctx['action_type'] = ActionTypeEnum.LAST_PAGE
            assert self._driver_type
            if self._driver_type._selected_view == ViewTypeEnum.JSON:
                ctx['action_obj'] = ObjectTypeEnum.TEXT_AREA
            elif self._driver_type._selected_view == ViewTypeEnum.TABULAR:
                ctx['action_obj'] = ObjectTypeEnum.TABULAR
            elif self._driver_type._selected_view == ViewTypeEnum.TREE:
                ctx['action_obj'] = ObjectTypeEnum.TREE

            self.executeAction(ctx)
            

    def _updatePaginationControls(self, hide_all=False):
        if hide_all is True or (self._current_page == 0 and self._last_page == 0):
            self._pagination_container.setVisible(False)
        else:
            self._pagination_container.setVisible(True)
            is_first_page = self._current_page <= 0
            is_last_page = self._current_page >= self._last_page
        
            self._first_page_btn.setEnabled(not is_first_page)
            self._prev_page_btn.setEnabled(not is_first_page)
            self._next_page_btn.setEnabled(not is_last_page)
            self._last_page_btn.setEnabled(not is_last_page)

    def refreshContent(self, response: AbstractDataResponse | None):
        self._cancel_btn.setEnabled(False)
        self._execute_btn.setEnabled(True)
        if response:
            self._response = response
        assert self._response
        metadata: dict = self._response.metadata()
        self._driver_type = metadata['type']
        assert self._driver_type
        try:
            if self._driver_type._selected_view == ViewTypeEnum.JSON:
                data = self._response.toJson()
                self._content_txt.refreshData(data)
                self._content_tab.setVisible(False)
                self._content_tree.setVisible(False)
                self._content_txt.setVisible(True)
            elif self._driver_type._selected_view == ViewTypeEnum.TABULAR:
                data = self._response.toTabular()
                self._content_tab.refreshData(data)
                self._content_txt.setVisible(False)
                self._content_tab.setVisible(True)
                self._content_tree.setVisible(False)
            elif self._driver_type._selected_view == ViewTypeEnum.TREE:
                data = self._response.toTree()
                self._content_tree.refreshData(data)
                self._content_txt.setVisible(False)
                self._content_tab.setVisible(False)
                self._content_tree.setVisible(True)
            self._content_label.setVisible(True)
            self._dbc_signals.status_notify.emit("Results:", f"{metadata['cur_page']*metadata['dim_page']+1} - {(metadata['cur_page']+1)*metadata['dim_page']} of {metadata.get('tot_result', 'UNKNOWN')}")
    
            self.setVisible(True)
            self._current_page = metadata.get("cur_page", 0)
            self._last_page = metadata.get("last_page", 0)
        except Exception as e:
            QMessageBox.information(self, "Error", str(e))
            self._current_page = 0
            self._last_page = 0
        finally:
            self._updatePaginationControls()
            

    def executeAction(self, ctx):
        try:
            self._dbc_signals.status_notify.emit("Executing query", "")
            response: AbstractDataResponse = executeCntAction(ctx)
            if response is not None:
                self._dbc_signals.results_updated.emit(response)
        except Exception as e:
            self.wrong_action.emit(self, "Error", str(e))
        finally:
            self.reset_query_buttons.emit()
            self._dbc_signals.status_notify.emit("", "")
