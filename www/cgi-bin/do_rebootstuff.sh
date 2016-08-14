#!/bin/sh

# Version: 3.00 2016-08-12
#	Changed ssh server to Openssh. SBP.
#	Changed RPi3 wifi firmware extension name. SBP.
#	Added "No network found!" message. GE.
#	Adjusted Mount point permissions for SCP. PH.
#	Changed Kernel Module update to handle individual modules. PH.
#	Updated LIRC section. GE.

# Version: 2.06 2016-06-04 GE
#	Changed order so httpd is started after LMS and added check for LMS running before starting Squeezelite
#	Added HDMIPOWER.
#	Moved bootfix script so it only starts after an insitu update.
#	Changed script so backup is only initiated when somthing needs saving
#	Fixed JIVELITE, SCREENROTATE variables (YES/NO).
#	Changed location of Bootfix
#	Activated Kernel Module Updates during insitu update.
#	Updated Mount lines

# Version: 2.05 2016-04-30 PH
#	Added firmware-brcmfmac43430.tcz
#	Added Mount for LMS Server Drive
#	Modified IQaudIO amp control
#	Changed if LMS Server is Enabled, Start before Squeezelite
#	Added Network Share Mount
#	Added download of kernel modules during insitu upgrade. Currently inactive for 2.05
#   Added bootfix routine to correct certain update issues during first boot.

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

