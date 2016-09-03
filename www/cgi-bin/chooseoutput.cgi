#!/bin/sh

# Version: 3.00 2016-07-04 SBP.
#	Added support for new DACs.

# Version: 0.11 2016-03-25 GE
#	Updated raspidac3 settings, CARD=Card.

# Version: 0.10 2016-02-21 SBP
#	Modified CARDNO.
#	Set OUTPUT to equal for alsaequal.
#	Added support for raspidac3 and rpi_dac.

# Version: 0.09 2016-01-15 GE
#	Deleted Reboot button.

# Version: 0.08 2015-10-09 SBP
#	Removed httpd decoding.
#	Added pcp_reboot_required.
#	Added _nohtml to mount and umount routines.

# Version: 0.07 2015-06-10 SBP
#	Modified to handle quotes around variables more consistently.

# Version: 0.06 2014-12-11 GE
#	HTML5 formatting.

# Version: 0.05 2014-11-03 SBP
#	Added support for the HiFiBerry AMP.

# Version: 0.04 2014-10-24 GE
#	Added textareas.
#	Using pcp_html_head now.
#	Minor tidyup.

# Version: 0.03 2014-09-25 SBP
#	Added support for the HiFiBerry DAC+ and Digi+.
#   Added support for the IQaudIO+ DAC.

# Version: 0.02 2014-08-08 GE
#	Major clean up.

# Version: 0.01 SBP
#	Original.

. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "Choose output" "SBP" "10" "squeezelite.cgi"

# Store the original values so we can see if they are changed
ORIG_AUDIO=$AUDIO
CHANGED=0

pcp_banner
pcp_running_script
pcp_squeezelite_stop
pcp_httpd_query_string

if [ $DEBUG -eq 1 ]; then
	echo '<p class="debug">[ DEBUG ] $AUDIO: '$AUDIO'<br />'
	echo '                 [ DEBUG ] $OUTPUT: '$OUTPUT'<br />'
	echo '                 [ DEBUG ] $ALSA_PARAMS: '$ALSA_PARAMS'</p>'
fi

echo '<textarea class="white" style="height: 80px;" >'
# Set the default settings
# Only do something if variable is changed
if [ "$ORIG_AUDIO" != "$AUDIO" ] ; then
echo '[ INFO ] Setting $AUDIO to '$AUDIO
case "$AUDIO" in
	Analog*)
		pcp_mount_mmcblk0p1_nohtml
		pcp_disable_i2s
		pcp_disable_HDMI
		OUTPUT="hw:CARD=ALSA"
		ALSA_PARAMS="80:::0"
		pcp_umount_mmcblk0p1_nohtml
	;;
	HDMI*)
		pcp_mount_mmcblk0p1_nohtml
		pcp_disable_i2s
		pcp_disable_HDMI
		pcp_enable_HDMI
		OUTPUT="sysdefault:CARD=ALSA"
		ALSA_PARAMS="::32:0"
		pcp_umount_mmcblk0p1_nohtml
		sudo amixer cset numid=3 2 >/dev/null 2>&1
	;;
	USB*)
		pcp_mount_mmcblk0p1_nohtml
		pcp_disable_i2s
		pcp_disable_HDMI
		OUTPUT=""
		ALSA_PARAMS="80:4::"
		pcp_umount_mmcblk0p1_nohtml
	;;
	I2SDAC*)
		pcp_mount_mmcblk0p1_nohtml
		pcp_enable_i2s_dac
		pcp_disable_HDMI
		OUTPUT="hw:CARD=sndrpihifiberry"
		ALSA_PARAMS="80:4::"
		pcp_umount_mmcblk0p1_nohtml
	;;
	I2SDIG*)
		pcp_mount_mmcblk0p1_nohtml
		pcp_enable_i2s_digi
		pcp_disable_HDMI
		OUTPUT="hw:CARD=sndrpihifiberry"
		ALSA_PARAMS="80:4::"
		pcp_umount_mmcblk0p1_nohtml
	;;
	I2SAMP*)
		pcp_mount_mmcblk0p1_nohtml
		pcp_enable_i2s_amp
		pcp_disable_HDMI
		OUTPUT="hw:CARD=sndrpihifiberry"
		ALSA_PARAMS="80:4::"
		pcp_umount_mmcblk0p1_nohtml
	;;
	IQaudio*)
		pcp_mount_mmcblk0p1_nohtml
		pcp_enable_iqaudio_dac
		pcp_disable_HDMI
		OUTPUT="hw:CARD=IQaudIODAC"
		ALSA_PARAMS="80:4::"
		pcp_umount_mmcblk0p1_nohtml
	;;
	I2SpIQAMP*)
		pcp_mount_mmcblk0p1_nohtml
		pcp_enable_iqaudio_amp
		pcp_disable_HDMI
		OUTPUT="hw:CARD=IQaudIODAC"
		ALSA_PARAMS="80:4::"
		pcp_umount_mmcblk0p1_nohtml
	;;
	I2SpDAC*)
		pcp_mount_mmcblk0p1_nohtml
		pcp_enable_hifiberry_dac_p
		pcp_disable_HDMI
		OUTPUT="hw:CARD=sndrpihifiberry"
		ALSA_PARAMS="80:4::"
		pcp_umount_mmcblk0p1_nohtml
	;;
	I2SpDIG*)
		pcp_mount_mmcblk0p1_nohtml
		pcp_enable_i2s_digi
		pcp_disable_HDMI
		OUTPUT="hw:CARD=sndrpihifiberry"
		ALSA_PARAMS="80:4::"
		pcp_umount_mmcblk0p1_nohtml
	;;
	I2SpDIGpro*)
		pcp_mount_mmcblk0p1_nohtml
		pcp_enable_hifiberry_digi_pro
		pcp_disable_HDMI
		OUTPUT="hw:CARD=sndrpihifiberrydigi"
		ALSA_PARAMS="80:4::"
		pcp_umount_mmcblk0p1_nohtml
	;;
	I2SpIQaudIO*)
		pcp_mount_mmcblk0p1_nohtml
		pcp_enable_iqaudio_dac_p
		pcp_disable_HDMI
		OUTPUT="hw:CARD=IQaudIODAC"
		ALSA_PARAMS="80:4::"
		pcp_umount_mmcblk0p1_nohtml
	;;
	I2SpIQaudIOdigi*)
		pcp_mount_mmcblk0p1_nohtml
		pcp_enable_iqaudio_digi
		pcp_disable_HDMI
		OUTPUT="hw:CARD=IQaudIODigi"
		ALSA_PARAMS="80:4::"
		pcp_umount_mmcblk0p1_nohtml
	;;
	justboomdac*)
		pcp_mount_mmcblk0p1_nohtml
		pcp_enable_justboomdac
		pcp_disable_HDMI
		OUTPUT="hw:CARD=sndrpijustboomd"
		ALSA_PARAMS="80:4::"
		pcp_umount_mmcblk0p1_nohtml
	;;
	justboomdigi*)
		pcp_mount_mmcblk0p1_nohtml
		pcp_enable_justboomdigi
		pcp_disable_HDMI
		OUTPUT="hw:CARD=sndrpijustboomd"
		ALSA_PARAMS="80:4::"
		pcp_umount_mmcblk0p1_nohtml
	;;
	raspidac3*)
		pcp_mount_mmcblk0p1_nohtml
		pcp_enable_raspidac3
		pcp_disable_HDMI
		OUTPUT="hw:CARD=Card"
		ALSA_PARAMS="80:4::"
		pcp_umount_mmcblk0p1_nohtml
	;;
	rpi_dac*)
		pcp_mount_mmcblk0p1_nohtml
		pcp_enable_rpi_dac
		pcp_disable_HDMI
		OUTPUT="hw:CARD=snd-rpi-dac"
		ALSA_PARAMS="80:4::"
		pcp_umount_mmcblk0p1_nohtml
	;;
	LOCO_dac*)
		pcp_mount_mmcblk0p1_nohtml
		pcp_enable_LOCO_dac
		pcp_disable_HDMI
		OUTPUT="hw:CARD=sndrpidionaudio"
		ALSA_PARAMS="80:4::"
		pcp_umount_mmcblk0p1_nohtml
	;;

	*)
		echo '[ ERROR ] Error setting $AUDIO to '$AUDIO
	;;
