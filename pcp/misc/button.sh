#!/bin/sh

# Play/stop Squeezelite
# Push button connected to GPIO17

player=started

echo "17" > /sys/class/gpio/export
echo "in" > /sys/class/gpio/gpio17/direction

while true
do
	PRESSED=$(cat /sys/class/gpio/gpio17/value)
	echo $PRESSED
	sleep 1
	if [ $PRESSED = 0 ]; then
		if [ $player = stopped ]; then
			echo "Start player"
			echo "play" | telnet 192.168.1.101:9090
			player=started
			sleep 3
		else
			echo "Stop player"
			echo "stop" | telnet 192.168.1.101:9090
			player=stopped
			sleep 3
		fi
	fi
done

echo "17" > /sys/class/gpio/unexport

exit
