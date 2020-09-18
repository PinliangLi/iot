
#pin 17 18 aktivieren#
echo"17" > /sys/class/gpio/export
echo"18" > /sys/class/gpio/export

#pin 17 18 als Ausgang#
echo "out" > /sys/class/gpio/gpio17/direction
echo "out" > /sys/class/gpio/gpio18/direction

#loop#
for ((i=0;i<10;++i))
do
	echo 1 > /sys/class/gpio/gpio17/value
	echo 0 > /sys/class/gpio/gpio17/value
	sleep 1

	echo 0 > /sys/class/gpio/gpio18/value
	echo 1 > /sys/class/gpio/gpio18/value
	sleep 1
done

#reset#
echo 0 > /sys/class/gpio/gpio17/value
echo 0 > /sys/class/gpio/gpio18/value

 
 
