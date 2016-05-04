#!/bin/sh

# Version: 2.06 2016-05-03 GE
#	Added HDMIPOWER.

# Version: 2.06 2016-04-23 SBP
#	Added download of kernel modules during insitu upgrade.

# Version: 0.27 2016-04-14 PH
#	Added firmware-brcmfmac43430.tcz
#	Added Mount for LMS Server Drive
#	Modified IQaudIO amp control
#	Changed if LMS Server is Enabled, Start before Squeezelite
#	Added Network Share Mount

# Version: 0.26 2016-02-26 GE
#	Added firmware-brcmwifi.tcz.
#	Added IR startup.
#	Changed squeezelite startup code.

# Version: 0.25 2016-02-02 SBP
#	Reordered custom alsactl restore.
#	Added LMS startup.

# Version: 0.24 2016-01-06 SBP
#	Added dbus, avahi and shairport-sync startup routines.

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
if [ PCP_SOURCE == "tcz" ]; then
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

# Check for bootfix script which will fix specific issues after insitu update - if present execute and then delete
if [ -f /mnt/mmcblk0p2/tce/bootfix/bootfix.sh ]; then
	echo "${GREEN}Fixing issues after insitu update.${NORMAL}"
	/mnt/mmcblk0p2/tce/bootfix/bootfix.sh
	rm -rf /mnt/mmcblk0p2/tce/bootfix
fi

# Mount USB stick if present
echo "${BLUE}Checking for newconfig.cfg on sda1... ${NORMAL}"

# Check if sda1 is mounted, otherwise mount it.
MNTUSB=/mnt/sda1
if mount | grep $MNTUSB; then
	echo "${YELLOW}  /dev/sda1 already mounted.${NORMAL}"
else
	# Check if sda1 is inserted before trying to mount it.
	if [ -e /dev/sda1 ]; then
		[ -d /mnt/sda1 ] || mkdir -p /mnt/sda1
		echo "${YELLOW}  Trying to mount /dev/sda1.${RED}"
		sudo mount /dev/sda1 >/dev/null 2>&1
	else
	echo "${YELLOW}  No USB Device detected in /dev/sda1${NORMAL}"
	fi
fi

# Check if newconfig.cfg is present
if [ -f $MNTUSB/newconfig.cfg ]; then
	echo -n "${YELLOW}  newconfig.cfg found on sda1.${NORMAL}"
	pcp_update_config_to_defaults
	sudo dos2unix -u $MNTUSB/newconfig.cfg
	# Read variables from newconfig and save to config.
	. $MNTUSB/newconfig.cfg
	pcp_mount_mmcblk0p1_nohtml >/dev/null 2>&1
	sudo mv $MNTUSB/newconfig.cfg $MNTUSB/usedconfig.cfg
	pcp_save_to_config
	pcp_disable_HDMI
	echo -n "${BLUE}Loading I2S modules... ${NORMAL}"
	pcp_read_chosen_audio
	echo "${GREEN}Done.${NORMAL}"
	pcp_timezone
	pcp_write_to_host
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
	pcp_update_config_to_defaults

	# Read variables from newconfig, set timezone, do audio stuff save to config and backup.
	sudo dos2unix -u /mnt/mmcblk0p1/newconfig.cfg	
	. /mnt/mmcblk0p1/newconfig.cfg
	pcp_save_to_config
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
	sudo rm -f /mnt/mmcblk0p1/newconfig.cfg
