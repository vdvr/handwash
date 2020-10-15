from datetime import datetime
from PyQt5.QtCore import Qt, pyqtSlot, QTimer
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
)



class DateTimeWidget(QWidget):
    def __init__(self, main=False):
        super().__init__()

        # Initialize current time and date label and add to layout
        dateNow = datetime.strftime(datetime.now(), "%A %d %B")
        timeNow = datetime.strftime(datetime.now(), "%H:%M")

        self.dateTimeLayout = QVBoxLayout()
        self.dateLbl = QLabel(dateNow)
        self.dateLbl.setObjectName("datebig" if main else "datesmall")
        self.dateLbl.setAlignment(Qt.AlignHCenter if main else Qt.AlignRight)
        self.dateTimeLayout.addWidget(self.dateLbl)

        self.timeLbl = QLabel(timeNow)
        self.timeLbl.setObjectName("timebig" if main else "timesmall")
        self.timeLbl.setAlignment(Qt.AlignHCenter if main else Qt.AlignRight)
        self.dateTimeLayout.addWidget(self.timeLbl)

        self.dateTimeLayout.addStretch()
        self.dateTimeLayout.setSpacing(0)

        self.setLayout(self.dateTimeLayout)

        # Start timer for current time
        self.clockTimer = QTimer()
        self.clockTimer.timeout.connect(self._updateClock)
        self.clockTimer.start(1000)
        

    @pyqtSlot()
    def _updateClock(self):
        
        # Set current time
        dateNow = datetime.strftime(datetime.now(), "%A %d %B")
        timeNow = datetime.strftime(datetime.now(), "%H:%M")
        self.dateLbl.setText(dateNow)
        self.timeLbl.setText(timeNow)