BACKUP=0
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
	# Make a new config files with default values and read it
	pcp_update_config_to_defaults
	. $CONFIGCFG
	# Read variables from newconfig and save to config.
	sudo dos2unix -u $MNTUSB/newconfig.cfg
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

	# Check for bootfix script which will fix specific issues after insitu update - if present execute and then delete
	if [ -f /mnt/mmcblk0p2/tce/bootfix/bootfix.sh ]; then
		echo "${GREEN}Fixing issues after insitu update.${NORMAL}"
		/mnt/mmcblk0p2/tce/bootfix/bootfix.sh
		rm -rf /mnt/mmcblk0p2/tce/bootfix
		pcp_backup_nohtml >/dev/null 2>&1
	fi

	echo -n "${YELLOW}  newconfig.cfg found on mmcblk0p1.${NORMAL}"
	# Make a new config files with default values and read it
	pcp_update_config_to_defaults
	. $CONFIGCFG
	# Read variables from newconfig, set timezone, do audio stuff save to config and backup.
	sudo dos2unix -u /mnt/mmcblk0p1/newconfig.cfg
	. /mnt/mmcblk0p1/newconfig.cfg

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
	sudo rm -f /mnt/mmcblk0p1/newconfig.cfg
	#cleanup all old kernel modules
	CURRENTKERNEL=$(uname -r)
	# Get list of kernel modules not matching current kernel.  And remove them
	ls /mnt/mmcblk0p2/tce/optional/*piCore*.tcz* | grep -v $CURRENTKERNEL | xargs -I {} rm -f {}
	# Check onboot to be sure there are no hard kernel references.   
	sed -i 's|[-][0-9].[0-9].*|-KERNEL.tcz|' /mnt/mmcblk0p2/tce/onboot.lst
	# Remove Dropbear extension, we are now using openssh
	rm -f /mnt/mmcblk0p2/tce/optional/dropbear.tcz*
	# should we put a copy of bootlog in the home directory???????
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
if [ "$WIFI" = "on" ]; then
	if grep -Fxq "wifi.tcz" /mnt/mmcblk0p2/tce/onboot.lst; then
		echo "${GREEN}Wifi firmware already loaded.${NORMAL}"
	else
		# Add wifi related modules back
		echo "${GREEN}Loading wifi firmware and modules.${NORMAL}"
		BACKUP=1
		sudo fgrep -vxf /mnt/mmcblk0p2/tce/onboot.lst /mnt/mmcblk0p2/tce/piCorePlayer.dep >> /mnt/mmcblk0p2/tce/onboot.lst

		sudo -u tc tce-load -i firmware-atheros.tcz >/dev/null 2>&1
		[ $? -eq 0 ] && echo "${YELLOW}  Atheros firmware loaded.${NORMAL}" || echo "${RED}  Atheros firmware load error.${NORMAL}"
		sudo -u tc tce-load -i firmware-brcmwifi.tcz >/dev/null 2>&1
		[ $? -eq 0 ] && echo "${YELLOW}  Broadcom firmware loaded.${NORMAL}" || echo "${RED}  Broadcom firmware load error.${NORMAL}"
		sudo -u tc tce-load -i firmware-ralinkwifi.tcz >/dev/null 2>&1
		[ $? -eq 0 ] && echo "${YELLOW}  Ralink firmware loaded.${NORMAL}" || echo "${RED}  Ralink firmware load error.${NORMAL}"
		sudo -u tc tce-load -i firmware-rtlwifi.tcz >/dev/null 2>&1
		[ $? -eq 0 ] && echo "${YELLOW}  Realtek firmware loaded.${NORMAL}" || echo "${RED}  Realtek firmware load error.${NORMAL}"
		sudo -u tc tce-load -i firmware-rpi3-wireless.tcz >/dev/null 2>&1
		[ $? -eq 0 ] && echo "${YELLOW}  RPi3B Broadcom firmware loaded.${NORMAL}" || echo "${RED}  RPi3B Broadcom firmware load error.${NORMAL}"
		sudo -u tc tce-load -i wifi.tcz >/dev/null 2>&1
		[ $? -eq 0 ] && echo "${YELLOW}  Wifi modules loaded.${NORMAL}" || echo "${RED}  Wifi modules load error.${NORMAL}"
		echo "${GREEN} Done.${NORMAL}"
	fi
fi

if [ "$WIFI" = "on" ]; then
	# Save the parameters to the wifi.db
	echo -n "${BLUE}Reading config.cfg... ${NORMAL}"
	. /usr/local/sbin/config.cfg
	echo "${GREEN}Done.${NORMAL}"

	# Check if wifi variables already are up-to-date in wifi.db so we don't need to update wifi.db and do an unwanted backup
	if [ x"" = x"$SSID" ]; then
		break
	else
		SSSID=`echo "$SSID" | sed 's/\ /\\\ /g'`
		# Change SSSID back to SSID
		SSID=$SSSID
		sudo echo ${SSID}$'\t'${PASSWORD}$'\t'${ENCRYPTION}> /tmp/wifi.db
	fi
	if cmp -s /home/tc/wifi.db /tmp/wifi.db; then
		echo -n "${BLUE}Wifi.db is up-to-date... ${NORMAL}"
	else
		BACKUP=1
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
	fi
	echo "${GREEN}Done.${NORMAL}"
fi

# Loading configuration file config.cfg
echo -n "${BLUE}Loading configuration file... ${NORMAL}"
. $CONFIGCFG
echo "${GREEN}Done.${NORMAL}"

# Connect wifi if WIFI is on
echo -n "${BLUE}Checking wifi... ${NORMAL}"
if [ "$WIFI" = "on" ]; then
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
if [ "$ALSAlevelout" = "Custom" ]; then
	alsactl restore
fi

# Check for onboard sound card is card=0 and analog is chosen, so amixer is only used here
aplay -l | grep 'card 0: ALSA'  >/dev/null 2>&1
if [ $? -eq 0 ] && [ "$AUDIO" = "Analog" ]; then
	# Set the analog output via audio jack
	sudo amixer cset numid=3 1 >/dev/null 2>&1
	if [ "$ALSAlevelout" = "Default" ]; then
		sudo amixer set PCM 400 unmute >/dev/null 2>&1
	fi
fi

# Check for onboard sound card is card=0, and HDMI is chosen so HDMI amixer settings is enabled
aplay -l | grep 'card 0: ALSA'  >/dev/null 2>&1
if [ $? -eq 0 ] && [ "$AUDIO" = "HDMI" ]; then
	if [ "$ALSAlevelout" = "Default" ]; then
		sudo amixer set PCM 400 unmute >/dev/null 2>&1
	fi
	# Set the analog output via HDMI out
	sudo amixer cset numid=3 2 >/dev/null 2>&1
fi
echo "${GREEN}Done.${NORMAL}"

# Unmute IQaudIO amplifier via GPIO pin 22
# Only do this if not controlling amp via squeezelite.
if [ "$AUDIO" = "I2SpIQAMP" ]; then
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
	if [ $((CNT++)) -gt 40 ]; then
		echo -n "${RED} No network found! ${NORMAL}"
		break
	else
		echo -n "."
		sleep 0.5
	fi
done
echo "${GREEN} Done ($CNT).${NORMAL}"

#==============================================================================
# WOL="yes"|"no"
# WOL_NIC="eth0"|"wlan0"|"wlan1"|... does wlan1 exist if e.g. user adds WiFi dongle on RPi3 with onboard WiFi enabled?
# WOL_LMSMACADDRESS="11:22:33:44:55:66"
# Only send LMS WOL command if LMS is not run locally
if [ "$LMSERVER" != "yes" ]; then
	if [ "$WOL" = "yes" ] && [ "$WOL_NIC" != "" ] && [ "$WOL_LMSMACADDRESS" != "" ]; then
		#Should we check for valid MAC address or should we asume this is covered in the applet/web interface??
		echo -n "${BLUE}Sending WOL magic packet ($WOL_LMSMACADDRESS)...${NORMAL}"
		sudo ether-wake -i $WOL_NIC $WOL_LMSMACADDRESS
		echo "${GREEN}Done.${NORMAL}"
		# sleep 10
	fi
fi
#==============================================================================

if [ "$IR_LIRC" = "yes" ]; then
	if [ "$JIVELITE" = "yes" ]; then
		echo -n "${BLUE}Starting lirc with Jivelite support... ${NORMAL}"
		/usr/local/sbin/lircd --device=/dev/${IR_DEVICE} --log=/var/log/pcp_lirc.log --uinput
	else
		echo -n "${BLUE}Starting lirc... ${NORMAL}"
		/usr/local/sbin/lircd --device=/dev/${IR_DEVICE} --log=/var/log/pcp_lirc.log
	fi
	echo "${GREEN}Done.${NORMAL}"
fi

# Mount USB Disk Selected on LMS Page
LMSMOUNTFAIL="0"
if [ "$MOUNTUUID" != "no" ]; then
	blkid | grep -q $MOUNTUUID
	if [ $? -eq 0 ]; then
		mkdir -p /mnt/$MOUNTPOINT
		chown tc.staff /mnt/$MOUNTPOINT
		DEVICE=$(blkid -U $MOUNTUUID)
		FSTYPE=$(blkid -U $MOUNTUUID | xargs -I {} blkid {} -s TYPE | awk -F"TYPE=" '{print $NF}' | tr -d "\"")
		case "$FSTYPE" in
			ntfs)
				umount $DEVICE  #ntfs cannot be dual mounted
				OPTIONS="-v -t ntfs-3g -o permissions"
				;;
			*) OPTIONS="-v";;
		esac
		mount $OPTIONS --uuid $MOUNTUUID /mnt/$MOUNTPOINT
		if [ $? -eq 0 ]; then
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
	chown tc.staff /mnt/$NETMOUNT1POINT
	echo -n "${BLUE}"
	case "$NETMOUNT1FSTYPE" in
		cifs)
			OPTIONS=""
			[ "$NETMOUNT1USER" != "" ] && OPTIONS="${OPTIONS}username=${NETMOUNT1USER},"
			[ "$NETMOUNT1PASS" != "" ] && OPTIONS="${OPTIONS}password=${NETMOUNT1PASS},"
			OPTIONS="${OPTIONS}${NETMOUNT1OPTIONS}"
			MNTCMD="-v -t $NETMOUNT1FSTYPE -o $OPTIONS //$NETMOUNT1IP/$NETMOUNT1SHARE /mnt/$NETMOUNT1POINT"
		;;
		nfs)
			OPTIONS="addr=${NETMOUNT1IP},nolock,${NETMOUNT1OPTIONS}"
			MNTCMD="-v -t $NETMOUNT1FSTYPE -o $OPTIONS $NETMOUNT1IP:$NETMOUNT1SHARE /mnt/$NETMOUNT1POINT"
		;;
	esac
	mount $MNTCMD
	if [ $? -eq 0 ]; then
		echo "${NORMAL}"
	else
		echo "${RED}Disk Mount Error.${NORMAL}"
		LMSMOUNTFAIL="1"
	fi
fi

# If running an LMS Server Locally, start squeezelite later
if [ "$LMSERVER" != "yes" ]; then
	if [ "$SQUEEZELITE" = "yes" ]; then
		echo -n "${BLUE}Starting Squeezelite... ${NORMAL}"
		/usr/local/etc/init.d/squeezelite start >/dev/null 2>&1
		echo "${GREEN}Done.${NORMAL}"
	fi
fi

echo -n "${BLUE}Starting Openssh server... ${NORMAL}"
/usr/local/etc/init.d/openssh start >/dev/null 2>&1
echo "${GREEN}Done.${NORMAL}"


if [ "$SHAIRPORT" = "yes" ]; then
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

if [ "$A_S_LMS" = "Enabled" ]; then
	echo -n "${BLUE}Starting auto start LMS... ${NORMAL}"
	pcp_auto_start_lms
	echo "${GREEN}Done.${NORMAL}"
fi

if [ "$A_S_FAV" = "Enabled" ]; then
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
	BACKUP=1
	echo "${GREEN}Done.${NORMAL}"
fi

if [ "$LMSERVER" = "yes" ]; then
	if [ "$LMSDATA" = "default" -o "$LMSMOUNTFAIL" = "0" ]; then
		echo -n "${BLUE}Starting LMS, this can take some time... ${NORMAL}"
		sudo /usr/local/etc/init.d/slimserver start
		echo "${GREEN}Done.${NORMAL}"
		if [ "$SQUEEZELITE" = "yes" ]; then
			#Wait for server to be responsive.
			echo -n "${YELLOW}Waiting for LMS to initiate."
			#Check response from port 3483 for Player Connects.
			CNT=1
			TEST=""
			while [ "$TEST" != "E" ];
			do
				TEST=$(echo "e" | nc -w 1 -u 127.0.0.1 3483)
				if [ $((CNT++)) -gt 20 ]; then
					echo "${RED} LMS not running ($CNT).${NORMAL}"
					break
				else
					echo -n "."
					[ "$TEST" != "E" ] && sleep 1
				fi
			done
			echo "${GREEN} Done ($CNT).${NORMAL}"

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

echo -n "${BLUE}Starting httpd web server... ${NORMAL}"
/usr/local/etc/init.d/httpd start >/dev/null 2>&1
echo "${GREEN}Done.${NORMAL}"

# Save the parameters to the config file
if [ $BACKUP -eq 1 ]; then
	echo -n "${BLUE}Saving the changes... ${NORMAL}"
	pcp_backup_nohtml >/dev/null 2>&1
	echo "${GREEN}Done.${NORMAL}"
fi

# Display the IP address
ifconfig eth0 2>&1 | grep inet >/dev/null 2>&1 && echo "${BLUE}eth0 IP: $(pcp_eth0_ip)${NORMAL}"
ifconfig wlan0 2>&1 | grep inet >/dev/null 2>&1 && echo "${BLUE}wlan0 IP: $(pcp_wlan0_ip)${NORMAL}"

echo "${GREEN}Finished piCorePlayer setup.${NORMAL}"

if [ "$JIVELITE" = "yes" ]; then
	echo -n "${BLUE}Starting Jivelite... ${NORMAL}"
	eventno=$( cat /proc/bus/input/devices | awk '/FT5406 memory based driver/{for(a=0;a>=0;a++){getline;{if(/mouse/==1){ print $NF;exit 0;}}}}')
	if [ x"" != x"$eventno" ];then
		export JIVE_NOCURSOR=1
		export TSLIB_TSDEVICE=/dev/input/$eventno
		export SDL_MOUSEDRV=TSLIB
		export SDL_MOUSEDEV=$TSLIB_TSDEVICE
	fi
	export HOME=/home/tc
	echo "${GREEN}Done.${NORMAL}"
	sudo -E -b /opt/jivelite/bin/jivelite.sh >/dev/null 2>&1
fi
