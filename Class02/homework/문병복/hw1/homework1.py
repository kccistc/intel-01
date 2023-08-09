from iotdemo import FactoryController
import time


with FactoryController('/dev/ttyACM1') as ctrl:
    print("start.")
    ctrl.system_start()
    #time.sleep(1)
    answer = ''
    while answer != 'q':
        answer=input()
        if answer == '1':
            ctrl.red = True
            print("red")
        elif answer == '2':
            ctrl.orange = True
            print("orange")
        elif answer == '3':
            ctrl.green = True
            print("green")
        elif answer == '4':
            ctrl.conveyor = True
            print("conveyor")
        elif answer == '5':
            ctrl.push_actuator(1)
            print("push_actuator(1)")
        elif answer == '6':
            ctrl.push_actuator(2)
            print("push_actuator(2)")

    ctrl.system_stop()
    #time.sleep(1)

print("Done.")