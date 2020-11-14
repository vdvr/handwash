from . import StepUI, IdleUI
import enum
import zmq
from PyQt5.QtCore import Qt, pyqtSlot, QTimer
from PyQt5.QtWidgets import (
    QMainWindow
)


context = zmq.Context()
send_socket = context.socket(zmq.PUSH)
send_socket.connect('tcp://127.0.0.1:5557')
recv_socket = context.socket(zmq.PULL)
recv_socket.connect('tcp://127.0.0.1:5556')


class Cmd(enum.Enum):
    ACK = 1
    NACK = 2
    REQ_WATER = 3
    REQ_SOAP = 4
    WATER_DONE = 5
    SOAP_DONE = 6


class MainUI(QMainWindow):
    def __init__(self, steps, startTxt=None, styleFile=None):
        super().__init__()

        self.com = serial.Serial("COM8", 9600, timeout=0)

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
        send_msg = cmd + '|' + args
        send_socket.send_string(send_msg)

    def getMsg(self):
        payload = recv_socket.recv_string()
        if payload:
            payload = payload.split('|')
            if (payload[0] == "water"):
                if (payload[1] == "request;"):
                    return {"cmd": Cmd["REQ_WATER"], "args": payload[1]}
                elif (payload[1] == "done;"):
                    return {"cmd": Cmd["WATER_DONE"], "args": payload[1]}
            elif (payload[0] == "soap"):
                if (payload[1] == "request;"):
                    return {"cmd": Cmd["REQ_SOAP"], "args": payload[1]}
                elif (payload[1] == "done;"):
                    return {"cmd": Cmd["SOAP_DONE"], "args": payload[1]}
