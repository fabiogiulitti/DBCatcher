from argparse import ArgumentParser
import sys
from PyQt6.QtWidgets import QApplication
from main.widgets.mainwindow import MainWindow
import main.cli_args as cli_args

parser = ArgumentParser()
parser.add_argument('-c', '--configFile', help='Specify alternative config file path')

args = parser.parse_args()

cli_args.config_file = args.configFile


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
