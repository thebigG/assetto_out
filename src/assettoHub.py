import sys
import json
import time
from multiprocessing import shared_memory
from pyacc.acc_types import SPageFilePhysics, SPageFileGraphic, SPageFileStatic

sys.path.insert(0, './pyserial')
import pyserial.serial as serial

acc_types = {
    'acpmf_physics': SPageFilePhysics,
    'acpmf_graphics': SPageFileGraphic,
    'acpmf_static': SPageFileStatic,
}

json_out = dict()


def serial_read():
    ser = serial.Serial('COM6', baudrate=9600, timeout=1)
    ser.write(b"Ping")


def main():
    corsa_shared_mem = "acpmf_physics"
    corsa_shm = shared_memory.SharedMemory(name=corsa_shared_mem)
    ser = serial.Serial('COM6', baudrate=9600, timeout=1)
    while True:
        # print("serial line:{}".format(ser.readline()))
        _obj = acc_types["acpmf_physics"].from_buffer(corsa_shm.buf)
        # buffer = corsa_shm.buf
        json_out["brake"] = _obj.brake
        data_out = json.dumps(json_out)
        ser.write(bytes(data_out, "utf8"))

        # print("json:{}".format(data_out))
        # print("arduino:{}".format(ser.readline()))

        time.sleep(0.5)


def serial_test():
    ser = serial.Serial('COM6', baudrate=9600, timeout=1)
    data_out = dict()
    data_out["brake"] = 0.35
    while True:
        json_out = json.dumps(data_out)
        ser.write(bytes(json_out, "utf8"))
        # print("Arduino msg:{}".format(ser.readline()))
        time.sleep(0.5)

serial_test()
# main()
