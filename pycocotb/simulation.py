import yaml
import subprocess
import importlib
from multiprocessing import Process
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
        self.p = subprocess.Popen('exec make', shell=True, preexec_fn=os.setsid)

    def finish(self):
        os.killpg(self.p.pid, 9)
        self.wait_finish()

    def wait_finish(self):
        self.p.wait()

    def __del__(self):
        self.finish()

