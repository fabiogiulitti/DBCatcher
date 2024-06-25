from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtGui import QStandardItemModel, QStandardItem

class DbContent(QTextEdit):
    def __init__(self,parent):
        super().__init__(parent)
        self.setReadOnly(True)


    def refreshText(self, text):
        if self.isVisible == False:
            self.setVisible(True)
        self.setText(text)
