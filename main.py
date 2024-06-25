import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout

import divetree
import divemongo

class DiveWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Dive into db')
        mylayout = QHBoxLayout()
        self.setGeometry(100, 100, 300, 200)
        fTree = divetree.DiveTree(self)
        mylayout.addWidget(fTree)
        #self.setTabOrder(fTree, sTree)
        #self.setTabOrder(sTree, fTree)
        self.setLayout(mylayout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DiveWindow()
    window.show()
    sys.exit(app.exec_())
