from iotdemo import FactoryController
import time

with FactoryController('/dev/ttyACM0') as ctrl:
    
    while True:
        print("1-start\t2-stop\t3-red\t4-orange\t5-green\t6-exit")
        eventint=int(input("number"))
        if eventint == 1:
            ctrl.system_start()

        elif eventint == 2:
            ctrl.system_stop()

        elif eventint == 3:
            ctrl.red=True
            if ctrl.red==True:
                ctrl.red=False

        elif eventint == 4:
            ctrl.orange=True
            if ctrl.orange==True:
                ctrl.orange=False

        elif eventint == 5:
            ctrl.green=True
            if ctrl.green==True:
                ctrl.green=False

        elif eventint == 6:
            
            break
            
    