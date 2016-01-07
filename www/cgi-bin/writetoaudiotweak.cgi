#!/bin/sh

# Version: 0.06 2016-01-07 SBP
#	Added ALSA Equalizer.
#	Added Shairport-sync.

# Version: 0.05 2015-09-19 SBP
#	Removed httpd decoding.

# Version: 0.04 2015-06-06 GE
#	Remove multiple spaces from CONFIGCFG.
#	Removed duplicate ALSA output level section.

# Version: 0.03 2015-01-28 GE
#	Included changefiq.sh.

# Version: 0.02 2014-12-10 GE
#	Using pcp_html_head now.
#	HTML5 formatting.

# Version: 0.01 2014-08-06 SBP
#	Original version.

. pcp-functions
pcp_variables

# Store the original values so we can see if they are changed
ORIG_ALSAeq="$ALSAeq"
ORIG_SHAIRPORT="$SHAIRPORT"
ORIG_ALSAlevelout="$ALSAlevelout"
ORIG_FIQ="$FIQ"
ORIG_CMD="$CMD"

pcp_html_head "Write to Audio Tweak" "SBP" "15" "tweaks.cgi"

pcp_banner
pcp_running_script
pcp_httpd_query_string

SHAIRP="shairport-sync"
AVAHI="avahi.tzc and needed packages"
WGET="/bin/busybox wget"

# Only offer reboot option if needed
REBOOT_REQUIRED=0

