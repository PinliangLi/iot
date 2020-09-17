echo "2" > /sys/class/gpio/export
echo "in" > /sys/class/gpio/gpio2/direction

while 1
do
    cat /sys/class/gpio/gpio2/value
    sleep 1
done
