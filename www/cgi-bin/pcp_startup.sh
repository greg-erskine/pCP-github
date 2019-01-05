#!/bin/sh

# Version: 4.2.0 2019-01-05

BACKUP=0
# Read from pcp-functions file
echo "${GREEN}Starting piCorePlayer setup...${NORMAL}"
echo -n "${BLUE}Loading pCP function files and pCP configuration file...${NORMAL}"
. /home/tc/www/cgi-bin/pcp-functions
. /home/tc/www/cgi-bin/pcp-soundcard-functions
. /home/tc/www/cgi-bin/pcp-wifi-functions
# Create link to old cfg location, as a bunch of extensions will break....need to update extensions.
ln -s $PCPCFG /usr/local/sbin/config.cfg
echo "${GREEN}Done.${NORMAL}"

ORIG_AUDIO="$AUDIO"

#****************************************************************************************
#*********************************Upgrade Process Start *********************************
# Mount USB stick if present.  Build list of usb stick 1st partitions.
# Check each partition for pcp.cfg.  The first one found stops the search.
#****************************************************************************************
NEWCONFIGFOUND=0
WPACONFIGFOUND=0
SSH=0
NEWCFGLIST=$(blkid -o device | grep -E 'sd[a-z]1|mmcblk0p1' | awk -F '/dev/' '{print $2}')
for DISK in $NEWCFGLIST; do
	echo "${BLUE}Checking for boot codes on $DISK...${NORMAL}"
	# Check if $DISK is mounted, otherwise mount it.
	if mount | grep ${DISK}; then
		eval ${DISK}WASMNT=1
	else
		eval ${DISK}WASMNT=0
		[ -d /mnt/$DISK ] || mkdir -p /mnt/$DISK
		echo "${YELLOW}  Trying to mount /dev/${DISK}.${RED}"
		mount /dev/$DISK >/dev/null 2>&1
	fi
	#------------------------------------------------------------------------------------
	# Look for ssh file on boot partition. Only start sshd if file found.
	#------------------------------------------------------------------------------------
	echo -n "${BLUE}Checking for ssh...${YELLOW}"
	[ -f /mnt/${DISK}/ssh ] && SSH=1
	[ $SSH -eq 1 ] && echo "found, ssh will start."
	#------------------------------------------------------------------------------------
	# Look for netusb on boot partition, and load net-usb-KERNEL.tcz
	#------------------------------------------------------------------------------------
	echo -n "${BLUE}Checking for netusb...${YELLOW}"
	if [ -f /mnt/${DISK}/netusb -o  -f /mnt/${DISK}/netusb.txt ]; then
		tce-status -i | grep -q "net-usb"
		if [ $? -eq 1 ]; then
			echo "Loading net-usb kernel modules.${NORMAL}"
			echo "net-usb-KERNEL.tcz" >> $ONBOOTLST
			sudo -u tc tce-load -i net-usb-KERNEL.tcz
			/etc/init.d/dhcp.sh &
		else
			echo "net-usb modules already loaded."
		fi
	fi
	#------------------------------------------------------------------------------------
	# Look for wpa_supplicant.conf on boot partition.
	#------------------------------------------------------------------------------------
	if [ -f /mnt/${DISK}/wpa_supplicant.conf ]; then
		echo "${YELLOW}  wpa_supplicant.conf found on ${DISK}.${NORMAL}"
		WPACONFIGFOUND=1
		[ -f $WPASUPPLICANTCONF ] && mv $WPASUPPLICANTCONF ${WPASUPPLICANTCONF}~
		cp /mnt/${DISK}/wpa_supplicant.conf $WPASUPPLICANTCONF
		chmod u=rw,g=,o= $WPASUPPLICANTCONF
		[ $? -eq 0 ] && mv /mnt/${DISK}/wpa_supplicant.conf /mnt/${DISK}/used_wpa_supplicant.conf
	fi
	#------------------------------------------------------------------------------------
	# Look for newpcp.cfg on boot partition.......normally part of insitu_upgrade
	#------------------------------------------------------------------------------------
	if [ -f /mnt/${DISK}/newpcp.cfg ]; then
		echo "${YELLOW}  newpcp.cfg found on ${DISK}.${NORMAL}"
		NEWCONFIGFOUND=1
		ln -s /mnt/$DISK /tmp/newconfig
	else
		echo "${YELLOW}  newpcp.cfg not found on ${DISK}.${NORMAL}"
		if [ $(eval echo \${${DISK}WASMNT}) -eq 0 ]; then
			umount /mnt/$DISK
		fi
	fi
	[ $NEWCONFIGFOUND -eq 1 ] && break
