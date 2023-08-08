from iotdemo import FactoryController

ctrl = FactoryController('/dev/ttyACM0')
 
try:
    while True:
        user_input=input()
        if user_input=='1':
            ctrl.system_start()
        elif user_input=='2':
            ctrl.system_stop()
except KeyboardInterrupt:
    pass