#-------New section that handle removal and update of kernel packages after pCP insitu update----
#	CURRENTKERNEL=$(uname -r)
#	ls /mnt/mmcblk0p2/tce/optional/*piCore* | grep -q $CURRENTKERNEL   # Assume if one is present, then all should be good
#	if [ "$?" = "0" ]; then
#		echo "${BLUE}Kernel modules found matching current kernel version $(CURRENTKERNEL)${NORMAL}"
#	else
#		for EXT in `ls /mnt/mmcblk0p2/tce/optional/*piCore* | sed -e 's|[-][0-9].[0-9].*||' | sort -u`; do
#			sudo -u tc pcp-load -r ${PCP_REPO} -w ${EXT}-KERNEL
#			if [ "$?" != "0" ]; then
#				echo "${RED}[ ERROR ] Error downloading ${EXT}${NORMAL}"
#				###Not sure what to do yet.
#			fi
#		done
#		#delete the old files, just print out for testing
#		ls /mnt/mmcblk0p2/tce/optional/*piCore* | grep -v $CURRENTKERNEL | xargs -I {} echo "Test....deleting {}"   
#		#ls /mnt/mmcblk0p2/tce/optional/*piCore* | grep -v $CURRENTKERNEL | xargs -I {} rm -f {}
#		
#		# Also need a check just to be sure onboot.lst doesn't have hard kernel references.
#	fi
#
#------End of insitu update section-------------------------------------------------------
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

		sudo -u tc tce-load -i firmware-atheros.tcz >/dev/null 2>&1
		[ $? = 0 ] && echo "${YELLOW}  Atheros firmware loaded.${NORMAL}" || echo "${RED}  Atheros firmware load error.${NORMAL}"
		sudo -u tc tce-load -i firmware-brcmwifi.tcz >/dev/null 2>&1
		[ $? = 0 ] && echo "${YELLOW}  Broadcom firmware loaded.${NORMAL}" || echo "${RED}  Broadcom firmware load error.${NORMAL}"
		sudo -u tc tce-load -i firmware-ralinkwifi.tcz >/dev/null 2>&1
		[ $? = 0 ] && echo "${YELLOW}  Ralink firmware loaded.${NORMAL}" || echo "${RED}  Ralink firmware load error.${NORMAL}"
		sudo -u tc tce-load -i firmware-rtlwifi.tcz >/dev/null 2>&1
		[ $? = 0 ] && echo "${YELLOW}  Realtek firmware loaded.${NORMAL}" || echo "${RED}  Realtek firmware load error.${NORMAL}"
		sudo -u tc tce-load -i firmware-brcmfmac43430.tcz >/dev/null 2>&1
		[ $? = 0 ] && echo "${YELLOW}  rpi3 Broadcom firmware loaded.${NORMAL}" || echo "${RED}  rpi3 Broadcom firmware load error.${NORMAL}"
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

# If Custom ALSA settings are used, then restore the settings
echo -n "${BLUE}Starting ALSA configuration... ${NORMAL}"
if [ $ALSAlevelout = Custom ]; then
	alsactl restore
fi

# Check for onboard sound card is card=0 and analog is chosen, so amixer is only used here
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
	if [ $ALSAlevelout = Default ]; then
		sudo amixer set PCM 400 unmute >/dev/null 2>&1
	fi
	# Set the analog output via HDMI out
	sudo amixer cset numid=3 2 >/dev/null 2>&1
fi
echo "${GREEN}Done.${NORMAL}"

# Unmute IQaudIO amplifier via GPIO pin 22
# Only do this if not controlling amp via squeezelite.
if [ $AUDIO = I2SpIQAMP ]; then
	if [ "$POWER_GPIO" = "" ]; then
		echo -n "${BLUE}Unmute IQaudIO AMP... ${NORMAL}"
		sudo sh -c "echo 22 > /sys/class/gpio/export"
		sudo sh -c "echo out >/sys/class/gpio/gpio22/direction"
		sudo sh -c "echo 1 >/sys/class/gpio/gpio22/value"
		echo "${GREEN}Done.${NORMAL}"
	fi
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

if [ $IR_LIRC = "yes" ]; then
	echo -n "${BLUE}Starting lirc... ${NORMAL}"
	/usr/local/sbin/lircd --device=/dev/lirc0
#	/usr/local/sbin/lircd --device=/dev/lirc0 --uinput
	echo "${GREEN}Done.${NORMAL}"
fi

