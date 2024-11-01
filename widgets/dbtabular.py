from PyQt6.QtWidgets import QTableView, QWidget

class DbTabular(QTableView):

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setTabKeyNavigation(False)

    