#========================================================================================================
# Routines
#--------------------------------------------------------------------------------------------------------
pcp_download_shairport() {
	pcp_sufficient_free_space 2000
	cd /tmp
	sudo rm -f /tmp/${SHAIRP}
	echo '<p class="info">[ INFO ] Downloading Shairport from Ralphy'\''s repository...</p>'
	[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Ralphy repo: '${REPOSITORY}'</p>'
	echo '<p class="info">[ INFO ] Download will take a few minutes. Please wait...</p>'

	$WGET -s ${REPOSITORY}${SHAIRP}
	if [ $? = 0 ]; then
		echo '<p class="info">[ INFO ] Downloading '$SHAIRP' and '$AVAHI'...'
		$WGET -P /tmp ${REPOSITORY}${SHAIRP}
		if [ $? = 0 ]; then
			echo '<p class="ok">[ OK ] Download successful.</p>'
			/usr/local/etc/init.d/shairport-sync stop >/dev/null 2>&1
#			sudo pkill shairport-sync
			sudo cp /tmp/$SHAIRP /mnt/mmcblk0p2/tce/shairport-sync
			sudo chown tc:staff /mnt/mmcblk0p2/tce/shairport-sync
			sudo chmod 755 /mnt/mmcblk0p2/tce/shairport-sync
		else
			echo '<p class="error">[ ERROR ] Shairport download unsuccessful, try again!</p>'
		fi
	else
		echo '<p class="error">[ ERROR ] Shairport not available in repository, try again later!</p>'
	fi

	sudo rm -f /tmp/avahi/*
	[ -d /tmp/avahi ] || sudo mkdir avahi
	echo '<p class="info">[ INFO ] Downloading Avahi from Ralphy'\''s repository...</p>'
	echo '<p class="info">[ INFO ] Download will take a few minutes. Please wait...</p>'

	$WGET -s ${REPOSITORY}avahi.tcz
	if [ $? = 0 ]; then
		RESULT=0
		echo -n '<p class="info">[ INFO ] Downloading Avahi'
		$WGET -P /tmp/avahi ${REPOSITORY}avahi.tcz
		[ $? = 0 ] && echo -n . || (echo $?; RESULT=1)
		$WGET -P /tmp/avahi ${REPOSITORY}avahi.tcz.dep
		[ $? = 0 ] && echo -n . || (echo $?; RESULT=1)
		$WGET -P /tmp/avahi ${REPOSITORY}avahi.tcz.md5.txt
		[ $? = 0 ] && echo -n . || (echo $?; RESULT=1)
		$WGET -P /tmp/avahi ${REPOSITORY}dbus.tcz
		[ $? = 0 ] && echo -n . || (echo $?; RESULT=1)
		$WGET -P /tmp/avahi ${REPOSITORY}dbus.tcz.md5.txt
		[ $? = 0 ] && echo -n . || (echo $?; RESULT=1)
		$WGET -P /tmp/avahi ${REPOSITORY}expat2.tcz
		[ $? = 0 ] && echo -n . || (echo $?; RESULT=1)
		$WGET -P /tmp/avahi ${REPOSITORY}expat2.tcz.md5.txt
		[ $? = 0 ] && echo -n . || (echo $?; RESULT=1)
		$WGET -P /tmp/avahi ${REPOSITORY}libattr.tcz
		[ $? = 0 ] && echo -n . || (echo $?; RESULT=1)
		$WGET -P /tmp/avahi ${REPOSITORY}libattr.tcz.md5.txt
		[ $? = 0 ] && echo -n . || (echo $?; RESULT=1)
		$WGET -P /tmp/avahi ${REPOSITORY}libavahi.tcz
		[ $? = 0 ] && echo -n . || (echo $?; RESULT=1)
		$WGET -P /tmp/avahi ${REPOSITORY}libavahi.tcz.dep
		[ $? = 0 ] && echo -n . || (echo $?; RESULT=1)
		$WGET -P /tmp/avahi ${REPOSITORY}libavahi.tcz.md5.txt
		[ $? = 0 ] && echo -n . || (echo $?; RESULT=1)
		$WGET -P /tmp/avahi ${REPOSITORY}libcap.tcz
		[ $? = 0 ] && echo -n . || (echo $?; RESULT=1)
		$WGET -P /tmp/avahi ${REPOSITORY}libcap.tcz.md5.txt
		[ $? = 0 ] && echo -n . || (echo $?; RESULT=1)
		$WGET -P /tmp/avahi ${REPOSITORY}libcofi.tcz
		[ $? = 0 ] && echo -n . || (echo $?; RESULT=1)
		$WGET -P /tmp/avahi ${REPOSITORY}libcofi.tcz.md5.txt
		[ $? = 0 ] && echo -n . || (echo $?; RESULT=1)
		$WGET -P /tmp/avahi ${REPOSITORY}libdaemon.tcz
		[ $? = 0 ] && echo -n . || (echo $?; RESULT=1)
		$WGET -P /tmp/avahi ${REPOSITORY}libdaemon.tcz.md5.txt
		[ $? = 0 ] && echo -n . || (echo $?; RESULT=1)
		$WGET -P /tmp/avahi ${REPOSITORY}nss-mdns.tcz
		[ $? = 0 ] && echo -n . || (echo $?; RESULT=1)
		$WGET -P /tmp/avahi ${REPOSITORY}nss-mdns.tcz.md5.txt
		[ $? = 0 ] && echo -n . || (echo $?; RESULT=1)
		if [ $RESULT = 0 ]; then
			echo '<p class="ok">[ OK ] Download successful.</p>'
			sudo chown -R tc:staff /tmp/avahi/*
			sudo chmod -R 644 /tmp/avahi/*
			sudo cp -rp /tmp/avahi/* /mnt/mmcblk0p2/tce/optional
		else
			echo '<p class="error">[ ERROR ] Avahi download unsuccessful, try again!</p>'
		fi
	else
		echo '<p class="error">[ ERROR ] Avahi not available in repository, try again later!</p>'
	fi
	SPACE=$(pcp_free_space k)
	[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Free space: '$SPACE'k</p>'
}

pcp_remove_shairport() {
	/usr/local/etc/init.d/shairport-sync stop >/dev/null 2>&1
#	sudo pkill shairport-sync
	sudo rm -f /mnt/mmcblk0p2/tce/shairport-sync
	sudo rm -f /mnt/mmcblk0p2/tce/optional/avahi.tcz*
	sudo rm -f /mnt/mmcblk0p2/tce/optional/dbus.tcz*
	sudo rm -f /mnt/mmcblk0p2/tce/optional/expat2.tcz*
	sudo rm -f /mnt/mmcblk0p2/tce/optional/libattr.tcz*
	sudo rm -f /mnt/mmcblk0p2/tce/optional/libavahi.tcz*
	sudo rm -f /mnt/mmcblk0p2/tce/optional/libcap.tcz*
	sudo rm -f /mnt/mmcblk0p2/tce/optional/libcofi.tcz*
	sudo rm -f /mnt/mmcblk0p2/tce/optional/libdaemon.tcz*
	sudo rm -f /mnt/mmcblk0p2/tce/optional/nss-mdns.tcz*
}

#========================================================================================
# ALSA output level section
#----------------------------------------------------------------------------------------
# Only do something if variable is changed
if [ $ORIG_ALSAlevelout != $ALSAlevelout ]; then
	echo '<hr>'
	echo '<p class="info">[ INFO ] ALSAlevelout is set to: '$ALSAlevelout'</p>'
	[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] ORIG_ALSAlevelout is: '$ORIG_ALSAlevelout'</p>'
	[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] ALSAlevelout is: '$ALSAlevelout'</p>'
	echo '<hr>'
else
	echo '<p class="info">[ INFO ] ALSAlevelout variable unchanged.</p>'
fi

#========================================================================================
# ALSA Equalizer section
#----------------------------------------------------------------------------------------
# Only do something if variable is changed
if [ $ORIG_ALSAeq != $ALSAeq ]; then
	REBOOT_REQUIRED=1
	echo '<hr>'
	echo '<p class="info">[ INFO ] ALSAeq is set to: '$ALSAeq'</p>'

	# Determination of the number of the current sound-card

	# If output is analog or HDMI then find the number of the used ALSA-card
	if [ $AUDIO = Analog ] || [ $AUDIO = HDMI ]; then
		CARDNO=$(sudo cat /proc/asound/cards | grep '\[' | grep 'ALSA' | awk '{print $1}')
	fi

	# If output is different from analog or HDMI then find the number of the non-ALSA card
	aplay -l | grep 'card 0: ALSA'  >/dev/null 2>&1
	if [ $? == 0 ]; then
		if [ $AUDIO != Analog ] && [ $AUDIO != HDMI ]; then
			CARDNO=$(sudo cat /proc/asound/cards | sed '/ALSA/d' | grep '\[' | awk '{print $1}')
		fi
	else
		if [ $AUDIO != Analog ] && [ $AUDIO != HDMI ]; then
			CARDNO=$(sudo cat /proc/asound/cards | grep '\[' | awk '{print $1}')
		fi
	fi

	[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] ORIG_ALSAeq is: '$ORIG_ALSAeq'</p>'
	[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] ALSAeq is: '$ALSAeq'</p>'
	[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Card has number: '$CARDNO'.</p>'
	[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] AUDIO is: '$AUDIO'</p>'

	case "$ALSAeq" in
		yes)
			echo '<p class="info">[ INFO ] ALSA equalizer: '$ALSAeq'</p>'
			OUTPUT="equal"
			if grep -Fxq "alsaequal.tcz" /mnt/mmcblk0p2/tce/onboot.lst; then
				[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] ALSA equalizer modules already loaded.</p>'
			else
				sudo echo "alsaequal.tcz" >> /mnt/mmcblk0p2/tce/onboot.lst
				sudo echo "caps-0.4.5.tcz" >> /mnt/mmcblk0p2/tce/onboot.lst
			fi
			sed -i "s/plughw:.*,0/plughw:"$CARDNO",0/g" /etc/asound.conf
			;;
		no)
			echo '<p class="info">[ INFO ] ALSA equalizer: '$ALSAeq'</p>'
			OUTPUT=""
			sudo sed -i '/alsaequal.tcz/d' /mnt/mmcblk0p2/tce/onboot.lst
			sudo sed -i '/caps/d' /mnt/mmcblk0p2/tce/onboot.lst
			;;
		*)
			echo '<p class="error">[ ERROR ] ALSA equalizer invalid: '$ALSAeq'</p>'
			;;
	esac
	echo '<hr>'
else
	echo '<p class="info">[ INFO ] ALSAeq variable unchanged.</p>'
fi

#========================================================================================
# CMD section
#----------------------------------------------------------------------------------------
# Only do something if variable is changed
if [ $ORIG_CMD != $CMD ]; then
	REBOOT_REQUIRED=1
	echo '<hr>'
	echo '<p class="info">[ INFO ] CMD is set to: '$CMD'</p>'
	[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] ORIG_CMD is: '$ORIG_CMD'</p>'
	[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] CMD is: '$CMD'</p>'

	case "$CMD" in
		"Default")
			echo '<p class="info">[ INFO ] CMD: '$CMD'</p>'
			#sudo ./disableotg.sh

			pcp_mount_mmcblk0p1

			if mount | grep $VOLUME; then
				# Remove dwc_otg_speed=1
				sed -i 's/dwc_otg.speed=1 //g' /mnt/mmcblk0p1/cmdline.txt
				pcp_umount_mmcblk0p1
			else
				echo '<p class="error">[ ERROR ] '$VOLUME' not mounted</p>'
			fi
			;;
		"Slow")
			echo '<p class="info">[ INFO ] CMD: '$CMD'</p>'
			#sudo ./enableotg.sh

			pcp_mount_mmcblk0p1

			if mount | grep $VOLUME; then
				# Remove dwc_otg_speed=1
				sed -i 's/dwc_otg.speed=1 //g' /mnt/mmcblk0p1/cmdline.txt

				# Add dwc_otg_speed=1
				sed -i '1 s/^/dwc_otg.speed=1 /' /mnt/mmcblk0p1/cmdline.txt
				pcp_umount_mmcblk0p1
			else
				echo '<p class="error">[ ERROR ] '$VOLUME' not mounted</p>'
			fi
			;;
		*)
			echo '<p class="error">[ ERROR ] CMD invalid: '$CMD'</p>'
			;;
	esac
	echo '<hr>'
else
	echo '<p class="info">[ INFO ] CMD variable unchanged.</p>'
fi

#========================================================================================
# SHAIRPORT section
#----------------------------------------------------------------------------------------
# Only do something if variable is changed
if [ $ORIG_SHAIRPORT != $SHAIRPORT ]; then
	REBOOT_REQUIRED=1
	echo '<hr>'
	echo '<p class="info">[ INFO ] SHAIRPORT is set to: '$SHAIRPORT'</p>'
	[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] ORIG_SHAIRPORT is: '$ORIG_SHAIRPORT'</p>'
	[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] SHAIRPORT is: '$SHAIRPORT'</p>'

	case "$SHAIRPORT" in
		yes)
			echo '<p class="info">[ INFO ] Shairport will be enabled.</p>'
			if grep -Fxq "avahi.tcz" /mnt/mmcblk0p2/tce/onboot.lst; then
				[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Shairport-sync already loaded.</p>'
			else
				sudo echo "avahi.tcz" >> /mnt/mmcblk0p2/tce/onboot.lst
				pcp_download_shairport
			fi
			CLOSEOUT="15"
			;;
		no)
			echo '<p class="info">[ INFO ] Shairport will be disabled.</p>'
			pcp_remove_shairport
			sudo sed -i '/avahi.tcz/d' /mnt/mmcblk0p2/tce/onboot.lst
			CLOSEOUT=""
			;;
		*)
			echo '<p class="error">[ ERROR ] Shairport selection invalid: '$SHAIRPORT'</p>'
			;;
	esac
	echo '<hr>'
else
	echo '<p class="info">[ INFO ] SHAIRPORT variable unchanged.</p>'
fi

#========================================================================================
# FIQ spilt section
#----------------------------------------------------------------------------------------
# Only do something if variable is changed
if [ $ORIG_FIQ != $FIQ ]; then
	REBOOT_REQUIRED=1
	echo '<hr>'
	echo '<p class="info">[ INFO ] FIQ is set to: '$FIQ'</p>'
	[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] ORIG_FIG is: '$ORIG_FIQ'</p>'
	[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] FIQ is: '$FIQ'</p>'

	pcp_mount_mmcblk0p1

	if mount | grep $VOLUME; then
		# Remove fiq settings
		sed -i 's/dwc_otg.fiq_fsm_mask=0x[1-8] \+//g' /mnt/mmcblk0p1/cmdline.txt
		# Add FIQ settings from config file
		sed -i '1 s/^/dwc_otg.fiq_fsm_mask='$FIQ' /' /mnt/mmcblk0p1/cmdline.txt

		[ $DEBUG = 1 ] && pcp_textarea "Current $CMDLINETXT" "cat $CMDLINETXT" 150
		pcp_umount_mmcblk0p1
	else
		echo '<p class="error">[ ERROR ] '$VOLUME' not mounted</p>'
	fi
	echo '<hr>'
else
	echo '<p class="info">[ INFO ] FIQ variable unchanged.</p>'
fi
#----------------------------------------------------------------------------------------

echo '<hr>'
pcp_save_to_config
pcp_backup
[ $DEBUG = 1 ] && pcp_textarea "Current $ASOUNDCONF" "cat $ASOUNDCONF" 150
[ $DEBUG = 1 ] && pcp_textarea "Current $ONBOOTLST" "cat $ONBOOTLST" 150
[ $DEBUG = 1 ] && pcp_textarea "Current $CONFIGCFG" "cat $CONFIGCFG" 150

[ $REBOOT_REQUIRED = 1 ] && pcp_reboot_required
pcp_go_back_button

echo '</body>'
echo '</html>'