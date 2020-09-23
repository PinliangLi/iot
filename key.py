#!/usr/bin/env python

#######################################################################
#                            Aufgabe 1                                #
#######################################################################

import sys, time
import random
import car_model
import math
import pygame 
#import RPi.GPIO as GPIO
import servo_ctrl
        

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
curr_last = 0

# start main pygame event processing loop here
pygame.display.init()

# set up the pygame screen enviroment
screen = pygame.display.set_mode((width, height))

# get a clock to generate frequent behaviour
clock = pygame.time.Clock()

Sim_Motor = car_model.Motor()
Sim_Steering = car_model.Steering()
Real_Motor = servo_ctrl.Motor()
Real_Steering = servo_ctrl.Steering()

# States of the keys
keystates = {'quit':False, 'up':False, 'down':False, 'reset_speed':False, 'reset_angle':False, 'engine_state':False, 'steering_state':False, 'mouse_event':False, 'left':False, 
             'right':False, 'simulate': False}
use_mouse = False
simulate = True
pygame.mouse.set_pos([width, height])

def speed_up(Sim_Motor, acc):
    speed = Sim_Motor.get_speed()
    acc = acc - (acc/2) * (1 + math.erf( (math.fabs(speed) - 5.5) / (math.sqrt(2 * math.pow(2.5, 2))) ))
    speed = speed + acc * delta
    Sim_Motor.set_speed(speed)

def speed_down(Sim_Motor, dec):
    speed = Sim_Motor.get_speed()
    dec = dec - (dec/2) * (1 + math.erf( (math.fabs(speed) - 5.5) / (math.sqrt(2 * math.pow(2.5, 2))) ))
    speed = speed - dec * delta
    Sim_Motor.set_speed(speed)

def speed_frict(Sim_Motor, frict):
    speed = Sim_Motor.get_speed()
    frict = (frict/2) * (1 + math.erf( (math.fabs(speed) - 11/2) / (math.sqrt(2 * 4**2)) ))
    speed = speed + frict * delta
    Sim_Motor.set_speed(speed)

def angle_return(Sim_Steering, angle_acc):
    angle = Sim_Steering.get_angle()
    angle = angle - angle_acc * delta
    Sim_Steering.set_angle(angle)

def angle_left(Sim_Steering, angle_acc):
    angle = Sim_Steering.get_angle()
    angle = angle + angle_acc * delta
    Sim_Steering.set_angle(angle)

def angle_right(Sim_Steering, angle_acc):
    angle = Sim_Steering.get_angle()
    angle = angle - angle_acc * delta
    Sim_Steering.set_angle(angle)

def mouse_turn(positionX, Sim_Steering, angle_acc):                 ###3b
    relevateX = positionX - width/2
    if relevateX < -100:
        angle_left(Sim_Steering, angle_acc)
    if relevateX > 100:
        angle_right(Sim_Steering, angle_acc)

def mouse_speed(positionY, Sim_Motor, acc, dec):
    relevateY = positionY - height/2
    if relevateY < -100:
        speed_up(Sim_Motor, acc)
    if relevateY > 100:
        speed_down(Sim_Motor, dec)



running = True
try:
    while running:
        # set clock frequency
        clock.tick(freq)
        
        # save the last speed 4 analysis
        last = speed_cur
        angle_last = angle_cur
        acc=2.6
        dec=4.5
        frict=-1.0
        PWM_speed_acc = 1.0
        PWM_speed_dec = 1.0
        PWM_angle_acc = 100.0
        # process input events
        for event in pygame.event.get():
        
            # exit on quit
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                use_mouse = True
                keystates['engine_state'] = True
                keystates['steering_state'] = True
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
                    Sim_Motor.change_engine_state()
                    Real_Motor.change_engine_state()
                    
                if event.key == pygame.K_d:
                    keystates['steering_state'] = True
                    Sim_Steering.change_steering_state()
                    Real_Steering.change_steering_state()
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
                if event.key == pygame.K_d:
                    keystates['steering_state'] = False
                if event.key == pygame.K_m:
                    if use_mouse:
                        use_mouse = False
                if event.key == pygame.K_v:
                    keystates['simulate'] = False
        # do something about the key states here, now that the event queue has been processed
        if keystates['quit']:
            running = False
        

        if simulate:
            if Sim_Motor.get_engine_state():
                print(Sim_Motor.get_engine_state())
                if use_mouse:                                       
                    mouse_position = pygame.mouse.get_pos()
                    mouse_speed(mouse_position[1], Sim_Motor, acc, dec)
                else:
                    pygame.event.set_allowed(pygame.KEYDOWN)
                    pygame.event.set_allowed(pygame.KEYUP)
                if keystates['up']:
                    speed_up(Sim_Motor, acc)
                if keystates['down']:
                    speed_down(Sim_Motor, dec)
            else :
                if Sim_Motor.get_speed() > 0.05:
                    speed_frict(Sim_Motor, frict)
                elif Sim_Motor.get_speed() < -0.05:
                    speed_frict(Sim_Motor, -frict)
                else :
                    speed = Sim_Motor.get_speed()
                    speed = 0
                    Sim_Motor.set_speed(speed)

            if Sim_Steering.get_steering_state():
                #print(Sim_Steering.get_steering_state())
                if use_mouse:                                       
                    mouse_position = pygame.mouse.get_pos()
                    mouse_turn(mouse_position[0], Sim_Steering, angle_acc)
                if keystates['left']:
                    angle_left(Sim_Steering, angle_acc)
                if keystates['right']:
                    angle_right(Sim_Steering, angle_acc)
            else :
                if Sim_Steering.get_angle() > 4:
                    angle_return(Sim_Steering, angle_acc)
                if Sim_Steering.get_angle() < -4:
                    angle_return(Sim_Steering, -angle_acc)
                else :
                    angle = Sim_Steering.get_angle()
                    angle = 0
                    Sim_Steering.set_angle(angle)

            if keystates['reset_speed']:
                Sim_Motor.reset_speed()
            if keystates['reset_angle']:
                Sim_Steering.reset_angle()




            speed_cur = Sim_Motor.get_speed()
            angle_cur = Sim_Steering.get_angle()
            print("({},{} --> {})".format(speed_cur, angle_cur, (speed_cur - last) / delta))

        else :
            print(Real_Motor.get_engine_state())
            print("({},{} --> {})".format(Real_Motor.get_speed(), Real_Steering.get_angle(), (Real_Motor.get_speed() - curr_last) / delta))
            if Real_Motor.get_engine_state():
                if use_mouse:
                    mouse_position = pygame.mouse.get_pos()
                    Real_Motor.PWM_mouse_speed(mouse_position[1], PWM_speed_acc, PWM_speed_dec, height)
                if keystates['up']:
                    Real_Motor.PWM_speed_up(PWM_speed_acc, delta)
                if keystates['down']:
                    Real_Motor.PWM_speed_down(PWM_speed_dec, delta)
            else :
                pass

            if Real_Steering.get_steering_state():
                if use_mouse:
                    mouse_position = pygame.mouse.get_pos() 
                    Real_Steering.PWM_mouse_turn(mouse_position[0], PWM_angle_acc, width)
                if keystates['left']:
                    Real_Steering.PWM_angle_left(PWM_angle_acc, delta)
                if keystates['right']:
                    Real_Steering.PWM_angle_right(PWM_angle_acc, delta)
            curr_last = Real_Motor.get_speed()

except KeyboardInterrupt:
    print ("Exiting through keyboard event (CTRL + C)")
    

# gracefully exit pygame here
pygame.quit()