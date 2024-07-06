import sys
from PyQt6.QtWidgets import QApplication
from widgets.mainwindow import MainWindow
from drivers.mongodb.contentactionrules import MyDriver

MyDriver()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
O