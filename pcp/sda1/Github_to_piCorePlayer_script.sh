#!/bin/sh

if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root."
   exit 1
fi


# First copy all pcp director from Github to /tmp via WinSCP (on the new raw piCore).
# Next copy the www director from Github to /tmp via WinSCP (on the new raw piCore).
# Then this script will copy all files and directories to the correct location.

#To do:
# Expand mmcblk0p2 to something like 50MB before continuing
DEVELOPMENT=1

if [ $DEVELOPMENT = 0 ]; then 
START=$(fdisk -ul /dev/mmcblk0 | awk ' /'mmcblk0p2'/ {print $2}')

echo "Start sector for mmcblk0p2 is:" $START
fdisk -u /dev/mmcblk0 <<EOF
p
d
2
n
p
2
$START
+42M
w
EOF

# need a reboot?? or.
sudo rebuildfstab
wait 4
sudo resize2fs /dev/mmcblk0p2
wait 8
sudo rebuildfstab
fi

TMP=/tmp          # this is where you copy the files to

PCP_HOME=/home/tc/www/cgi-bin   # Not used yet
CSS_HOME=/home/tc/www/css       # Not used yet
IMG_HOME=/home/tc/www/images    # Not used yet
JS_HOME=/home/tc/www/js         # Not used yet
SBIN=/usr/local/sbin
OPT=/opt                        # Not used yet
INITD=/usr/local/etc/init.d     # Not used yet
STORAGE=/mnt/mmcblk0p2/tce
TCZ_PLACE=/mnt/mmcblk0p2/tce/optional


#Remove any dos-to-unix end of line problems from the files before using them:
sudo find /tmp/www -type f ! -name "*.tcz" ! -name "*.png" ! -name "*.gif" -print0 | xargs -0 dos2unix
sudo find /tmp/pcp -type f ! -name "*.tcz" ! -name "*.png" ! -name "*.gif" -print0 | xargs -0 dos2unix


