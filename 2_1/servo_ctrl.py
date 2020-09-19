#!/usr/bin/env python

#######################################################################
#                            Aufgabe 1.3                              #
#######################################################################

#import gpio_class

#def write(servo, pulse):
    #gpio_class.write(servo, pulse)


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
           # write(PWM_PIN, pulse)
        elif 0 < speed < 11:
            self.pulse = (speed - 0)/11 * 50 + 150
            #write(PWM_PIN, pulse)
        elif -11 < speed < 0:
            self.pulse = (speed + 11)/11 * 50 + 100
            #write(PWM_PIN, pulse)
        elif speed >= 11:
            self.pulse = 200
            #write(PWM_PIN, pulse)
        else:                                             ###elif
            self.pulse = 100
            #write(PWM_PIN, pulse)
        print('$pulse')

    def get_speed(self):
        return self.speed

    def stop(self):
        self.engine_state = False
        pass

    def get_engine_state(self):
        return self.engine_state

    def PWM_speed_up(self, acc, delta):
        self.speed =  self.get_speed() + acc * delta  #m -> M
        self.set_speed(speed)

    def PWM_speed_down(self, dec, delta):
        self.speed =  self.get_speed() - dec * delta
        self.set_speed(speed)

    def PWM_mouse_speed(positionY, self, acc, dec):      ###new func
        relevateY = positionY - height/2
        if relevateY < -100:
            self.PWM_speed_up(self, acc)
        if relevateY > 100:
            self.PWM_speed_down(self, dec)

class Steering(object):
    PWM_PIN = 2     # GPIO pin 12
    min_pulse = 115
    max_pulse = 195
    def __init__(self, pulse=None, angle=None, steering_state=False):
        self.pulse = pulse
        self.angle = angle
        self.steering_state = steering_state

    def set_angle(self, angle):
        self.steering_state = True
        self.angle = angle
        if angle > 45:
            self.pulse = 195
            #write(PWM_PIN, pulse)
        elif angle < -45:
            self.pulse = 115
            #write(PWM_PIN, pulse)
        else:
            pulse = 4 / 450 * angle + 155
            #write(PWM_PIN, pulse)
        print('$pulse')

    def get_angle(self):
        return self.angle

    def stop(self):
        self.steering_state = False

    def get_engin_state():
        return self.steering_state

    def PWM_angle_left(self, angle_acc, delta):
        angle = self.get_angle() + angle_acc * delta
        self.set_angle(angle)

    def PWM_angle_right(self, angle_acc, delta):
        angle = self.get_angle() - angle_acc * delta
        self.set_angle(angle)

    def PWM_mouse_turn(positionX, self, angle_acc):      ###new func
        relevateX = positionX - width/2
        if relevateX < -100:
            self.PWM_angle_left(self, angle_acc)
        if relevateX > 100:
            self.PWM_angle_right(self, angle_acc)
