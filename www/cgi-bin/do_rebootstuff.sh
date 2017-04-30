#!/bin/sh

# Version: 3.21 2017-04-30
#	Changed vfat mounts....again. PH.

# Version: 3.20 2017-04-22
#	Added crond message. GE
#	Updates for vfat mount permissions. PH
#	Changed rpi3 disable wifi to overlays on new config start. PH
#	Fixed boot Removal of old kernel modules. PH
#	Added setting SCREENROTATE to config.txt during newconfig process. PH
#	Reordered a few things that didn't need to be done before newconfig. PH
#  Added check for jivelite startup to avoid confusion on updateing to new image. PH
#	Turn HDMIPOWER to on during upgrades. PH

# Version: 3.10 2017-01-02
#	Added Samba Server Support. PH
#	Removed IQaudIO AMP unmute from here. SBP
#	Changes for shairport-sync. Incomplete. PH
#	Fixed newconfig.cfg process. PH
#	Set rpi3wifi blacklist in newconfig process. PH

# Version: 3.02 2016-09-19
#	Added pcp_reset_repository. GE.

# Version: 3.00 2016-08-12
#	Changed ssh server to Openssh. SBP
#	Changed RPi3 wifi firmware extension name. SBP
#	Added "No network found!" message. GE
#	Adjusted Mount point permissions for SCP. PH
#	Changed Kernel Module update to handle individual modules. PH
#	Updated LIRC section. GE

BACKUP=0
# Read from pcp-functions file
echo "${GREEN}Starting piCorePlayer setup...${NORMAL}"
echo -n "${BLUE}Loading pcp-functions...and pCP configuration file.${NORMAL}"
. /home/tc/www/cgi-bin/pcp-functions
. /home/tc/www/cgi-bin/pcp-soundcard-functions
echo "${GREEN}Done.${NORMAL}"

ORIG_AUDIO="$AUDIO"

