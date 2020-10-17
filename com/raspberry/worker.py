#!/usr/bin/python3.7

import asyncio
import aioserial
from packet import Packet

serial_port = "/dev/serial0"
serial_baudrate = 115200
aio: aioserial.AioSerial = aioserial.AioSerial(port=serial_port, baudrate=serial_baudrate)

async def serial_writer(serialized):
    await aio.write_async(serialized.encode())

async def handler(reader, writer):
    data = await reader.read(40)
    message = data.decode()
    print(f"\nReceived from writer.py")
    
    message = message.split('\x00')
    pkg = Packet(message[0], message[1])
    pkg.pp()
    await serial_writer(pkg.serialize())

    print("Connection Closed")
    writer.close()

async def socket_worker():
    server = await asyncio.start_server(
        handler, '127.0.0.1', 8888)

    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(socket_worker())
    loop.run_forever()