from . import StepUI, IdleUI
import enum
import zmq
from PyQt5.QtCore import Qt, pyqtSlot, QTimer
from PyQt5.QtWidgets import (
    QMainWindow
)

class Cmd(enum.Enum):
    ACK = 0x20
    NACK = 0x21
    POLL_REQUEST = 0x30
    POLL_REPLY = 0x31
    REQ_WATER = 0x32
    REQ_SOAP = 0x33
    WATER_DONE = 0x34
    SOAP_DONE = 0x35

context = zmq.Context()

send_sock = context.socket(zmq.PUSH)
send_socket.connect('tcp://127.0.0.1:5556')

recv_sock = context.socket(zmq.PUSH)
recv_socket.connect('tcp://127.0.0.1:5555')

class MainUI(QMainWindow):
    def __init__(self, steps, startTxt=None, styleFile=None):
        super().__init__()

        self.sender = send_socket
        self.receiver = 
        
        self.setCursor(Qt.BlankCursor)

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
        payload = cmd + ';' + args
        self.sender.send_string(payload)


    def getMsg(self):
        payload = self.receiver.recv_string()
        if payload:
            msg = payload.decode("ascii")
            msg.split(';')
            cmd = Cmd(msg[0])
            return {"cmd": cmd, "args": msg[1:]}
