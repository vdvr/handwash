from . import DateTimeWidget
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout
)

class IdleUI(QWidget):
    def __init__(self, styleFile):
        super().__init__()

        # Set global Qt style sheet
        if styleFile != None:
            with open(styleFile) as styleFileObj:
                self.setStyleSheet(styleFileObj.read())

        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.mainLayout.addStretch(2)
        self.dateTime = DateTimeWidget(main=True)
        self.mainLayout.addWidget(self.dateTime, 1)
        self.mainLayout.addStretch(2)


    def show(self):
        self.setWindowTitle("Idle Screen")
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.showFullScreen()