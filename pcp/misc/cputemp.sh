#!/bin/sh

. /home/tc/www/cgi-bin/pcp-rpi-functions

while true
do
	TEMP=$(pcp_rpi_thermal_temp)
	TIME=$(date | awk '{print $4}' | awk -F: '{print $1, $2}' | sed 's/ /:/g')
	echo "$TIME $TEMP" | awk '{print $1,$3}'
	sleep 60
done
