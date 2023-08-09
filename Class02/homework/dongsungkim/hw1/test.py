import time
from iotdemo import FactoryController

with FactoryController('/dev/ttyACM0') as ctrl:
    ctrl.system_start()
    time.sleep(1)

    ctrl.green = FactoryController.DEV_ON
    time.sleep(1)
    
    ctrl.red = FactoryController.DEV_ON
    time.sleep(1)

    ctrl.orange = FactoryController.DEV_ON
    time.sleep(1)

    ctrl.conveyor = FactoryController.DEV_ON
    time.sleep(1)

    ctrl.push_actuator(1)
    time.sleep(1)

    
    ctrl.green = FactoryController.DEV_OFF
    time.sleep(1)
    
    ctrl.red = FactoryController.DEV_OFF
    time.sleep(1)

    ctrl.orange = FactoryController.DEV_OFF
    time.sleep(1)

    ctrl.conveyor = FactoryController.DEV_OFF
    time.sleep(1)
    
    ctrl.push_actuator(2)
    time.sleep(1)

    ctrl.system_stop()
    time.sleep(1)

    print('done')