#!/bin/sh

# Burn latest piCore onto SD card
# Boot using newly created SD card
# Copy this script to home directory (/home/tc)
# Run this script to
#  - Create /mnt/.../copy2fs
#  - Do a backup $sudo filetool.sh -b
#  - Reboot
# Copy all pcp directory from Github to /tmp via WinSCP
# Copy the www directory from Github to /tmp via WinSCP
# Run this script to
#  - Expand /dev/mmcblk0p2 to +40M
#  - Copy all files and directories to the correct locations.

. /etc/init.d/tc-functions

TMP=/tmp                               # This is where you copy the files to
PCP_HOME=/home/tc/www/cgi-bin          # Not used yet
CSS_HOME=/home/tc/www/css              # Not used yet
IMG_HOME=/home/tc/www/images           # Not used yet
JS_HOME=/home/tc/www/js                # Not used yet
SBIN=/usr/local/sbin
OPT=/opt                               # Not used yet
INITD=/usr/local/etc/init.d            # Not used yet
STORAGE=/mnt/mmcblk0p2/tce
TCZ_PLACE=/mnt/mmcblk0p2/tce/optional

#=========================================================================================
# Get file routine
#   directory file directory
#       $1     $2     $3
#-----------------------------------------------------------------------------------------
getfile() {
	cp -v $1/$2 $3
}

#=========================================================================================
# Get package routine
#-----------------------------------------------------------------------------------------
getpackage() {
	if [ ! -f /mnt/mmcblk0p2/tce/optional/$1 ]; then
		sudo -u tc tce-load -wi $1
	fi
}

#=========================================================================================
# Check if partition is mounted otherwise mount it
#-----------------------------------------------------------------------------------------
pcp_mount() {
	PARTITION=$1
	if mount | grep /mnt/$PARTITION; then
		echo "${RED}[ ERROR ] /mnt/$PARTITION already mounted.${NORMAL}"
		RESULT=0
	else
		echo "${GREEN}[ INFO ] Mounting /mnt/$PARTITION...${NORMAL}"
		sudo mount /mnt/$PARTITION
		RESULT=$?
	fi
	[ $RESULT = 0 ] || echo "${RED}[ ERROR ] Mounting /mnt/$PARTITION.${NORMAL}"
}

#=========================================================================================
# Check if partition is unmounted otherwise unmount it
#-----------------------------------------------------------------------------------------
pcp_umount() {
	PARTITION=$1
	if mount | grep /mnt/$PARTITION; then
		echo "${GREEN}[ INFO ] Unmounting /mnt/$PARTITION...${NORMAL}"
		sudo umount /mnt/$PARTITION
		RESULT=$?
	else
		echo "${RED}[ ERROR ] /mnt/$PARTITION already unmounted.${NORMAL}"
		RESULT=0
	fi
	[ $RESULT = 0 ] || echo "${RED}[ ERROR ] Unmounting /mnt/$PARTITION.${NORMAL}"
}

clear

# Check that you are running the script as root
if [ "$(id -u)" != "0" ]; then
	echo "${RED}[ ERROR ] This script must be run as root.${NORMAL}"
	exit 1
else
	echo "${GREEN}[ INFO ] This script is running as root.${NORMAL}"
fi

# Set copy2fs.flg and reboot so mmcblk0p2 can be unmounted
pcp_mount mmcblk0p2
[ $RESULT = 0 ] || exit

if [ ! -f /mnt/mmcblk0p2/tce/copy2fs.flg ]; then
	echo "${RED}[ ERROR ] copy2fs.flg not found.${NORMAL}"
	touch /mnt/mmcblk0p2/tce/copy2fs.flg
	[ $? = 0 ] && "${YELLOW}[ INFO ] copy2fs.flg created.${NORMAL}"
	sudo filetool.sh -b
	echo "${RED}[ ERROR ] Rebooting.1...${NORMAL}"
	sudo reboot
	exit 1
else
	echo "${GREEN}[ INFO ] copy2fs.flg found.${NORMAL}"
fi

echo "${GREEN}[ INFO ] Continuing...${NORMAL}"

