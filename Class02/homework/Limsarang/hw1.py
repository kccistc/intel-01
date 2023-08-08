import time
from iotdemo import FactoryController


ctrl = FactoryController('/dev/ttyACM0')
print("what's your number?")

while 1 : 
    input_num = input()
    time.sleep(100)
    if input_num == 1 :
        ctrl.system_start()
        time.sleep(100)

    elif input_num == 2 :
        ctrl.system_stop()
        time.sleep(100)

    elif input_num == 3 :
        ctrl.red = True
        time.sleep(100)

    elif input_num == 4 :
        ctrl.orange = True
        time.sleep(100)

    elif input_num == 5 :
        ctrl.green = True
        time.sleep(100)

    elif input_num == 6 :
        ctrl.conveyor()
        time.sleep(100)

    elif input_num == 7 :
        ctrl.push_actuator(1)
        time.sleep(100)

    elif input_num == 8 :
        ctrl.push_actuator(2)
        time.sleep(100)
        
    else :
        break


        
