#!/usr/bin/env python3

import threading
import time
import numpy as np
import os
import sys
import shlex

channel = 1

sinarray = (np.sin(np.array(np.arange(99) * 2 * np.pi / 100)) + 1 ) / 2 # generate sin table

pwmarray = sinarray * 100 # convert to duty cycle percentage

def shellexec(cmd):
    return shlex.os.system(cmd)

class LED(threading.Thread):
    def __init__(self, freq = 1):
        threading.Thread.__init__(self)
        self.freq = freq
        self.period = 1/self.freq # Calculate freq to period
        self.sleeptime = self.period/100 # Calculate period to sleep time

    def run(self):
        while 1:
            for k in range(100):
                time.sleep(self.sleeptime)
                shellexec('echo ' + str(channel) + '=' + str(pwmarray[k]) + '%' + ' > /dev/servoblaster')

#print(sinarray)

blink = LED(1) # Frep in brackets

blink.start()

blink.join()

