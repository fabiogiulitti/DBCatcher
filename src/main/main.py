from argparse import ArgumentParser
from pathlib import Path
import sys
from PyQt6.QtWidgets import QApplication
from main.widgets.mainwindow import MainWindow
import main.cli_args as cli_args

parser = ArgumentParser()
parser.add_argument('-c', '--configFile', help='Specify alternative config file path')

args = parser.parse_args()

cli_args.config_file = args.configFile


STYLE_QSS = Path(__file__).resolve().parent / "widgets" / "style.qss"


def _load_stylesheet() -> str:
    try:
        return STYLE_QSS.read_text(encoding="utf-8")
    except OSError:
        return ""


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    qss = _load_stylesheet()
    if qss:
        app.setStyleSheet(qss)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
