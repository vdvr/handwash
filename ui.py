import sys
from datetime import datetime
import locale
import yaml
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout, 
    QGraphicsScene, 
    QGraphicsView,
)
from PyQt5.QtSvg import QGraphicsSvgItem
from PyQt5.QtCore import Qt, pyqtSlot, QTimer
from PyQt5.QtGui import QFont, QFontDatabase



class Step:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.description = kwargs.get("description")
        self.durationS = kwargs.get("durationS", 0) + 1
        self.image = kwargs.get("image")



class StepUI(QWidget):
    def __init__(self, steps=None):
        super().__init__()
        
        # Initialize properties
        self.currentStep = None
        self.stepQueue = steps
        self.totalSteps = len(steps)

        # Initialize window
        self.setWindowTitle('Hand Washing Steps')
        self.setStyleSheet("background-color: black")

        # Initialize layouts 
        self.mainLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.bottomLayout = QHBoxLayout()
        self.setLayout(self.mainLayout)

        # Import fonts
        self._importFonts()

        # Add layouts, step photo and description to main layout
        self.mainLayout.addLayout(self.topLayout, 2)

        self.photoView = QGraphicsView()
        self.photoView.setStyleSheet('border: none')
        self.photoView.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.mainLayout.addWidget(self.photoView, 6)

        self.stepDescLbl = QLabel()
        self.stepDescLbl.setFont(QFont("Roboto Condensed", 30))
        self.stepDescLbl.setStyleSheet("color: white;")
        self.stepDescLbl.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.mainLayout.addWidget(self.stepDescLbl, 1)

        self.mainLayout.addLayout(self.bottomLayout, 1)

        # Initialize time left label and add to layout
        self.timeLeftLbl = QLabel()
        self.timeLeftLbl.setFont(QFont("Roboto", 90, QFont.Thin))
        self.timeLeftLbl.setStyleSheet("color: white; margin: 20px;")
        self.timeLeftLbl.setAlignment(Qt.AlignLeft)
        self.topLayout.addWidget(self.timeLeftLbl)

        # Initialize step label and add to layout
        self.stepLayout = QVBoxLayout()
        self.stepTxtLbl = QLabel("Stap:")
        self.stepTxtLbl.setFont(QFont("Roboto Condensed", 30, QFont.Bold))
        self.stepTxtLbl.setStyleSheet("color: white; margin: 30px 40px 0px;")
        self.stepTxtLbl.setAlignment(Qt.AlignRight)
        self.stepLayout.addWidget(self.stepTxtLbl)

        self.stepNrLbl = QLabel()
        self.stepNrLbl.setFont(QFont("Roboto", 50, QFont.Light))
        self.stepNrLbl.setStyleSheet("color: white; margin: 0px 20px;")
        self.stepNrLbl.setAlignment(Qt.AlignRight)
        self.stepLayout.addWidget(self.stepNrLbl)
        self.stepLayout.addStretch()
        self.stepLayout.setSpacing(0)
        self.topLayout.addLayout(self.stepLayout)

        # Initialize current time and date label and add to layout
        dateNow = datetime.strftime(datetime.now(), "%A %d %B")
        timeNow = datetime.strftime(datetime.now(), "%H:%M")

        self.dateTimeLayout = QVBoxLayout()
        self.dateLbl = QLabel(dateNow)
        self.dateLbl.setFont(QFont("Roboto Condensed", 20, QFont.Light))
        self.dateLbl.setStyleSheet("color: white; margin: 0px 20px;")
        self.dateLbl.setAlignment(Qt.AlignRight)
        self.dateTimeLayout.addWidget(self.dateLbl)

        self.timeLbl = QLabel(timeNow)
        self.timeLbl.setFont(QFont("Roboto", 40, QFont.Bold))
        self.timeLbl.setStyleSheet("color: white; margin: 0px 20px;")
        self.timeLbl.setAlignment(Qt.AlignRight)
        self.dateTimeLayout.addWidget(self.timeLbl)
        self.dateTimeLayout.addStretch()
        self.dateTimeLayout.setSpacing(0)
        self.bottomLayout.addLayout(self.dateTimeLayout)

        # Start timer for current time
        self.clockTimer = QTimer()
        self.clockTimer.timeout.connect(self._updateClock)
        self.clockTimer.start(1000)

        # Start showing steps
        if steps != None:
            self._nextStep()
            self.show()


    def _importFonts(self):
        QFontDatabase.addApplicationFont("fonts/Roboto/Roboto-Thin.ttf")
        QFontDatabase.addApplicationFont("fonts/Roboto/Roboto-Light.ttf")
        QFontDatabase.addApplicationFont("fonts/Roboto/Roboto-Regular.ttf")
        QFontDatabase.addApplicationFont("fonts/Roboto/Roboto-Medium.ttf")
        QFontDatabase.addApplicationFont("fonts/Roboto/Roboto-Bold.ttf")
        QFontDatabase.addApplicationFont("fonts/Roboto/Roboto-Black.ttf")
        QFontDatabase.addApplicationFont("fonts/RobotoCondensed/RobotoCondensed-Light.ttf")
        QFontDatabase.addApplicationFont("fonts/RobotoCondensed/RobotoCondensed-Regular.ttf")
        QFontDatabase.addApplicationFont("fonts/RobotoCondensed/RobotoCondensed-Bold.ttf")


    def _nextStep(self):
        # Exit if no steps left
        stepsLeft = len(self.stepQueue)
        if stepsLeft < 1:
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
        scene = QGraphicsScene()
        photoItem = QGraphicsSvgItem(self.currentStep.image)
        photoItem.setScale(4)
        scene.addItem(photoItem)
        self.photoView.setScene(scene)
        
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
            self._nextStep()

        else:
            self.timeLeftLbl.setText(f"{durationS - 1} s")
        

    @pyqtSlot()
    def _updateClock(self):
        
        # Set current time
        dateNow = datetime.strftime(datetime.now(), "%A %d %B")
        timeNow = datetime.strftime(datetime.now(), "%H:%M")
        self.dateLbl.setText(dateNow)
        self.timeLbl.setText(timeNow)



    def show(self):
        self.showFullScreen()



if __name__ == "__main__":
    locale.setlocale(locale.LC_TIME, "nl_BE")

    with open('steps.yaml') as f:
        yamlSteps = yaml.safe_load(f)
    
    steps = [
        Step(
            name=name,
            **stepOpt
        )
            for step in yamlSteps["steps"] 
            for (name, stepOpt) in step.items()
    ]
    
    app = QApplication(sys.argv)
    stepUI = StepUI(steps)
    sys.exit(app.exec_())