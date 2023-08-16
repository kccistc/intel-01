from iotdemo import FactoryController
import time

with FactoryController('/dev/ttyACM0') as ctrl:
    ctrl.system_start()
    
    userinput = 0
    while True:
        userinput = input("사용할 기능의 번호를 입력하세요 : ")
        if userinput == '1':
            ctrl.system_start()
        elif userinput == '2':
            ctrl.system_stop()
        elif userinput == '3':
            ctrl.red = True
            time.sleep(1)
        elif userinput == '4':
            ctrl.orange = True
            time.sleep(1)
        elif userinput == '5':
            ctrl.green = True
            time.sleep(1)
        elif userinput == '6':
            ctrl.conveyor = True
            time.sleep(1)
        elif userinput == '7':
            ctrl.push_actuator(1)
            time.sleep(1)
        elif userinput == '8':
            ctrl.push_actuator(2)
            time.sleep(1)
        else:
            break
    ctrl.system_stop()
        
print("Done.")
