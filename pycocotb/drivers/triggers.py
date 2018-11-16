import cocotb
from threading import Thread
from cocotb.triggers import Event
from cocotb.result import ReturnValue

def _wait_python_function_thread(event, ret, func, args):
    if args is None:
        args = []
    assert isinstance(args, list)
    print("thread")
    ret.append(func(*args))
    event.set()

@cocotb.coroutine
def wait_python_function(func, args=None):
    evnt = Event()
    ret = []
    t = Thread(target=_wait_python_function_thread, args=[evnt, ret, func, args])
    t.start()
    yield evnt.wait()
    raise ReturnValue(ret[0])



class Triggers(object):
    def __init__(self, comm):
        self.comm = comm

    def rising_edge(self, signal):
        self.comm.send_recv('yield RisingEdge({})'.format(signal))

    def edge(self, signal):
        self.comm.send_recv('yield Edge({})'.format(signal))

    def falling_edge(self, signal):
        self.comm.send_recv('yield FallingEdge({})'.format(signal))

    def time(self, time, unit='ns'):
        self.comm.send_recv('yield Timer({}, units="{}")'.format(time, unit))

    def read_only(self):
        self.comm.send_recv('yield ReadOnly()')

