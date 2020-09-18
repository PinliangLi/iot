#!/usr/bin/env python

#######################################################################
#                            Aufgabe 1.3                              #
#######################################################################

import gpio_class

def write(servo, pulse):
    gpio_class.write(servo, pulse)

class Motor(object):
    PWM_PIN = 1     # GPIO pin 11
    min_pulse = 100
    max_pulse = 200
    def __init__(self, pulse=None, speed=None, engine_state=False):
        self.pulse = pulse
        self.speed = speed
        self.engine_state = engine_state
    def set_speed(self, speed):
        self.engine_state = True
        self.speed = speed
        if speed == 0:
            self.pulse = 150
            write(PWM_PIN, pulse)
        elif 0 < speed < 11:
            self.pulse = (speed - 0)/11 * 50 + 150
            write(PWM_PIN, pulse)
        elif -11 < speed < 0:
            self.pulse = (speed + 11)/11 * 50 + 100
            write(PWM_PIN, pulse)
        elif speed >= 11:
            self.pulse = 200
            write(PWM_PIN, pulse)
        elif speed <= -11:
            self.pulse = 100
            write(PWM_PIN, pulse)
    def get_speed(self):
        return self.speed
    def stop(self):
        self.engine_state = False
        pass
    def get_engin_state():
        return self.engine_state

class Steering(object):
    PWM_PIN = 2     # GPIO pin 12
    min_pulse = 100
    max_pulse = 200
    def __init__(self, servo=None):
        return
    def set_angle(self, angle):
        return
    def stop(self):
        return

