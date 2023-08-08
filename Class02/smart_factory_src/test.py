from iotdemo import FactoryController
import time

with FactoryController('/dev/ttyACM0') as ctrl:
    ctrl.red = False
    ctrl.green = False
    ctrl.orange = False
    ctrl.conveyor = False
    print("start")
    time.sleep(1)
    ctrl.system_start()
    ctrl.system_stop()
    time.sleep(1)
    ctrl.red = True
    time.sleep(1)
    ctrl.green = True
    time.sleep(1)
    ctrl.orange = True
    time.sleep(1)
    ctrl.conveyor = True
    time.sleep(1)
    ctrl.push_actuator(1)
    time.sleep(1)
    ctrl.push_actuator(2)

    print("end")