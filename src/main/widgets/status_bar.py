from PyQt6.QtWidgets import QStatusBar, QWidget, QLabel, QFrame
from main.widgets.utils import DBCSignals

class DBCStatusBar(QStatusBar):

    def __init__(self, parent: QWidget, signals: DBCSignals) -> None:
        super().__init__(parent)
        self.setSizeGripEnabled(False)
        self.lbl_context = QLabel(self)
        self.addWidget(self.lbl_context)
        self.lbl_status = QLabel(self)
        line_separator = QFrame()
        line_separator.setFrameShape(QFrame.Shape.VLine)
        line_separator.setFrameShadow(QFrame.Shadow.Sunken)
        self.addWidget(line_separator)
        self.addWidget(self.lbl_status)
        self.show()

        signals.status_notify.connect(self.on_status_notify)


    def on_status_notify(self, msg_context, msg_status):
        if msg_context:
            self.lbl_context.setText(msg_context)
        if msg_status:
            self.lbl_status.setText(msg_status)
