#!/bin/sh

# Version: 0.23 2015-10-27 SBP
#	Added touchscreeen controls for Jivelite.

# Version: 0.22 2015-09-24 SBP
#	Updated newconfig.cfg routines.
#	Updated Waiting for soundcards to populate routine.
#	Added ln -s /usr/local/bin/scp /usr/bin/scp.

# Version: 0.21 2015-08-23 SBP
#	Enabling DT loading of audio cards.
#	Changed /usr/local/sbin/dropbearmulti to /usr/local/bin/dropbearmulti.

# Version: 0.20 2015-07-09 SBP
#	Revised method of loading wifi firmware.

# Version: 0.19 2015-07-04 GE
#	Added dropbear fix to allow scp to work between piCorePlayers.

# Version: 0.18 2015-06-25 SBP
#	Added script that automatically set correct timezone.

# Version: 0.17 2015-06-04 GE
#	Renamed $pCPHOME to $PCPHOME.
#	Minor updates.

# Version: 0.16 2015-05-21 SBP
#	Use saved custom ALSA settings after pCP updating.

# Version: 0.16 2015-05-10 GE
#	Added wait for network before starting squeezelite.

# Version: 0.15 2015-05-06 SBP
#	Added logic to skip not needed options.

# Version: 0.14 2015-04-05 SBP
#	Added logic to wait for soundcards and restart squeezelite if not properly started.

# Version: 0.13 2015-03-24 SBP
#	Added section to load wifi for wifi only based systems (like RPi-A+).
#	Revised program startup order.

# Version: 0.12 2015-02-15 SBP
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

. /home/tc/www/cgi-bin/pcp-functions

# Read from pcp-functions file
echo "${GREEN}Starting piCorePlayer setup...${NORMAL}"
echo -n "${BLUE}Loading pcp-functions... ${NORMAL}"
pcp_variables
echo "${GREEN}Done.${NORMAL}"

# Read from config file.
echo -n "${BLUE}Loading configuration file... ${NORMAL}"
. $CONFIGCFG
echo "${GREEN}Done.${NORMAL}"

# Remove all traces of pCP if pCP.tcz is deleted
# for now we need to check if pCP is installed via pCP.tcz or via the old piCorePlayer
# in the future this check is not needed

# Check for pCP installed via pCP.tcz and pCP.tcz not present any more
if [ PCP_SOURCE = tcz ]; then 
	if [ ! -f /mnt/mmcblk0p2/tce/optional/pCP.tcz ]; then
			echo "${YELLOW} Removing all traces of piCorePlayer... ${NORMAL}"
			sudo sed -i "/do_rebootstuff.sh/d" /opt/bootlocal.sh
			sudo sed -i "/usr\/local\/sbin\/config.cfg/d" /opt/.filetool.lst
#			sudo filetool.sh -b						# should be enabled later but not while testing
			echo "${GREEN} Done. will reboot in 5 sec. ${NORMAL}"
			wait 5
#			sudo reboot								# should be enabled later but not while testing
		else
			break
	fi
else
	break
fi

# Mount USB stick if present
echo "${BLUE}Checking for newconfig.cfg on sda1... ${NORMAL}"

# Check if sda1 is mounted, otherwise mount it
MNTUSB=/mnt/sda1
if mount | grep $MNTUSB; then
	echo "${YELLOW}  sda1 mounted.${NORMAL}"
else
	# FIX: check if sda1 is inserted before trying to mount it.
	echo "${YELLOW}  Trying to mount sda1.${RED}"
	sudo mount /dev/sda1 >/dev/null 2>&1
fi

# Check if newconfig.cfg is present
if [ -f $MNTUSB/newconfig.cfg ]; then
	echo -n "${YELLOW}  newconfig.cfg found on sda1.${NORMAL}"
	sudo dos2unix -u $MNTUSB/newconfig.cfg
	# Read variables from newconfig and save to config.
	. $MNTUSB/newconfig.cfg
	pcp_mount_mmcblk0p1_nohtml >/dev/null 2>&1
	sudo mv $MNTUSB/newconfig.cfg $MNTUSB/usedconfig.cfg
	pcp_disable_HDMI
	echo -n "${BLUE}Loading I2S modules... ${NORMAL}"
	pcp_read_chosen_audio
	echo "${GREEN}Done.${NORMAL}"
	pcp_timezone
	pcp_write_to_host
	pcp_save_to_config
	pcp_backup_nohtml >/dev/null 2>&1
	echo "${RED}Rebooting needed to enable your settings... ${NORMAL}"
	sleep 3
	sudo reboot
