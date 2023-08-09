from iotdemo import FactoryController
import time

with FactoryController('/dev/ttyACM0') as ctrl:
    time.sleep(2)
    ctrl.red = False # pin 2 on
    print("red False")
    time.sleep(2) 
    ctrl.red = True  # pin 2 off
    print("red True")

    time.sleep(2)
    ctrl.orange = False # pin 3 off
    print("orange False")
    time.sleep(2) 
    ctrl.orange = True  # pin 3 on
    print("orange True")

    time.sleep(2)
    ctrl.green = False # pin 4 off
    print("green False")
    time.sleep(2)
    ctrl.green = True # pin 4 on
    print("green True")

    time.sleep(2)
    ctrl.conveyor = False # pin 8 off, pin 9 on
    print("conveyor False")
    time.sleep(2)
    ctrl.conveyor = True  # pin 8 on, pin 9 off
    print("conveyor True")

    time.sleep(2)
    ctrl.system_start() #pin 2 off, pin 3 off, ctrl.conveyor True
    print("system_start")
    time.sleep(5)
    ctrl.system_stop()
    print("system_stop")  #pin 2 on, pin 3 on, ctrl.conveyor False

    time.sleep(5)
    ctrl.push_actuator(1) #pin 6 on
    print("push_actuator 1") 
    time.sleep(2)
    ctrl.push_actuator(2) #pin 6 off
    print("push_actuator 2")
    time.sleep(2)
    print("end")

