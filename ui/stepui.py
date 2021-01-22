from . import DateTimeWidget, MediaView
from microbe_ar import MicrobeARObj
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import (
    Qt, 
    pyqtSignal,
    pyqtSlot,
    QTimer,
    QThread,
)
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
)

DIM = (640, 480)


class StepUI(QWidget):
    finished = pyqtSignal()

    def __init__(self, steps, styleFile=None, usingAR=True, microbeRes="res/microbes"):
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
        
        # self.mediaView = MediaView()

        self.usingAR = usingAR
        if usingAR:
            self.videoFeed = QLabel()
            self.videoFeed.resize(*DIM)
            self.videoFeed.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.mainLayout.addWidget(self.videoFeed, 6)
        # else:
        #     self.mainLayout.addWidget(self.mediaView, 6)
        #     self.mediaView.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

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

        # if usingAR:
        #     self.mediaView.setAlignment(Qt.AlignLeft)
        #     self.bottomLayout.addWidget(self.mediaView)
        #     self.bottomLayout.addStretch(1)
        self.dateTime = DateTimeWidget(main=False)
        self.bottomLayout.addWidget(self.dateTime)

        if usingAR:
            self.microbeThread = QThread()
            self.microbeObj = MicrobeARObj(microbeRes, self.totalSteps)
            self.microbeObj.moveToThread(self.microbeThread)
            self.microbeThread.started.connect(self.microbeObj.startRunning)
            self.finished.connect(self.microbeThread.quit)
            self.microbeObj.newFrameAvail.connect(self.updateVideoFeed)
            self.microbeThread.start()

        # Start showing steps
        self.nextStep()


    def nextStep(self):
        # Exit if no steps left
        stepsLeft = len(self.stepQueue)
        if stepsLeft < 1:
            # self.mediaView.mediaplayer.stop()
            self.finished.emit()
            return

        # Calculate steps left and current step nr
        self.currentStep = self.stepQueue[0]
        self.stepDuration = self.currentStep.durationS
        currentStepNr = self.totalSteps - stepsLeft + 1

        # Update UI labels
        durationS = self.stepDuration
        if durationS == None:
            self.timeLeftLbl.setText("")
        else:
            self.timeLeftLbl.setText(f"{durationS - 1} s")
        self.stepNrLbl.setText(f"{currentStepNr} / {self.totalSteps}")
        self.stepDescLbl.setText(self.currentStep.description)
        
        # Update UI image
        # self.mediaView.setSource(self.currentStep.displayPath)
        
        # Start timer to decrease time left label
        if durationS != None:
            self.timeLeftTimer = QTimer()
            self.timeLeftTimer.timeout.connect(self._decreaseDuration)
            self.timeLeftTimer.start(1000)

        self.stepQueue.pop(0)

        if self.usingAR:
            self.microbeObj.delMicrobe()


    @pyqtSlot()
    def _decreaseDuration(self):
        self.stepDuration -= 1
        durationS = self.stepDuration

        if durationS <= 0:
            self.timeLeftTimer.stop()
            self.nextStep()

        else:
            self.timeLeftLbl.setText(f"{durationS - 1} s")

    
    @pyqtSlot(QImage)
    def updateVideoFeed(self, image):
        self.videoFeed.setPixmap(QPixmap.fromImage(image))


    def show(self):
        self.setWindowTitle("Hand Washing Steps")
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.showFullScreen()