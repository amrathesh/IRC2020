import Jetson.GPIO as GPIO
from time import sleep
def blink(actuator_control_pin_1_number):
	GPIO.output(actuator_control_pin_1_number, GPIO.HIGH)
	sleep(2)
	GPIO.output(actuator_control_pin_1_number, GPIO.LOW)
	sleep(2)
if __name__=='__main__':
	actuator_1_control_pin_1 = 11#pin 33#63
	GPIO.setmode(GPIO.BOARD)
	
	GPIO.setwarnings(False)
	GPIO.setup(actuator_1_control_pin_1, GPIO.OUT, initial = GPIO.HIGH)
	
	while(True):
		blink(actuator_1_control_pin_1)
