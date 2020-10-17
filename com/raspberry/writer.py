#!/usr/bin/python3.7

import sys
import asyncio
from packet import Packet

async def send_to_worker(message):
    writer = await asyncio.open_connection(
        '127.0.0.1', 8888)
    writer.write(message.encode('ascii'))
    writer.close()

if __name__ == '__main__':
    pkg = Packet(sys.argv[1], sys.argv[2])
    asyncio.run(send_to_worker(pkg.serialize()))