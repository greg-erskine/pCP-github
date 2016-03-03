#!/bin/sh

#========================================================================================
# Basic gpio script
#----------------------------------------------------------------------------------------
# squeezelite -S /home/tc/powerscript.sh
# 
# squeezelite sets $1 to:
#	0: off
#	1: on
#	2: initialising
#----------------------------------------------------------------------------------------

# Version: 0.01 2016-03-03 GE
#	Original.

# type tty at prompt to determine dev

#TERMINAL=/dev/console		# boot console

TERMINAL=/dev/pts/0			# ssh window

case $1 in
	2)
		echo "$1: Initialising..." >$TERMINAL
		;;
	1)
		echo "$1: turn on" >$TERMINAL
		;;
	0)
		echo "$1: turn off" >$TERMINAL
		;;
esac