#****************Upgrade Process Start *********************************
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
	echo "${YELLOW}  newconfig.cfg found on sda1.${NORMAL}"
	# Make a new config files with default values and read it
	pcp_update_config_to_defaults
	. $CONFIGCFG
	# Read variables from newconfig and save to config.
	sudo dos2unix -u $MNTUSB/newconfig.cfg
	. $MNTUSB/newconfig.cfg
	pcp_mount_mmcblk0p1_nohtml >/dev/null 2>&1
	sudo mv $MNTUSB/newconfig.cfg $MNTUSB/usedconfig.cfg
	pcp_timezone
	pcp_write_to_host
	[ "$RPI3INTWIFI" = "off" ] && echo "dtoverlay=pi3-disable-wifi" >> $CONFIGTXT 
	case "$SCREENROTATE" in
		0|no) sed -i "s/\(lcd_rotate=\).*/\10/" $CONFIGTXT;;
		180|yes) sed -i "s/\(lcd_rotate=\).*/\12/" $CONFIGTXT;;
	esac
	#During an newconfig update, turn HDMI back on. Incase there are problems.
	HDMIPOWER="on"
	# pcp_read_chosen_audio works from $CONFIGCFG, so lets write what we have so far.
	pcp_save_to_config
	pcp_disable_HDMI
	echo -n "${BLUE}Setting Soundcard from newconfig... ${NORMAL}"
	[ "$AUDIO" = "USB" ] && USBOUTPUT="$OUTPUT"
	pcp_read_chosen_audio noumount
	echo "${GREEN}Done.${NORMAL}"
	pcp_save_to_config
	pcp_backup_nohtml >/dev/null 2>&1
	echo "${RED}Rebooting needed to enable your settings... ${NORMAL}"
	sleep 3
	sudo reboot
	exit 0
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

	echo "${YELLOW}  newconfig.cfg found on mmcblk0p1.${NORMAL}"
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
	pcp_timezone
	pcp_write_to_host
	[ "$RPI3INTWIFI" = "off" ] && sed -i 's/$/ blacklist=brcmfmac/' $CMDLINETXT 
	case "$SCREENROTATE" in
		0|no) sed -i "s/\(lcd_rotate=\).*/\10/" $CONFIGTXT;;
		180|yes) sed -i "s/\(lcd_rotate=\).*/\12/" $CONFIGTXT;;
	esac
	#During an insitu update, turn HDMI back on. Incase there are problems.
	HDMIPOWER="on"
	#pcp_read_chosen_audio works from $CONFIGCFG, so lets write what we have so far.
	pcp_save_to_config
	pcp_disable_HDMI
	echo -n "${BLUE}Setting Soundcard from newconfig... ${NORMAL}"
	[ "$AUDIO" = "USB" ] && USBOUTPUT="$OUTPUT"
	pcp_read_chosen_audio noumount
	echo "${GREEN}Done.${NORMAL}"
	pcp_save_to_config
	sudo rm -f /mnt/mmcblk0p1/newconfig.cfg
	#cleanup all old kernel modules
	CURRENTKERNEL=$(uname -r)
	# Get list of kernel modules not matching current kernel.  And remove them
	CKCORE=$(uname -r | cut -d '-' -f2)
	CKCORE=${CKCORE%+}  #Strip the + or _v7+
	ls /mnt/mmcblk0p2/tce/optional/*${CKCORE%_v7}*.tcz* | grep -v $CURRENTKERNEL | xargs -r -I {} rm -f {}
	# Check onboot to be sure there are no hard kernel references.   
	sed -i 's|[-][0-9].[0-9].*|-KERNEL.tcz|' /mnt/mmcblk0p2/tce/onboot.lst
	# Remove Dropbear extension, we are now using openssh
	ls -1 /mnt/mmcblk0p2/tce/optional | grep dropbear | xargs -r -I {} rm -f {}
	sed -i '/dropbear/d' /opt/.filetool.lst
	sed -i '/dropbear/d' /mnt/mmcblk0p2/tce/onboot.lst
	#Remove lines containing only white space
	sed -i '/^\s*$/d' /mnt/mmcblk0p2/tce/onboot.lst
	# should we put a copy of bootlog in the home directory???????
	pcp_backup_nohtml >/dev/null 2>&1
	echo "${RED}Rebooting needed to enable your settings... ${NORMAL}"
	sleep 3
	sudo reboot
	exit 0
else
	echo -n "${YELLOW}  newconfig.cfg not found on mmcblk0p1.${NORMAL}"
fi
pcp_umount_mmcblk0p1_nohtml >/dev/null 2>&1
echo "${GREEN} Done.${NORMAL}"
#****************Upgrade Process End *********************************

# Set default respository incase it has been set to something non-standard.
echo -n "${BLUE}Setting piCore repository... ${NORMAL}"
pcp_reset_repository &
echo "${GREEN}Done.${NORMAL}"

echo -n "${BLUE}Generating drop-down list... ${NORMAL}"
pcp_sound_card_dropdown &
echo "${GREEN}Done.${NORMAL}"

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
		[ $? -eq 0 ] && echo "${YELLOW}  Broadcom USB firmware loaded.${NORMAL}" || echo "${RED}  Broadcom USB firmware load error.${NORMAL}"
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
	if [ $((CNT++)) -gt 40 ]; then
		echo "${RED} Failed ($CNT).${NORMAL}"
		break
	else
		echo -n "."
		sleep 0.5
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
		# Should we check for valid MAC address or should we asume this is covered in the applet/web interface??
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
	echo "${BLUE}Mounting USB Drives...${YELLOW}"
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
			vfat|fat32)
				#if Filesystem support installed, use utf-8 charset for fat.
				df | grep -qs ntfs
				[ "$?" = "0" ] && CHARSET=",iocharset=utf8" || CHARSET=""
				umount $DEVICE  # need to unmount vfat incase 1st mount is not utf8
				OPTIONS="-v -t vfat -o noauto,users,exec,umask=000,flush${CHARSET}"
			;;
			*)
				OPTIONS="-v"
			;;
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
	echo "${BLUE}Mounting Network Drive...${YELLOW}"
	mkdir -p /mnt/$NETMOUNT1POINT
	chown tc.staff /mnt/$NETMOUNT1POINT
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
		echo "${BLUE}Disk Mounted at /mnt/${NETMOUNT1POINT}."
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
	echo -n "${BLUE}Starting Shairport daemon... ${NORMAL}"
	/usr/local/etc/init.d/shairport-sync start >/dev/null 2>&1
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
			# Wait for server to be responsive.
			echo -n "${YELLOW}Waiting for LMS to initiate."
			# Check response from port 3483 for Player Connects.
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

if [ "$SAMBA" = "yes" ]; then
	echo "${BLUE}Starting Samba Server...${NORMAL}"
	[ -x /usr/local/etc/init.d/samba ] && /usr/local/etc/init.d/samba start
	echo "${GREEN}Done.${NORMAL}"
fi

echo -n "${BLUE}Starting httpd web server... ${NORMAL}"
/usr/local/etc/init.d/httpd start >/dev/null 2>&1
echo "${GREEN}Done.${NORMAL}"

if [ x"" != x"$USER_COMMAND_1" ] || [ x"" != x"$USER_COMMAND_2" ] || [ x"" != x"$USER_COMMAND_3" ]; then
	echo -n "${BLUE}Starting user commands... ${NORMAL}"
	pcp_user_commands
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
	if [ -x /opt/jivelite/bin/jivelite.sh ]; then
		echo "${GREEN}Done.${NORMAL}"
		sudo -E -b /opt/jivelite/bin/jivelite.sh >/dev/null 2>&1
	else
		echo "${RED}There is a problem with the Jivelite installation. Please remove and reinstall jivelite.${NORMAL}"
	fi
fi

echo "${BLUE}crond syncing time... ${NORMAL}"

unset ORIG_AUDIO
