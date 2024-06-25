import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from widgets.divecontent import DiveContent

import divetree
import divemongo

class DiveWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Dive into db')
        mylayout = QHBoxLayout()
        self.setGeometry(200, 200, 600, 400)
        fTree = divetree.DiveTree(self)
        mylayout.addWidget(fTree)
        content = DiveContent(self)
        content.setVisible(True)
        fTree.content = content
        self.setTabOrder(fTree, content)
        self.setTabOrder(content, fTree)
        self.setLayout(mylayout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DiveWindow()
    window.show()
    sys.exit(app.exec_())
