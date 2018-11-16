

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

