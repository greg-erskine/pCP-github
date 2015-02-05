#!/bin/sh

# Version: 0.11 2015-01-28 GE
#	Added pcp_auto_start_fav.
#	Added stop/start crond.
#	Added pcp_user_commands.
#	Moved timezone before essential stuff.

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

echo "[ INFO ] Running do_rebootstuff.sh..."
echo "[ INFO ] Loading pcp-functions"
# Read from pcp-functions file
. /home/tc/www/cgi-bin/pcp-functions
pcp_variables
. $CONFIGCFG
echo "[ INFO ] Loading pcp-lms-functions"
. /home/tc/www/cgi-bin/pcp-lms-functions

echo "[ INFO ] Checking for newconfig.cfg on sda1"
# Mount USB stick if present
# Check if sda1 is mounted otherwise mount it

MNTUSB=/mnt/sda1
if mount | grep $MNTUSB; then
	echo "mounted"
	else
	echo "now trying to mount USB"
	sudo mount /dev/sda1
fi

# Check if newconfig.cfg is present
if [ -f $MNTUSB/newconfig.cfg ]; then
	sudo dos2unix -u $MNTUSB/newconfig.cfg
	# Read variables from newconfig and save to config.
	. $MNTUSB/newconfig.cfg
	echo "[ INFO ] Updating configuration"
	#Save to config file
	pcp_save_to_config
fi

# Rename the newconfig file on USB
if [ -f /mnt/sda1/newconfig.cfg ]; then sudo mv /mnt/sda1/newconfig.cfg /mnt/sda1/usedconfig.cfg; fi

echo "[ INFO ] Checking for newconfig.cfg on mmcblk0p1"
# Check if a newconfig.cfg file is present on mmcblk0p1 - requested by SqueezePlug and CommandorROR and used for insitu update
sudo mount /dev/mmcblk0p1
if [ -f /mnt/mmcblk0p1/newconfig.cfg ]; then
	sudo dos2unix -u /mnt/mmcblk0p1/newconfig.cfg
	# Read variables from newconfig and save to config.
	. /mnt/mmcblk0p1/newconfig.cfg
	echo "[ INFO ] Updating configuration"
	# Save the parameters to the config file
	pcp_save_to_config	
fi

# Save changes caused by the presence of a newconfig.cfg file
if [ -f /mnt/mmcblk0p1/newconfig.cfg ]; then sudo filetool.sh -b; fi
# Delete the newconfig file
sudo rm -f /mnt/mmcblk0p1/newconfig.cfg
sleep 1
sudo umount /mnt/mmcblk0p1

# Section to save the parameters to the wifi.db - this is a new version in order to saving space and backslash in SSID which is needed in wifi.db
# so a name like "steens wifi" should be saved as  "steens\ wifi"
echo "[ INFO ] Reading config.cfg"
. /usr/local/sbin/config.cfg

# sudo chmod 766 /home/tc/wifi.db
# Only add backslash if not empty
echo "[ INFO ] Updating wifi.db"
if [ x"" = x"$SSID" ]; then
	break
else
	SSSID=`echo "$SSID" | sed 's/\ /\\\ /g'`
	# Change SSSID back to SSID
	SSID=$SSSID
	sudo echo ${SSID}$'\t'${PASSWORD}$'\t'${ENCRYPTION}> /home/tc/wifi.db
	pcp_backup_nohtml
fi

# We do have a problem with SSID's which don't have a name - should we use the next section for these SSIDs - I have not tested the code
# Saves SSID if empty
# if [ x"" = x"$SSID" ]; then sudo chmod 766 /home/tc/wifi.db; sudo echo ${SSID}$'\t'${PASSWORD}$'\t'${ENCRYPTION}> /home/tc/wifi.db; else fi
# NEW Section ends here

# Save changes caused by the presence of a newconfig.cfg file and wifi copy from config.cfg to wifi.db fie
# Is already save - I think - sudo filetool.sh -b

# Stuff previously handled by bootlocal.sh - but sits better here allowing for in situ update of as bootlocal then can be kept free from piCorePlayer stuff
# allowing any custom changes to bootlocal.sh to be maintained as it is not overwritten by in situ update.

echo "[ INFO ] Loading snd modules" 
sudo modprobe snd-bcm2835
#sudo modprobe -r snd_soc_wm8731
sudo modprobe snd_soc_bcm2708_i2s
sudo modprobe bcm2708_dmaengine
sudo modprobe snd_soc_wm8804

# Read from config file.
. $CONFIGCFG

echo "[ INFO ] Checking wifi is ON?"
# Logic that will skip the wifi connection if wifi is disabled
if [ $WIFI = on ]; then 
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
			echo "connected"      
		else
			echo "Network connection down! Attempting reconnection two times before continuing."
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

# New section using Gregs functions, Remove all I2S stuff and load the correct modules

echo "[ INFO ] Loading I2S modules"

if [ $AUDIO = HDMI ]; then sudo $pCPHOME/enablehdmi.sh; else sudo $pCPHOME/disablehdmi.sh; fi

sleep 1
# Loads the correct output audio modules
pcp_read_chosen_audio

# Sleep for 1 sec otherwise aplay can not see the card
sleep 1
# Check for onboard sound card is card=0 and analog is chosen, so amixer is only used here
echo "[ INFO ] Doing ALSA configuration"
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

# Only call timezone function if timezone variable is set
if [ x"" != x"$TIMEZONE" ]; then
	echo "[ INFO ] Setting timezone"
	pcp_set_timezone
fi

# Start the essential stuff for piCorePlayer
echo "[ INFO ] Loading the main daemons"
echo -n "[ INFO ] "
/usr/local/etc/init.d/dropbear start
echo -n "[ INFO ] "
/usr/local/etc/init.d/httpd start
sleep 1
echo -n "[ INFO ] "
/usr/local/etc/init.d/squeezelite start

echo "[ INFO ] Doing auto start LMS"
#pcp_auto_start_lms

echo "[ INFO ] Doing auto start FAV"
#pcp_auto_start_fav

echo "[ INFO ] Doing user commands"
#pcp_user_commands

echo "[ INFO ] Start/restart crond"
/etc/init.d/services/crond start
