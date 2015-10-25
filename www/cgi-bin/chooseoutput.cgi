#!/bin/sh

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

pcp_banner
pcp_running_script
pcp_squeezelite_stop
pcp_httpd_query_string

if [ $DEBUG = 1 ]; then
	echo '<p class="debug">[ DEBUG ] $AUDIO: '$AUDIO'<br />'
	echo '                 [ DEBUG ] $OUTPUT: '$OUTPUT'<br />'
	echo '                 [ DEBUG ] $ALSA_PARAMS: '$ALSA_PARAMS'</p>'
fi

echo '<textarea class="white" style="height: 80px;" >'
echo '[ INFO ] Setting $AUDIO to '$AUDIO

# Set the default settings
case "$AUDIO" in
	Analog*)
		pcp_mount_mmcblk0p1_nohtml
		pcp_disable_i2s
		pcp_disable_HDMI
		OUTPUT="sysdefault:CARD=ALSA"
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
	I2SpIQaudIO*)
		pcp_mount_mmcblk0p1_nohtml
		pcp_enable_iqaudio_dac_p
		pcp_disable_HDMI
		OUTPUT="hw:CARD=IQaudIODAC"
		ALSA_PARAMS="80:4::"
		pcp_umount_mmcblk0p1_nohtml
		;;
	*)
		echo '[ ERROR ] Error setting $AUDIO to '$AUDIO
		;;
esac

echo '</textarea>'

if [ $DEBUG = 1 ]; then
	echo '<p class="debug">[ DEBUG ] $AUDIO: '$AUDIO'<br />'
	echo '                 [ DEBUG ] $OUTPUT: '$OUTPUT'<br />'
	echo '                 [ DEBUG ] $ALSA_PARAMS: '$ALSA_PARAMS'<br />'
	echo '                 [ DEBUG ] $DT_MODE: '$DT_MODE'</p>'
fi

pcp_save_to_config

pcp_textarea "" "cat $CONFIGCFG" 380

pcp_squeezelite_start

pcp_backup
pcp_go_back_button
pcp_reboot_button			# DELETE THIS??????

pcp_reboot_required

echo '</body>'
echo '</html>'