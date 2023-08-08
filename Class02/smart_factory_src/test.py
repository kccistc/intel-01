from iotdemo import FactoryController
import time

with FactoryController('/dev/ttyACM0') as ctrl:

    while(1):
        input_num = input()
        
        if(input_num == 1):
            ctrl.system_start()
        elif(input_num == 2):
            ctrl.system_stop()
        elif(input_num == 3):
            ctrl.red()
        elif(input_num == 4):
            ctrl.orange()
        elif(input_num == 5):
            ctrl.green()
        elif(input_num == 6):
            ctrl.conveyor()
        elif(input_num == 7):
            ctrl.push_actuator(1)
        elif(input_num == 8):
            ctrl.push_actuator(2)
        else:
            break


print("close")