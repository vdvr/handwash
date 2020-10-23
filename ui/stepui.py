from . import DateTimeWidget, MediaView
from PyQt5.QtCore import Qt, pyqtSlot, QTimer
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
)



class StepUI(QWidget):
    def __init__(self, steps=None, styleFile=None):
        super().__init__()
        
        # Initialize properties
        self.currentStep = None
        self.stepQueue = steps
        self.totalSteps = len(steps)

        # Set global Qt style sheet
        if styleFile != None:
            with open(styleFile) as styleFileObj:
                self.setStyleSheet(styleFileObj.read())

        # Initialize layouts 
        self.mainLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.bottomLayout = QHBoxLayout()
        self.setLayout(self.mainLayout)

        # Add layouts, step photo and description to main layout
        self.mainLayout.addLayout(self.topLayout, 2)

        self.mediaView = MediaView()
        self.mediaView.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.mainLayout.addWidget(self.mediaView, 6)

        self.stepDescLbl = QLabel()
        self.stepDescLbl.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.mainLayout.addWidget(self.stepDescLbl, 1)

        self.mainLayout.addLayout(self.bottomLayout, 1)

        # Initialize time left label and add to layout
        self.timeLeftLbl = QLabel()
        self.timeLeftLbl.setObjectName("timeleft")
        self.timeLeftLbl.setAlignment(Qt.AlignLeft)
        self.topLayout.addWidget(self.timeLeftLbl)

        # Initialize step label and add to layout
        self.stepLayout = QVBoxLayout()
        self.stepTxtLbl = QLabel("Stap:")
        self.stepTxtLbl.setObjectName("steptext")
        self.stepTxtLbl.setAlignment(Qt.AlignRight)
        self.stepLayout.addWidget(self.stepTxtLbl)

        self.stepNrLbl = QLabel()
        self.stepNrLbl.setObjectName("stepnr")
        self.stepNrLbl.setAlignment(Qt.AlignRight)
        self.stepLayout.addWidget(self.stepNrLbl)
        self.stepLayout.addStretch()
        self.stepLayout.setSpacing(0)
        self.topLayout.addLayout(self.stepLayout)

        self.dateTime = DateTimeWidget(main=False)
        self.bottomLayout.addWidget(self.dateTime)

        # Start showing steps
        self.nextStep()


    def nextStep(self):
        # Exit if no steps left
        stepsLeft = len(self.stepQueue)
        if stepsLeft < 1:
            self.close()
            return

        # Calculate steps left and current step nr
        self.currentStep = self.stepQueue[0]
        currentStepNr = self.totalSteps - stepsLeft + 1

        # Update UI labels
        durationS = self.currentStep.durationS
        self.timeLeftLbl.setText(f"{durationS - 1} s")
        self.stepNrLbl.setText(f"{currentStepNr} / {self.totalSteps}")
        self.stepDescLbl.setText(self.currentStep.description)
        
        # Update UI image
        self.mediaView.setSource(self.currentStep.displayPath)
        
        # Start timer to decrease time left label
        self.timeLeftTimer = QTimer()
        self.timeLeftTimer.timeout.connect(self._decreaseDuration)
        self.timeLeftTimer.start(1000)

        self.stepQueue.pop(0)


    @pyqtSlot()
    def _decreaseDuration(self):
        self.currentStep.durationS -= 1
        durationS = int(self.currentStep.durationS)

        if durationS <= 0:
            self.timeLeftTimer.stop()
            self.nextStep()

        else:
            self.timeLeftLbl.setText(f"{durationS - 1} s")


    def show(self):
        self.setWindowTitle("Hand Washing Steps")
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.showFullScreen()