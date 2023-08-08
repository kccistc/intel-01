from iotdemo import FactoryController
import time
import keyboard

led_states = {
    2: False,
    3: False,
    4: False,
    9: False,
    6: False,
    7: False
}

def toggle_led(ctrl, pin):
    global led_states
    if led_states[pin]:
        ctrl.digital_write(pin, False)
        led_states[pin] = False
        print(f"LED on pin {pin} turned OFF")
    else:
        ctrl.digital_write(pin, True)
        led_states[pin] = True
        print(f"LED on pin {pin} turned ON")

while True:
	with FactoryController('/dev/ttyACM0') as ctrl:
		key = keyboard.read_event()
		if key.name == '1':
			ctrl.system_start()
			print("Start")
			time.sleep(1)
		if key.name == '2':
			ctrl.system_stop()
			print("Stop")
			time.sleep(1)
		if key.name == '3':
			toggle_led(ctrl, 2)
			time.sleep(1)
		if key.name == '4':
			toggle_led(ctrl, 3)
			time.sleep(1)
		if key.name == '5':
			toggle_led(ctrl, 4)
			time.sleep(1)
		if key.name == '6':
			toggle_led(ctrl, 9)
			time.sleep(1)
		if key.name == '7':
			toggle_led(ctrl, 6)
			time.sleep(1)
		if key.name == '8':
			toggle_led(ctrl, 7)
			time.sleep(1)
		if key.name == 'q':
			print("Done")
			break