done

# Check if newpcp.cfg was found in search
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
		echo -n "${BLUE}[ INFO ] Restoring ALSA asound.conf...${NORMAL}"
		sudo cp /tmp/newconfig/asound.conf /etc/
		sudo mv -f /tmp/newconfig/asound.conf /tmp/newconfig/usedasound.conf
		echo "${GREEN}Done.${NORMAL}"
	fi
	if [ -f /tmp/newconfig/asound.state ]; then
		echo -n "${BLUE}[ INFO ] Restoring custom ALSA asound.state...${NORMAL}"
		sudo cp /tmp/newconfig/asound.state /var/lib/alsa/
		sudo mv -f /tmp/newconfig/asound.state /tmp/newconfig/usedasound.state
		echo "${GREEN}Done.${NORMAL}"
	fi
	#-----------------------------------------------------------------------------------------
	# Make a new config files with default values and read it
	pcp_update_config_to_defaults
	. $PCPCFG
	# Read variables from newpcp and save to config.
	sudo dos2unix -u /tmp/newconfig/newpcp.cfg
	. /tmp/newconfig/newpcp.cfg
	pcp_mount_bootpart_nohtml >/dev/null 2>&1
	sudo mv -f /tmp/newconfig/newpcp.cfg /tmp/newconfig/usedpcp.cfg
	pcp_timezone
	pcp_write_to_host
	######## This section deals with adding dtoverlays back to config.txt based
		# Disable RPI3 or ZeroW internal wifi on by default from upgrade
		if [ "$RPI3INTWIFI" = "off" ]; then
			echo -n "${BLUE}[ INFO ] Disabling rpi internal wifi...${NORMAL}"
			echo "dtoverlay=pi3-disable-wifi" >> $CONFIGTXT
			echo "${GREEN}Done.${NORMAL}"
		fi
		# Enable RPI3 or ZeroW internal bluetooth off by default from upgrade
		if [ "$RPIBLUETOOTH" = "on" ]; then
			echo -n "${BLUE}[ INFO ] Enabling rpi internal bluetooth...${NORMAL}"
			sed -i '/dtoverlay=pi3-disable-bt/d' $CONFIGTXT
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
			echo -n "${BLUE}[ INFO ] Adding gpio-ir overlay to config.txt...${NORMAL}"
			#lirc-rpi is obsolete, make sure there are no remnants
			sed -i '/dtoverlay=lirc-rpi/d' $CONFIGTXT
			sed -i '/dtoverlay=gpio-ir/d' $CONFIGTXT
			sudo echo "dtoverlay=gpio-ir,gpio_pin=$IR_GPIO_IN" >> $CONFIGTXT
			if [ "$IR_GPIO_OUT" != "" ]; then
				#might need testing, some recommend dtoverlay=pwm-ir-tx 
				sudo echo "dtoverlay=gpio-ir-tx,gpio_pin=$IR_GPIO_OUT" >> $CONFIGTXT
			fi
			echo "${GREEN}Done.${NORMAL}"
		fi
		# Setup GPIO Shutdown and Poweroff overlays
		if [ "$GPIOPOWEROFF" = "yes" ]; then
			echo -n "${BLUE}[ INFO ] Adding gpio-poweroff overlay to config.txt...${NORMAL}"
			sed -i '/dtoverlay=gpio-poweroff/d' $CONFIGTXT
			[ $GPIOPOWEROFF_HI = "yes" ] && ACTIVELOW="" || ACTIVELOW=",active_low=1"
			echo "dtoverlay=gpio-poweroff,gpiopin=${GPIOPOWEROFF_GPIO}${ACTIVELOW}" >> $CONFIGTXT
		fi
		if [ "$GPIOSHUTDOWN" = "yes" ]; then
			echo -n "${BLUE}[ INFO ] Adding gpio-shutdown overlay to config.txt...${NORMAL}"
			sed -i '/dtoverlay=gpio-shutdown/d' $CONFIGTXT
			[ $GPIOSHUTDOWN_HI = "yes" ] && ACTIVELOW="active_low=0" || ACTIVELOW="active_low=1"
			echo "dtoverlay=gpio-shutdown,gpio_pin=${GPIOSHUTDOWN_GPIO},${ACTIVELOW},gpio_pull=${GPIOSHUTDOWN_PU}" >> $CONFIGTXT
		fi
		# Setup CPU Isolation
		if [ "$CPUISOL" = "enabled" ]; then
			echo -n "${BLUE}[ INFO ] Setting up CPU Isolation...${NORMAL}"
			sed -i 's/isolcpus[=][^ ]* //g' $CMDLINETXT
			sed -i '1 s/^/isolcpus=0,3 /' $CMDLINETXT
			echo "${GREEN}Done.${NORMAL}"
		fi
		# This will read newconfig and create wpa_supplicant.conf
		# Used during the upgrade from 3.5.0 to 4.0.0
		# DO NOT PROMOTE THIS METHOD IT WILL BE DELETE <=== GE
		if [ "$WIFI" = "on" -a ! -f $WPASUPPLICANTCONF ]; then
			WPACONFIGFILE="/tmp/newconfig/usedpcp.cfg"
			pcp_wifi_update_wifi_onbootlst
			pcp_wifi_read_newconfig "colour"
			pcp_wifi_write_wpa_supplicant "colour"
		fi
	######## CONFIG.TXT Section End
	# During an newconfig update, turn HDMI back on, and turn off Overclocking Variables incase there are problems.
	HDMIPOWER="on"
	OVERCLOCK="NONE"
	ADVOVERCLOCK="None"
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
	# Disable alsaequal if it doesn't exists on new image.
	if [ "$OUTPUT" = "equal" ]; then
		if [ ! -f $TCEMNT/tce/optional/alsaequal.tcz ]; then
			echo "${YELLOW}[ WARN ] Disabling Alsaequal, please re-install.${NORMAL}"
			OUTPUT=""
			ALSAeq="no"
		fi
	fi
	# Disable Jivelite if it doesn't exists on new image.
	if [ "$JIVELITE" = "yes" ]; then
		if [ ! -f $TCEMNT/tce/optional/pcp-jivelite.tcz ]; then
			echo "${YELLOW}[ WARN ] Disabling Jivelite, please re-install.${NORMAL}"
			JIVELITE="no"
		fi
	fi
	# pcp_read_chosen_audio works from $PCPCFG, so lets write what we have so far.
	pcp_save_to_config
	pcp_disable_HDMI
	echo -n "${BLUE}[ INFO ] Setting Soundcard from newpcp.cfg...${NORMAL}"
	[ "$AUDIO" = "USB" ] && USBOUTPUT="$OUTPUT"
	pcp_read_chosen_audio noumount
	pcp_save_to_config
	echo "${GREEN}Done.${NORMAL}"

	# Cleanup all old kernel modules.
	CURRENTKERNEL=$(uname -r)
	# Get list of kernel modules not matching current kernel and remove them.
	ls $TCEMNT/tce/optional/*.tcz* | grep -E '(pcpCore)|(pcpAudioCore)' | grep -v $CURRENTKERNEL | xargs -r -I {} rm -f {}
	# Check onboot to be sure there are no hard kernel references.
	sed -i 's|[-][0-9].[0-9].*|-KERNEL.tcz|' $ONBOOTLST
	# Remove lines containing only white space.
	sed -i '/^\s*$/d' $ONBOOTLST

	pcp_backup_nohtml >/dev/null 2>&1
	echo -n "${BLUE}[ INFO ] Saving a copy of the upgrade log to ${YELLOW}${TCEMNT}/tce/pcp_insitu_upgrade.log ${BLUE}...${NORMAL}"
	cp -f /var/log/pcp_boot.log ${TCEMNT}/tce/pcp_insitu_upgrade.log
	echo "${GREEN}Done.${NORMAL}"
	echo "${RED}Rebooting needed to enable your settings...${NORMAL}"
	sleep 3
	sudo reboot
	exit 0
fi
#****************************************************************************************
#***********************************Upgrade Process End *********************************
#****************************************************************************************

#========================================================================================
# Replace default rotdash
#----------------------------------------------------------------------------------------
if [ "$ROTDASH" = "yes" ]; then
	echo -n "${BLUE}Replacing existing rotdash...${NORMAL}"
	pcp_create_rotdash &
	echo "${GREEN}Done.${NORMAL}"
fi

# Set default repository in case it has been set to something non-standard.
echo -n "${BLUE}Setting piCore repository...${NORMAL}"
pcp_reset_repository &
echo "${GREEN}Done.${NORMAL}"

echo -n "${BLUE}Generating drop-down list...${NORMAL}"
pcp_sound_card_dropdown &
echo "${GREEN}Done.${NORMAL}"

# Startup AP mode if enabled.
if [ "$APMODE" = "yes" ]; then
	echo -n "${BLUE}Starting pCP AP Mode...${NORMAL}"
	[ -x /usr/local/etc/init.d/pcp-apmode ] && /usr/local/etc/init.d/pcp-apmode start || echo "${RED}pcp-apmode extension not loaded.${NORMAL}"
	echo "${GREEN}Done.${NORMAL}"
fi

#========================================================================================
# Start wifi.
#----------------------------------------------------------------------------------------
WPACONFIGFILE=$WPASUPPLICANTCONF

if [ $WPACONFIGFOUND -eq 1 ]; then
	WIFI="on"
	pcp_save_to_config
	dos2unix -u $WPACONFIGFILE
	if [ $(pcp_wifi_maintained_by_user) -ne 0 ]; then
		pcp_wifi_read_wpa_supplicant "colour"
		pcp_wifi_write_wpa_supplicant "colour"
	fi
	pcp_wifi_update_wifi_onbootlst
	pcp_backup_nohtml
	echo "${RED}Reboot needed to enable wifi...${NORMAL}"
	sleep 3
	sudo reboot
	exit 0
fi

#----------------------------------------------------------------------------------------
# **** Catch all for broken onboot.lst during pCP4.0.0 beta testing. ****
#----------------------------------------------------------------------------------------
if [ "$WIFI" = "on" ]; then
	grep firmware-ralinkwifi.tcz ${ONBOOTLST} >/dev/null 2>&1
	if [ $? -eq 1 ]; then
		pcp_wifi_update_wifi_onbootlst
		echo "${RED}Reboot needed to enable wifi...${NORMAL}"
		sleep 3
		sudo reboot
		exit 0
	fi
fi
#----------------------------------------------------------------------------------------

if [ "$WIFI" = "on" ]; then
	echo "${BLUE}Starting wifi...${NORMAL}"
	/usr/local/etc/init.d/wifi wlan0 start
	echo "${GREEN}Done.${NORMAL}"
fi
#----------------------------------------------------------------------------------------

# Loading configuration file pcp.cfg
echo -n "${BLUE}Loading configuration file...${NORMAL}"
. $PCPCFG
echo "${GREEN}Done.${NORMAL}"

echo -n "${BLUE}Loading pcp-lms-functions...${NORMAL}"
. /home/tc/www/cgi-bin/pcp-lms-functions
echo "${GREEN}Done.${NORMAL}"

# This routine will load the contents of the selected Card Config file.
pcp_load_card_conf

echo -n "${YELLOW}Waiting for soundcard ${CARDNAME} to populate."
if [ $CARDNAME != "BTSpeaker" ]; then
	CNT=1
	until aplay -l | grep '\[' | grep -q $CARDNAME 2>&1
	do
		if [ $((CNT++)) -gt 40 ]; then
			echo "${RED} Failed to find $CARDNAME ($CNT).${NORMAL}"
			break
		else
			echo -n "."
			sleep 0.5
		fi
	done
else
	echo -n "${BLUE}Bluetooth Output selected..."
fi
echo "${GREEN} Done ($CNT).${NORMAL}"

# Start the essential stuff for piCorePlayer.
echo -n "${YELLOW}Waiting for network."
CNT=1
until ifconfig | grep -q Bcast
do
	if [ $((CNT++)) -gt $NETWORK_WAIT ]; then
		echo -n "${RED} No network found!${NORMAL}"
		break
	else
		echo -n "."
		sleep 0.5
	fi
done
echo "${GREEN} Done ($CNT).${NORMAL}"

# If Custom ALSA settings are used, then restore the settings.
echo -n "${BLUE}Starting ALSA configuration...${NORMAL}"
if [ "$ALSAlevelout" = "Custom" ]; then
	# It seems the first attempt to load the state fails with some error. Looking at debug, it appears that not everything is initialized
	# yet.  Since the state may contain extra cards, Load only the asound state for the selected card,
	# and make sure it completes without error.
	CNT=1
	until false; do
		alsactl restore $CARDNAME
		[ $? -eq 0 ] && break
		if [ $((CNT++)) -gt 5 ]; then
			echo "${RED} ALSA restore error!${NORMAL}"
			break
		else
			echo -n "."
			sleep 0.25
		fi
	done
	echo "${GREEN}($CNT)${NORMAL}"
fi

# Run custom audio card boot script.
if [ "$AUDIOBOOTSCRIPT" != "" ]; then
	echo -n "${BLUE}Running audio card boot script... ${YELLOW}"
	$AUDIOBOOTSCRIPT
	echo "${GREEN} Done.${NORMAL}"
fi

# Check for onboard sound card is card=0 and analog is chosen, so amixer is only used here.
aplay -l | grep 'card 0: ALSA'  >/dev/null 2>&1
if [ $? -eq 0 ] && [ "$AUDIO" = "Analog" ]; then
	# Set the analog output via audio jack.
	sudo amixer cset numid=3 1 >/dev/null 2>&1
	if [ "$ALSAlevelout" = "Default" ]; then
		sudo amixer set PCM 400 unmute >/dev/null 2>&1
	fi
fi

# Check for onboard sound card is card=0, and HDMI is chosen so HDMI amixer settings is enabled.
aplay -l | grep 'card 0: ALSA'  >/dev/null 2>&1
if [ $? -eq 0 ] && [ "$AUDIO" = "HDMI" ]; then
	if [ "$ALSAlevelout" = "Default" ]; then
		sudo amixer set PCM 400 unmute >/dev/null 2>&1
	fi
	# Set the analog output via HDMI out.
	sudo amixer cset numid=3 2 >/dev/null 2>&1
fi
echo "${GREEN}Done.${NORMAL}"

if [ "$OUTPUT" = "equal" ]; then
	pcp_load_card_conf
	echo -n "${BLUE}Checking proper card number for Alsaequal...${NORMAL}"
	[ "$CARDNO" != "" ] && sed -i "s/plughw:.*,0/plughw:"$CARDNO",0/g" /etc/asound.conf || echo "{$RED}Selected card not found in /proc/asound/cards."
	echo "${GREEN}Done.${NORMAL}"
fi

#========================================================================================
# WOL="yes"|"no"
# WOL_NIC="eth0"|"wlan0"|"wlan1"|... does wlan1 exist if user adds WiFi dongle on RPi3 with onboard WiFi enabled?
# WOL_LMSMACADDRESS="11:22:33:44:55:66"
# Only send LMS WOL command if LMS is not run locally
#----------------------------------------------------------------------------------------
if [ "$LMSERVER" != "yes" ]; then
	if [ "$WOL" = "yes" ] && [ "$WOL_NIC" != "" ] && [ "$WOL_LMSMACADDRESS" != "" ]; then
		# Should we check for valid MAC address or should we assume this is covered in the applet/web interface??
		echo -n "${BLUE}Sending WOL magic packet ($WOL_LMSMACADDRESS)...${NORMAL}"
		sudo ether-wake -i $WOL_NIC $WOL_LMSMACADDRESS
		echo "${GREEN}Done.${NORMAL}"
	fi
fi

#========================================================================================
# INFRARED remote control - Start lircd if needed.
#----------------------------------------------------------------------------------------
if [ "$IR_LIRC" = "yes" ]; then
	LIRCD=/usr/local/sbin/lircd

	if [ -x $LIRCD ]; then
		LIRCVER="$($LIRCD --version | awk '{printf "%s", $2}')"

		if [ "$LIRCVER" = "0.9.0" ]; then
			if [ "$JIVELITE" = "yes" ]; then
				echo -n "${BLUE}Starting lirc with Jivelite support...${NORMAL}"
				$LIRCD --device=/dev/${IR_DEVICE} --log=/var/log/pcp_lirc.log --uinput
			else
				echo -n "${BLUE}Starting lirc...${NORMAL}"
				$LIRCD --device=/dev/${IR_DEVICE} --log=/var/log/pcp_lirc.log
			fi
		else
			echo -n "${BLUE}Starting lirc...${NORMAL}"
			$LIRCD --device=/dev/${IR_DEVICE} --logfile=/var/log/pcp_lirc.log

			if [ "$JIVELITE" = "yes" ]; then
				echo -n "${BLUE}Starting lirc Jivelite support...${NORMAL}"
				"${LIRCD}-uinput" --logfile=/var/log/pcp_lirc_uinput.log &
			fi
		fi
		echo "${GREEN}Done.${NORMAL}"
	fi
fi

#========================================================================================
# Start openssh if file ssh found. $SSH set in NEWCONFIGFOUND process.
#----------------------------------------------------------------------------------------
if [ $SSH -eq 1 ]; then
	echo -n "${BLUE}Starting Openssh server...${NORMAL}"
	/usr/local/etc/init.d/openssh start >/dev/null 2>&1
	echo "${GREEN}Done.${NORMAL}"
else
	echo -n "${YELLOW}Openssh server is disabled...${NORMAL}"
fi

#========================================================================================
# Mount USB Disk Selected on LMS Page
#----------------------------------------------------------------------------------------
LMSMOUNTFAIL="0"
# READ Conf file
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
						umount $DEVICE  # ntfs cannot be dual mounted.
						OPTIONS="-v -t ntfs-3g -o permissions,noatime"
					;;
					vfat|fat32)
						# If Filesystem support installed, use utf-8 charset for fat.
						df | grep -qs ntfs
						[ "$?" = "0" ] && CHARSET=",iocharset=utf8" || CHARSET=""
						umount $DEVICE  # need to unmount vfat incase 1st mount is not utf8
						OPTIONS="-v -t vfat -o noauto,users,noatime,exec,umask=000,flush${CHARSET}"
					;;
					exfat)
						CHARSET=",iocharset=utf8"
						umount $DEVICE  # Need to unmount incase 1st mount is not utf8.
						OPTIONS="-v -o noauto,users,noatime,exec,umask=000,flush,uid=1001,gid=50${CHARSET}"
					;;
					*)
						OPTIONS="-v -o noatime"
					;;
				esac
				echo "${BLUE}Mounting USB Drive: $UUID...${YELLOW}"
				case "$FSTYPE" in
					exfat) modprobe fuse; mount.exfat $OPTIONS $DEVICE /mnt/$POINT;;
					*) mount $OPTIONS --uuid $UUID /mnt/$POINT;;
				esac
				if [ $? -eq 0 ]; then
					echo "${BLUE}Disk Mounted at /mnt/$POINT.${NORMAL}"
				else
					echo "${RED}Disk Mount Error.${NORMAL}"
					LMSMOUNTFAIL="1"
				fi
			else
				 echo "${RED}Disk ${UUID} Not Found, Please insert drive and Reboot.${NORMAL}"
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
	#cifs does not automatically load arc4, which is in the dependancies needed for SMB3 to work
	modprobe arc4
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
					MNTCMD="-v -t $FSTYPE -o $OPTS //$IP/\"$(${HTTPD} -f -d $SHARE)\" /mnt/$PNT"
				;;
				nfs)
					OPTS="addr=${IP},nolock,${OPTIONS}"
					MNTCMD="-v -t $FSTYPE -o $OPTS $IP:\"$(${HTTPD} -f -d $SHARE)\" /mnt/$PNT"
				;;
			esac
			RETRIES=3  # Retry network mounts, in case of power failure, and all devices restarting.
			while [ $RETRIES -gt 0 ]; do
				/bin/sh -c "mount ${MNTCMD}"
				if [ $? -eq 0 ]; then
					RETRIES=0
					echo "${BLUE}Disk Mounted at /mnt/${PNT}."
				else
					RETRIES=$((RETRIES-1))
					if [ $RETRIES -eq 0 ]; then
						echo "${RED}Disabling network mount from server at ${IP}.${NORMAL}"
						cp -f $NETMOUNTCONF /tmp/netconf
						cat /tmp/netconf | awk '/^\[/ {m++}{if(m=='$I')sub("NETENABLE\=yes","NETENABLE\=no")}1' > $NETMOUNTCONF
						LMSMOUNTFAIL="1"
					else
						echo "${RED}Disk Mount Error, Retrying $RETRIES more times...sleeping 10 seconds.${YELLOW}"
						sleep 10
					fi
				fi
			done
		fi
		I=$((I+1))
	done
	echo "${GREEN}Done.${NORMAL}"
fi

# If running an LMS Server Locally, start squeezelite later.
if [ "$LMSERVER" != "yes" ]; then
	if [ "$SQUEEZELITE" = "yes" ]; then
		echo "${BLUE}Starting Squeezelite and/or Shairport-sync...${YELLOW}"
		pcp_squeezelite_start nohtml
		echo "${GREEN}Done.${NORMAL}"
	fi
fi

# Automatically set the timezone.
if [ x"" = x"$TIMEZONE" ] && [ $(pcp_internet_accessible) = 0 ]; then
	echo "${BLUE}Auto set timezone settings, can be updated on tweaks page...${NORMAL}"
	# Fetch timezone from Ubuntu's geoip server.
	TZ1=`wget -O - -q http://geoip.ubuntu.com/lookup | sed -n -e 's/.*<TimeZone>\(.*\)<\/TimeZone>.*/\1/p'`
	# Translate country/city to timezone string.
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
		echo -n "${BLUE}Starting LMS, this can take some time...${NORMAL}"
		sudo /usr/local/etc/init.d/slimserver start
		echo "${GREEN}Done.${NORMAL}"
		if [ "$SQUEEZELITE" = "yes" ]; then
			# Wait for server to be responsive.
			echo -n "${YELLOW}Waiting for LMS to initiate."
			# Check response from port 3483 for Player Connects.
			CNT=1
			CHK=""
			while [ "$CHK" != "E" ];
			do
				CHK=$(echo "e" | nc -w 1 -u 127.0.0.1 3483)
				if [ $((CNT++)) -gt 20 ]; then
					echo "${RED} LMS not running ($CNT).${NORMAL}"
					break
				else
					echo -n "."
					[ "$CHK" != "E" ] && sleep 1
				fi
			done
			echo "${GREEN} Done ($CNT).${NORMAL}"

		echo "${BLUE}Starting Squeezelite and/or Shairport-sync...${YELLOW}"
			pcp_squeezelite_start nohtml
			echo "${GREEN}Done.${NORMAL}"
		fi
	else
		echo "${RED}LMS data disk failed mount, LMS and squeezelite will not start.${NORMAL}"
	fi
