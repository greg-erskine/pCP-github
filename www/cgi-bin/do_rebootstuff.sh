#!/bin/sh

# Version: 012 2015-02-15 SBP
#	Updated order.

# Version: 0.11 2015-02-09 GE
#	Added pcp_auto_start_fav.
#	Added stop/start crond.
#	Added pcp_user_commands.
#	Moved timezone before essential stuff.
#	Added ANSI colours to messages.

# Version: 0.10 2015-01-06 SBP
#	Removed unneeded piCorePlayer.dep check

# Version: 0.09 2014-12-09 SBP
#	Added support for the HiFiBerry AMP card.
#	Moved saving to config file from extern newconfig to pcp-functions.
#	Moved loading correct audio modules to pcp-functions.

# Version: 0.08 2014-10-09 SBP
#	Added Analog/HDMI output selection (moved from enable/disablehdmi.sh)

# Version: 0.07 2014-10-07 GE
#	Added echos for booting debugging purposes.

# Version: 0.06 2014-09-28 SBP
#	Added support for the HiFiBerry+ and IQaudIO+ cards. Improved the custom ALSA settings logic.

# Version: 0.05 2014-09-04 GE
#	Added cron-job variables and LMS auto-start variable.

# Version: 0.06 2014-09-09 GE
#	Added pcp_auto_start_lms at end of script.

# Version: 0.05 2014-09-04 GE
#	Added timezone function.

# Version: 0.04 2014-08-31 SBP
#	Minor formatting.

# Version: 0.03 2014-08-30 SBP
#	Clean up + added analog amixer use.
#	Improved the alsamixer use.

# Version: 0.02 2014-08-26 GE
#	Clean up.

# Version: 0.01 2014-06-25 SBP
#	Original.

#set -x

. /home/tc/www/cgi-bin/pcp-functions
#. /etc/init.d/tc-functions

echo ""
# Read from pcp-functions file
echo "${GREEN}Starting piCorePlayer setup...${NORMAL}"
echo -n "${BLUE}Loading pcp-functions... "
pcp_variables
echo "${GREEN}Done.${NORMAL}"

# Read from config file.
echo -n "${BLUE}Loading configuration file... ${NORMAL}"
. $CONFIGCFG
echo "${GREEN}Done.${NORMAL}"

# Mount USB stick if present
echo "${BLUE}Checking for newconfig.cfg on sda1... ${NORMAL}"

# Check if sda1 is mounted otherwise mount it
MNTUSB=/mnt/sda1
if mount | grep $MNTUSB; then
	echo "${YELLOW}- sda1 mounted${NORMAL}"
else
	# FIX: check if sda1 is inserted before trying to mount it.
	echo "${YELLOW}- Trying to mount sda1${RED}"
	sudo mount /dev/sda1
fi

# Check if newconfig.cfg is present
if [ -f $MNTUSB/newconfig.cfg ]; then
	echo "${YELLOW}- newconfig.cfg found on sda1${NORMAL}"
	sudo dos2unix -u $MNTUSB/newconfig.cfg
	# Read variables from newconfig and save to config.
	. $MNTUSB/newconfig.cfg
	echo -n "${BLUE}Updating configuration... ${NORMAL}"
	#Save to config file
	pcp_save_to_config
	echo "${GREEN}Done.${NORMAL}"
if [ $AUDIO = HDMI ]; then sudo $pCPHOME/enablehdmi.sh; else sudo $pCPHOME/disablehdmi.sh; fi
#sleep 1
fi

# Rename the newconfig file on USB
if [ -f /mnt/sda1/newconfig.cfg ]; then sudo mv /mnt/sda1/newconfig.cfg /mnt/sda1/usedconfig.cfg; fi