# Check there are no loop mounted filesystems
if df | grep /dev/loop; then
	echo "${RED}[ ERROR ] Loop mounted filesystems found - reboot required.${NORMAL}"
	echo "${RED}[ ERROR ] Rebooting.2...${NORMAL}"
	sudo reboot
	exit 1
else
	echo "${GREEN}[ INFO ] No loop mounted filesystems found.${NORMAL}"
fi

# Check for /tmp/www and /tmp/pcp directories
if [ -d /tmp/www ]; then
	echo "${GREEN}[ INFO ] /tmp/www directory found.${NORMAL}"
else
	echo "${RED}[ ERROR ] /tmp/www directory not found - winSCP directory over.${NORMAL}"
	CONTINUE=NO
fi
if [ -d /tmp/pcp ]; then
	echo "${GREEN}[ INFO ] /tmp/pcp directory found.${NORMAL}"
else
	echo "${RED}[ ERROR ] /tmp/pcp directory not found - winSCP directory over.${NORMAL}"
	CONTINUE=NO
fi
[ "$CONTINUE" = "NO" ] && exit

DEVELOPMENT=0

if [ $DEVELOPMENT = 0 ]; then
	pcp_umount mmcblk0p2
	[ $RESULT = 0 ] || exit

	START=$(fdisk -l | awk '/mmcblk0p2/ {print $2}')
	echo "${YELLOW}===================================================================="
	echo "${YELLOW}[ INFO ] Start sector for mmcblk0p2 is: ${START}${YELLOW}"
	sudo fdisk /dev/mmcblk0 <<EOF
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
	sudo e2fsck -fy /dev/mmcblk0p2
	sudo resize2fs /dev/mmcblk0p2
	fdisk -l
	echo "${YELLOW}====================================================================${NORMAL}"
	echo ""
fi

# Remove any dos-to-unix end of line problems from the files before using them:
echo "${GREEN}[ INFO ] Setting end of line markers to unix - dos2unix${NORMAL}"
sudo find /tmp/www -type f ! -name "*.tcz" ! -name "*.png" ! -name "*.gif" -print0 | xargs -0 dos2unix
sudo find /tmp/pcp -type f ! -name "*.tcz" ! -name "*.png" ! -name "*.gif" -print0 | xargs -0 dos2unix

pcp_mount mmcblk0p2
[ $RESULT = 0 ] || exit

