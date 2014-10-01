#!/bin/sh
#set -x

if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root."
   exit 1
fi

#=========================================================================================
# Make directories routine
#
#	directory protection owner
#	   $1        $2       $3
#-----------------------------------------------------------------------------------------
makedir() {
	if [ -d $1 ]; then
		echo "[ WARN ] directory $1 already exists."
	else
		mkdir /home/tc/pcp/$1
		chmod $2 /home/tc/pcp/$1
		chown $3 /home/tc/pcp/$1
	fi
}

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

#=========================================================================================
#
#-----------------------------------------------------------------------------------------
makedir conf          755 tc:staff
makedir documentation 755 tc:staff
makedir init.d        755 tc:staff
makedir misc          755 tc:staff
makedir mmcblk0p1     755 tc:staff
makedir opt           755 tc:staff
makedir sbin          755 tc:staff
makedir sda1          755 tc:staff
makedir temp          755 tc:staff

#-----------------------------------------------------------------------------------------
#       |  from directory      |  filename          |  to directory
#-----------------------------------------------------------------------------------------
getfile /home/tc               wifi.db              /home/tc/pcp/conf
getfile /etc/sysconfig         timezone             /home/tc/pcp/conf
getfile /usr/local/sbin        config.cfg           /home/tc/pcp/conf
getfile /usr/local/sbin        piversion.cfg        /home/tc/pcp/conf
getfile /etc                   wpa_supplicant.conf  /home/tc/pcp/conf
getfile /etc                   asound.conf          /home/tc/pcp/conf
getfile /etc                   modprobe.conf        /home/tc/pcp/conf

getfile /usr/local/etc/init.d  squeezelite          /home/tc/pcp/init.d
getfile /usr/local/etc/init.d  httpd                /home/tc/pcp/init.d

getfile /opt                   .filetool.lst        /home/tc/pcp/opt
getfile /opt                   bootlocal.sh         /home/tc/pcp/opt
getfile /opt                   bootsync.sh          /home/tc/pcp/opt

getfile /usr/local/sbin        Set_nrPacks.sh       /home/tc/pcp/sbin
getfile /usr/local/sbin        picoreplayer         /home/tc/pcp/sbin
getfile /usr/local/sbin        set_*.sh             /home/tc/pcp/sbin
getfile /usr/local/sbin        settings_menu.sh     /home/tc/pcp/sbin
getfile /usr/local/sbin        updates_sql.sh       /home/tc/pcp/sbin
getfile /usr/local/sbin        upsample.sh          /home/tc/pcp/sbin
getfile /usr/local/sbin        wifi_picoreplayer.sh /home/tc/pcp/sbin


getfile /mnt/mmcblk0p2/tce    piCorePlayer.dep      /home/tc/pcp/conf



# Collect file from sda1

# Check if sda1 is mounted otherwise mount it
if mount | grep /mnt/sda1; then
	echo '[ ERROR ] '/mnt/sda1' already mounted.'
else
	echo '[ INFO ] Mounting /mnt/sda1...'
	sudo mount /dev/sda1
fi

getfile /mnt/sda1/pcp         pcp_create_img.sh     /home/tc/pcp/sda1

# Unmount sda1
sync
sync
echo '[ INFO ] Unmounting /mnt/sda1...'
sudo umount /dev/sda1



# Collect files from mmcblk0p1

# Check if mmcblk0p1 is mounted otherwise mount it
if mount | grep /mnt/mmcblk0p1; then
	echo '[ ERROR ] '/mnt/mmcblk0p1' already mounted.'
else
	echo '[ INFO ] Mounting /mnt/mmcblk0p1...'
	sudo mount /dev/mmcblk0p1
fi

getfile /mnt/mmcblk0p1        cmdline.txt           /home/tc/pcp/mmcblk0p1
getfile /mnt/mmcblk0p1        config.txt            /home/tc/pcp/mmcblk0p1
getfile /mnt/mmcblk0p1        LICENCE.piCorePlayer  /home/tc/pcp/mmcblk0p1

# Unmount mmcblk0p1
sync
sync
echo '[ INFO ] Unmounting /mnt/mmcblk0p1...'
sudo umount /dev/mmcblk0p1


exit
