from iotdemo import FactoryController
import time

#with FactoryController('/dev/ttyACM0') as ctrl:

ctrl = FactoryController('/dev/ttyACM0')

ctrl.system_start()

ctrl.red = False
ctrl.orange = False
ctrl.green = False
ctrl.conveyor = False
ctrl.push_actuator(1)
ctrl.push_actuator(2)


ctrl.red = True
time.sleep(1)
ctrl.red = False
time.sleep(1)
ctrl.orange = True
time.sleep(1)
ctrl.orange = False
time.sleep(1)
ctrl.green = True
time.sleep(1)
ctrl.green = False
time.sleep(1)
ctrl.conveyor = True
time.sleep(1)
ctrl.conveyor = False
time.sleep(1)
ctrl.push_actuator(1)
time.sleep(1)
ctrl.push_actuator(2)
time.sleep(1)


print('done')
ctrl.close()
