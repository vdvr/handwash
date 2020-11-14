import asyncio
import concurrent
import zmq
import threading
from serial import Serial

class Cmd(enum.Enum):
    ACK = 0x20
    NACK = 0x21
    POLL_REQUEST = 0x30
    POLL_REPLY = 0x31
    REQ_WATER = 0x32
    REQ_SOAP = 0x33
    WATER_DONE = 0x34
    SOAP_DONE = 0x35

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
    

def deserialize(serialized: str) -> Package:
    """
    Deserialize a package to its components
    """
    if (serialized[0] == '\x02'): # STX check
        if (serialized[-2] == '\x03'): # ETX check
            serialized = serialized[1:-2].split('\r') # ['cmd\x00', 'args\x00']
            return Package(serialized[0][:-1], serialized[1][:-1])

# Normal serial blocking reads
# This could also do any processing required on the data
def get_byte():
    b = s.read(1)
    # print(b)
    return b

# Runs blocking function in executor, yielding the result
@asyncio.coroutine
def get_byte_async():
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        res = yield from loop.run_in_executor(executor, get_byte)
        return res

def get_and_print():
    b = ''
    readed = b""
    while (b != b'\x02'):
        b = yield from get_byte_async()
    readed += b'\x02'
    while (b != b'\x03'):
        readed += yield from get_byte_async()
    return readed
        

s = Serial("/dev/serial0", 57600, timeout=10)
loop = asyncio.get_event_loop()

def roll():
    loop.run_until_complete(get_and_print())
    pkg = deserialize(readed)
    ui_sock.send_string(pkg.serialize())

if __name__ == "__main__":
    readed = ""
    try:
        roll()
    except KeyboardInterrupt:
        loop.close()
        pass
    finally:
        roll()
