from typing import Optional
from PyQt6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout
)
from PyQt6 import QtGui

from main.widgets.utils import DBCSignals


class ModalDialog(QDialog):
    def __init__(self, parent, ddl_text: str, dbc_signals: DBCSignals):
        super().__init__(parent)
        self.setWindowTitle("Definition detail")
        self.resize(600, 400)

        layout = QVBoxLayout()
        self._text_edit = QTextEdit()
        self._text_edit.setPlainText(ddl_text)
        self._text_edit.setReadOnly(True)
        self._text_edit.setFont(QtGui.QFont("Courier New", 10))
        layout.addWidget(self._text_edit)

        button_copy = QPushButton("Copy")
        button_close = QPushButton("Close")

        button_copy.clicked.connect(self._copyTextToClipboard)
        button_close.clicked.connect(self.close)

        button_layout = QHBoxLayout()
        button_layout.addWidget(button_copy)
        button_layout.addWidget(button_close)
        layout.addLayout(button_layout)
        self.setLayout(layout)
        self.open()

        dbc_signals.show_detail.connect(self._showDetail)


    def _showDetail(self, text: str, title: Optional[str]):
        self._text_edit.setPlainText(text)
        self.setWindowTitle(title)
        self.open()

    def closeEvent(self, event: Optional[QtGui.QCloseEvent]):
        self._text_edit.clear()


    def _copyTextToClipboard(self):
        clipboard = QApplication.clipboard()
        assert clipboard
        clipboard.setText(self._text_edit.toPlainText())        