else
	echo -n "${YELLOW}  newconfig.cfg not found on sda1.${NORMAL}"
fi
echo "${GREEN} Done.${NORMAL}"

# Check if a newconfig.cfg file is present on mmcblk0p1 - requested by SqueezePlug and CommandorROR and used for insitu update
echo "${BLUE}Checking for newconfig.cfg on mmcblk0p1... ${NORMAL}"
pcp_mount_mmcblk0p1_nohtml >/dev/null 2>&1
if [ -f /mnt/mmcblk0p1/newconfig.cfg ]; then
	echo -n "${YELLOW}  newconfig.cfg found on mmcblk0p1.${NORMAL}"
	sudo dos2unix -u /mnt/mmcblk0p1/newconfig.cfg

	# Read variables from newconfig, set timezone, do audio stuff save to config and backup.
	. /mnt/mmcblk0p1/newconfig.cfg
	sudo rm -f /mnt/mmcblk0p1/newconfig.cfg
	#=========================================================================================
	# Copy ALSA settings back so they are restored after an update
	#-----------------------------------------------------------------------------------------
	sudo cp /mnt/mmcblk0p1/asound.conf /etc/ >/dev/null 2>&1
	sudo rm -f /mnt/mmcblk0p1/asound.conf >/dev/null 2>&1
	sudo cp /mnt/mmcblk0p1/asound.state /var/lib/alsa/ >/dev/null 2>&1
	sudo rm /mnt/mmcblk0p1/asound.state >/dev/null 2>&1
	#-----------------------------------------------------------------------------------------
	pcp_disable_HDMI
	echo -n "${BLUE}Loading I2S modules... ${NORMAL}"
	pcp_read_chosen_audio
	echo "${GREEN}Done.${NORMAL}"
	pcp_timezone
	pcp_write_to_host
	pcp_save_to_config
	pcp_backup_nohtml >/dev/null 2>&1
	echo "${RED}Rebooting needed to enable your settings... ${NORMAL}"
	sleep 3
	sudo reboot
else
	echo -n "${YELLOW}  newconfig.cfg not found on mmcblk0p1.${NORMAL}"
fi
pcp_umount_mmcblk0p1_nohtml >/dev/null 2>&1
echo "${GREEN} Done.${NORMAL}"

# If using a RPi-A+ card or wifi manually set to on - we need to load the wireless firmware if not already loaded
if [ $WIFI = "on" ]; then
	if grep -Fxq "wifi.tcz" /mnt/mmcblk0p2/tce/onboot.lst; then
		echo "${GREEN}Wifi firmware already loaded.${NORMAL}"
	else
		# Add wifi related modules back
		echo "${GREEN}Loading wifi firmware and modules.${NORMAL}"
		sudo fgrep -vxf /mnt/mmcblk0p2/tce/onboot.lst /mnt/mmcblk0p2/tce/piCorePlayer.dep >> /mnt/mmcblk0p2/tce/onboot.lst
		sudo -u tc tce-load -i firmware-ralinkwifi.tcz >/dev/null 2>&1
		[ $? = 0 ] && echo "${YELLOW}  Ralink firmware loaded.${NORMAL}" || echo "${RED}  Ralink firmware load error.${NORMAL}"
		sudo -u tc tce-load -i firmware-rtlwifi.tcz >/dev/null 2>&1
		[ $? = 0 ] && echo "${YELLOW}  Realtek firmware loaded.${NORMAL}" || echo "${RED}  Realtek firmware load error.${NORMAL}"
		sudo -u tc tce-load -i firmware-atheros.tcz >/dev/null 2>&1
		[ $? = 0 ] && echo "${YELLOW}  Atheros firmware loaded.${NORMAL}" || echo "${RED}  Atheros firmware load error.${NORMAL}"
		sudo -u tc tce-load -i wifi.tcz >/dev/null 2>&1
		[ $? = 0 ] && echo "${YELLOW}  Wifi modules loaded.${NORMAL}" || echo "${RED}  Wifi modules load error.${NORMAL}"
		echo "${GREEN} Done.${NORMAL}"
	fi
fi

