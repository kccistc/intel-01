# %%
from iotdemo import FactoryController
import time

with FactoryController('/dev/ttyACM0') as ctrl:
    ctrl.system_start()
    time.sleep(1)
    input_q = ''
    while input_q !='q':
        input_q = input()
        if input_q == '1':
            ctrl.red=FactoryController.DEV_ON
            print("Done red.")
            time.sleep(1)        
            ctrl.red=FactoryController.DEV_OFF
            time.sleep(1)
        if input_q == '2':
            ctrl.orange=FactoryController.DEV_ON
            print("Done. orange")
            time.sleep(1)
            ctrl.orange=FactoryController.DEV_OFF
            time.sleep(1)
        if input_q == '3':
            ctrl.green=FactoryController.DEV_ON
            print("Done. green")
            time.sleep(1)
            ctrl.green=FactoryController.DEV_OFF
            time.sleep(1)

        if input_q == '4':
            ctrl.conveyor=FactoryController.DEV_ON
            print("Done. conveyor")
            time.sleep(1)
            ctrl.conveyor=FactoryController.DEV_OFF
            time.sleep(1)
        
        if input_q == '5':
            ctrl.push_actuator(1)
            print("Done. push_actuator1")
            time.sleep(1)            

        if input_q == '6':
            ctrl.push_actuator(2)
            print("Done. push_actuator2")
            time.sleep(1)
            
       


print("Done.")


# %%
