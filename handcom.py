from asyncio import get_event_loop
import binascii
import concurrent
import zmq
import threading
import serial
from time import sleep

class Package:
    def __init__(self, command, arguments) -> None:
        self.command = command + '\0'
        self.arguments = arguments + '\0'
    
    def command2hex(self) -> str:
        return bytes.fromhex(self.command)
    
    def arguments2hex(self) -> str:
        return bytes.fromhex(self.arguments)

    def serialize(self) -> str:
        return self.command + ';' + self.arguments
    

context = zmq.Context()
ui_sock = context.socket(zmq.PUSH)
ui_sock.bind("tcp://*:5555")

def serialize(pkg: Package) -> str:
    """
    Serialize a package to a sendable string
    """
    serialized = ""
    serialized += '\x02' # STX
    serialized += pkg.command2hex()
    serialized += '\r'
    serialized += pkg.arguments2hex()
    serialized += '\x03'
    serialized += '\x00'
    

def deserialize(serialized) -> Package:
    """
    Deserialize a package to its components
    """
    if (serialized[0] == 2): # STX check
        if (serialized[-1] == 3): # ETX
            string = serialized[1:-1]
            string = ''.join(chr(i) for i in string)
            string = string.split('\r')

            return Package(string[0], string[1])

if __name__ == "__main__":
    readed = b""
    b = b""
    while True:
        ser = serial.Serial('/dev/serial0', 57600)
        read = ser.read_until(b'\x03')
        pkg = deserialize(read)
        ui_sock.send_string(pkg.serialize())
        sleep(0.02)