echo "${BLUE}Checking for newconfig.cfg on mmcblk0p1...  ${NORMAL}"
# Check if a newconfig.cfg file is present on mmcblk0p1 - requested by SqueezePlug and CommandorROR and used for insitu update
pcp_mount_mmcblk0p1_nohtml
if [ -f /mnt/mmcblk0p1/newconfig.cfg ]; then
	echo "${YELLOW}- newconfig.cfg found on mmcblk0p1${NORMAL}"
	sudo dos2unix -u /mnt/mmcblk0p1/newconfig.cfg
	# Read variables from newconfig and save to config.
	. /mnt/mmcblk0p1/newconfig.cfg
	pcp_save_to_config
if [ $AUDIO = HDMI ]; then sudo $pCPHOME/enablehdmi.sh; else sudo $pCPHOME/disablehdmi.sh; fi
#sleep 1
# Delete the newconfig file
sudo rm -f /mnt/mmcblk0p1/newconfig.cfg
fi
pcp_umount_mmcblk0p1_nohtml


	# If using a RPi-A+ card with wifi on we need to load the wireless firmware if not already loaded and then reboot
	if [ $(pcp_rpi_is_model_Aplus) = 0 ] || [ $WIFI == "\"on\"" ]; then
		if grep -Fxq "wifi.tcz" /mnt/mmcblk0p2/tce/onboot.lst
			then
			echo "${BLUE}wifi firmware already loaded${NORMAL}"
			else
			# Add wifi related modules back
			sudo fgrep -vxf /mnt/mmcblk0p2/tce/onboot.lst /mnt/mmcblk0p2/tce/piCorePlayer.dep >> /mnt/mmcblk0p2/tce/onboot.lst
			echo "${BLUE}Will reboot now and then wifi firmware will be loaded${NORMAL}"
			pcp_save_to_config
			pcp_backup_nohtml
			sleep 4
			sudo reboot 
		fi
	fi


# Save the parameters to the wifi.db
echo -n "${BLUE}Reading config.cfg... ${NORMAL}"
. /usr/local/sbin/config.cfg
echo "${GREEN}Done.${NORMAL}"

# Only add backslash if not empty
echo "${BLUE}Updating wifi.db... ${NORMAL}"
if [ x"" = x"$SSID" ]; then
	break
else
	SSSID=`echo "$SSID" | sed 's/\ /\\\ /g'`
	# Change SSSID back to SSID
	SSID=$SSSID
	sudo echo ${SSID}$'\t'${PASSWORD}$'\t'${ENCRYPTION}> /home/tc/wifi.db
fi
echo "${GREEN}Done.${NORMAL}"

echo -n "${BLUE}Loading configuration file... ${NORMAL}"
# Read from config file.
. $CONFIGCFG
echo "${GREEN}Done.${NORMAL}"

echo -n "${BLUE}Loading snd modules... ${NORMAL}" 
sudo modprobe snd-bcm2835
#sudo modprobe -r snd_soc_wm8731
sudo modprobe snd_soc_bcm2708_i2s
#sudo modprobe bcm2708_dmaengine
sudo modprobe snd_soc_wm8804
echo "${GREEN}Done.${NORMAL}"

echo "${BLUE}Checking wifi... ${NORMAL}"
# Logic that will skip the wifi connection if wifi is disabled
if [ $WIFI = on ]; then
	echo "${YELLOW}wifi is on${NORMAL}"
	sudo ifconfig wlan0 down
	sleep 1
	sudo ifconfig wlan0 up
	sleep 1
	sudo iwconfig wlan0 power off &>/dev/null
	sleep 1
	#usr/local/bin/wifi.sh -a 2>&1 > /tmp/wifi.log
	/usr/local/bin/wifi.sh -a
	sleep 1

	# Logic that will try to reconnect to wifi if failed - will try two times before continuing booting
	for i in 1 2; do
		if ifconfig wlan0 | grep -q "inet addr:" ; then
			echo "${YELLOW}connected${NORMAL}"      
		else
			echo "${RED}Network connection down! Attempting reconnection two times before continuing.${NORMAL}"
			sudo ifconfig wlan0 down
			sleep 1
			sudo ifconfig wlan0 up
			sleep 1
			sudo iwconfig wlan0 power off &>/dev/null
			sleep 1
			sudo /usr/local/bin/wifi.sh -a
			sleep 10
	   fi
	done
