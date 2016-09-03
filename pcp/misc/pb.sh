#!/bin/sh +x

# Version: 0.01 2016-08-30 GE
#	Original.

#===========================================================================
# This script polls GPIOs at a regular interval to determine if a push
# button is pressed.
#---------------------------------------------------------------------------
NO_OF_PB=1

PB1_GPIO=17
PB2_GPIO=18
PB3_GPIO=20

PB1_COMMAND="pcp next"
PB2_COMMAND="pcp next"
PB3_COMMAND="pcp prev"

INTERVAL=0.5

#===========================================================================
# Initialise GPIOs
#---------------------------------------------------------------------------
pcp_initalise() {
	for i in `seq $NO_OF_PB`
	do
		PCP_PB_GPIO=$(eval "echo \$PB${i}_GPIO")
		sudo sh -c 'echo '"$PCP_PB_GPIO"' > /sys/class/gpio/export'
		sudo sh -c 'echo "in" > /sys/class/gpio/gpio'"$PCP_PB_GPIO"'/direction'
	done
}

#===========================================================================
# Cleanup when ^C pressed
#---------------------------------------------------------------------------
pcp_cleanup() {
	echo "Cleaning up..."
	for i in `seq $NO_OF_PB`
	do
		PCP_PB_GPIO=$(eval "echo \$PB${i}_GPIO")
		sudo sh -c 'echo '"$PCP_PB_GPIO"' > /sys/class/gpio/unexport'
	done
	exit 0
}
#---------------------------------------------------------------------------

trap "pcp_cleanup" 2

pcp_initalise

#===========================================================================
# This section needs to be a fast as possible, so it is adviseable to hard
# code rather than doing calculations.
#---------------------------------------------------------------------------

#while true
#do
#	sleep $INTERVAL
#	for i in `seq $NO_OF_PB`
#	do
#		PCP_PB_GPIO=$(eval "echo \$PB${i}_GPIO")
#		if [ $(cat /sys/class/gpio/gpio${PCP_PB_GPIO}/value) -eq 0 ]; then
#			echo "PB${i} pressed"
#			pcp next
#		else
#			echo "PB${i} not pressed"
#		fi
#	done
#done


while true
do
	sleep $INTERVAL
		[ $(cat /sys/class/gpio/gpio17/value) -eq 0 ] && echo "PB1 pressed"
		[ $(cat /sys/class/gpio/gpio18/value) -eq 1 ] && echo "PB2 pressed"
		[ $(cat /sys/class/gpio/gpio19/value) -eq 1 ] && echo "PB3 pressed"
	done
done


exit
