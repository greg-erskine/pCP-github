#!/bin/sh


while true
do
	echo "====================================================="
	date
	echo "squeezelite -d:"
	echo "---------------"
	timeout -t 1 /mnt/mmcblk0p2/tce/squeezelite-armv6hf -d slimproto=info 2>&1 | grep -o from:.*:3483 | grep -oE '([0-9]{1,3}[\.]){3}[0-9]{1,3}'
	echo "netstat:"
	echo "--------"
	netstat -nt 2>&1 | grep :3483 | awk '{print $5}' | awk -F: '{print $1}'
	echo "-----------------------------------------------------"
	echo ""
	sleep 5
done