import sys
import json
import time
from multiprocessing import shared_memory

import _ctypes

from pyacc.acc_types import SPageFilePhysics, SPageFileGraphic, SPageFileStatic
from ctypes import LittleEndianStructure, c_int, c_float, Array
import ctypes.wintypes
import argparse

# The following import assumes that "src" is the current working directory
sys.path.insert(0, './pyserial')
import serial as serial

import yaml

import serial.tools.list_ports as list_ports

import socket
import sys

# https://assettocorsamods.net/threads/doc-shared-memory-reference.58/
acc_types = {
    'acpmf_physics': SPageFilePhysics,
    'acpmf_graphics': SPageFileGraphic,
    'acpmf_static': SPageFileStatic,
}

json_out = dict()


def serial_read():
    ser = serial.Serial('COM6', baudrate=9600, timeout=1)
    ser.write(b"Ping")


def serial_test():
    ser = serial.Serial('COM6', baudrate=9600, timeout=1)
    data_out = dict()
    data_out["brake"] = 0.35
    while True:
        json_out = json.dumps(data_out)
        ser.write(bytes(json_out, "utf8"))
        time.sleep(0.5)


def parse_cli():
    parser = argparse.ArgumentParser(description='Args')
    parser.add_argument("--config", type=str, required=True,
                        help='YAML Config file')

    return parser.parse_args()


def main():
    args = parse_cli()
    print(f"args: {args.config}")
    corsa_physics = SPageFilePhysics()
    config = None
    data_count = 0
    with open(args.config) as file:
        config = yaml.safe_load(file)
    # print(f"config:{config}")
    mode = config["mode"]
    # TODO: move corsa_shared_mem to config file
    corsa_shared_mem = "acpmf_physics"
    try:
        corsa_shm = shared_memory.SharedMemory(name=corsa_shared_mem)
    except:
        print(f"Shared memory block '{corsa_shared_mem}' not available. Are you sure Assetto Corsa is running?")
        exit(-1)
    # print(list_ports.comports()[0].hwid)
    if mode == "SERIAL":
        serial_port = config["port"]
        try:
            ser = serial.Serial(serial_port, baudrate=9600, timeout=1)
        except:
            print(f"Not able to open '{serial_port}'. Ensure this port is not being used by any other applications"
                  f" and is plugged in.")
            exit(-1)
        while True:
            _obj = acc_types["acpmf_physics"].from_buffer(corsa_shm.buf)
            _obj_dict = fields_to_dict(_obj)
            data_out = json.dumps(_obj_dict)
            # print(f"data_out:{data_out}")
            data = bytes(data_out, "utf8")
            ser.write(data)
            print(f"TX count:{data_count}")
            print(f"{len(data)} bytes sent")
            data_count += 1
            # time.sleep(0.5)
    elif mode == "UDP":
        while True:
            _obj = acc_types["acpmf_physics"].from_buffer(corsa_shm.buf)
            _obj_dict = fields_to_dict(_obj)
            data_out = json.dumps(_obj_dict)
            HOST, PORT = config['host'], config['port']
            # SOCK_DGRAM is the socket type to use for UDP sockets
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            data = bytes(data_out + "\n", "utf8")
            sock.sendto(data, (HOST, PORT))
            print(f"TX count:{data_count}")
            print(f"{len(data)} bytes sent")
            data_count += 1
    else:
        print(f"Mode '{mode}' is not supported.")


def fields_to_dict(corsa_obj):
    fields_dict = dict()
    for f in corsa_obj._fields_:
        # TODO:Add support for arrays
        if type(f[1]).__name__ == 'PyCSimpleType':
            fields_dict[f[0]] = getattr(corsa_obj, f[0])

    return fields_dict


main()
