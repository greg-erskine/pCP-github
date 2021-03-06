#!/bin/sh
#
# piCorePlayer Power Button Script - Used to shutdown pCP with a GPIO input.
#
#	Version 1.1 2018-06-24
#		Bug fix for --low
#
#
#  Defaults are for the Audiophonics power button
DEBUG=0
IN_LOW=0
PIN_IN=17
PIN_OUT=22
PUPDOWN="off"

PATH=/bin:/usr/bin:/usr/local/bin

usage() {
	echo "  usage: $0 [-i] [-o] [--low] [--help] [--debug]"
	echo "            -i        GPIO input pin to shutdown pCP"
	echo "            -o        GPIO output pin for successful pCP boot"
	echo "            --low     Input is active low (and set pull up resistor)"
	echo "            --high    Input is active high (and set pull down resistor)"
	echo "            --debug   Script run as normal, but will not shutdown pCP"
	echo "            --help    script usage"
	echo ""
	echo "            Note: pin numbers are in BCM notation"
	echo ""
	exit 1
}

validate_pin(){
	VAL=$(echo $1 | grep -o '[[:digit:]]*')

	if [ "$VAL" != "" ]; then
		if [ $VAL -le 31 ]; then
			return 0
		fi
	fi
	return 1
}

O=$(getopt -al help,low,high,debug -- i:o:h "$@") || exit 1
eval set -- "$O"

[ "$1" = "--" ] && echo "No command line settings, Using defaults"; echo ""

while true; do
	case "$1" in
		-i) PIN_IN=$2; shift;;
		-o) PIN_OUT=$2; shift;;
		--debug) DEBUG=1;;
		--low) IN_LOW=1; PUPDOWN="up";;
		--high) IN_LOW=0; PUPDOWN="down";;
		--help) usage;;
		--) shift; break;;
		-*) usage;;
		*) break;;
	esac
	shift
done

echo "piCorePlayer Power button shutdown script starting..."

validate_pin $PIN_IN
if [ $? -ne 0 ]; then
	echo "Error in Input Pin Assignment"
	exit 1
fi
validate_pin $PIN_OUT
if [ $? -ne 0 ]; then
	echo "Error in Output Pin Assignment"
	exit 1
fi

echo "Asserting pins : "
echo -n "ShutDown : GPIO${PIN_IN}=in, "
[ ${IN_LOW} -eq 1 ] && echo "Low" || echo "High"
echo "BootOK   : GPIO${PIN_OUT}=out, High"

gpio -g mode $PIN_IN in
gpio -g mode $PIN_IN $PUPDOWN
gpio -g mode $PIN_OUT out
gpio -g write $PIN_OUT 1

[ $IN_LOW -eq 0 ] && IN_CHK=1 || IN_CHK=0

while [ 1 ]; do
  if [ "$(/usr/local/bin/gpio -g read ${PIN_IN})" = "$IN_CHK" ]; then
        echo "piCorePlayer shutting down."
        [ $DEBUG -eq 0 ] && sudo /sbin/poweroff
        break
  fi
  /bin/sleep 1
done

exit 0
