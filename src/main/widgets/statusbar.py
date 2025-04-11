from PyQt6.QtWidgets import QStatusBar, QWidget
from PyQt6.QtCore import Qt

class ContentStatus(QStatusBar):
    def __init__(self, parent: QWidget | None = ...) -> None:
        super().__init__(parent)
        self.showMessage("(Fixed message)")
        self.setAccessibleDescription("barra di stato")
        self.show()