fi

echo -n "${BLUE}Loading pcp-lms-functions... ${NORMAL}"
. /home/tc/www/cgi-bin/pcp-lms-functions
echo "${GREEN}Done.${NORMAL}"

echo "${BLUE}Loading I2S modules... ${NORMAL}"
#if [ $AUDIO = HDMI ]; then sudo $pCPHOME/enablehdmi.sh; else sudo $pCPHOME/disablehdmi.sh; fi
#sleep 1
# Loads the correct output audio modules
pcp_read_chosen_audio
echo "${GREEN}Done.${NORMAL}"

# Sleep for 1 sec otherwise aplay can not see the card
sleep 1

# Check for onboard sound card is card=0 and analog is chosen, so amixer is only used here
echo "${BLUE}Starting ALSA configuration... ${NORMAL}"
aplay -l | grep 'card 0: ALSA' &> /dev/null
if [ $? == 0 ] && [ $AUDIO = Analog ]; then
	sudo amixer cset numid=3 1				#set the analog output via audio jack
	if [ $ALSAlevelout = Default ]; then
		sudo amixer set PCM 400 unmute
	fi
fi

# Check for onboard sound card is card=0, and HDMI is chosen so HDMI amixer settings is enabled
aplay -l | grep 'card 0: ALSA' &> /dev/null
if [ $? == 0 ] && [ $AUDIO = HDMI ]; then
	sudo amixer cset numid=3 2				#set the analog output via HDMI out
fi 

# If Custom ALSA settings are used, then restore the settings
if [ $ALSAlevelout = Custom ]; then
	alsactl restore
fi
echo "${GREEN}Done.${NORMAL}"

# Only call timezone function if timezone variable is set
if [ x"" != x"$TIMEZONE" ]; then
	echo -n "${BLUE}Setting timezone... ${NORMAL}"
	pcp_set_timezone
	echo "${GREEN}Done.${NORMAL}"
fi

# Start the essential stuff for piCorePlayer
echo "${BLUE}Loading the main daemons..."
echo -n "${BLUE}"
/usr/local/etc/init.d/dropbear start
echo "${GREEN}Done.${NORMAL}"

echo -n "${BLUE}"
/usr/local/etc/init.d/httpd start
sleep 1
echo "${GREEN}Done.${NORMAL}"

echo -n "${BLUE}"
/usr/local/etc/init.d/squeezelite start
echo "${GREEN}Done.${NORMAL}"

echo -n "${BLUE}Starting auto start LMS... ${NORMAL}"
pcp_auto_start_lms
echo "${GREEN}Done.${NORMAL}"

echo -n "${BLUE}Starting auto start FAV... ${NORMAL}"
pcp_auto_start_fav
echo "${GREEN}Done.${NORMAL}"

echo -n "${BLUE}Starting user commands... ${NORMAL}"
pcp_user_commands
echo "${GREEN}Done.${NORMAL}"

echo -n "${BLUE}Starting crond... ${NORMAL}"
/etc/init.d/services/crond start 2>&1
echo "${GREEN}Done.${NORMAL}"

if [ $JIVELITE = "YES" ]; then
echo -n "${BLUE}Starting Jivelite... ${NORMAL}"
/opt/jivelite/bin/jivelite-sp 2>&1
echo "${GREEN}Done.${NORMAL}"
fi

echo -n "${BLUE}Updating configuration... ${NORMAL}"
# Placed here in order to only backup once during do_rebootstuff
# Save the parameters to the config file
# pcp_save_to_config
pcp_backup_nohtml
echo "${GREEN}Done.${NORMAL}"