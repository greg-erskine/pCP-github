#!/bin/sh

# Version: 3.22 2017-07-23
#	Added pcp_create_rotdash. GE.

# Version: 3.21 2017-07-11
#	Changed vfat mounts....again. PH.
#	Set boot/tce device from /etc/sysconfig/tcedir link
#	Support multiple USB mounts. PH.
#	Support multiple Network mounts. PH.
#	Updated insitu_update process. Copy of log saved to tcedir/pcp_insitu_upgrade.log. PH.
#	Added cardnumber detection for use with aslaequal. PH.

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
# Mount USB stick if present.  Build list of usb stick 1st partitions
# Check each partition for newconfig.cfg.  The first one found stops the search
NEWCONFIGFOUND=0
NEWCFGLIST=$(blkid -o device | grep -E 'sd[a-z]1|mmcblk0p1' | awk -F '/dev/' '{print $2}')
for DISK in $NEWCFGLIST; do
	echo "${BLUE}Checking for newconfig.cfg on $DISK... ${NORMAL}"
	# Check if $DISK is mounted, otherwise mount it.
	if mount | grep ${DISK}; then
		eval ${DISK}WASMNT=1
	else
		eval ${DISK}WASMNT=0
		[ -d /mnt/$DISK ] || mkdir -p /mnt/$DISK
		echo "${YELLOW}  Trying to mount /dev/${DISK}.${RED}"
		mount /dev/$DISK >/dev/null 2>&1
	fi
	if [ -f /mnt/$DISK/newconfig.cfg ]; then
		echo "${YELLOW}  newconfig.cfg found on ${DISK}.${NORMAL}"
		NEWCONFIGFOUND=1
		ln -s /mnt/$DISK /tmp/newconfig
	else
		echo "${YELLOW}  newconfig.cfg not found on ${DISK}.${NORMAL}"
		if [ $(eval echo \${${DISK}WASMNT}) -eq 0 ]; then
			umount /mnt/$DISK
		fi
	fi
	[ $NEWCONFIGFOUND -eq 1 ] && break
done

#========================================================================================
# Replace default rotdash
#----------------------------------------------------------------------------------------
if [ "$ROTDASH" = "yes" ]; then
	echo -n "${BLUE}[ INFO ] Replacing existing rotdash.${NORMAL}"
	pcp_create_rotdash &
	echo "${GREEN}Done.${NORMAL}"
fi

