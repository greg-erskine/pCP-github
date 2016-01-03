#!/bin/sh

# Version: 0.07 2016-01-03 SBP
#	Added Shairport-sync.

# Version: 0.06 2016-01-01 SBP
#	Added ALSA Equalizer.

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
#find the original values so we can see if they are changed
ori_ALSAeq="$ALSAeq"
ori_SHAIRPORT="$SHAIRPORT"
ori_ALSAlevelout=$ALSAlevelout
ori_FIQ="$FIQ"
ori_CMD=$CMD




#. $CONFIGCFG

pcp_html_head "Write to Audio Tweak" "SBP" "15" "tweaks.cgi"

pcp_banner
pcp_running_script
pcp_httpd_query_string


SHAIRP="shairport-sync"
AVAHI="avahi.tzc and needed packages"
 
#========================================================================================================
# Routines
#--------------------------------------------------------------------------------------------------------
pcp_download_shairport() {
	cd /tmp
	sudo rm -f /tmp/${SHAIRP}
	echo '<p class="info">[ INFO ] Downloading Shairport from Ralphy'\''s repository...</p>'
	echo '<p class="info">[ INFO ] Download will take a few minutes. Please wait...</p>'

	/bin/busybox wget -s ${REPOSITORY}${SHAIRP}
	if [ $? = 0 ]; then
		echo '<p class="info">[ INFO ] Downloading '$SHAIRP' and '$AVAHI'...'
		wget -P /tmp ${REPOSITORY}${SHAIRP}
		if [ $? = 0 ]; then
			echo '<p class="ok">[ OK ] Download successful.</p>'
			sudo pkill shairport-sync
			sudo cp /tmp/$SHAIRP /mnt/mmcblk0p2/tce/shairport-sync            
			sudo chown tc:staff /mnt/mmcblk0p2/tce/shairport-sync
			sudo chmod 755 /mnt/mmcblk0p2/tce/shairport-sync
			else
			echo '<p class="error">[ ERROR ] Shairport download unsuccessful, try again!</p>'
		fi
	else
		echo '<p class="error">[ ERROR ] Shairport not available in repository, try again later!</p>'
	fi

	sudo rm -f /tmp/avahi/
	echo '<p class="info">[ INFO ] Downloading Avahi from Ralphy'\''s repository...</p>'
	echo '<p class="info">[ INFO ] Download will take a few minutes. Please wait...</p>'

	/bin/busybox wget -s ${REPOSITORY}avahi.tcz
	if [ $? = 0 ]; then
		echo '<p class="info">[ INFO ] Downloading Avahi...'
		wget -P /tmp/avahi ${REPOSITORY}avahi.tcz
		wget -P /tmp/avahi ${REPOSITORY}avahi.tcz.dep
		wget -P /tmp/avahi ${REPOSITORY}avahi.tcz.md5.txt
		wget -P /tmp/avahi ${REPOSITORY}dbus.tcz
		wget -P /tmp/avahi ${REPOSITORY}dbus.tcz.md5.txt
		wget -P /tmp/avahi ${REPOSITORY}expat2.tcz
		wget -P /tmp/avahi ${REPOSITORY}expat2.tcz.md5.txt
		wget -P /tmp/avahi ${REPOSITORY}libattr.tcz
		wget -P /tmp/avahi ${REPOSITORY}libattr.tcz.md5.txt
		wget -P /tmp/avahi ${REPOSITORY}libavahi.tcz
		wget -P /tmp/avahi ${REPOSITORY}libavahi.tcz.dep
		wget -P /tmp/avahi ${REPOSITORY}libavahi.tcz.md5.txt
		wget -P /tmp/avahi ${REPOSITORY}libcap.tcz
		wget -P /tmp/avahi ${REPOSITORY}libcap.tcz.md5.txt
		wget -P /tmp/avahi ${REPOSITORY}libcofi.tcz
		wget -P /tmp/avahi ${REPOSITORY}libcofi.tcz.md5.txt
		wget -P /tmp/avahi ${REPOSITORY}libdaemon.tcz
		wget -P /tmp/avahi ${REPOSITORY}libdaemon.tcz.md5.txt
		wget -P /tmp/avahi ${REPOSITORY}nss-mdns.tcz
		wget -P /tmp/avahi ${REPOSITORY}nss-mdns.tcz.md5.txt
		if [ $? = 0 ]; then
			echo '<p class="ok">[ OK ] Download successful.</p>'
			sudo pkill shairport-sync
			sudo chown -R tc:staff /tmp/avahi/*
			sudo chmod -R 755 /tmp/avahi/*
			sudo cp -r /tmp/avahi/* /mnt/mmcblk0p2/tce/optional            
			else
			echo '<p class="error">[ ERROR ] Avahi download unsuccessful, try again!</p>'
		fi
	else
		echo '<p class="error">[ ERROR ] Avahi not available in repository, try again later!</p>'
	fi
}





#========================================================================================
# ALSA output level section
#----------------------------------------------------------------------------------------
echo '<p class="info">[ INFO ] ALSAlevelout is set to: '$ALSAlevelout'</p>'
# Only do anything if variable is changed:
[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ]Original ALSAlevelout variable is: '$ori_ALSAlevelout'</p>'
[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ]Nwe ALSAlevelout variable is: '$ALSAlevelout'</p>'
if [ $ori_ALSAlevelout = $ALSAlevelout ]; then 
echo "ALSAlevelout variabel unchanged"
fi


#========================================================================================
# ALSA Equalizer section
#----------------------------------------------------------------------------------------
echo '<p class="info">[ INFO ] ALSA equalizer: '$ALSAeq'</p>'
#determination of the number of the current sound-card:

#if output is analog or HDMI then find the number of the used ALSA-card
	if [ $AUDIO = Analog ] || [ $AUDIO = HDMI ]; then
	CARDNO=$(sudo cat /proc/asound/cards | grep '\[' | grep 'ALSA' | awk '{print $1}')
	fi

#if output is different from analog or HDMI then find the number of the non-ALSA card
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

# Only do anything if variable is changed:
[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ]variable ori_ALSAeq is: '$ori_ALSAeq'</p>'
[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ]variable new ALSAeq is: '$ALSAeq'</p>'
if [ $ori_ALSAeq != $ALSAeq ]; then

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

else
echo "ALSAequal variabel unchanged"
fi
[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Card has number:'$CARDNO'.</p>'
[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] AUDIO='$AUDIO'</p>'



#========================================================================================
# CMD section
#----------------------------------------------------------------------------------------
echo '<p class="info">[ INFO ] CMD: '$CMD'</p>'
# Only do anything if variable is changed:
[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ]original CMD variable is: '$ori_CMD'</p>'
[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ]New CMD variable is: '$CMD'</p>'
if [ $ori_CMD != $CMD ]; then 
case "$CMD" in 
	"Default")
		echo '<p class="info">[ INFO ] CMD: '$CMD'</p>'
		sudo ./disableotg.sh
		;;
	"Slow")
		echo '<p class="info">[ INFO ] CMD: '$CMD'</p>'
		sudo ./enableotg.sh
		;;
	*)
		echo '<p class="error">[ ERROR ] CMD invalid: '$CMD'</p>'
		;;
esac
else
echo "CMD variabel unchanged"
fi

#========================================================================================
# SHAIRPORT section
#----------------------------------------------------------------------------------------
echo '<p class="info">[ INFO ] Shairport is enabled? '$SHAIRPORT'</p>'
# Only do anything if variable is changed:
[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ]original SHAIRPORT variable is: '$ori_SHAIRPORT'</p>'
[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ]New SHAIRPORT variable is: '$SHAIRPORT'</p>'
if [ $ori_SHAIRPORT != $SHAIRPORT ]; then 
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
		sudo sed -i '/avahi.tcz/d' /mnt/mmcblk0p2/tce/onboot.lst
		CLOSEOUT=""
		;;
	*)
		echo '<p class="error">[ ERROR ] Shairport selection invalid: '$SHAIRPORT'</p>'
		;;
esac

	[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Shairport variable is:'$SHAIRPORT'.</p>'
else
echo "SHAIRPORT variabel unchanged"
fi

#========================================================================================
# FIQ spilt section
#----------------------------------------------------------------------------------------
echo '<p class="info">[ INFO ] FIQ is set to: '$FIQ'</p>'
# Only do anything if variable is changed:
[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ]original FIG variable is: '$ori_FIQ'</p>'
[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ]New FIQ variable is: '$FIQ'</p>'
if [ $ori_FIQ != $FIQ ]; then 

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

else
echo "FIQ variabel unchanged"
fi
#----------------------------------------------------------------------------------------
pcp_save_to_config
pcp_backup
	[ $DEBUG = 1 ] && pcp_textarea "Current $ASOUNDCONF" "cat $ASOUNDCONF" 150
	[ $DEBUG = 1 ] && pcp_textarea "Current $ONBOOTLST" "cat $ONBOOTLST" 150
	[ $DEBUG = 1 ] && pcp_textarea "Current $CONFIGCFG" "cat $CONFIGCFG" 150
pcp_go_back_button
pcp_reboot_required

echo '</body>'
echo '</html>'