import sys
import ac
import acsys
import json
# import serial
# from hello_world_test.hello_world import hello_world, get_hello_world

l_lapcount=0
lapcount=0
ser = None


def acMain(ac_version):
    global ser
    appWindow = ac.newApp("assetto_hub")
    ac.setSize(appWindow, 200, 200)
    ac.log("***************1")
    # ser = serial.Serial('COM6', baudrate=9600, timeout=1)
    ac.log("***************2")
    return "assetto_hub_app"

def acUpdate(deltaT):
   global l_lapcount, lapcount, ser
   brake_pression = ac.getCarState(0, acsys.CS.Brake)
   json_data = dict()
   ac.log("***************3")
   # out_data =
   json_data["brake"] = brake_pression
   ac.log("***************4")
   json_data = json.dumps(json_data)
   ac.log("json data:{}".format(json_data))
   ac.log("***************5")
   # ac.log("From module:{}".format(get_hello_world()))
   # ac.log("serial data:{}".format(ser.rseadline()))
   # if laps > lapcount:
   #    lapcount = laps
   #    ac.setText(l_lapcount, "Laps: {}".format(lapcount))


# def test():
#     hello_world()
#
# test()