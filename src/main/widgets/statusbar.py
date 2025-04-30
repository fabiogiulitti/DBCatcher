from PyQt6.QtWidgets import QStatusBar, QWidget, QLabel
from PyQt6.QtCore import Qt


class ContentStatus(QStatusBar):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setAccessibleDescription("barra di stato")
        self.show()
#        self.showMessage("(Fixed message)")
#        self.addWidget(QLabel("(fixet status label)"))
        

