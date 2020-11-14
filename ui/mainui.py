from . import StepUI, IdleUI
import enum
from PyQt5.QtCore import Qt, pyqtSlot, QTimer
from PyQt5.QtWidgets import (
    QMainWindow
)
import serial

class Cmd(enum.Enum):
    ACK = 1
    NACK = 2
    REQ_WATER = 3
    REQ_SOAP = 4
    WATER_DONE = 5
    SOAP_DONE = 6
    


class MainUI(QMainWindow):
    def __init__(self, device, steps, startTxt=None, styleFile=None):
        super().__init__()

        self.com = serial.Serial(device, 9600, timeout=0)

        if styleFile != None:
            with open(styleFile) as styleFileObj:
                self.setStyleSheet(styleFileObj.read())
        self.steps = steps
        self.startTxt = startTxt
        
        self.isStarted = False
        self.setCentralWidget(IdleUI(startTxt))

        self.timeReadMsg = QTimer()
        self.timeReadMsg.timeout.connect(self._handleMsg)
        self.timeReadMsg.start(10)


    def show(self):
        self.setWindowTitle("Hand Wash Mirror")
        #self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.showFullScreen()


    @pyqtSlot() 
    def idle(self):
        self.isStarted = False
        self.setCentralWidget(IdleUI(self.startTxt))


    def startSteps(self):
        stepUI = StepUI(self.steps.copy())
        stepUI.finished.connect(self.idle)
        self.setCentralWidget(stepUI)
        self.isStarted = True


    @pyqtSlot()
    def _handleMsg(self):
        msg = self.getMsg()
        if not msg:
            return
            
        cmd = msg["cmd"]

        if not self.isStarted:
            if (cmd == Cmd["REQ_WATER"] and self.steps[0].water or
                cmd == Cmd["REQ_SOAP"] and self.steps[0].soap):

                self.sendMsg(Cmd["ACK"], "")
                self.startSteps()
                return

        else:
            currentStep = self.centralWidget().currentStep

            if (cmd == Cmd["REQ_WATER"] and currentStep.water or
                cmd == Cmd["REQ_SOAP"] and currentStep.soap):

                self.sendMsg(Cmd["ACK"], "")
                return
            
            elif (cmd == Cmd["WATER_DONE"] and currentStep.water or
                  cmd == Cmd["SOAP_DONE"] and currentStep.soap):
                
                self.centralWidget().nextStep()
                return
        
        self.sendMsg(Cmd["NACK"], "")


    def sendMsg(self, cmd, args):
        payload = f"{cmd.value}{args}\n".encode("ascii")
        self.com.write(payload)


    def getMsg(self):
        payload = self.com.readline()
        if payload:
            msg = payload.decode("ascii")
            cmd = Cmd(int(msg[0]))
            return {"cmd": cmd, "args": msg[:-1]}