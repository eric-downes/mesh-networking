#!/usr/bin/env python
import random
import time

from mesh.links import UDPLink
from mesh.programs import BaseProgram
from mesh.filters import UniqueFilter
from mesh.node import Node

class SensorReaderProgram(BaseProgram):
    def recv(self, packet, interface) -> None:
        # We received a response.  Print it.
        print('\nreceived: {}'.format(packet.decode()))


if __name__ == "__main__":
    links = [UDPLink('en0', 2010), UDPLink('en1', 2011), UDPLink('en2', 2012), UDPLink('en3', 2013)]
    node = Node(links, 'me', Filters=(UniqueFilter,), Program=SensorReaderProgram)
    [link.start() for link in links]
    node.start()

    print("Make sure sensor.py is running on another laptop to send data to you on en0.")
    try:
        seq_num = random.randint(0, 2**32 - 1)
        while True:
            # Send a query.  Sequence number is so every query is unique.
            node.send(bytes(f'read_time {seq_num}', 'UTF-8'))
            time.sleep(1.0)
            seq_num += 1
            if seq_num == 2**32:
                seq_num = 0

    except (EOFError, KeyboardInterrupt):   # graceful CTRL-D & CTRL-C
        node.stop()
        [link.stop() for link in links]
