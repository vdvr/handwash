import sys
from datetime import datetime
import yaml
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout, 
)
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtCore import Qt, pyqtSlot, QTimer
from PyQt5.QtGui import QFont



class Step:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.description = kwargs.get("description")
        self.durationMs = kwargs.get("durationMs")
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

        # Add layouts and step photo to main layout
        self.mainLayout.addLayout(self.topLayout)
        self.stepPhoto = QSvgWidget()
        self.mainLayout.addWidget(self.stepPhoto, alignment=Qt.AlignHCenter | Qt.AlignVCenter)
        self.mainLayout.addLayout(self.bottomLayout)

        # Initialize time left label and add to layout
        self.timeLeftLbl = QLabel()
        self.timeLeftLbl.setFont(QFont('Arial', 20))
        self.timeLeftLbl.setStyleSheet('color: white')
        self.timeLeftLbl.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.topLayout.addWidget(self.timeLeftLbl)

        # Initialize step label and add to layout
        self.stepNrLbl = QLabel()
        self.stepNrLbl.setFont(QFont('Arial', 20))
        self.stepNrLbl.setStyleSheet('color: white')
        self.stepNrLbl.setAlignment(Qt.AlignRight | Qt.AlignTop)
        self.topLayout.addWidget(self.stepNrLbl)

        # Initialize current time label and add to layout
        time = datetime.strftime(datetime.now(), "%d/%m/%y %H:%M")
        self.timeLbl = QLabel(f"Tijd: {time}")
        self.timeLbl.setFont(QFont('Arial', 20))
        self.timeLbl.setStyleSheet('color: white')
        self.timeLbl.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.bottomLayout.addWidget(self.timeLbl)

        # Start timer for current time
        self.clockTimer = QTimer()
        self.clockTimer.timeout.connect(self._updateClock)
        self.clockTimer.start(1000)

        # Start showing steps
        if steps != None:
            self._nextStep()
            self.show()


    @pyqtSlot()
    def _nextStep(self):

        # Calculate steps left and current step nr
        self.currentStep = self.stepQueue[0]
        stepsLeft = len(self.stepQueue)
        currentStepNr = self.totalSteps - stepsLeft + 1

        # Update UI labels
        durationS = int(self.currentStep.durationMs / 1000)
        self.timeLeftLbl.setText(f"Duur: {durationS}s")
        self.stepNrLbl.setText(f"Stap: {currentStepNr}/{self.totalSteps}")
        
        # Update UI image
        newPhoto = QSvgWidget(self.currentStep.image)
        self.mainLayout.replaceWidget(self.stepPhoto, newPhoto)
        self.stepPhoto = newPhoto
        
        # Start timer to call nextStep
        if stepsLeft > 1:
            QTimer.singleShot(self.currentStep.durationMs, self._nextStep)
        
        # Start timer to decrease time left label
        self.timeLeftTimer = QTimer()
        self.timeLeftTimer.timeout.connect(self._decreaseDuration)
        self.timeLeftTimer.start(200)

        self.stepQueue.pop(0)


    @pyqtSlot()
    def _decreaseDuration(self):
        self.currentStep.durationMs -= 200
        durationS = int(self.currentStep.durationMs / 1000)

        if durationS <= 0:
            self.timeLeftTimer.stop()

        self.timeLeftLbl.setText(f"Duur: {durationS}s")
        

    @pyqtSlot()
    def _updateClock(self):
        
        # Set current time
        time = datetime.strftime(datetime.now(), "%d/%m/%y %H:%M")
        self.timeLbl.setText(f"Tijd: {time}")



    def show(self):
        self.showFullScreen()



if __name__ == "__main__":
    with open('steps.yaml') as f:
        yamlSteps = yaml.safe_load(f)
    print(yamlSteps["steps"])
    
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