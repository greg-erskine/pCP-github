#!/bin/sh

if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root."
   exit 1
fi


# First copy all pcp director from Github to /tmp via WinSCP (on the new piCore).
# Next copy the www director from Github to /tmp via WinSCP (on the new piCore).
# Then this script will copy all files and directories to the correct location.

TMP=/tmp/          # this is where you copy the files to

PCP_HOME=/home/tc/www/cgi-bin   # Not used yet
CSS_HOME=/home/tc/www/css       # Not used yet
IMG_HOME=/home/tc/www/css       # Not used yet
JS_HOME=/home/tc/www/css        # Not used yet
SBIN=/usr/local/sbin
OPT=/opt                        # Not used yet
INITD=/usr/local/etc/init.d     # Not used yet
STORAGE=/mnt/mmcblk0p1/tce

#=========================================================================================
# Get file routine
#   Will probably try to use scp eventually.
#
#	directory file directory
#	  $1        $2      $3
#-----------------------------------------------------------------------------------------
getfile() {
	cp -p -v $1/$2 $3
}

#-----------------------------------------------------------------------------------------
#       |  from directory      |  filename          |  to directory
#-----------------------------------------------------------------------------------------
getfile $TMP/pcp/conf          wifi.db              /home/tc
getfile $TMP/pcp/conf          timezone             /etc/sysconfig
getfile $TMP/pcp/conf          config.cfg           $SBIN
getfile $TMP/pcp/conf          piversion.cfg        $SBIN
#getfile $TMP/pcp/conf          wpa_supplicant.conf  /etc
getfile $TMP/pcp/conf          asound.conf          /etc
getfile $TMP/pcp/conf          modprobe.conf        /etc
getfile $TMP/pcp/conf          piCorePlayer.dep     /mnt/mmcblk0p2/tce

getfile $TMP/pcp/init.d        squeezelite          /usr/local/etc/init.d
getfile $TMP/pcp/init.d        httpd                /usr/local/etc/init.d

getfile $TMP/pcp/opt           .filetool.lst        /opt
getfile $TMP/pcp/opt           bootlocal.sh         /opt
getfile $TMP/pcp/opt           bootsync.sh          /opt

getfile $TMP/pcp/sbin          webgui               /usr/local/sbin



# Check if mmcblk0p1 is mounted otherwise mount it
if mount | grep /mnt/mmcblk0p1; then
	echo '[ ERROR ] '/mnt/mmcblk0p1' already mounted.'
else
	echo '[ INFO ] Mounting /mnt/mmcblk0p1...'
	sudo mount /dev/mmcblk0p1
fi


getfile $TMP/pcp/mmcblk0p1     cmdline.txt           /mnt/mmcblk0p1
getfile $TMP/pcp/mmcblk0p1     config.txt            /mnt/mmcblk0p1
getfile $TMP/pcp/mmcblk0p1     LICENCE.piCorePlayer  /mnt/mmcblk0p1

# Unmount mmcblk0p1
sync
sync
echo '[ INFO ] Unmounting /mnt/mmcblk0p1...'
sudo umount /dev/mmcblk0p1




getfile $TMP/pcp/mmcblk0p2     onboot.lst            $STORAGE


