

class Clock(object):
    def __init__(self, comm):
        self.comm = comm
        self.comm.send_recv('import cocotb.clock')

    def start(self, signal, period, unit='ns'):
        msg = 'cocotb.clock.Clock({}, {}, units="{}").start()'
        msg = msg.format(signal, period, unit)
        msg = 'cocotb.fork({})'.format(msg)
        return self.comm.send_recv(msg)

