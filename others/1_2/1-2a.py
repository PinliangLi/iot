#!/usr/bin/env python3

import time
import RPi.GPIO as GPIO

flag = False # Create a flag bool variable

def _initgpio():
    # Initialize gpio mode
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT)
    GPIO.setup(18, GPIO.OUT)

    # Initialize gpio status
    GPIO.output(17, 1)
    GPIO.output(18, 1)

_initgpio()

while 1:
    GPIO.output(17, int(flag)) # Type casting
    flag = not flag
    GPIO.output(18, int(flag))
    time.sleep(1)

