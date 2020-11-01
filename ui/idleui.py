from . import DateTimeWidget
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
)

class IdleUI(QWidget):
    def __init__(self, startTxt=None, styleFile=None):
        super().__init__()

        # Set global Qt style sheet
        if styleFile != None:
            with open(styleFile) as styleFileObj:
                self.setStyleSheet(styleFileObj.read())

        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.mainLayout.addStretch(5)
        self.dateTime = DateTimeWidget(main=True)
        self.mainLayout.addWidget(self.dateTime, 3)
        if startTxt:
            startLabel = QLabel(startTxt)
            startLabel.setObjectName("starttext")
            startLabel.setAlignment(Qt.AlignHCenter)
            self.mainLayout.addWidget(startLabel)
        self.mainLayout.addStretch(5)


    def show(self):
        self.setWindowTitle("Idle Screen")
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.showFullScreen()