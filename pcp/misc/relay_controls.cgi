#!/bin/sh

# Version: 0.01 2014-11-07 GE
#	Original.

. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "Relay Control" "GEx"

[ $DEBUG = 1 ] && echo '<body>' || echo '<body onload="javascript:location.href=document.referrer;">'

pcp_running_script

pcp_httpd_query_string

#=========================================================================================
# Initialise GPIO for replays
#-----------------------------------------------------------------------------------------

# echo "17" > /sys/class/gpio/export
# sudo sh -c 'echo 17 > /sys/class/gpio/export'

# echo "in" > /sys/class/gpio/gpio17/direction
# echo "1" > /sys/class/gpio/gpio17/active_low
# PRESSED=$(cat /sys/class/gpio/gpio17/value)
# echo "17" > /sys/class/gpio/unexport




#=========================================================================================
# Map relay to GPIO
#-----------------------------------------------------------------------------------------
case $RELAY in
	RLY1)
		GPIO=gpio17
		;;
	RLY2)
		GPIO=gpio27
		;;
esac

if [ $DEBUG = 1 ]; then 
	echo '<p class="debug">[ DEBUG ] $RELAY: '$RELAY'<br />'
	echo '                 [ DEBUG ] $ACTION: '$ACTION'<br />'
	echo '                 [ DEBUG ] $GPIO: '$GPIO'</p>'
fi

case $ACTION in
	on)
		echo "0" > /sys/class/gpio/$GPIO/value
		;;
	off)
		echo "1" > /sys/class/gpio/$GPIO/value
		;;
esac

[ $DEBUG = 1 ] && pcp_go_back_button || pcp_footer

echo '</body>'
echo '</html>'