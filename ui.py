import sys
import time
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout, 
    QGraphicsView,
)
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtCore import Qt

class Step:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.description = kwargs.get("description")
        self.stepNr = kwargs.get("stepNr")
        self.durationMs = kwargs.get("durationMs")
        self.image = kwargs.get("image")

class StepUI(QWidget):
    def __init__(self, totalSteps, firstStep=None):
        super().__init__()
        
        # Initialize properties
        self.currentStep = None
        self.totalSteps = totalSteps

        # Initialize window
        self.setWindowTitle('Hand Washing Steps')
        self.setStyleSheet("background-color: black")
        #self.move(0, 0)

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

        if firstStep != None:
            self.setStep(firstStep)
            self.show()


    def setStep(self, step):
        self.currentStep = step

        # Update UI labels
        durationS = int(step.durationMs / 1000)
        self.timeLeftLbl.setText(f"Duur: {durationS}s")
        self.stepNrLbl.setText(f"Stap: {step.stepNr}/{self.totalSteps}")
        
        # Update UI image
        newPhoto = QSvgWidget(step.image)
        self.mainLayout.replaceWidget(self.stepPhoto, newPhoto)
        self.stepPhoto = newPhoto
        

    def show(self):
        self.showFullScreen()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    stepUI = StepUI(9, Step(name="Inzepen",
                            description="Neem zeep uit de zeepdispenser", 
                            stepNr=1,
                            durationMs=5_000,
                            image="images/steps/1.svg"))
    sys.exit(app.exec_())