# Check if newconfig.cfg was found in search
if [ $NEWCONFIGFOUND -eq 1 ]; then
	echo "${BLUE}[ INFO ] Processing saved Configuration file from ${DISK}...${NORMAL}"
	# Check for bootfix script which will fix specific issues after insitu update - if present execute and then delete
	if [ -f $TCEMNT/tce/bootfix/bootfix.sh ]; then
		echo -n "${BLUE}[ INFO ] Fixing any issues after insitu update.${NORMAL}"
		$TCEMNT/tce/bootfix/bootfix.sh
		rm -rf $TCEMNT/tce/bootfix
		pcp_backup_nohtml >/dev/null 2>&1
		echo "${GREEN}Done.${NORMAL}"
	fi
	#=========================================================================================
	# Copy ALSA settings back so they are restored after an update
	#-----------------------------------------------------------------------------------------
	if [ -f /tmp/newconfig/asound.conf ]; then
		echo -n "${BLUE}[ INFO ] Restoring asound.conf...${NORMAL}"
		sudo cp /tmp/newconfig/asound.conf /etc/ 
		sudo mv -f /tmp/newconfig/asound.conf /tmp/newconfig/usedasound.conf
		echo "${GREEN}Done.${NORMAL}"
	fi
	if [ -f /tmp/newconfig/asound.state ]; then
		echo -n "${BLUE}[ INFO ] Restoring custom alsa asound.state...${NORMAL}"
		sudo cp /tmp/newconfig/asound.state /var/lib/alsa/
		sudo mv -f /tmp/newconfig/asound.state /tmp/newconfig/usedasound.state
		echo "${GREEN}Done.${NORMAL}"
	fi
	#-----------------------------------------------------------------------------------------
	# Make a new config files with default values and read it
	pcp_update_config_to_defaults
	. $CONFIGCFG
	# Read variables from newconfig and save to config.
	sudo dos2unix -u /tmp/newconfig/newconfig.cfg
	. /tmp/newconfig/newconfig.cfg
	pcp_mount_bootpart_nohtml >/dev/null 2>&1
	sudo mv -f /tmp/newconfig/newconfig.cfg /tmp/newconfig/usedconfig.cfg
	pcp_timezone
	pcp_write_to_host
	######## This section deals with adding dtoverlays back to config.txt based
		# Disable RPI3 or ZeroW internal wifi
		if [ "$RPI3INTWIFI" = "off" ]; then
			echo -n "${BLUE}[ INFO ] Disabling rpi internal wifi...${NORMAL}"
			echo "dtoverlay=pi3-disable-wifi" >> $CONFIGTXT
			echo "${GREEN}Done.${NORMAL}"
		fi
		# Set Screen Rotate
		echo -n "${BLUE}[ INFO ] Setting Screen Rotation...${NORMAL}"
		case "$SCREENROTATE" in
			0|no) sed -i "s/\(lcd_rotate=\).*/\10/" $CONFIGTXT;;
			180|yes) sed -i "s/\(lcd_rotate=\).*/\12/" $CONFIGTXT;;
		esac
		echo "${GREEN}Done.${NORMAL}"
		# Setup LIRC overlay
		if [ "$IR_LIRC" = "yes" ]; then
			echo -n "${BLUE}[ INFO ] Adding lirc-rpi overlay to config.txt... ${NORMAL}"
			sed -i '/dtoverlay=lirc-rpi/d' $CONFIGTXT
			if [ "$IR_GPIO_OUT" = "" ]; then
				sudo echo "dtoverlay=lirc-rpi,gpio_in_pin=$IR_GPIO_IN" >> $CONFIGTXT
			else
				sudo echo "dtoverlay=lirc-rpi,gpio_in_pin=$IR_GPIO_IN,gpio_out_pin=$IR_GPIO_OUT" >> $CONFIGTXT
			fi
			echo "${GREEN}Done.${NORMAL}"
		fi
	######## CONFIG.TXT Section End
	#During an newconfig update, turn HDMI back on. Incase there are problems.
	HDMIPOWER="on"
	# If MOUNTUUID and MOUNTPOINT Exist in newconfig, then create a usbdrives.conf
	if [ "$MOUNTUUID" != "no" -a "$MOUNTPOINT" != "" ]; then
		echo -n "${BLUE}[ INFO ] Upgrading USB mount configuration files.${NORMAL}"
		echo "[newconfig]" >> $USBMOUNTCONF
		echo "USBDISK=enabled" >> $USBMOUNTCONF
		echo "MOUNTPOINT=${MOUNTPOINT}" >> $USBMOUNTCONF
		echo "MOUNTUUID=${MOUNTUUID}" >> $USBMOUNTCONF
		echo "${GREEN}Done.${NORMAL}"
	fi
	if [ "$NETMOUNT1" != "no" -a "$NETMOUNT1POINT" != "" ]; then
		echo -n "${BLUE}[ INFO ] Upgrading Network mount configuration files.${NORMAL}"
		echo "[newconfig]" >> $NETMOUNTCONF
		echo "NETENABLE=yes" >> $NETMOUNTCONF
		echo "NETMOUNTPOINT=${NETMOUNT1POINT}" >> $NETMOUNTCONF
		echo "NETMOUNTIP=${NETMOUNT1IP}" >> $NETMOUNTCONF
		echo "NETMOUNTSHARE=${NETMOUNT1SHARE}" >> $NETMOUNTCONF
		echo "NETMOUNTFSTYPE=${NETMOUNT1FSTYPE}" >> $NETMOUNTCONF
		echo "NETMOUNTUSER=${NETMOUNT1USER}" >> $NETMOUNTCONF
		echo "NETMOUNTPASS=${NETMOUNT1PASS}" >> $NETMOUNTCONF
		echo "NETMOUNTOPTIONS=${NETMOUNT1OPTIONS}" >> $NETMOUNTCONF
		echo "${GREEN}Done.${NORMAL}"
	fi
	# pcp_read_chosen_audio works from $CONFIGCFG, so lets write what we have so far.
	pcp_save_to_config
	pcp_disable_HDMI
	echo -n "${BLUE}[ INFO ] Setting Soundcard from newconfig... ${NORMAL}"
	[ "$AUDIO" = "USB" ] && USBOUTPUT="$OUTPUT"
	pcp_read_chosen_audio noumount
	pcp_save_to_config
	echo "${GREEN}Done.${NORMAL}"

	#cleanup all old kernel modules
	CURRENTKERNEL=$(uname -r)
	# Get list of kernel modules not matching current kernel.  And remove them
	ls $TCEMNT/tce/optional/*.tcz* | grep -E '(pcpCore)|(pcpAudioCore)' | grep -v $CURRENTKERNEL | xargs -r -I {} rm -f {}
	# Check onboot to be sure there are no hard kernel references.   
	sed -i 's|[-][0-9].[0-9].*|-KERNEL.tcz|' $ONBOOTLST
	#Remove lines containing only white space
	sed -i '/^\s*$/d' $ONBOOTLST

	pcp_backup_nohtml >/dev/null 2>&1
	echo -n "${BLUE}[ INFO ] Saving a copy of the upgrade log to ${YELLOW}${TCEMNT}/pcp_insitu_upgrade.log ${BLUE}... ${NORMAL}"
	cp -f /var/log/pcp_boot.log ${TCEMNT}/tce/pcp_insitu_upgrade.log
	echo "${GREEN}Done.${NORMAL}"
	echo "${RED}Rebooting needed to enable your settings... ${NORMAL}"
	sleep 3
	sudo reboot
	exit 0
fi
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
	if grep -Fxq "wifi.tcz" $ONBOOTLST; then
		echo "${GREEN}Wifi firmware already loaded.${NORMAL}"
	else
		# Add wifi related modules back
		echo "${GREEN}Loading wifi firmware and modules.${NORMAL}"
		BACKUP=1
		sudo fgrep -vxf $ONBOOTLST $TCEMNT/tce/piCorePlayer.dep >> $ONBOOTLST

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

if [ "$OUTPUT" = "equal" ]; then
	echo -n "${BLUE}Checking proper card number for Alsaequal... ${NORMAL}"
	pcp_find_card_number
	sed -i "s/plughw:.*,0/plughw:"$CARDNO",0/g" /etc/asound.conf
	echo "${GREEN}Done.${NORMAL}"
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

echo -n "${BLUE}Starting Openssh server... ${NORMAL}"
/usr/local/etc/init.d/openssh start >/dev/null 2>&1
echo "${GREEN}Done.${NORMAL}"

# Mount USB Disk Selected on LMS Page
LMSMOUNTFAIL="0"
#	READ Conf file
if [ -f  ${USBMOUNTCONF} ]; then
	echo "${BLUE}Mounting USB Drives...${YELLOW}"
	SC=0
	while read LINE; do
		case $LINE in
			[*)SC=$((SC+1));;
			*USBDISK*) eval USBDISK${SC}=$(pcp_trimval "${LINE}");;
			*POINT*) eval MOUNTPOINT${SC}=$(pcp_trimval "${LINE}");;
			*UUID*) eval MOUNTUUID${SC}=$(pcp_trimval "${LINE}");;
			*);;
		esac
	done < $USBMOUNTCONF
	I=0
	while [ $I -le $SC ]; do
		ENABLED=$(eval echo "\${USBDISK${I}}")
		if [ "$ENABLED" != "" ]; then
			POINT=$(eval echo "\${MOUNTPOINT${I}}")
			UUID=$(eval echo "\${MOUNTUUID${I}}")
			blkid | grep -q $UUID
			if [ $? -eq 0 ]; then
				mkdir -p /mnt/$POINT
				chown tc.staff /mnt/$POINT
				DEVICE=$(blkid -U $UUID)
				FSTYPE=$(blkid -U $UUID | xargs -I {} blkid {} -s TYPE | awk -F"TYPE=" '{print $NF}' | tr -d "\"")
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
				echo "${BLUE}Mounting USB Drive: $UUID...${YELLOW}"
				mount $OPTIONS --uuid $UUID /mnt/$POINT
				if [ $? -eq 0 ]; then
					echo "${BLUE}Disk Mounted at /mnt/$POINT.${NORMAL}"
				else
					echo "${RED}Disk Mount Error.${NORMAL}"
					LMSMOUNTFAIL="1"
				fi
			else
				 echo "${RED}Disk ${UUID} Not Found, Please insert drive and Reboot${NORMAL}"
				 LMSMOUNTFAIL="1"
			fi
		fi
		I=$((I+1))
	done
	echo "${GREEN}Done.${NORMAL}"
fi

# Mount Network Disk Selected on LMS Page
if [ -f  ${NETMOUNTCONF} ]; then
	echo "${BLUE}Mounting Network Drive...${YELLOW}"
	NUMNET=0
	while read LINE; do
		case $LINE in
			[*) NUMNET=$((NUMNET+1));;
			*NETENABLE*) eval NETENABLE${NUMNET}=$(pcp_trimval "${LINE}");;
			*MOUNTPOINT*) eval NETMOUNTPOINT${NUMNET}=$(pcp_trimval "${LINE}");;
			*MOUNTIP*) eval NETMOUNTIP${NUMNET}=$(pcp_trimval "${LINE}");;
			*MOUNTSHARE*) eval NETMOUNTSHARE${NUMNET}=$(pcp_trimval "${LINE}");;
			*FSTYPE*) eval NETMOUNTFSTYPE${NUMNET}=$(pcp_trimval "${LINE}");;
			*PASS*) eval NETMOUNTPASS${NUMNET}=$(pcp_trimval "${LINE}");;
			*USER*) eval NETMOUNTUSER${NUMNET}=$(pcp_trimval "${LINE}");;
			*MOUNTOPTIONS*) eval NETMOUNTOPTIONS${NUMNET}=$(echo "${LINE}" | awk -F= '{ st = index($0,"=");print substr($0,st+1)}');;
			*);;
		esac
	done < $NETMOUNTCONF
	I=1
	while [ $I -le $NUMNET ]; do
		if [ $(eval echo "\${NETENABLE${I}}") = "yes" ]; then
			PNT=$(eval echo \${NETMOUNTPOINT${I}})
			IP=$(eval echo \${NETMOUNTIP${I}})
			SHARE=$(eval echo \${NETMOUNTSHARE${I}})
			FSTYPE=$(eval echo \${NETMOUNTFSTYPE${I}})
			USER=$(eval echo \${NETMOUNTUSER${I}})
			PASS=$(eval echo \${NETMOUNTPASS${I}})
			OPTIONS=$(eval echo \${NETMOUNTOPTIONS${I}})
			mkdir -p /mnt/$PNT
			chown tc.staff /mnt/$PNT
			case "$FSTYPE" in
				cifs)
					OPTS=""
					[ "$USER" != "" ] && OPTS="${OPTS}username=${USER},"
					[ "$PASS" != "" ] && OPTS="${OPTS}password=${PASS},"
					OPTS="${OPTS}${OPTIONS}"
					MNTCMD="-v -t $FSTYPE -o $OPTS //$IP/$SHARE /mnt/$PNT"
				;;
				nfs)
					OPTS="addr=${IP},nolock,${OPTIONS}"
					MNTCMD="-v -t $FSTYPE -o $OPTS $IP:$SHARE /mnt/$PNT"
				;;
			esac
			RETRIES=3  #Retry network mounts, incase of power failure, and all devices restarting.
			while [ $RETRIES -gt 0 ]; do
				mount $MNTCMD
				if [ $? -eq 0 ]; then
					RETRIES=0
					echo "${BLUE}Disk Mounted at /mnt/${PNT}."
				else
					RETRIES=$((RETRIES-1))
					if [ $RETRIES -eq 0 ]; then
						echo "${RED}Disabling network mount from server at ${IP}${NORMAL}"
						cp -f $NETMOUNTCONF /tmp/netconf
						cat /tmp/netconf | awk '/^\[/ {m++}{if(m=='$I')sub("NETENABLE\=yes","NETENABLE\=no")}1' > $NETMOUNTCONF
						LMSMOUNTFAIL="1"
					else
						echo "${RED}Disk Mount Error, Retrying $RETRIES more times......sleeping 10 seconds${YELLOW}"
						sleep 10
					fi
				fi
			done
		fi
		I=$((I+1))
	done
	echo "${GREEN}Done.${NORMAL}"
fi

# If running an LMS Server Locally, start squeezelite later
if [ "$LMSERVER" != "yes" ]; then
	if [ "$SQUEEZELITE" = "yes" ]; then
		echo -n "${BLUE}Starting Squeezelite... ${NORMAL}"
		/usr/local/etc/init.d/squeezelite start >/dev/null 2>&1
		echo "${GREEN}Done.${NORMAL}"
	fi
fi

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
	pcp_mount_bootpart_nohtml >/dev/null 2>&1
	pcp_set_timezone >/dev/null 2>&1
	pcp_umount_bootpart_nohtml >/dev/null 2>&1
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