if [ $WIFI = "on" ]; then
	# Save the parameters to the wifi.db
	echo -n "${BLUE}Reading config.cfg... ${NORMAL}"
	. /usr/local/sbin/config.cfg
	echo "${GREEN}Done.${NORMAL}"

	# Only add backslash if not empty
	echo -n "${BLUE}Updating wifi.db... ${NORMAL}"
	if [ x"" = x"$SSID" ]; then
		break
	else
		SSSID=`echo "$SSID" | sed 's/\ /\\\ /g'`
		# Change SSSID back to SSID
		SSID=$SSSID
		sudo echo ${SSID}$'\t'${PASSWORD}$'\t'${ENCRYPTION}> /home/tc/wifi.db
	fi
	echo "${GREEN}Done.${NORMAL}"
fi

# Loading configuration file config.cfg
echo -n "${BLUE}Loading configuration file... ${NORMAL}"
. $CONFIGCFG
echo "${GREEN}Done.${NORMAL}"

# Connect wifi if WIFI is on
echo -n "${BLUE}Checking wifi... ${NORMAL}"
if [ $WIFI = on ]; then
	echo "${YELLOW}  wifi is on.${NORMAL}"
	sleep 1
	sudo ifconfig wlan0 down
	sudo ifconfig wlan0 up
	sudo iwconfig wlan0 power off >/dev/null 2>&1
	sudo /usr/local/bin/wifi.sh -a

	# Try to reconnect to wifi if failed - will try two times before continuing booting
	for i in 1 2; do
		if ifconfig wlan0 | grep -q "inet addr:"; then
			echo "${YELLOW}  wifi is connected ($i).${NORMAL}"
		else
			echo "${RED}  Network connection down! Attempting reconnection two times before continuing.${NORMAL}"
			sudo ifconfig wlan0 down
			sleep 1
			sudo ifconfig wlan0 up
			sleep 1
			sudo iwconfig wlan0 power off >/dev/null 2>&1
			sleep 1
			sudo /usr/local/bin/wifi.sh -a
			sleep 5
	   fi
	done
fi
echo "${GREEN}Done.${NORMAL}"

echo -n "${BLUE}Loading pcp-lms-functions... ${NORMAL}"
. /home/tc/www/cgi-bin/pcp-lms-functions
echo "${GREEN}Done.${NORMAL}"

echo -n "${YELLOW}Waiting for soundcards to populate."
CNT=1
until aplay -l | grep -q PLAYBACK 2>&1
do
	if [ $((CNT++)) -gt 20 ]; then
	echo "${RED} Failed ($CNT).${NORMAL}"
		break
	else
		echo -n "."
		sleep 1
	fi
done
echo "${GREEN} Done ($CNT).${NORMAL}"

# Check for onboard sound card is card=0 and analog is chosen, so amixer is only used here
echo -n "${BLUE}Starting ALSA configuration... ${NORMAL}"
aplay -l | grep 'card 0: ALSA'  >/dev/null 2>&1
if [ $? == 0 ] && [ $AUDIO = Analog ]; then
	# Set the analog output via audio jack
	sudo amixer cset numid=3 1 >/dev/null 2>&1
	if [ $ALSAlevelout = Default ]; then
		sudo amixer set PCM 400 unmute >/dev/null 2>&1
	fi
fi

# Check for onboard sound card is card=0, and HDMI is chosen so HDMI amixer settings is enabled
aplay -l | grep 'card 0: ALSA'  >/dev/null 2>&1
if [ $? == 0 ] && [ $AUDIO = HDMI ]; then
	# Set the analog output via HDMI out
	sudo amixer cset numid=3 2 >/dev/null 2>&1
	if [ $ALSAlevelout = Default ]; then
		sudo amixer set PCM 400 unmute >/dev/null 2>&1
	fi
fi

# If Custom ALSA settings are used, then restore the settings
if [ $ALSAlevelout = Custom ]; then
	alsactl restore
fi
echo "${GREEN}Done.${NORMAL}"

# Unmute IQaudIO amplifier via GPIO pin 22
if [ $AUDIO = I2SpIQAMP ]; then
echo -n "${BLUE}Unmute IQaudIO AMP... ${NORMAL}"
	sudo sh -c "echo 22 > /sys/class/gpio/export"
	sudo sh -c "echo out >/sys/class/gpio/gpio22/direction"
	sudo sh -c "echo 1 >/sys/class/gpio/gpio22/value"
echo "${GREEN}Done.${NORMAL}"
fi

# Start the essential stuff for piCorePlayer
echo -n "${YELLOW}Waiting for network."
CNT=1
until ifconfig | grep -q Bcast
do
	if [ $((CNT++)) -gt 20 ]; then
		break
	else
		echo -n "."
		sleep 1
	fi
done
echo "${GREEN} Done ($CNT).${NORMAL}"

