# %%
from iotdemo import FactoryController
import time

with FactoryController('/dev/ttyACM0') as ctrl:
    ctrl.system_start()
    time.sleep(1)
    input = ''
    while input !='q':
        input = input()
        if input == 1:
            ctrl.red=FactoryController.DEV_ON
            print("Done red.")
            time.sleep(1)        
            ctrl.red=FactoryController.DEV_OFF
            time.sleep(1)
        if input == 2:
            ctrl.orange=FactoryController.DEV_ON
            print("Done. orange")
            time.sleep(1)
            ctrl.orange=FactoryController.DEV_OFF
            time.sleep(1)
        if input == 3:
            ctrl.green=FactoryController.DEV_ON
            print("Done. green")
            time.sleep(1)
            ctrl.green=FactoryController.DEV_OFF
            time.sleep(1)

        if input == 4:
            ctrl.conveyor=FactoryController.DEV_ON
            print("Done. conveyor")
            time.sleep(1)
            ctrl.conveyor=FactoryController.DEV_OFF
            time.sleep(1)
        
        if input == 5:
            ctrl.push_actuator(1)
            print("Done. push_actuator1")
            time.sleep(1)            

        if input == 6:
            ctrl.push_actuator(2)
            print("Done. push_actuator2")
            time.sleep(1)
            
       


print("Done.")


# %%
