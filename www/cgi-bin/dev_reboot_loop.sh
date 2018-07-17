#!/bin/sh

# Version: 4.0.0 2018-07-17

#========================================================================================
# This script writes a date stamp to ${BOOTMNT}/pcp_reboot_loop.log then
# reboots after a delay. Default delay is 10 seconds + 10 seconds wait for ntp.
#----------------------------------------------------------------------------------------
#  1. Add "/home/tc/www/cgi-bin/dev_reboot_loop.sh 30" to User Command #1.
#  2. Reboot.
#  3. Use command "wc -l pcp_reboot_loop.log" to count number of reboots.
#  4. To break loop add ${BOOTMNT}/norebootloop.
#----------------------------------------------------------------------------------------

. /home/tc/www/cgi-bin/pcp-functions

REBOOT_LOOP="${BOOTMNT}/pcp_reboot_loop.log"
DELAY="10"
[ "$1" = "" ] || DELAY=$1

# Wait for ntp time to be set otherwise epoch will be written to file.
sleep 10

pcp_mount_bootpart_nohtml >/dev/null 2>&1

REBOOTS=$(wc -l ${REBOOT_LOOP} | awk '{print $1}')

# Safe guard - add file norebootloop to boot partition to break loop.
if [ -f ${BOOTMNT}/norebootloop ]; then
	echo "[ INFO ] Found norebootloop, exiting..."
	pcp_umount_bootpart_nohtml >/dev/null 2>&1
	exit 1
fi

date >> $REBOOT_LOOP
pcp_umount_bootpart_nohtml >/dev/null 2>&1
echo
echo "Rebooting...(${REBOOTS})"

#------------------------------------------Countdown loop--------------------------------
CNT=0
until false; do
	echo -n -e "\b\b\b\b$(($DELAY - $CNT)) "
	[ $((CNT++)) -eq $DELAY ] && break || sleep 1
done
echo ""
#----------------------------------------------------------------------------------------

pcp rb
