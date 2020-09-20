#!/bin/bash

sudo ifconfig ra0 192.168.1.xxx netmask 255.255.255.0 up


sudo iwconfig ra0 essid off
sudo iwconfig ra0 essid group02h

ping 192.168.1.1

#server time1.rrzn.uni-hannover.de
sudo service ntp stop
sudo service ntp start


sudo ip route change 172.23.0.0/16 dev ra0