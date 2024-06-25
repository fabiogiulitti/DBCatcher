from PyQt6.QtWidgets import QStatusBar, QWidget

class ContentStatus(QStatusBar):
    def __init__(self, parent: QWidget | None = ...) -> None:
        super().__init__(parent)
        self.showMessage("(Fixed text)")
        self.show()
        self.showMessage("(Fixed text)")
