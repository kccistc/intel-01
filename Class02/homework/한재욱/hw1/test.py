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
            ctrl.__led(2,True)
            if ctrl.__led(2,True):
                ctrl.__led(2,False)

        elif eventint == 4:
            ctrl.__led(3,True)
            if ctrl.__led(3,True):
                ctrl.__led(3,False)

        elif eventint == 5:
            ctrl.__led(4,True)
            if ctrl.__led(4,True):
                ctrl.__led(4,False)

        elif eventint == 6:
            
            break
            
    