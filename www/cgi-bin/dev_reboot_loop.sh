#!/bin/sh

# Version: 3.5.0 2018-02-07
#	Original. GE.
#	Make it work on USB bootdisk. PH.

# This script writes a date stamp to /mnt/mmcblk0p1/reboot_loop.log then reboots after a delay.
# Add "/home/tc/www/cgi-bin/dev_reboot_loop.sh 30" to User Command #1.
# Use command "wc -l reboot_loop.log" to count number of reboots.
# Payload will not run if /mnt/mmcblk0p1/norebootloop exists.

. /home/tc/www/cgi-bin/pcp-functions

REBOOT_LOOP="${BOOTMNT}/reboot_loop.log"
DELAY="10"
[ "$1" = "" ] || DELAY=$1

# Wait for ntp time to be set otherwise epoch will be written to file.
sleep 10

pcp_mount_bootpart_nohtml

# Safe guard - add file norebootloop to boot partition to break loop.
if [ -f ${BOOTMNT}/norebootloop ]; then
	echo "[ INFO ] found norebootloop, exiting..."
	pcp_umount_bootpart_nohtml
	exit 1
fi

date >> $REBOOT_LOOP

pcp_umount_bootpart_nohtml

# Countdown loop
CNT=0
until false; do
	echo -n "$(($DELAY - $CNT))."
	[ $((CNT++)) -eq $DELAY ] && break || sleep 1
done
echo ""

pcp rb
