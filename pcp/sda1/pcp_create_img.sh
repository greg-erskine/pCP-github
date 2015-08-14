#!/bin/sh
#
# This script creates the following files:
#	1. piCorePlayer.img
#	2. piCorePlayer_boot.tar.gz
#	3. piCorePlayer_tce.tar.gz
#
# This script should be copied to and run from /mnt/sda1/pcp.
#	1. sudo mount /mnt/sda1
#	2. cp pcp_create_img.sh to /mnt/sda1/pcp
#	3. sudo ./pcp_create_img.sh

# Version: 0.06 2015-08-14 SBP
#	Reused pcp-function for making default configuration.

# Version: 0.05 2015-01-21 GE
#	Updated default configuration.

# Version: 0.04 2014-10-19 GE
#	Updated default configuration.

# Version: 0.03 2014-10-08 GE
#	Set $MODE=0 in pcp-functions.
#	Checked for OliWeb.

# Version: 0.02 2014-08-28 GE
#	Renamed to pcp_create_img.sh
#	Major changes to piCorePlayer_script.sh

# Version: 0.01 2014-05-28 SBP
#	Original piCorePlayer_script.sh

#set -x
clear

if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root."
   exit 1
fi

. /home/tc/www/cgi-bin/pcp-functions

DEBUG=0
PIVERSION_CFG=/usr/local/sbin/piversion.cfg
CONFIGCFG=/usr/local/sbin/config.cfg

#=========================================================================================
# Display instructions for preparation before running this script
#-----------------------------------------------------------------------------------------
echo
echo =======================================================
echo "                     REMINDERS"
echo -------------------------------------------------------
echo "1. Have you synchronised files using winscp?"
echo "2. This script will RESET all pCP settings to DEFAULT"
echo =======================================================
echo

read -p "Continue? (y)es/(n)o " ANS
case $ANS in
	y|Y|yes)
		;;
	*)
		exit
		;;
esac

echo ================================================================================
echo "                      Files currently on /mnt/sda1"
echo --------------------------------------------------------------------------------
ls -al /mnt/sda1
echo ================================================================================
echo

[ -f $PIVERSION_CFG ] && . $PIVERSION_CFG
VERSION=$(echo $PIVERS | awk '{ print $2 }')
NAME=piCorePlayer$VERSION

echo =====================================================
echo "   Current contents of "$PIVERSION_CFG
echo -----------------------------------------------------
cat $PIVERSION_CFG
echo =====================================================
echo
echo Creating image: $NAME

read -p "Continue? (y)es/(n)o/(c)hange " ANS

case $ANS in
	y|Y|yes)
		;;
	c|C|change)
		read -p "Enter NEW version: " NEWVERSION
		rm -f $PIVERSION_CFG
		touch $PIVERSION_CFG
		chown root:root $PIVERSION_CFG
		chmod 777 $PIVERSION_CFG
		echo \#piCorePlayer version > $PIVERSION_CFG
		echo 'PIVERS="piCorePlayer '$NEWVERSION'"' >> $PIVERSION_CFG
		chmod 644 $PIVERSION_CFG
		$0
		exit
		;;
	n|N|no)
		exit
		;;
	*)
		echo "[ ERROR ] Invalid option!"
		exit
		;;
esac

#=========================================================================================
# Look for old files
#-----------------------------------------------------------------------------------------
echo =======================================================
echo "Looking for old OliWeb..."
echo -------------------------------------------------------
sudo find / -name "[O|o]li[W|w]eb*" -print
echo
echo =======================================================
echo

read -p "Continue? (y)es/(n)o " ANS

case $ANS in
	y|Y|yes)
		;;
	n|N|no)
		exit
		;;
	*)
		echo "[ ERROR ] Invalid option!"
		exit
		;;
esac

#=========================================================================================
# Sets the following:
# 	1. $DEBUG=0 and $TEST=0 in pcp-functions
#	2. /etc/sysconfig/timezone is deleted.
#	3. Set /usr/local/sbin/config.cfg to default settings.
#-----------------------------------------------------------------------------------------
if [ -f ~/www/cgi-bin/pcp-functions ]; then
	echo "Updating DEBUG and TEST in pcp-functions..."
	sed -i "s/\(DEBUG=\).*/\10/" ~/www/cgi-bin/pcp-functions
	sed -i "s/\(TEST=\).*/\10/" ~/www/cgi-bin/pcp-functions
	sed -i "s/\(MODE=\).*/\10/" ~/www/cgi-bin/pcp-functions
fi

if [ -f /etc/sysconfig/timezone ]; then
	echo "Resetting timezone file..."
	ls -al /etc/sysconfig/timezone
	rm -f /etc/sysconfig/timezone
	touch /etc/sysconfig/timezone
	ls -al /etc/sysconfig/timezone
fi

if [ -f $CONFIGCFG ]; then
	echo "Setting configuration defaults values..."
pcp_reset_config_to_defaults
fi

#=========================================================================================
# Tidy up some files
#-----------------------------------------------------------------------------------------
rm -f /home/tc/.ash_history

#=========================================================================================
# Create a fresh copy of mydata.tcz before image creation starts.
#-----------------------------------------------------------------------------------------
echo "Doing a mydata backup..."
filetool.sh -b

#=========================================================================================
# Create tar and image files.
#-----------------------------------------------------------------------------------------
[ -d /mnt/sda1/"$NAME" ] && rm -rf /mnt/sda1/"$NAME"
mount /dev/mmcblk0p1
mkdir /mnt/sda1/"$NAME"
tar -zcvf /mnt/sda1/"$NAME"/"$NAME"_boot.tar.gz /mnt/mmcblk0p1
tar -zcvf /mnt/sda1/"$NAME"/"$NAME"_tce.tar.gz /mnt/mmcblk0p2/tce
dd if=/dev/mmcblk0 of=/mnt/sda1/"$NAME"/"$NAME".img bs=1M count=75
sync;sync

echo Created these files:
ls -al /mnt/sda1/"$NAME"

#=========================================================================================
# Display instructions for un-mounting USB drive
#-----------------------------------------------------------------------------------------
echo
echo =====================================================
echo "1. Close all applications accessing USB drive"
echo "2. Change directory to $HOME - cd ~"
echo "3. Un-mount USB drive - sudo umount /mnt/sda1"
echo =====================================================
echo

exit

#=========================================================================================
# Prompt to umount /mnt/sda1???
#-----------------------------------------------------------------------------------------
read -p "Umount sda1? y/n " ANS

[ $ANS != y ] && exit
cd $HOME
umount /mnt/sda1
echo "Safe to remove sda1"
