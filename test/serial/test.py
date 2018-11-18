from pycocotb.simulation import Simulation
import logging
import json
import zmq
import time
import yaml
from serial import Serial
import sys
from time import sleep


class VirtualUart(object):
    def __init__(self, dev, baudrate=9600, sim=False):
        if not sim:
            self.dev = Serial(dev)
            self.write = self.dev.write
            self.read = self.dev.read
        else:
            context = zmq.Context()
            self.dev = context.socket(zmq.PAIR)
            self.dev.bind('ipc://'+ dev)
            self.write = self.dev.send
            self.read = lambda size: b''.join([self.dev.recv() for _ in range(size)])


if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    if len(sys.argv) < 2:
        sim = Simulation()
        sim.set_config(file='settings.yaml')
        sim.build()
        sim.run()
        dev = sim.settings['devices']['uart']['dev']
    else:
        sim = None
        with open('settings.yaml') as f:
            dev = yaml.load(f)['devices']['uart']['dev']

    uart = VirtualUart(dev, sim=sim)
    sleep(1)
    logging.info('Sending: Hola')
    uart.write(b'Hola')
    logging.info('Received: {}'.format(uart.read(size=4)))

