#!/usr/bin/env python
import re
import time

from mesh.links import UDPLink
from mesh.programs import BaseProgram
from mesh.filters import UniqueFilter
from mesh.node import Node

TIME_QUERY_PATTERN = re.compile(r'\Aread_time\b')

class SensorProgram(BaseProgram):
    def recv(self, packet, interface) -> None:
        message = packet.decode()
        print('\nreceived: {}'.format(message))
        if TIME_QUERY_PATTERN.match(message):
            answer = self.read_time()
            print('\nsending time: {}'.format(answer))
            self.node.send(bytes(str(answer), 'UTF-8'))

    def read_time(self) -> int:
        return int(time.time())

if __name__ == "__main__":
    links = [UDPLink('en0', 2010), UDPLink('en1', 2011), UDPLink('en2', 2012), UDPLink('en3', 2013)]
    node = Node(links, 'me', Filters=(UniqueFilter,), Program=SensorProgram)
    [link.start() for link in links]
    node.start()

    print("Run sensor_reader.py on another laptop to read sensor data on en0.")
    try:
        while True:
            time.sleep(0.3)

    except (EOFError, KeyboardInterrupt):   # graceful CTRL-D & CTRL-C
        node.stop()
        [link.stop() for link in links]
