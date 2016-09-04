#!/bin/sh

# Flash LED on GPIO 4

echo "4" > /sys/class/gpio/export
echo "out" > /sys/class/gpio/gpio4/direction

while true
do
	sleep 0.5
	echo "1" > /sys/class/gpio/gpio4/value
	sleep 0.5
	echo "0" > /sys/class/gpio/gpio4/value
done