# Remove any tcz package from piCore first time through
if [ -f $TCZ_PLACE/mc.tcz ]; then
	echo "${GREEN}[ INFO ] Removing tcz packages from piCore${NORMAL}"
	rm -f $TCZ_PLACE/*.*
	rm -f /usr/local/tce.installed/*
	tce-audit builddb                        # STEEN, IS THIS NECESSARY ?????
fi

#-----------------------------------------------------------------------------------------
#       from directory      |  filename          |  to directory
#-----------------------------------------------------------------------------------------
echo "${GREEN}[ INFO ] Copying pCP files into place...${YELLOW}"

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

#getfile $TMP/pcp/sbin          webgui               $SBIN
#chown root:root $SBIN/webgui
#chmod u=rwx,g=rx,o=rx $SBIN/webgui

getfile $TMP/pcp/sbin          setup                $SBIN
chown root:root $SBIN/setup
chmod u=rwx,g=rx,o=rx $SBIN/setup

getfile $TMP/pcp/mmcblk0p2     onboot.lst           $STORAGE
chown tc:staff $STORAGE/onboot.lst
chmod u=rwx,g=rwx,o=rx $STORAGE/onboot.lst

sleep 2

pcp_mount mmcblk0p1
[ $RESULT = 0 ] || exit

#getfile $TMP/pcp/mmcblk0p1     cmdline.txt           /mnt/mmcblk0p1
#getfile $TMP/pcp/mmcblk0p1     config.txt            /mnt/mmcblk0p1
getfile $TMP/pcp/mmcblk0p1      LICENCE.piCorePlayer  /mnt/mmcblk0p1

echo "${GREEN}[ INFO ] Updating cmdline.txt...${GREEN}"
echo smsc95xx.turbo_mode=N noswap showapps cron >> /mnt/mmcblk0p1/cmdline.txt

echo "${YELLOW}====================================================================${NORMAL}"
cat /mnt/mmcblk0p1/cmdline.txt
echo "${YELLOW}====================================================================${NORMAL}"

echo "${GREEN}[ INFO ] Updating config.txt...${GREEN}"
sed -i '/overclock the arm/d' /mnt/mmcblk0p1/config.txt
sed -i '/#arm_freq/d' /mnt/mmcblk0p1/config.txt
sed -i '/current/d' /mnt/mmcblk0p1/config.txt

echo "#---pCP----------------------------------------------" >> /mnt/mmcblk0p1/config.txt
echo "dtparam=audio" >> /mnt/mmcblk0p1/config.txt
echo "" >> /mnt/mmcblk0p1/config.txt
echo "# uncomment to overclock the arm. 700 MHz is the default." >> /mnt/mmcblk0p1/config.txt
echo "#arm_freq=" >> /mnt/mmcblk0p1/config.txt
echo "#core_freq=" >> /mnt/mmcblk0p1/config.txt
echo "#sdram_freq=" >> /mnt/mmcblk0p1/config.txt
echo "#over_voltage=" >> /mnt/mmcblk0p1/config.txt
echo "#force_turbo=" >> /mnt/mmcblk0p1/config.txt
echo "#gpu_mem=" >> /mnt/mmcblk0p1/config.txt
echo "" >> /mnt/mmcblk0p1/config.txt
echo "# Force max current to USB" >> /mnt/mmcblk0p1/config.txt
echo "max_usb_current=1" >> /mnt/mmcblk0p1/config.txt
echo "" >> /mnt/mmcblk0p1/config.txt
sed -i '/hiss/d' /mnt/mmcblk0p1/config.txt
echo '# Remove audio hiss' >> /mnt/mmcblk0p1/config.txt
sed -i '/disable_audio_dither=1/d' /mnt/mmcblk0p1/config.txt
echo "disable_audio_dither=1" >> /mnt/mmcblk0p1/config.txt

echo "${YELLOW}====================================================================${NORMAL}"
cat /mnt/mmcblk0p1/config.txt
echo "${YELLOW}====================================================================${NORMAL}"

sync
sync
pcp_umount mmcblk0p1
[ $RESULT = 0 ] || exit

# Copy www directory and set permissions
echo "${GREEN}[ INFO ] Copy www directory and set permissions.${YELLOW}"
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
echo "${GREEN}[ INFO ] Downloading essential tcz packages...${YELLOW}"
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
#getpackage faad2.tcz
#getpackage libsoxr.tcz
#getpackage libffmpeg.tcz

#--------------------------------------------
# Download Ralphy's files
#--------------------------------------------
echo "${GREEN}[ INFO ] Downloading Ralphy's tcz packages...${YELLOW}"

#rm -f /mnt/mmcblk0p2/tce/squeezelite-armv6hf
#sudo wget -P /mnt/mmcblk0p2/tce/ http://ralph_irving.users.sourceforge.net/pico/squeezelite-armv6hf
#sudo chmod u+x /mnt/mmcblk0p2/tce/squeezelite-armv6hf

echo "${GREEN}[ INFO ] Copying Ralphy's tcz packages...${YELLOW}"
getfile $TMP/pcp/Ralphys_files libffmpeg.tcz $TCZ_PLACE
chown tc:staff $TCZ_PLACE/libffmpeg.tcz
chmod u=rw,g=rw,o=r $TCZ_PLACE/libffmpeg.tcz

getfile $TMP/pcp/Ralphys_files libsoxr.tcz $TCZ_PLACE
chown tc:staff $TCZ_PLACE/libsoxr.tcz
chmod u=rw,g=rw,o=r $TCZ_PLACE/libsoxr.tcz

# For now we use Ralphy's instead of the official faad2.tcz package
getfile $TMP/pcp/Ralphys_files libfaad.tcz $TCZ_PLACE
chown tc:staff $TCZ_PLACE/libfaad.tcz
chmod u=rw,g=rw,o=r $TCZ_PLACE/libfaad.tcz

#--------------------------------------------
# Do a backup
#--------------------------------------------
#sudo alsactl store
echo "${GREEN}"
sudo filetool.sh -b
echo "${NORMAL}"
