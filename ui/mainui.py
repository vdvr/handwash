from . import StepUI, IdleUI
import enum
import sysv_ipc
import codecs

from PyQt5.QtCore import Qt, pyqtSlot, QTimer
from PyQt5.QtWidgets import (
    QMainWindow
)

class Cmd(enum.Enum):
    ACK = 0x20
    NACK = 0x21
    POLL_REQUEST = '0'
    POLL_REPLY = '1'
    REQ_WATER = '2'
    REQ_SOAP = '3'
    WATER_DONE = '4'
    SOAP_DONE = '5'


class MainUI(QMainWindow):
    def __init__(self, steps, startTxt=None, styleFile=None):
        super().__init__()

        rq = sysv_ipc.MessageQueue(12345, sysv_ipc.IPC_CREAT)
        sq = sysv_ipc.MessageQueue(778899, sysv_ipc.IPC_CREAT)

        self.sender = sq
        self.receiver = rq

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
        self.showNormal()


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
        payload = str(cmd.value) + ';' + args
        self.sender.send(payload, True, type=1)


    def getMsg(self):
        try:
            payload = self.receiver.receive(block=False)
        except:
            return
        (payload, payload_type) = payload
        payload = payload.decode("utf-8").split('\x00', 1)[0]
        print(payload)
        if payload:
            payload.split(';')
            cmd = Cmd(payload[0])
            return {"cmd": cmd, "args": payload[1:]}
