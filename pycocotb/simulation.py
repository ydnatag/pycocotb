import yaml
import subprocess
import importlib
from multiprocessing import Process
from pycocotb.remote import RemoteClient
from pycocotb.triggers import Triggers
from pycocotb.clock import Clock
import logging
import os

class Simulation(object):

    default_settings = {'path':os.getenv('PWD'),
                        'cocotb_path':None,
                        'sim':None,
                        'mode':'legacy',
                        'files':None,
                        'sim_args':None,
                        'toplevel':None,
                        'module':None}

    def __init__(self):
        self.settings = self.default_settings
        self.devs = {}
        self.log = logging.getLogger('Sim')

    def set_config(self, file):
        self.settings_file = file
        with open(file) as f:
            settings = yaml.load(f)

        for k in settings['simulation'].keys():
            self.settings[k] = settings['simulation'][k]

        for key, conf in settings['simulation']['devices'].items():
            #mod = importlib.import_module(conf['module'])
            #dev_class = getattr(mod, conf['class'])
            #self.devs[key] = dev_class(dut, conf['dev'], **(conf['args']))
            pass

    def build_with_make(self):
        os.system('make build -C {}'.format(self.settings['path']))

    def generate_make(self):
        lines = []
        lines.append('COCOTB = ' + self.settings['cocotb_path'])
        lines.append('TOPLEVEL_LANG = ' + 'verilog')
        lines.append('VERILOG_SOURCES = ' + ' '.join(self.settings['files']))
        lines.append('TOPLEVEL = ' + self.settings['toplevel'])
        lines.append('MODULE = ' + self.settings['module'])
        lines.append('export CONFIG_YAML = ' + self.settings_file)
        lines.append('include $(COCOTB)/makefiles/Makefile.inc')
        lines.append('include $(COCOTB)/makefiles/Makefile.sim')
        lines.append('')

        with open(self.settings['path'] + 'Makefile','+w') as f:
            f.writelines([l + '\n' for l in lines])

    def build(self):
        if not self.settings['files']:
            raise ValueError('No files')
        if not self.settings['toplevel']:
            raise ValueError('No toplevel')
        if not self.settings['sim']:
            raise ValueError('No simulator')
        self.generate_make()
        self.build_with_make()

    def clean(self):
        os.system("rm -rf sim_build")
        os.system("rm -f Makefile")
        os.system("rm -f results.xml")

    def run(self):
        self.p = subprocess.Popen('exec make', shell=True, stdout=subprocess.DEVNULL, preexec_fn=os.setsid)
        #self.comm = RemoteClient(debug=True)
        #self.wait = Triggers(self.comm)
        #self.clock = Clock(self.comm)

    def import_module(self, module):
        self.comm.send_recv('import {}'.format(module))

    def fork(self, cr, args=None):
        if not args:
            args = []
        msg = 'cocotb.fork({}({}))'.format(cr, ', '.join(args))
        return self.comm.send_recv(msg)

    def finish(self, force=False): #TODO: Not working
        os.killpg(self.p.pid, 9)
        self.wait_finish()

    def wait_finish(self):
        self.p.wait()


    def get_value(self, signal):
        ret = self.comm.send_recv(signal)
        self.log.debug("get_value:%s => %s" % (signal, ret))
        return ret

    def set_value(self, signal, value):
        ret = self.comm.send_recv("%s = %s" % (signal, value))
        self.log.debug("set_value:%s <= %s" % (signal, value))

    def __del__(self):
        self.finish()

