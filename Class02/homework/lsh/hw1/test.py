from iotdemo import FactoryController
import time



with FactoryController('/dev/ttyACM0') as ctrl:

    red = False
    orange = False
    green = False

    while True:
        a = input()

        if a == '0':
            break

        if a == '1':
            ctrl.system_start()
            time.sleep(1)

        if a == '2':
            ctrl.system_stop()
            time.sleep(1)

        if a == '3':
            if red == False:
                ctrl.red = FactoryController.DEV_OFF
                red = True

            elif red == True:
                ctrl.red = FactoryController.DEV_ON
                red = False

        if a == '4':
            if orange == False:
                ctrl.orange = FactoryController.DEV_OFF
                orange = True

            elif orange == True:
                ctrl.orange = FactoryController.DEV_ON
                orange = False

        if a == '5':
            if green == False:
                ctrl.green = FactoryController.DEV_OFF
                green = True

            elif green == True:
                ctrl.green = FactoryController.DEV_ON
                green = False


print("Done.")