echo -n "${BLUE}Starting Squeezelite... ${NORMAL}"
/usr/local/etc/init.d/squeezelite start >/dev/null 2>&1
echo "${GREEN}Done.${NORMAL}"

echo -n "${BLUE}Starting Dropbear SSH server... ${NORMAL}"
/usr/local/etc/init.d/dropbear start >/dev/null 2>&1
echo "${GREEN}Done.${NORMAL}"

# Dropbear fix to allow scp to work
if [ ! -e /usr/bin/dbclient ]; then
	echo -n "${BLUE}Fixing Dropbear symbolic links... ${NORMAL}"
	ln -s /usr/local/bin/dropbearmulti /usr/bin/dbclient
	ln -s /usr/local/bin/scp /usr/bin/scp
	echo "${GREEN}Done.${NORMAL}"
fi

echo -n "${BLUE}Starting httpd web server... ${NORMAL}"
/usr/local/etc/init.d/httpd start >/dev/null 2>&1
echo "${GREEN}Done.${NORMAL}"

if [ $A_S_LMS = "Enabled" ]; then
	echo -n "${BLUE}Starting auto start LMS... ${NORMAL}"
	pcp_auto_start_lms
	echo "${GREEN}Done.${NORMAL}"
fi

if [ $A_S_FAV = "Enabled" ]; then
	echo -n "${BLUE}Starting auto start FAV... ${NORMAL}"
	pcp_auto_start_fav
	echo "${GREEN}Done.${NORMAL}"
fi

if [ x"" != x"$USER_COMMAND_1" ] || [ x"" != x"$USER_COMMAND_2" ] || [ x"" != x"$USER_COMMAND_3" ]; then
	echo -n "${BLUE}Starting user commands... ${NORMAL}"
	pcp_user_commands
	echo "${GREEN}Done.${NORMAL}"
fi

# Automatically set the timezone
if [ x"" = x"$TIMEZONE" ] && [ $(pcp_internet_accessible) = 0 ]; then
	echo "${BLUE}Auto set timezone settings, can be updated on tweaks page... ${NORMAL}"
	# Fetch timezone from Ubuntu's geoip server
	TZ1=`wget -O - -q http://geoip.ubuntu.com/lookup | sed -n -e 's/.*<TimeZone>\(.*\)<\/TimeZone>.*/\1/p'`
	# Translate country/city to timezone string
	TIMEZONE=`wget -O - -q http://svn.fonosfera.org/fon-ng/trunk/luci/modules/admin-fon/root/etc/timezones.db | grep $TZ1 | sed "s@$TZ1 @@"`
	echo "${YELLOW}Timezone settings for $TZ1 are used.${NORMAL}"
	pcp_save_to_config
	pcp_mount_mmcblk0p1_nohtml >/dev/null 2>&1
	pcp_set_timezone >/dev/null 2>&1
	pcp_umount_mmcblk0p1_nohtml >/dev/null 2>&1
	TZ=$TIMEZONE
	echo "${GREEN}Done.${NORMAL}"
fi

# Save the parameters to the config file
echo -n "${BLUE}Updating configuration... ${NORMAL}"
pcp_backup_nohtml >/dev/null 2>&1
echo "${GREEN}Done.${NORMAL}"

# Display the IP address
ifconfig eth0 2>&1 | grep inet >/dev/null 2>&1 && echo "${BLUE}eth0 IP: $(pcp_eth0_ip)${NORMAL}"
ifconfig wlan0 2>&1 | grep inet >/dev/null 2>&1 && echo "${BLUE}wlan0 IP: $(pcp_wlan0_ip)${NORMAL}"

echo "${GREEN}Finished piCorePlayer setup.${NORMAL}"


if [ $JIVELITE = "YES" ]; then
     echo -n "${BLUE}Starting Jivelite... ${NORMAL}"
     eventno=$( cat /proc/bus/input/devices | awk '/FT5406 memory based driver/{for(a=0;a>=0;a++){getline;{if(/mouse/==1){ print $NF;exit 0;}}}}')
    if [ x"" != x$eventno ];then
        export JIVE_NOCURSOR=1
        export TSLIB_TSDEVICE=/dev/input/$eventno
        export SDL_MOUSEDRV=TSLIB
        export SDL_MOUSEDEV=$TSLIB_TSDEVICE
    fi
                                     
    export HOME=/home/tc
    sudo -E -b /opt/jivelite/bin/jivelite.sh
    echo "${GREEN}Done.${NORMAL}"
fi
