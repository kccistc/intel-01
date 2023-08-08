from iotdemo import FactoryController
import time



with FactoryController('/dev/ttyACM3') as ctrl:


    while True:

    
        x = input()
        if x=='1':

        
            ctrl.system_start()
            time.sleep(1)

        
        if x=='2':
        
            ctrl.system_stop()
            time.sleep(1)
        
        if x=='3':
        
            ctrl.red = FactoryController.DEV_OFF
            ctrl.orange = FactoryController.DEV_ON
            ctrl.green = FactoryController.DEV_ON
            ctrl.conveyor = FactoryController.DEV_ON
            time.sleep(1)
        
        if x=='4':
        
            ctrl.orange = FactoryController.DEV_OFF
            ctrl.red = FactoryController.DEV_ON
            ctrl.green = FactoryController.DEV_ON
            ctrl.conveyor = FactoryController.DEV_ON
            time.sleep(1)
        
        if x=='5':
        
            ctrl.green = FactoryController.DEV_OFF
            ctrl.red = FactoryController.DEV_ON
            ctrl.orange = FactoryController.DEV_ON
            ctrl.conveyor = FactoryController.DEV_ON
            time.sleep(1)
        if x=='6':
            ctrl.green = FactoryController.DEV_ON
            ctrl.red = FactoryController.DEV_ON
            ctrl.orange = FactoryController.DEV_ON
            ctrl.conveyor = FactoryController.DEV_OFF
            time.sleep(1)
        if x=='7':
            ctrl.push_actuator(1)
            time.sleep(1)
        if x=='8':
            ctrl.push_actuator(2)
            time.sleep(1)
        




    



