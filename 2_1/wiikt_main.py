#!/usr/bin/env python

#######################################################################
#                            Aufgabe 2	                              #
#######################################################################

from linuxWiimoteLib import *
import bluetooth
import servo_ctl
import math
import threading

Real_Motor = servo_ctl.Motor()
Real_Steering = servo_ctl.Real_Steering()
One_speed = 5
Two_speed = 10


class Turning(threading.Thread):
	"""docstring for Turning"""
	def __init__(self, wii, omega = 0.5):
		super(Turning, self).__init__()
		self. wii = wii
		self.omega = omega
	
	def run(self):

		last_rotate = 0

		while True:
			rotate_x, rotate_y, rotate_z = wiimote.getGyroState()
			new_rotate = self.omega * rotate_z + (1 - w) * last_rotate
			actually_rotate = alpa * math.pow(new_rotate, n_pow) + (1 - alpa) * new_rotate
			Real_Steering.set_angle(actually_rotate)
			last_rotate = new_rotate


			



device = None
# initialize wiimote
wiimote = Wiimote()

#Insert address and name of device here
near_devices = bluetooth.discover_devices(lookup_names=True)
print("Found {} devices.".format(len(near_devices)))

for addr, name in near_devices:
    print("{} --> {}".format(addr, name))
    if "Joy" in name:
    	device = (addr, name)
    	print(device)

connected = False

try:
	print ("Press SYNC on wiimote to make it discoverable")
	while (not connected):
		connected = wiimote.Connect(device)

	print ("succesfully connected")

	wiimote.SetAccelerometerMode()

	wiistate = wiimote.WiimoteState

	turning = Turning(wiimote)
	while True:

		# re-calibrate accelerometer
		if (wiistate.ButtonState.Home):
			print ('re-calibrating')
			wiimote.calibrateAccelerometer()
			sleep(0.1)	

		if (wiistate.ButtonState.Up):
			print("Speed up")
			Real_Motor.PWM_speed_up(1, 0.1)
			print("Speed:", Real_Motor.get_speed())

		if (wiistate.ButtonState.Down):
			print("Speed down")
			Real_Motor.PWM_speed_down(1, 0.1)			
			print("Speed:", Real_Motor.get_speed())

		if (wiistate.ButtonState.Left):
			print("left")
			Real_Steering.PWM_angle_left(300, 0.1)
			print("angle:", Real_Steering.get_angle())

		if (wiistate.ButtonState.Right):
			print("right")
			Real_Steering.PWM_angle_right(300, 0.1)
			print("angle:", Real_Steering.get_angle())

		if (wiistate.ButtonState.One):
			print("One Button Down Speed:" One_speed)
			Real_Motor.set_speed(One_speed)

		if (wiistate.ButtonState.Two):
			print("Two Button Down Speed:" Two_speed)
			Real_Motor.set_speed(Two_speed)
		
		Speed = Real_Motor.get_speed()

		if 0 <= math.fabs(Speed) <= 4:
			wiimote.SetLEDs(True,False,False,False)

		elif 4 < math.fabs(Speed) <= 8:
			wiimote.SetLEDs(True,True,False,False)

		elif 8 < math.fabs(Speed) < 11:
			wiimote.SetLEDs(True,True,True,False)			

		elif Speed == 11
			wiimote.SetLEDs(True,True,True,True)

		else :
			wiimote.SetLEDs(True,False,False,False)

		if (wiistate.ButtonState.A):
			print("Reset")
			Real_Motor.set_speed(0)
			Real_Steering.set_angle(0)
		






except KeyboardInterrupt:
	print ("Exiting through keyboard event (CTRL + C)")
	exit(wiimote)
