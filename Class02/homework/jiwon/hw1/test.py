from iotdemo import FactoryController
import time

with FactoryController('/dev/ttyACM0') as ctrl:
    print("start ")
    time.sleep(1)
    
    ctrl.system_start()
    print("system start")
    time.sleep(1)

    '''initial'''
    print("start init")
    ctrl.red = False
    ctrl.orange = False
    ctrl.green = False
    #ctrl.push_actuator(1)
    #ctrl.push_actuator(2)
    ctrl.conveyor = False
    time.sleep(1)

    '''end of initial'''

    #pin 2 = RED
    ctrl.red = False
    print("Red Start")
    time.sleep(1)

    #pin 3 = Orange
    ctrl.orange = True # True : 3 Low  False : 3 High 
    print("Orange Start")
    time.sleep(1)

    #pin 4 = Green
    ctrl.green = True # No action
    print("Green Start")
    time.sleep(1)

    #pin 6 = actuator1
    ctrl.push_actuator(1) #low active 
    print("Act1 Start")
    time.sleep(1)

    #pin 7 = actuator2
    ctrl.push_actuator(2) #low active
    print("Act2 Start")
    time.sleep(1)

    #pin 9 = conveyor PWM
    ctrl.conveyor = True #False  # No action
    print("Conveyor Start")
    time.sleep(1)
    
    
    #time.sleep(2)

    
    print("Done")
    #ctrl.system_stop(1)
    
    