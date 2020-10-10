import sys
import time
import yaml
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout, 
    QGraphicsView,
)
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtCore import Qt, pyqtSlot, QTimer



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
        self.steps = steps
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
        self.timeLeftLbl.setStyleSheet('color: white')
        self.timeLeftLbl.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.topLayout.addWidget(self.timeLeftLbl)

        # Initialize step label and add to layout
        self.stepNrLbl = QLabel()
        self.stepNrLbl.setStyleSheet('color: white')
        self.stepNrLbl.setAlignment(Qt.AlignRight | Qt.AlignTop)
        self.topLayout.addWidget(self.stepNrLbl)

        # Initialize current time label and add to layout
        self.timeLbl = QLabel()
        self.timeLbl.setStyleSheet('color: white')
        self.timeLbl.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.bottomLayout.addWidget(self.timeLbl)

        if steps != None:
            self.nextStep()
            self.show()

    @pyqtSlot()
    def nextStep(self):
        self.currentStep = self.steps[0]
        stepsLeft = len(self.steps)
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
            QTimer.singleShot(self.currentStep.durationMs, self.nextStep)
        
        # Start timer to decrease time left label
        self.timeLeftTimer = QTimer()
        self.timeLeftTimer.timeout.connect(self.decreaseDuration)
        self.timeLeftTimer.start(200)

        self.steps.pop(0)

    @pyqtSlot()
    def decreaseDuration(self):
        self.currentStep.durationMs -= 200
        durationS = int(self.currentStep.durationMs / 1000)

        if durationS <= 0:
            self.timeLeftTimer.stop()

        self.timeLeftLbl.setText(f"Duur: {durationS}s")
        

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