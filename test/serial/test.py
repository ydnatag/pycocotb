from pycocotb.simulation import Simulation
from pycocotb.devices import SimSerial
import logging
import time
from serial import Serial
from time import sleep


if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    sim = Simulation()
    sim.set_config(file='settings.yaml')
    sim.build()
    sim.run()
    dev = sim.settings['devices']['uart']['dev']

    uart = SimSerial(dev, sim=sim)
    sleep(1)
    logging.info('Sending: Hola')
    uart.write(b'Hola')
    logging.info('Received: {}'.format(uart.read(size=4)))

