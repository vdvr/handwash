'''
RASPBERRY PI SIMULATION

RECEIVE:
prints all serial connection,
debug information prefixed by "INFO:"
communication packets in "CMD: ... ARGS: ..." format
each newline represents data ending with \3 character

TRANSMIT:
write command in hexadecimal and arguments in ASCII format and press enter
see list of commands below, nothing is send if not one of those
command and arguments separated by space, e.g. "31 test" for command POLL_REQUEST and arg test
if data is received and printed while typing, typed text will be chopped in half, just keep typing as if nothing happened
'''

import sys
import serial
import threading
import enum

class Cmd(enum.Enum):
    ACK = 0x20
    NACK = 0x21
    POLL_REQUEST = 0x30
    POLL_REPLY = 0x31
    REQUEST_WATER = 0x32
    REQUEST_SOAP = 0x33
    WATER_DONE = 0x34
    SOAP_DONE = 0x35


class ArduinoSerial(serial.Serial):
    def readuntil(self, s):
        r = b''
        c = b''
        while (c != s):
            c = self.read()
            if c == b'':
                return b''
            else:
                r += c
        return r

    def txThread(self):
        while True:
            cmd_in, *args_in = input().split(' ')
            try:
                cmd = int(cmd_in, 16)
                payload = f"\2{chr(cmd)}\r{''.join(args_in)}\3"
                self.write(payload.encode('ascii'))
            except:
                pass

    def rxThread(self):
        while True:
            rx_frame = self.readuntil(b'\x03')
            try:
                payload = rx_frame.decode('ascii')
            except:
                print(rx_frame)
                continue
            
            if (ord(payload[0]) == 2) and (ord(payload[-1]) == 3):
                cmd, *args = payload[1:-1].split('\r')
                try:
                    cmd = Cmd(ord(cmd)).name
                except:
                    pass

                print(f"CMD: {cmd}, ARGS {args}")
            else:
                print(f"INFO: {payload[:-1]}")


if __name__ == '__main__':
    dev = '/dev/serial0' if len(sys.argv) == 1 else sys.argv[1]
    global ser_dev
    ser_dev = ArduinoSerial(dev, 9600)
    threading.Thread(target=ser_dev.rxThread).start()
    threading.Thread(target=ser_dev.txThread).start()
