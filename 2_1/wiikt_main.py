#!/usr/bin/env python

#######################################################################
#                            Aufgabe 2	                              #
#######################################################################

from linuxWiimoteLib import *
import bluetooth
import servo_ctl
import math

Real_Motor = servo_ctl.Motor()
Real_Steering = servo_ctl.Real_Steering()
One_speed = 5
Two_speed = 10


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

		if (not wiistate.ButtonState.Home):
			triple(acc_X, acc_Y, acc_Z) = wiimote.getAccelState()
			print ("({},{},{})".format(acc_X, acc_Y, acc_Z))
		else:
			print 're-calibrating'
			wiimote.calibrateAccelerometer()
		if (wiistate.ButtonState.B):
			triple(angle_X, angle_Y, angle_Z) = wiimote.getGyroState()
			if angle_Y == 0:
				speed_cur = 0
			elif -45 < angle_Y < 0:
				speed_cur = - angle_Y / 45 * 11
			elif 0 < angle_Y < 45:
				speed_cur = angle_Y / 45 * 11
			elif angle_Y == 45:
				speed_cur = 11
			elif angle_Y == -45:
				speed_cur = -11
			Real_Motor.set_speed(speed_cur)


			



except KeyboardInterrupt:
	print ("Exiting through keyboard event (CTRL + C)")
	exit(wiimote)
