#!/bin/sh

# Turn LED on GPIO4 on, off or flash

flash_led() {
	while true
	do
		sleep 0.5
		echo "0" > /sys/class/gpio/gpio4/value
		sleep 0.5
		echo "1" > /sys/class/gpio/gpio4/value
	done
}

echo "4" > /sys/class/gpio/export
echo "out" > /sys/class/gpio/gpio4/direction

case $1 in
	on)
		echo "0" > /sys/class/gpio/gpio4/value
		;;
	off)
		echo "1" > /sys/class/gpio/gpio4/value
		;;
	flash)
		flash_led
		;;
	*)
		echo "led on|off|flash"
		;;
esac

echo "4" > /sys/class/gpio/unexport

exit
