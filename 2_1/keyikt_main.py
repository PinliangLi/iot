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
keystates = {'quit':False, 'up':False, 'down':False, 'reset_speed':False, 'engine_state':False}


running = True
try:
    while running:
        # set clock frequency
        clock.tick(freq);
        
        # save the last speed 4 analysis
        last = speed_cur
        acc=2.6
        dec=4.5
        frict=-1
        # process input events
        for event in pygame.event.get():
        
            # exit on quit
            if event.type == pygame.QUIT:
                running = False

            # check for key down events (press)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    keystates['quit'] = True
                if event.key == pygame.K_UP:
                    keystates['up'] = True
                if event.key == pygame.K_DOWN:
                    keystates['down'] = True
                if event.key == pygame.K_r:
                    keystates['reset_speed'] = True
                if event.key == pygame.K_s:
                    keystates['engine_state'] = True

            # check for key up events (release)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_q:
                    keystates['quit'] = False
                if event.key == pygame.K_UP:
                    keystates['up'] = False
                if event.key == pygame.K_DOWN:
                    keystates['down'] = False
                if event.key == pygame.K_r:
                    keystates['reset_speed'] = False
                if event.key == pygame.K_s:
                    keystates['engine_state'] = False
                    car.change_engine_state()


        # do something about the key states here, now that the event queue has been processed
        if keystates['quit']:
            running = False
        
        
        if car.get_engine_state():
            if keystates['up']:
                speed = car.get_speed()
                acc = acc - (acc/2) * (1 + math.erf( (math.fabs(speed) - 5.5) / (math.sqrt(2 * math.pow(2.5, 2))) ))
                speed = speed + acc * delta
                car.set_speed(speed)

            if keystates['down']:
                speed = car.get_speed()
                dec = dec - (dec/2) * (1 + math.erf( (math.fabs(speed) - 5.5) / (math.sqrt(2 * math.pow(2.5, 2))) ))
                speed = speed - dec * delta
                car.set_speed(speed)
        else :
            if car.get_speed() > 0.05:
                speed = car.get_speed()
                frict = (frict/2) * (1 + math.erf( (math.fabs(speed) - 11/2) / (math.sqrt(2 * 4**2)) ))
                speed = speed + frict * delta
                car.set_speed(speed)
            elif car.get_speed() < -0.05:
                speed = car.get_speed()
                frict = (frict/2) * (1 + math.erf( (math.fabs(speed) - 11/2) / (math.sqrt(2 * 4**2)) ))
                speed = speed - frict * delta
                car.set_speed(speed)
            else :
                speed = car.get_speed()
                speed = 0
                car.set_speed(speed)


        if keystates['reset_speed']:
            car.reset_speed()

        speed_cur = car.get_speed()
        print ("({},{} --> {})".format(speed_cur, angle_cur, (speed_cur - last) / delta))
    
except KeyboardInterrupt:
    print ("Exiting through keyboard event (CTRL + C)")
    
# gracefully exit pygame here
pygame.quit()

