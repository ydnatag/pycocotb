
import cocotb
from pycocotb.remote import RemoteServer
from cocotb.triggers import *

@cocotb.test()
def remote_test(dut):
    dut._log.info('Starting')
    srv = RemoteServer(debug=True)
    while True:
        msg = srv.recv()
        cmd = msg.split(" ")[0]
        if cmd == 'yield':
            yield eval(msg[6:])
            ret = ""
        elif cmd == 'break':
            srv.send("")
            break
        elif cmd == 'import':
            exec(msg)
            ret = ""
        else:
            if '=' in msg:
                exec(msg)
                ret = ""
            else:
                ret = str(eval(msg.split('=')[0]))
        srv.send(ret)


