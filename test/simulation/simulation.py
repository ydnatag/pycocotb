from pycocotb.simulation import Simulation
import logging

if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    sim = Simulation()
    sim.get_config(file='settings.yaml')
    sim.build()
    sim.run()

    dut = sim.get_dut()

    dut.get_value('dut.a')
    dut.set_value('dut.a', 1)
    sim.wait.time(10)

    dut.set_value('dut.a', 0)
    sim.wait.read_only()
    dut.get_value('dut.a')

    sim.wait.time(10)
    sim.clock.start('dut.a', 1, 'us')

    #sim.import_module('cocotb.clock')
    #sim.fork('cocotb.clock.Clock(dut.a, 100, units="ns").start')
    for _ in range(10):
        sim.wait.rising_edge('dut.a')

    for _ in range(10):
        sim.wait.edge('dut.a')

    for _ in range(10):
        sim.wait.falling_edge('dut.a')

    sim.finish()
    sim.comm.send('break')
    sim.comm.recv()

    sim.wait_finish()