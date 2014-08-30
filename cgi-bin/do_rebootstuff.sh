#!/bin/sh

# Version: 0.04 2014-08-31 SBP
#	Minor formatting.

# Version: 0.03 2014-08-30 SBP
#	Clean up + added analog amixer use.
#	Improved the alsamixer use.

# Version: 0.02 2014-08-26 GE
#	Clean up.

# Version: 0.01 2014-06-25 SBP
#	Original.

set -x

# Read from pcp-functions file
. /home/tc/www/cgi-bin/pcp-functions
pcp_variables
. $CONFIGCFG

# Add eventual missing packages to onboot.lst. It is important if different versions of piCorePlayer have different needs.
# moved to do_update script, can be deleted if OK  
fgrep -vxf /mnt/mmcblk0p2/tce/onboot.lst /mnt/mmcblk0p2/tce/piCorePlayer.dep >> /mnt/mmcblk0p2/tce/onboot.lst

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

	# Save the parameters to the config file
	sudo sed -i "s/\(NAME=\).*/\1$NAME/" $CONFIGCFG
	sudo sed -i "s/\(OUTPUT=\).*/\1$OUTPUT/" $CONFIGCFG
	sudo sed -i "s/\(ALSA_PARAMS=\).*/\1$ALSA_PARAMS/" $CONFIGCFG
	sudo sed -i "s/\(BUFFER_SIZE=\).*/\1$BUFFER_SIZE/" $CONFIGCFG
	sudo sed -i "s/\(_CODEC=\).*/\1$_CODEC/" $CONFIGCFG
	sudo sed -i "s/\(PRIORITY=\).*/\1$PRIORITY/" $CONFIGCFG
	sudo sed -i "s/\(MAX_RATE=\).*/\1$MAX_RATE/" $CONFIGCFG
	sudo sed -i "s/\(UPSAMPLE=\).*/\1$UPSAMPLE/" $CONFIGCFG
	sudo sed -i "s/\(MAC_ADDRESS=\).*/\1$MAC_ADDRESS/" $CONFIGCFG
	sudo sed -i "s/\(SERVER_IP=\).*/\1$SERVER_IP/" $CONFIGCFG
	sudo sed -i "s/\(LOGLEVEL=\).*/\1$LOGLEVEL/" $CONFIGCFG
	sudo sed -i "s/\(LOGFILE=\).*/\1$LOGFILE/" $CONFIGCFG
	sudo sed -i "s/\(DSDOUT=\).*/\1$DSDOUT/" $CONFIGCFG
	sudo sed -i "s/\(VISULIZER=\).*/\1$VISULIZER/" $CONFIGCFG
	sudo sed -i "s/\(OTHER=\).*/\1$OTHER/" $CONFIGCFG
	sudo sed -i "s/\(AUDIO=\).*/\1$AUDIO/" $CONFIGCFG
	sudo sed -i "s/\(HOST=\).*/\1$HOST/" $CONFIGCFG
	sudo sed -i "s/\(SSID=\).*/\1$SSID/" $CONFIGCFG
	sudo sed -i "s/\(PASSWORD=\).*/\1$PASSWORD/" $CONFIGCFG
	sudo sed -i "s/\(ENCRYPTION=\).*/\1$ENCRYPTION/" $CONFIGCFG
	sudo sed -i "s/\(OVERCLOCK=\).*/\1$OVERCLOCK/" $CONFIGCFG
	sudo sed -i "s/\(CMD=\).*/\1$CMD/" $CONFIGCFG
	sudo sed -i "s/\(WIFI=\).*/\1$WIFI/" $CONFIGCFG
	sudo sed -i "s/\(FIQ=\).*/\1$FIQ/" $CONFIGCFG
	sudo sed -i "s/\(ALSAlevelout=\).*/\1$ALSAlevelout/" $CONFIGCFG
fi

# Rename the newconfig file on USB
if [ -f /mnt/sda1/newconfig.cfg ]; then sudo mv /mnt/sda1/newconfig.cfg /mnt/sda1/usedconfig.cfg; fi

# Check if a newconfig.cfg file is present on mmcblk0p1 - requested by SqueezePlug and CommandorROR and used for insitu update
sudo mount /dev/mmcblk0p1
if [ -f /mnt/mmcblk0p1/newconfig.cfg ]; then
	sudo dos2unix -u /mnt/mmcblk0p1/newconfig.cfg

	# Read variables from newconfig and save to config.
	. /mnt/mmcblk0p1/newconfig.cfg

	# Save the parameters to the config file
	sudo sed -i "s/\(NAME=\).*/\1$NAME/" $CONFIGCFG
	sudo sed -i "s/\(OUTPUT=\).*/\1$OUTPUT/" $CONFIGCFG
	sudo sed -i "s/\(ALSA_PARAMS=\).*/\1$ALSA_PARAMS/" $CONFIGCFG
	sudo sed -i "s/\(BUFFER_SIZE=\).*/\1$BUFFER_SIZE/" $CONFIGCFG
	sudo sed -i "s/\(_CODEC=\).*/\1$_CODEC/" $CONFIGCFG
	sudo sed -i "s/\(PRIORITY=\).*/\1$PRIORITY/" $CONFIGCFG
	sudo sed -i "s/\(MAX_RATE=\).*/\1$MAX_RATE/" $CONFIGCFG
	sudo sed -i "s/\(UPSAMPLE=\).*/\1$UPSAMPLE/" $CONFIGCFG
	sudo sed -i "s/\(MAC_ADDRESS=\).*/\1$MAC_ADDRESS/" $CONFIGCFG
	sudo sed -i "s/\(SERVER_IP=\).*/\1$SERVER_IP/" $CONFIGCFG
	sudo sed -i "s/\(LOGLEVEL=\).*/\1$LOGLEVEL/" $CONFIGCFG
	sudo sed -i "s/\(LOGFILE=\).*/\1$LOGFILE/" $CONFIGCFG
	sudo sed -i "s/\(DSDOUT=\).*/\1$DSDOUT/" $CONFIGCFG
	sudo sed -i "s/\(VISULIZER=\).*/\1$VISULIZER/" $CONFIGCFG
	sudo sed -i "s/\(OTHER=\).*/\1$OTHER/" $CONFIGCFG
	sudo sed -i "s/\(AUDIO=\).*/\1$AUDIO/" $CONFIGCFG
	sudo sed -i "s/\(HOST=\).*/\1$HOST/" $CONFIGCFG
	sudo sed -i "s/\(SSID=\).*/\1$SSID/" $CONFIGCFG
	sudo sed -i "s/\(PASSWORD=\).*/\1$PASSWORD/" $CONFIGCFG
	sudo sed -i "s/\(ENCRYPTION=\).*/\1$ENCRYPTION/" $CONFIGCFG
	sudo sed -i "s/\(OVERCLOCK=\).*/\1$OVERCLOCK/" $CONFIGCFG
	sudo sed -i "s/\(CMD=\).*/\1$CMD/" $CONFIGCFG
	sudo sed -i "s/\(WIFI=\).*/\1$WIFI/" $CONFIGCFG
	sudo sed -i "s/\(FIQ=\).*/\1$FIQ/" $CONFIGCFG
	sudo sed -i "s/\(ALSAlevelout=\).*/\1$ALSAlevelout/" $CONFIGCFG