# Remove any tcz package from piCore first
rm -f $TCZ_PLACE/*.*
rm -f /usr/local/tce.installed/*
tce-audit builddb

#=========================================================================================
# Get file routine
#   Will probably try to use scp eventually.
#
#	directory file directory
#	  $1        $2      $3
#-----------------------------------------------------------------------------------------
getfile() {
	cp -v $1/$2 $3
}

#-----------------------------------------------------------------------------------------
#       |  from directory      |  filename          |  to directory
#-----------------------------------------------------------------------------------------
getfile $TMP/pcp/conf          wifi.db              /home/tc
chown root:root /home/tc/wifi.db
chmod u=rw,g=rw,o=r /home/tc/wifi.db

getfile $TMP/pcp/conf          timezone             /etc/sysconfig
chown root:root /etc/sysconfig/timezone
chmod u=rw,g=rw,o=r /etc/sysconfig/timezone

getfile $TMP/pcp/conf          config.cfg           $SBIN
chown root:root $SBIN/config.cfg
chmod u=rwx,g=rx,o=rx $SBIN/config.cfg

getfile $TMP/pcp/conf          piversion.cfg        $SBIN
chown root:root $SBIN/piversion.cfg
chmod u=rw,g=r,o=r $SBIN/piversion.cfg

#getfile $TMP/pcp/conf         wpa_supplicant.conf /etc

getfile $TMP/pcp/conf          asound.conf          /etc
chown root:root /etc/asound.conf
chmod u=rwx,g=rx,o=rx /etc/asound.conf

getfile $TMP/pcp/conf          modprobe.conf        /etc
chown root:root /etc/modprobe.conf
chmod u=rwx,g=rx,o=rx /etc/modprobe.conf

getfile $TMP/pcp/conf          piCorePlayer.dep     $STORAGE
chown root:root $STORAGE/piCorePlayer.dep
chmod u=rw,g=r,o=r $STORAGE/piCorePlayer.dep

getfile $TMP/pcp/etc           motd                 /etc
chown root:root /etc/motd
chmod u=rw,g=r,o=r /etc/motd

getfile $TMP/pcp/init.d        squeezelite          $INITD
chown root:root $INITD/squeezelite
chmod u=rwx,g=rx,o=rx $INITD/squeezelite

getfile $TMP/pcp/init.d        httpd                $INITD
chown root:root $INITD/httpd
chmod u=rwx,g=rx,o=rx $INITD/httpd

getfile $TMP/pcp/opt           .filetool.lst        /opt
chown root:staff /opt/.filetool.lst
chmod u=rw,g=rw,o=r /opt/.filetool.lst

getfile $TMP/pcp/opt           bootlocal.sh         /opt
chown root:staff /opt/bootlocal.sh
chmod u=rwx,g=rwx,o=rx /opt/bootlocal.sh

getfile $TMP/pcp/opt           bootsync.sh          /opt
chown root:staff /opt/bootsync.sh
chmod u=rwx,g=rwx,o= /opt/bootsync.sh

getfile $TMP/pcp/sbin          webgui               $SBIN
chown root:root $SBIN/webgui
chmod u=rwx,g=rx,o=rx $SBIN/webgui

getfile $TMP/pcp/sbin          setup                $SBIN
chown root:root $SBIN/setup
chmod u=rwx,g=rx,o=rx $SBIN/setup

getfile $TMP/pcp/mmcblk0p2     onboot.lst            $STORAGE
chown tc:staff $STORAGE/onboot.lst
chmod u=rwx,g=rwx,o=rx $STORAGE/onboot.lst

# Check if mmcblk0p1 is mounted otherwise mount it
if mount | grep /mnt/mmcblk0p1; then
	echo '[ ERROR ] '/mnt/mmcblk0p1' already mounted.'
else
	echo '[ INFO ] Mounting /mnt/mmcblk0p1...'
	sudo mount /dev/mmcblk0p1
fi

sleep 2
#getfile $TMP/pcp/mmcblk0p1     cmdline.txt           /mnt/mmcblk0p1
#getfile $TMP/pcp/mmcblk0p1     config.txt            /mnt/mmcblk0p1
getfile $TMP/pcp/mmcblk0p1      LICENCE.piCorePlayer  /mnt/mmcblk0p1

# Unmount mmcblk0p1
sync
sync
echo '[ INFO ] Unmounting /mnt/mmcblk0p1...'
sudo umount /dev/mmcblk0p1




#Copy www directory and set permissions

sudo rm -rf /home/tc/www
sudo cp -vr $TMP/www /home/tc/

chown -R tc:staff /home/tc/www
chmod u=rwx,g=rx,o= /home/tc/www/cgi-bin/*
chmod u=rw,g=r,o= /home/tc/www/css/*
chmod u=rw,g=r,o= /home/tc/www/images/*
chmod u=rw,g=r,o= /home/tc/www/js/*
chmod u=r,g=r,o= /home/tc/www/index.html


#--------------------------------------------
# Download essential tcz-packages
#--------------------------------------------

getpackage() {
	if [ ! -f /mnt/mmcblk0p2/tce/optional/$1 ]; then
	sudo -u tc tce-load -wi $1 >> /tmp/pcp.tcz.txt 2>&1
	fi
}

wait 2
getpackage busybox-httpd.tcz
getpackage dropbear.tcz
getpackage alsa.tcz
getpackage alsa-config.tcz
getpackage flac.tcz
getpackage libvorbis.tcz
getpackage libmad.tcz
getpackage wifi.tcz
getpackage firmware-atheros.tcz
getpackage firmware-ralinkwifi.tcz
getpackage firmware-rtlwifi.tcz
getpackage faad2.tcz
#getpackage libsoxr.tcz
#getpackage libffmpeg.tcz


#Download Ralphys files
rm -f /mnt/mmcblk0p2/tce/squeezelite-armv6hf
sudo wget -P /mnt/mmcblk0p2/tce/ http://ralph_irving.users.sourceforge.net/pico/squeezelite-armv6hf
sudo chmod u+x /mnt/mmcblk0p2/tce/squeezelite-armv6hf

getfile $TMP/pcp/Ralphys_files          libffmpeg.tcz     $TCZ_PLACE
chown tc:staff $TCZ_PLACE/libffmpeg.tcz
chmod u=rw,g=rw,o=r $TCZ_PLACE/libffmpeg.tcz

getfile $TMP/pcp/Ralphys_files          libsoxr.tcz     $TCZ_PLACE
chown tc:staff $TCZ_PLACE/libsoxr.tcz
chmod u=rw,g=rw,o=r $TCZ_PLACE/libsoxr.tcz

#For now we use the official faad2.tcz package
#getfile $TMP/pcp/Ralphys_files          libfaad.tcz     $TCZ_PLACE
#chown tc:staff $TCZ_PLACE/libfaad.tcz
#chmod u=rw,g=rw,o=r $TCZ_PLACE/libfaad.tcz


# Make a backup
sudo filetool.sh -b




