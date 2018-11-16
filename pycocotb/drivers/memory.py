import os
import mmap

class Memory(object):
    def __init__(self, file, length):
        self.file = os.open(file, os.O_CREAT|os.O_SYNC|os.O_RDWR)
        os.write(self.file, bytes(length))
        self.mem = mmap.mmap(self.file, length)

    def __getitem__(self, item):
        return self.mem[item]

    def __setitem__(self, item, value):
        self.mem[item] = value

