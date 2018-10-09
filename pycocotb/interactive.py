
import cocotb
import importlib
import yaml
from cocotb.triggers import Timer
import os

@cocotb.test()
def remote_test(dut):
    with open(os.getenv('CONFIG_YAML')) as f:
        sim_config = yaml.load(f)['simulation']

    devs = {}
    for key, conf in sim_config['devices'].items():
        mod = importlib.import_module(conf['module'])
        dev_class = getattr(mod, conf['class'])
        devs[key] = dev_class(dut, conf['dev'], **(conf['args']))

    dut._log.info('Starting')

    while True:
        yield Timer(1000, units='us')


