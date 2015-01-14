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

	# Set variables to default values
	sudo sed -i "s/\(NAME=\).*/\1\"piCorePlayer\"/" $CONFIGCFG
	sudo sed -i "s/\(OUTPUT=\).*/\1\"sysdefault:CARD=ALSA\"/" $CONFIGCFG
	sudo sed -i "s/\(ALSA_PARAMS=\).*/\1\"80:::0\"/" $CONFIGCFG
	sudo sed -i "s/\(BUFFER_SIZE=\).*/\1\"\"/" $CONFIGCFG
	sudo sed -i "s/\(_CODEC=\).*/\1\"\"/" $CONFIGCFG
	sudo sed -i "s/\(PRIORITY=\).*/\1\"\"/" $CONFIGCFG
	sudo sed -i "s/\(MAX_RATE=\).*/\1\"\"/" $CONFIGCFG
	sudo sed -i "s/\(UPSAMPLE=\).*/\1\"\"/" $CONFIGCFG
	sudo sed -i "s/\(MAC_ADDRESS=\).*/\1\"\"/" $CONFIGCFG
	sudo sed -i "s/\(SERVER_IP=\).*/\1\"\"/" $CONFIGCFG
	sudo sed -i "s/\(LOGLEVEL=\).*/\1\"\"/" $CONFIGCFG
	sudo sed -i "s/\(LOGFILE=\).*/\1\"\"/" $CONFIGCFG
	sudo sed -i "s/\(DSDOUT=\).*/\1\"\"/" $CONFIGCFG
	sudo sed -i "s/\(VISULIZER=\).*/\1\"\"/" $CONFIGCFG
	sudo sed -i "s/\(OTHER=\).*/\1\"\"/" $CONFIGCFG
	sudo sed -i "s/\(AUDIO=\).*/\1\"\Analog\"/" $CONFIGCFG
	sudo sed -i "s/\(HOST=\).*/\1\"piCorePlayer\"/" $CONFIGCFG
	sudo sed -i "s/\(SSID=\).*/\1\"wireless\"/" $CONFIGCFG
	sudo sed -i "s/\(PASSWORD=\).*/\1\"password\"/" $CONFIGCFG
	sudo sed -i "s/\(ENCRYPTION=\).*/\1\"WPA\"/" $CONFIGCFG
	sudo sed -i "s/\(OVERCLOCK=\).*/\1\"NONE\"/" $CONFIGCFG
	sudo sed -i "s/\(CMD=\).*/\1\"Default\"/" $CONFIGCFG
	sudo sed -i "s/\(WIFI=\).*/\1\"off\"/" $CONFIGCFG
	sudo sed -i "s/\(FIQ=\).*/\1\"0x7\"/" $CONFIGCFG
	sudo sed -i "s/\(ALSAlevelout=\).*/\1\"Default\"/" $CONFIGCFG
	sudo sed -i "s/\(TIMEZONE=\).*/\1\"\"/" $CONFIGCFG
	sudo sed -i "s/\(REBOOT *=*\).*/\1\"Disabled\"/" $CONFIGCFG
	sudo sed -i "s/\(RB_H *=*\).*/\1\"0\"/" $CONFIGCFG
	sudo sed -i "s/\(RB_WD *=*\).*/\1\"0\"/" $CONFIGCFG
	sudo sed -i "s/\(RB_DMONTH *=*\).*/\1\"0\"/" $CONFIGCFG
	sudo sed -i "s/\(RESTART *=*\).*/\1\"Disabled\"/" $CONFIGCFG
	sudo sed -i "s/\(RS_H *=*\).*/\1\"0\"/" $CONFIGCFG
	sudo sed -i "s/\(RS_WD *=*\).*/\1\"0\"/" $CONFIGCFG
	sudo sed -i "s/\(RS_DMONTH *=*\).*/\1\"0\"/" $CONFIGCFG
	sudo sed -i "s/\(AUTOSTARTLMS=\).*/\1\"\"/" $CONFIGCFG
	sudo sed -i "s/\(AUTOSTARTFAV=\).*/\1\"\"/" $CONFIGCFG
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
dd if=/dev/mmcblk0 of=/mnt/sda1/"$NAME"/"$NAME".img bs=1M count=65
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
