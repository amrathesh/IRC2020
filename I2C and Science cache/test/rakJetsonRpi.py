from smbus import SMBus
import Jetson.GPIO as GPIO
from time import sleep

addr = 0x8 # bus address
bus = SMBus(0) # indicates /dev/ic2-0
controlPin = 11

def init_rpi():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setwarnings(False)
	GPIO.setup(controlPin, GPIO.OUT, initial = GPIO.LOW)
	
init_rpi()

while True:
	try:
		num = [69,127,254]
		GPIO.output(controlPin,GPIO.LOW)
		bus.write_block_data(addr,6,num)
		GPIO.output(controlPin, GPIO.HIGH)
		sleep(0.01)
 	except Exception as e:
		print(e)
		pass
