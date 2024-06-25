from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QStandardItemModel, QStandardItem

class DiveContent(QTextEdit):
    def __init__(self,parent):
        super().__init__(parent)
        self.setReadOnly(True)


    def refreshText(self, text):
        if self.isVisible == False:
            self.setVisible(True)
        self.setText(text)
