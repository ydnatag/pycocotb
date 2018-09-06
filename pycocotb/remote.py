import zmq
import logging

class RemoteClient(object):
    def __init__(self, debug=False):
        self.debug = debug
        self.log = logging.getLogger('RemoteClient')
        if debug:
            self.log.setLevel(logging.DEBUG)

        self.ctx = zmq.Context()
        self.socket = self.ctx.socket(zmq.REQ)
        self.socket.connect("ipc:///tmp/pycocotb")

    def send_recv(self, msg):
        self.send(msg)
        return self.recv()

    def send(self, msg):
        self.log.debug("RemoteClient:send {}".format(msg))
        self.socket.send_string(msg)

    def recv(self):
        msg = self.socket.recv_string()
        self.log.debug("RemoteClient:recv {}".format(msg))
        return msg

class RemoteServer(object):
    def __init__(self, debug=False):
        self.debug = debug
        self.log = logging.getLogger('RemoteServer')
        if debug:
            self.log.setLevel(logging.DEBUG)
        self.ctx = zmq.Context()
        self.socket = self.ctx.socket(zmq.REP)
        self.socket.bind("ipc:///tmp/pycocotb")

    def send(self, msg):
        self.log.debug(str(msg))
        self.socket.send_string(msg)

    def recv(self):
        msg = self.socket.recv_string()
        self.log.debug(str(msg))
        return msg




