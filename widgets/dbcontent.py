from PyQt6.QtWidgets import QTextEdit, QSizePolicy
from PyQt6.QtGui import QStandardItemModel, QStandardItem

class DbContent(QTextEdit):
    def __init__(self,parent):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setAccessibleDescription("Content view")
        self.setAccessibleName("Content view box")
        #self.resize(400, 300)
        self.show()


    def refreshText(self, text):
        if self.isVisible == False:
            self.setVisible(True)
        self.setText(text)
