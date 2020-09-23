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

def angle_dec(Sim_Steering, angle_acc):     #how quick for angle return
    angle = Sim_Steering.get_angle()
    angle = angle - angle_acc * delta
    Sim_Steering.set_angle(angle)

def angle_return(Sim_Steering, angle_acc):  #automaticly turn into front when not turning left or right
    if Sim_Steering.get_angle() > 4:
        angle_dec(Sim_Steering, angle_acc)
    elif Sim_Steering.get_angle() < -4:
        angle_dec(Sim_Steering, -angle_acc)
    else :
        angle = Sim_Steering.get_angle()
        angle = 0
        Sim_Steering.set_angle(angle)

def mouse_turn(positionX, Sim_Steering):             
    relevateX = positionX - width/2
    angle = relevateX / (width/2) * (-45)
    Sim_Steering.set_angle(angle)

def mouse_speed(positionY, Sim_Motor):
    relevateY = positionY - height/2
    speed = relevateY / (height/2) * (-11)
    Sim_Motor.set_speed(speed)

def PWM_speed_up(Motor, acc):
    speed =  Motor.get_speed() + acc * delta  #m -> M
    Motor.set_speed(speed)

def PWM_speed_down(Motor, dec):
    speed =  Motor.get_speed() - dec * delta
    Motor.set_speed(speed)

def PWM_angle_left(Motor, angle_acc):
    angle = Motor.get_angle() + angle_acc * delta
    Motor.set_angle(angle)

def PWM_angle_right(Motor, angle_acc):
    angle = Motor.get_angle() - angle_acc * delta
    Motor.set_angle(angle)

def PWM_mouse_turn(positionX, Motor):      ###new func
    relevateX = positionX - width/2
    angle = relevateX / (width/2) * (-45)
    Sim_Steering.set_angle(angle)

def PWM_mouse_speed(positionY, Motor, acc, dec):      ###new func
    relevateY = positionY - height/2
    speed = relevateY / (height/2) * (-11)
    Sim_Motor.set_speed(speed)

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
        PWM_speed_acc = 1
        PWM_speed_dec = 1
        PWM_angle_acc = 100
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
                    
                if event.key == pygame.K_d:
                    keystates['steering_state'] = True
                    Sim_Steering.change_steering_state()
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
                    mouse_speed(mouse_position[1], Sim_Motor)
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
                    mouse_turn(mouse_position[0], Sim_Steering)
                else:
                    if keystates['left']:
                        angle_left(Sim_Steering, angle_acc)
                    if keystates['right']:
                        angle_right(Sim_Steering, angle_acc)
                    if not keystates['left'] and not keystates['right']:
                        angle_return(Sim_Steering, angle_acc)
            else :
                pass

            if keystates['reset_speed']:
                Sim_Motor.reset_speed()
            if keystates['reset_angle']:
                Sim_Steering.reset_angle()




            speed_cur = Sim_Motor.get_speed()
            angle_cur = Sim_Steering.get_angle()

        else :
            if Real_Motor.get_engine_state():
                if use_mouse:
                    mouse_position = pygame.mouse.get_pos()
                    PWM_mouse_speed(mouse_position[1], Real_Motor)
                if keystates['up']:
                    PWM_speed_up(Real_Motor, PWM_speed_acc)
                if keystates['down']:
                    PWM_speed_down(Real_Motor, PWM_speed_dec)
            else :
                pass

            if Real_Steering.get_steering_state():
                if use_mouse:
                    mouse_position = pygame.mouse.get_pos() 
                    PWM_mouse_turn(mouse_position[0], Real_Steering)
                if keystates['left']:
                    PWM_angle_left(Real_Steering, PWM_angle_acc)
                if keystates['right']:
                    PWM_angle_right(Real_Steering, PWM_angle_acc)
            else :
                pass


        print ("({},{} --> {})".format(speed_cur, angle_cur, (speed_cur - last) / delta))
except KeyboardInterrupt:
    print ("Exiting through keyboard event (CTRL + C)")
    

# gracefully exit pygame here
pygame.quit()