esac
CHANGED=1
else
	echo '[ INFO ] AUDIO variable unchanged.'
fi
echo '</textarea>'

#----If ALSA equalizer is chosen output should always be equal----
[ "$ALSAeq" = "yes" ] && OUTPUT="equal"

#----If ALSA equalizer is chosen then the card number in alsa equalizer part of asound.conf should be updated if another card is chosen----
# Determination of the number of the current sound-card

# If output is analog or HDMI then find the number of the used ALSA-card
if [ "$AUDIO" = "Analog" ] || [ "$AUDIO" = "HDMI" ]; then
	CARDNO=$(sudo cat /proc/asound/cards | grep '\[' | grep 'ALSA' | awk '{print $1}')
fi

# If output is different from analog or HDMI then find the number of the non-ALSA card
# For now we simply set the card number to 1. The problem is that I2S cards needs a reboot to show up.
if [ "$AUDIO" != "Analog" ] && [ "$AUDIO" != "HDMI" ]; then
	CARDNO=1
fi

#========================================================================================
#CARDS=$(cat /proc/asound/card*/id)
#NO_OF_CARDS=$(echo $CARDS | wc -w )

#tc@piScreen:/proc/asound/card1$ ls
#id        pcm0c/    pcm0p/    stream0   usbbus    usbid     usbmixer

#cat /proc/asound/card1/pcm0p/info | grep 'id' | awk -F ": " '{print $2}'

#========================================================================================
#case $AUDIO in
#	Analog|HDMI)
#		CARDNO=$(cat /proc/asound/cards | grep ': bcm2835' | grep 'ALSA' | awk '{print $1}')
#	;;
#	USB*)
#		# Do USB cards always have USB in description?
#		CARDNO=$(cat /proc/asound/cards | grep '\]:' | grep 'USB' | awk '{print $1}')
#	;;
#	*)
#		#CARDNO=$(cat /proc/asound/cards | grep '\]:' | grep -v 'ALSA' | grep -v 'USB' | awk '{print $1}')
#		CARDNO=1
#	;;
#esac
#========================================================================================

sed -i "s/plughw:.*,0/plughw:"$CARDNO",0/g" /etc/asound.conf
# We might have an issue if both I2S DACS and USB DACs are attached at the same time..

if [ $DEBUG -eq 1 ]; then
	echo '<p class="debug">[ DEBUG ] $AUDIO: '$AUDIO'<br />'
	echo '                 [ DEBUG ] $OUTPUT: '$OUTPUT'<br />'
	echo '                 [ DEBUG ] $ALSA_PARAMS: '$ALSA_PARAMS'<br />'
	echo '                 [ DEBUG ] $DT_MODE: '$DT_MODE'</p>'
fi



pcp_squeezelite_start

if [ "$CHANGED" = "1" ]; then
pcp_save_to_config
pcp_textarea "" "cat $CONFIGCFG" 380
pcp_backup
pcp_reboot_required
fi
pcp_go_back_button

echo '</body>'
echo '</html>'