import RPi.GPIO as GPIO

import time

def __init__GPIO():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(17, GPIO.OUT)
	GPIO.setup(18, GPIO.OUT)
#
	GPIO.output(17,0)
	GPIO.output(18,0)#


def ledblink(times):
	for i in range(0,times):
		GPIO.output(17,1)
		GPIO.output(18,0)
		time.sleep(1)
		GPIO.output(18,1)
		GPIO.output(17,0)
		time.sleep(1)
