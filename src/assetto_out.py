import sys
import json
import time
from multiprocessing import shared_memory
from pyacc.acc_types import SPageFilePhysics, SPageFileGraphic, SPageFileStatic

import argparse

# The following import assumes that "src" is the current working directory
sys.path.insert(0, './pyserial')
import serial as serial

import yaml

import serial.tools.list_ports as list_ports

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
    config = None
    with open(args.config) as file:
        config = yaml.safe_load(file)
    # print(f"config:{config}")
    mode = config["mode"]
    # print(list_ports.comports()[0].hwid)
    if mode == "SERIAL":
        serial_port = config["port"]
        # TODO: move corsa_shared_mem to config file
        corsa_shared_mem = "acpmf_physics"
        try:
            corsa_shm = shared_memory.SharedMemory(name=corsa_shared_mem)
        except:
            print(f"Shared memory block '{corsa_shared_mem}' not available. Are you sure Assetto Corsa is running?")
            exit(-1)
        try:
            ser = serial.Serial(serial_port, baudrate=9600, timeout=1)
        except:
            print(f"Not able to open '{serial_port}'. Ensure this port is not being used by any other applications"
                  f" and is plugged in.")
            exit(-1)
        while True:
            _obj = acc_types["acpmf_physics"].from_buffer(corsa_shm.buf)
            json_out["brake"] = _obj.brake
            data_out = json.dumps(json_out)
            ser.write(bytes(data_out, "utf8"))
            time.sleep(0.5)


main()
