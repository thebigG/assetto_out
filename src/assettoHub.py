import sys
import json
import time
from multiprocessing import shared_memory
from pyacc.acc_types import SPageFilePhysics, SPageFileGraphic, SPageFileStatic


acc_types = {
    'acpmf_physics': SPageFilePhysics,
    'acpmf_graphics': SPageFileGraphic,
    'acpmf_static': SPageFileStatic,
}


def test():
    corsa_shared_mem = "acpmf_physics"
    corsa_shm = shared_memory.SharedMemory(name=corsa_shared_mem)
    while True:
        # print("serial line:{}".format(ser.readline()))
        _obj = acc_types["acpmf_physics"].from_buffer(corsa_shm.buf)
        buffer = corsa_shm.buf
        print(bytes(buffer[8:12]))
        print("obj:{}".format(_obj.brake))
        time.sleep(0.5)

test()