fi

# Save changes caused by the presence of a newconfig.cfg file
if [ -f /mnt/mmcblk0p1/newconfig.cfg ]; then sudo filetool.sh -b; fi
# Delete the newconfig file
sudo rm -f /mnt/mmcblk0p1/newconfig.cfg
sleep 1
sudo umount /mnt/mmcblk0p1

#Section to save the parameters to the wifi.db - this is a new version in order to saving space and backslash in SSID which is needed in wifi.db
# so a name like "steens wifi" should be saved as  "steens\ wifi"
. /usr/local/sbin/config.cfg
#sudo chmod 766 /home/tc/wifi.db
#Only add backslash if not empty
if [ X"" = X"$SSID" ]; then break
else SSSID=`echo "$SSID" | sed 's/\ /\\\ /g'`
#Change SSSID back to SSID
SSID=$SSSID
sudo echo ${SSID}$'\t'${PASSWORD}$'\t'${ENCRYPTION}> /home/tc/wifi.db
sudo filetool.sh -b
fi

# We do have a problem with SSID's which don't have a name - should we use the next section for these SSIDs - I have not tested the code
# Saves SSID if empty
# if [ X"" = X"$SSID" ]; then sudo chmod 766 /home/tc/wifi.db; sudo echo ${SSID}$'\t'${PASSWORD}$'\t'${ENCRYPTION}> /home/tc/wifi.db; else fi
# NEW Section ends here

# Save changes caused by the presence of a newconfig.cfg file and wifi copy from config.cfg to wifi.db fie
# Is already save - I think - sudo filetool.sh -b

# Stuff previously handled by bootlocal.sh - but sits better here allowing for in situ update of as bootlocal then can be kept free from piCorePlayer stuff
# allowing any custom changes to bootlocal.sh to be maintained as it is not overwritten by in situ update.
 
sudo modprobe snd-bcm2835
#sudo modprobe -r snd_soc_wm8731
sudo modprobe snd_soc_bcm2708_i2s
sudo modprobe bcm2708_dmaengine
sudo modprobe snd_soc_wm8804

#Read from config file.
. $CONFIGCFG

# Logic that will skip the wifi connection if wifi is disabled
if [ $WIFI = on ]; then 
	sudo ifconfig wlan0 down
	sleep 1
	sudo ifconfig wlan0 up
	sleep 1
	sudo iwconfig wlan0 power off &>/dev/null
	sleep 1
	#usr/local/bin/wifi.sh -a 2>&1 > /tmp/wifi.log
	usr/local/bin/wifi.sh -a
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
if [ $AUDIO = HDMI ]; then sudo $pCPHOME/enablehdmi.sh; else sudo $pCPHOME/disablehdmi.sh; fi
if [ $AUDIO = Analog ]; then pcp_disable_i2s; else break; fi
if [ $AUDIO = USB ]; then pcp_disable_i2s; else break; fi
if [ $AUDIO = I2SDAC ]; then pcp_enable_i2s_dac; else break; fi
if [ $AUDIO = I2SDIG ]; then pcp_enable_i2s_digi; else break; fi
if [ $AUDIO = IQaudio ]; then pcp_enable_iqaudio_dac; else break; fi

# Check for onboard sound card is card=0, so amixer is only used here
aplay -l | grep 'card 0: ALSA' &> /dev/null
if [ $? = 0 ] && [ $AUDIO = Analog ]; then
	sudo amixer cset numid=3 1
	if [ $ALSAlevelout = Default ]; then
		sudo amixer set PCM 400 unmute
	fi
fi

# Check for onboard sound card is card=0, so HDMI amixer settings is only used here
aplay -l | grep 'card 0: ALSA' &> /dev/null
if [ $? = 0 ] && [ $AUDIO = HDMI ]; then
	sudo amixer cset numid=3 2
fi

# ALSA output level stuff
if [ $ALSAlevelout = Custom ]; then
	sudo alsactl restore
fi

# Start the essential stuff for piCorePlayer
/usr/local/etc/init.d/dropbear start
/usr/local/etc/init.d/httpd start
sleep 3
/usr/local/etc/init.d/squeezelite start
