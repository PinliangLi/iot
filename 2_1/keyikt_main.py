#!/usr/bin/env python

#######################################################################
#                            Aufgabe 1                                #
#######################################################################

import sys, time
import random
import car_model
import math
import pygame       


width = 800
height = 600

freq = 50  # Sets the frequency of input procession
delta = 1.0 / freq # time per step
acc = 2.6  # Max acceleration of the car (per sec.)
dec = 4.5  # Max deceleration of the car (per sec.)
frict = -1  # max friction
angle_acc = 300  # max change of angle (per sec.)

speed_cur = 0
angle_cur = 0


# start main pygame event processing loop here
pygame.display.init()

# set up the pygame screen enviroment
screen = pygame.display.set_mode((width, height))

# get a clock to generate frequent behaviour
clock = pygame.time.Clock()
car = car_model.Car()

# States of the keys
keystates = {'quit':False, 'up':False, 'down':False, 'reset_speed':False, 'reset_angle':False, 'engine_state':False, 'mouse_event':False, 'left':False, 
             'right':False, 'simulate': False}
use_mouse = False
simulate = True
pygame.mouse.set_pos([width/2, height/2])

def speed_up(car, acc):
    speed = car.get_speed()
    acc = acc - (acc/2) * (1 + math.erf( (math.fabs(speed) - 5.5) / (math.sqrt(2 * math.pow(2.5, 2))) ))
    speed = speed + acc * delta
    car.set_speed(speed)

def speed_down(car, dec):
    speed = car.get_speed()
    dec = dec - (dec/2) * (1 + math.erf( (math.fabs(speed) - 5.5) / (math.sqrt(2 * math.pow(2.5, 2))) ))
    speed = speed - dec * delta
    car.set_speed(speed)

def speed_frict(car, frict):
    speed = car.get_speed()
    frict = (frict/2) * (1 + math.erf( (math.fabs(speed) - 11/2) / (math.sqrt(2 * 4**2)) ))
    speed = speed + frict * delta
    car.set_speed(speed)

def angle_left(car, angle_acc):
    angle = car.get_angle()
    angle = angle + angle_acc * delta
    car.set_angle(angle)

def angle_right(car, angle_acc):
    angle = car.get_angle()
    angle = angle - angle_acc * delta
    car.set_angle(angle)


def mouse_turn(positionX, car, angle_acc):
    relevateX = positionX - width/2
    if relevateX < -100:
        angle_left(car, angle_acc)
    elif relevateX > 100:
        angle_right(car, angle_acc)


def mouse_speed(positionY, car, acc, dec):
    relevateY = positionY - width/2
    if relevateY < -100:
        speed_up(car, acc)
    if relevateY > 100:
        speed_down(car, dec)

running = True
try:
    while running:
        # set clock frequency
        clock.tick(freq);
        
        # save the last speed 4 analysis
        last = speed_cur
        angle_last = angle_cur
        acc=2.6
        dec=4.5
        frict=-1
        # process input events
        for event in pygame.event.get():
        
            # exit on quit
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                use_mouse = True
                keystates['engine_state'] = True
            # check for key down events (press)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    keystates['quit'] = True
                if event.key == pygame.K_UP:
                    keystates['up'] = True
                if event.key == pygame.K_DOWN:
                    keystates['down'] = True
                if event.key == pygame.K_LEFT:
                    keystates['left'] = True
                if event.key == pygame.K_RIGHT:
                    keystates['right'] = True
                if event.key == pygame.K_r:
                    keystates['reset_speed'] = True
                    keystates['reset_angle'] = True
                if event.key == pygame.K_s:
                    keystates['engine_state'] = True
                    car.change_engine_state()
                if event.key == pygame.K_m:
                    if use_mouse:
                        use_mouse = False
                if event.key == pygame.K_v:
                    keystates['simulate'] = True
                    simulate = not simulate
                    

            # check for key up events (release)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_q:
                    keystates['quit'] = False
                if event.key == pygame.K_UP:
                    keystates['up'] = False
                if event.key == pygame.K_DOWN:
                    keystates['down'] = False
                if event.key == pygame.K_LEFT:
                    keystates['left'] = False
                if event.key == pygame.K_RIGHT:
                    keystates['right'] = False
                if event.key == pygame.K_r:
                    keystates['reset_speed'] = False
                    keystates['rest_angle'] = False
                if event.key == pygame.K_s:
                    keystates['engine_state'] = False
                if event.key == pygame.K_m:
                    if use_mouse:
                        use_mouse = False
                if event.key == pygame.K_v:
                    keystates['simulate'] = False
        # do something about the key states here, now that the event queue has been processed
        if keystates['quit']:
            running = False
        

        if simulate:
            if car.get_engine_state():
                print(car.get_engine_state())
                if use_mouse:
                    mouse_position = pygame.mouse.get_pos()
                    mouse_turn(mouse_position[0], car, angle_acc)
                    mouse_speed(mouse_position[1], car, acc, dec)
                if keystates['up']:
                    speed_up(car, acc)

                if keystates['down']:
                    speed_down(car, dec)

                if keystates['left']:
                    angle_left(car, angle_acc)

                if keystates['right']:
                    angle_right(car, angle_acc)
            else :
                if car.get_speed() > 0.05:
                    speed_frict(car, frict)
                elif car.get_speed() < -0.05:
                    speed_frict(car, -frict)
                else :
                    speed = car.get_speed()
                    speed = 0
                    car.set_speed(speed)
            if keystates['reset_speed']:
                car.reset_speed()
            if keystates['reset_angle']:
                car.reset_angle()



            speed_cur = car.get_speed()
            angle_cur = car.get_angle()

        else :
            if car.get_engine_state():
                if use_mouse:
                    mouse_position = pygame.mouse.get_pos()
                
                if keystates['up']:
                    pass

                if keystates['down']:
                    pass

                if keystates['left']:
                    pass

                if keystates['right']:
                    pass
            else :
                pass


        print ("({},{} --> {})".format(speed_cur, angle_cur, (speed_cur - last) / delta))
except KeyboardInterrupt:
    print ("Exiting through keyboard event (CTRL + C)")
    

# gracefully exit pygame here
pygame.quit()