# Mount USB Disk Selected on LMS Page
LMSMOUNTFAIL="0"
if [ "$MOUNTUUID" != "no" ]; then
	blkid | grep -q $MOUNTUUID
	if [ "$?" = "0" ]; then 
		mkdir -p /mnt/$MOUNTPOINT
		mount --uuid $MOUNTUUID /mnt/$MOUNTPOINT
		if [ "$?" = "0" ]; then
			echo "${BLUE}Disk Mounted at /mnt/$MOUNTPOINT.${NORMAL}"
		else
			echo "${RED}Disk Mount Error.${NORMAL}"
			LMSMOUNTFAIL="1"
		fi
	else
		 echo "${RED}Disk ${MOUNTUUID} Not Found, Please insert drive and Reboot${NORMAL}"
		 LMSMOUNTFAIL="1"
	fi
fi

# Mount Network Disk Selected on LMS Page
if [ "$NETMOUNT1" = "yes" ]; then
	mkdir -p /mnt/$NETMOUNT1POINT
	echo -n "${BLUE}"
	mount -v -t $NETMOUNT1FSTYPE -o username=$NETMOUNT1USER,password=$NETMOUNT1PASS,$NETMOUNT1OPTIONS //$NETMOUNT1IP/$NETMOUNT1SHARE /mnt/$NETMOUNT1POINT
	if [ "$?" = "0" ]; then
		echo "${NORMAL}"
	else
		echo "${RED}Disk Mount Error.${NORMAL}"
		LMSMOUNTFAIL="1"
	fi
fi

# If running an LMS Server Locally, start squeezelite later
if [ $LMSERVER != "yes" ]; then   
	if [ $SQUEEZELITE = "yes" ]; then
		echo -n "${BLUE}Starting Squeezelite... ${NORMAL}"
		/usr/local/etc/init.d/squeezelite start >/dev/null 2>&1
		echo "${GREEN}Done.${NORMAL}"
	fi
fi

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

if [ $SHAIRPORT = "yes" ]; then
	echo -n "${BLUE}Starting dbus daemon... ${NORMAL}"
	/usr/local/etc/init.d/dbus start >/dev/null 2>&1
	echo "${GREEN}Done.${NORMAL}"

	echo -n "${BLUE}Starting avahi daemon... ${NORMAL}"
	/usr/local/etc/init.d/avahi start >/dev/null 2>&1
	echo "${GREEN}Done.${NORMAL}"

	echo -n "${BLUE}Starting Shairport daemon... ${NORMAL}"
	/usr/local/etc/init.d/shairport-sync start >/dev/null 2>&1
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

if [ $LMSERVER = "yes" ]; then
	if [ "$LMSDATA" = "default" -o "$LMSMOUNTFAIL" = "0" ]; then
		echo -n "${BLUE}Starting LMS, this can take some time... ${NORMAL}"
		sudo /usr/local/etc/init.d/slimserver start
		echo "${GREEN}Done.${NORMAL}"
		if [ $SQUEEZELITE = "yes" ]; then
			sleep 5    ###Wait for server to be responsive.   Need to fix this with a port check.
			echo -n "${BLUE}Starting Squeezelite... ${NORMAL}"
			/usr/local/etc/init.d/squeezelite start >/dev/null 2>&1
			echo "${GREEN}Done.${NORMAL}"
		fi
	else
		echo "${RED}LMS data disk failed mount, LMS and squeezelite will not start.${NORMAL}"
	fi
fi

# Turn HDMI power off to save ~20ma
if [ "$HDMIPOWER" = "off" ]; then
	echo -n "${BLUE}Powering off HDMI... ${NORMAL}"
	if which tvservice >/dev/null 2>&1; then
		tvservice -o >/dev/null 2>&1
		echo "${GREEN}Done.${NORMAL}"
	else
		echo "${RED}FAIL.${NORMAL}"
	fi
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
	echo "${GREEN}Done.${NORMAL}"
	sudo -E -b /opt/jivelite/bin/jivelite.sh  
fi
