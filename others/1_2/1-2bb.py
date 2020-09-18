#!/usr/bin/env python3

import threading
import time
import RPi.GPIO as GPIO

flag = False # Create a flag bool variable

class LED(threading.Thread):
    def __init__(self, freq = 1):
        threading.Thread.__init__(self)
        self.freq = freq
        self.period = 1/self.freq # Calculate freq to period
        self.sleeptime = self.period/2 # Calculate period to sleep time

        # Initialize gpio mode
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(17, GPIO.OUT)

        # Initialize gpio status
        GPIO.output(17, 1)

    def run(self):
        global flag
        while 1:
            time.sleep(self.sleeptime)
            GPIO.output(17, int(flag)) # Type casting
            flag = not flag

blink = LED(1) # Frep in brackets

blink.start()

blink.join()

