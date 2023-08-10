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
            ctrl.red = FactoryController.DEV_ON
            time.sleep(1)
            ctrl.red = FactoryController.DEV_OFF
            print("red")
        elif answer == '2':
            ctrl.orange = FactoryController.DEV_ON
            time.sleep(1)
            ctrl.orange = FactoryController.DEV_OFF
            print("orange")
        elif answer == '3':
            ctrl.green = FactoryController.DEV_ON
            time.sleep(1)
            ctrl.green = FactoryController.DEV_OFF
            print("green")
        elif answer == '4':
            ctrl.conveyor = FactoryController.DEV_ON
            time.sleep(1)
            ctrl.conveyor = FactoryController.DEV_OFF
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