import sys
import serial
import enum


class Cmd(enum.Enum):
    ACK = 1
    NACK = 2
    REQ_WATER = 3
    REQ_SOAP = 4
    WATER_DONE = 5
    SOAP_DONE = 6

if __name__ == '__main__':
    dev = '/dev/serial0' if len(sys.argv) == 1 else sys.argv[1]
    with serial.Serial(dev, 9600, timeout=0, write_timeout=0) as ser_dev:
        print(f"device: {ser_dev.name}")
        while True:
            inp = input('to send: ')
            try:
                print(Cmd(int(inp)))
                ser_dev.reset_output_buffer()
                cmd = (inp + '\n').encode("ascii")
                ser_dev.write(cmd)
            except:
                msg = ser_dev.readline().decode("ascii")
                ser_dev.reset_input_buffer()
                try:
                    cmd = Cmd(int(msg[0])).name
                    print(f"cmd: {cmd}, args: {msg[1:-1]}")
                except:
                    pass