#!/bin/sh

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
#. $CONFIGCFG

pcp_html_head "Write to Audio Tweak" "SBP" "15" "tweaks.cgi"

pcp_banner
pcp_running_script
pcp_httpd_query_string

#========================================================================================
# ALSA output level section
#----------------------------------------------------------------------------------------
echo '<p class="info">[ INFO ] ALSAlevelout is set to: '$ALSAlevelout'</p>'

#========================================================================================
# ALSA Equalizer section
#----------------------------------------------------------------------------------------
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
		if [ $AUDIO = "Analog" ] || [ $AUDIO = "HDMI" ]; then
			sed -i 's/plughw:1,0/plughw:0,0/g' /etc/asound.conf
		fi
		if [ $AUDIO = "USB" ] || [ $AUDIO = "I2S" ]; then
			sed -i 's/plughw:0,0/plughw:1,0/g' /etc/asound.conf
		fi
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

[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] AUDIO='$AUDIO'</p>'
[ $DEBUG = 1 ] && pcp_textarea "Current $ASOUNDCONF" "cat $ASOUNDCONF" 150
[ $DEBUG = 1 ] && pcp_textarea "Current $ONBOOTLST" "cat $ONBOOTLST" 150

#========================================================================================
# CMD section
#----------------------------------------------------------------------------------------
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

#========================================================================================
# FIQ spilt section
#----------------------------------------------------------------------------------------
echo '<p class="info">[ INFO ] FIQ is set to: '$FIQ'</p>'
pcp_mount_mmcblk0p1

if mount | grep $VOLUME; then
	# Remove fiq settings
	sed -i 's/dwc_otg.fiq_fsm_mask=0x[1-8] \+//g' /mnt/mmcblk0p1/cmdline.txt
	# Add FIQ settings from config file
	sed -i '1 s/^/dwc_otg.fiq_fsm_mask='$FIQ' /' /mnt/mmcblk0p1/cmdline.txt

	[ $DEBUG = 1 ] && pcp_show_cmdline_txt
	pcp_umount_mmcblk0p1
else
	echo '<p class="error">[ ERROR ] '$VOLUME' not mounted</p>'
fi

#----------------------------------------------------------------------------------------
pcp_save_to_config
pcp_backup
[ $DEBUG = 1 ] && pcp_show_config_cfg
pcp_go_back_button
pcp_reboot_required

echo '</body>'
echo '</html>'