import cocotb
from cocotb.triggers import Event
import struct
import zmq
from threading import Thread
from cocotb.result import ReturnValue
from cocotb.triggers import FallingEdge, RisingEdge, Timer

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


class Uart(object):
    nbits = 8
    parity = False
    baudrate = 9600
    stop = 1
    def __init__(self, dut, dev=None, prefix='', **kwargs):
        self.tx = getattr(dut, prefix + 'TX')
        self.rx = getattr(dut, prefix + 'RX')
        self.dut = dut
        for k, v in kwargs.items():
            setattr(self, k, v)

        if dev is not None:
            context = zmq.Context()
            self.socket = context.socket(zmq.PAIR)
            self.socket.connect("ipc://%s" % dev)

        self.period = int(1/self.baudrate*1000*1000*1000)
        cocotb.fork(self.tx_monitor_coroutine())
        cocotb.fork(self.rx_driver_coroutine())

    @cocotb.coroutine
    def rx_driver_coroutine(self):
        half_period_timer = Timer(self.period/2, units='ns')
        period_timer = Timer(self.period, units='ns')
        idle_timer = Timer(self.period/10, units='ns')
        self.rx <= 1
        while True:
            data = yield wait_python_function(self.socket.recv)
            self.dut._log.info("receved {}".format(data))
            #try:
            #    data = self.socket.recv(flags=zmq.NOBLOCK)
            #    self.dut._log.info("Recved")
            #except zmq.ZMQError as exc:
            #    if exc.errno == zmq.EAGAIN:
            #        self.dut._log.info("Nono")
            #        yield PythonTrigger()
            #        continue
            #    else:
            #        raise
            for _d in data:
                self.rx <= 0
                yield period_timer
                for i in range(self.nbits):
                    self.rx <= (_d >> (self.nbits-1-i) ) & 1
                    yield period_timer
                self.rx <= 0
                yield period_timer
                self.rx <= 1
                yield period_timer


    @cocotb.coroutine
    def tx_monitor_coroutine(self):
        start = FallingEdge(self.tx)
        half_period_timer = Timer(self.period/2, units='ns')
        period_timer = Timer(self.period, units='ns')
        while True:
            yield start
            yield half_period_timer
            data = 0
            for i in range(self.nbits):
                yield period_timer
                data = (data << 1) | (self.tx.value.integer & 1)
            for i in range(self.stop):
                yield period_timer
            yield half_period_timer
            self.socket.send(bytes(chr(data),encoding='utf-8'))





