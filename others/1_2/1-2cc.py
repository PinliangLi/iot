#!/usr/bin/env python3

import random
import threading
import time
import RPi.GPIO as GPIO

randmin = 1 # def the random integer range
randmax = 1000

def _initgpio():
    # Initialize gpio mode
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(2, GPIO.IN)

def thdstart():
    blink1.start()
    blink2.start()

    blink1.join()
    blink2.join()

class LED(threading.Thread):
    def __init__(self, freq = 1):
        threading.Thread.__init__(self)
        self.freq = freq
        self.period = 1/self.freq # Calculate freq to period
        self.sleeptime = self.period/2 # Calculate period to sleep time

        # Initialize gpio mode
        GPIO.setup(17, GPIO.OUT)

        # Initialize gpio status
        GPIO.output(17, 1)

    def run(self):
        flag = False
        while 1:
            time.sleep(self.sleeptime)
            GPIO.output(17, int(flag)) # Type casting
            flag = not flag

    def terminate(self):
        self._running = False

_initgpio() # init the key input

blink1 = LED(1) # Init frep in brackets
blink2 = LED(1)

thdstart()

while 1:
    while GPIO.input(2):
        blink1.terminate() # terminate the old threads
        blink2.terminate()

        del blink1 # destory
        del blink2

        blink1 = LED(random.randint(randmin, randmax)) # recreat the obj with new random freq
        blink2 = LED(random.randint(randmin, randmax))

        thdstart()

