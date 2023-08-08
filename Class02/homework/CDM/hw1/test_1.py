from iotdemo import FactoryController
import time

with FactoryController('/dev/ttyACM0') as ctrl:      

    while True:
        a=input()

        if a== '1':
            ctrl.system_start()
        
        if a== '2':
            ctrl.system_stop()
        if a== '3':
            ctrl.red= FactoryController.DEV_OFF
            ctrl.orange=FactoryController.DEV_ON
            ctrl.green=FactoryController.DEV_ON
            ctrl.conveyor=FactoryController.DEV_ON
        if a== '4':
            ctrl.orange= FactoryController.DEV_OFF
            ctrl.red=FactoryController.DEV_ON
            ctrl.green=FactoryController.DEV_ON
            ctrl.conveyor=FactoryController.DEV_ON
        if a== '5':
            ctrl.green= FactoryController.DEV_OFF
            ctrl.red=FactoryController.DEV_ON
            ctrl.orange=FactoryController.DEV_ON
            ctrl.conveyor=FactoryController.DEV_ON
        if a== '6':
            ctrl.conveyor= FactoryController.DEV_OFF
            ctrl.red=FactoryController.DEV_ON
            ctrl.orange=FactoryController.DEV_ON
            ctrl.green=FactoryController.DEV_ON
        if a== '7':
            ctrl.conveyor= FactoryController.DEV_ON
            ctrl.red=FactoryController.DEV_ON
            ctrl.orange=FactoryController.DEV_ON
            ctrl.green=FactoryController.DEV_ON
            ctrl.push_actuator(1)
        if a== '8':
            ctrl.conveyor= FactoryController.DEV_ON
            ctrl.red=FactoryController.DEV_ON
            ctrl.orange=FactoryController.DEV_ON
            ctrl.green=FactoryController.DEV_ON
            ctrl.push_actuator(2)





print("Done.")