fi

# Turn HDMI power off to save ~20ma.
if [ "$HDMIPOWER" = "off" ]; then
	echo -n "${BLUE}Powering off HDMI...${NORMAL}"
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

echo -n "${BLUE}Starting httpd web server...${NORMAL}"
/usr/local/etc/init.d/httpd start >/dev/null 2>&1
echo "${GREEN}Done.${NORMAL}"

if [ x"" != x"$USER_COMMAND_1" ] || [ x"" != x"$USER_COMMAND_2" ] || [ x"" != x"$USER_COMMAND_3" ]; then
	echo -n "${BLUE}Starting user commands...${NORMAL}"
	pcp_user_commands
	echo "${GREEN}Done.${NORMAL}"
fi

if [ "$A_S_LMS" = "Enabled" ]; then
	echo -n "${BLUE}Starting auto start LMS...${NORMAL}"
	pcp_lms_auto_start_lms
	echo "${GREEN}Done.${NORMAL}"
fi

if [ "$A_S_FAV" = "Enabled" ]; then
	echo -n "${BLUE}Starting auto start FAV...${NORMAL}"
	pcp_lms_auto_start_fav
	echo "${GREEN}Done.${NORMAL}"
fi

# Save the parameters to the config file.
if [ $BACKUP -eq 1 ]; then
	echo -n "${BLUE}Saving the changes...${NORMAL}"
	pcp_backup_nohtml >/dev/null 2>&1
	echo "${GREEN}Done.${NORMAL}"
fi

# Display the IP address.
ifconfig eth0 2>&1 | grep inet >/dev/null 2>&1 && echo "${BLUE}eth0 IP: $(pcp_eth0_ip)${NORMAL}"
ifconfig wlan0 2>&1 | grep inet >/dev/null 2>&1 && echo "${BLUE}wlan0 IP: $(pcp_wlan0_ip)${NORMAL}"

echo -n "${BLUE}Setting cpu scaling governor...${NORMAL}"
echo -n $CPUGOVERNOR | sudo tee /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
echo "${GREEN} Done.${NORMAL}"

echo "${GREEN}Finished piCorePlayer setup.${NORMAL}"
sudo su -c 'echo "Finished piCorePlayer setup." > /dev/kmsg'

if [ "$JIVELITE" = "yes" ]; then
	echo -n "${BLUE}Starting Jivelite...${NORMAL}"
	eventno=$( cat /proc/bus/input/devices | awk '/FT5406 memory based driver/{for(a=0;a>=0;a++){getline;{if(/mouse/==1){ print $NF;exit 0;}}}}')
	if [ x"" != x"$eventno" ];then
		export JIVE_NOCURSOR=1
		export TSLIB_TSDEVICE=/dev/input/$eventno
		export SDL_MOUSEDRV=TSLIB
		export SDL_MOUSEDEV=$TSLIB_TSDEVICE
	fi
	export HOME=/home/tc
	# Alternative jivelite script, mainly used for waveshare devices.  Located on persistent partition. (/mnt/mmcblk0p2 or partition where tce is located)
	if [ -x $TCEMNT/tce/jivelite.sh ]; then
		echo "${GREEN}Done.${NORMAL}"
		sudo -E -b $TCEMNT/tce/jivelite.sh >/dev/null 2>&1
	elif [ -x /opt/jivelite/bin/jivelite.sh ]; then
		echo "${GREEN}Done.${NORMAL}"
		sudo -E -b /opt/jivelite/bin/jivelite.sh >/dev/null 2>&1
	else
		echo "${RED}There is a problem with the Jivelite installation. Please remove and reinstall jivelite.${NORMAL}"
	fi
fi

echo "${BLUE}crond syncing time...${NORMAL}"

unset ORIG_AUDIO
