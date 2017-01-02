#!/bin/sh

# Version: 3.03 2016-10-14
#	Enhanced format. GE.
#	Set mmap=1 for all configurations. GE.

# Version: 3.02 2016-09-19
#	Added Hifiberry Digi+ Pro support. SBP.
#	Fixed problem with selection of certain cards. GE/SBP.

# Version: 3.00 2016-07-04
#	Added new DACs - justboomdigi, justboomdac, dionaudio-loco. SBP.

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

. pcp-soundcard-functions
. pcp-functions
pcp_variables
. $CONFIGCFG
# Store the original values so we can see if they are changed
ORIG_AUDIO="$AUDIO"

pcp_html_head "Choose output" "SBP" "10" "squeezelite.cgi"

pcp_banner
pcp_running_script
pcp_httpd_query_string

pcp_table_top "Choose output"

if [ $DEBUG -eq 1 ]; then
	echo '<p class="debug">[ DEBUG ] $ORIG_AUDIO: '$ORIG_AUDIO'<br />'
	echo '                 [ DEBUG ] $OUTPUT: '$OUTPUT'<br />'
	echo '                 [ DEBUG ] $ALSA_PARAMS: '$ALSA_PARAMS'</p>'
fi

if [ "$ORIG_AUDIO" = "$AUDIO" ]; then
	echo '<p class="info">[ INFO ] Audio output ($AUDIO) unchanged, still '$AUDIO'.</p>'
	echo '<p class="info">[ INFO ] Nothing to do.</p>'
	unset CHANGED
else
	echo '<p class="info">[ INFO ] Audio output ($AUDIO) changed from '$ORIG_AUDIO' to '$AUDIO'.</p>'
	# the next line is needed to clear OUTPUT from here when selecting USB. Whereas when pcp_read_chosen_audio is called from do_rebootstuff it should use the correct USB OUTPUT from newconfig.
	USBOUTPUT="" 
	CHANGED=TRUE
fi

# Only do something if $AUDIO variable has changed
if [ $CHANGED ]; then
	pcp_squeezelite_stop
	pcp_soundcontrol

	# To save the default dt-overlay parameter (PARAMS1) in config.cfg
	PARAM1="$PARAMS1"      # NEEDED AS PARAM1 IS THE VALUE SAVED IN CONFIG:CFG

	# Set the default settings
	echo '<p class="info">[ INFO ] Setting Audio output ($AUDIO) to '$AUDIO'</p>'

	# If ALSA equalizer is chosen output it should always be equal
	[ "$ALSAeq" = "yes" ] && OUTPUT="equal"

	# If ALSA equalizer is chosen then the card number in alsa equalizer part of asound.conf should be updated if another card is chosen
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

	# We might have an issue if both I2S DACs and USB DACs are attached at the same time.
	sed -i "s/plughw:.*,0/plughw:"$CARDNO",0/g" /etc/asound.conf

	#========================================================================================
	# FUTURE DEVELOPMENT. GE.
	#========================================================================================
	# CARDS=$(cat /proc/asound/card*/id)
	# NO_OF_CARDS=$(echo $CARDS | wc -w )
	#
	# tc@piScreen:/proc/asound/card1$ ls
	# id        pcm0c/    pcm0p/    stream0   usbbus    usbid     usbmixer
	#
	# cat /proc/asound/card1/pcm0p/info | grep 'id' | awk -F ": " '{print $2}'
	#
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

	if [ $DEBUG -eq 1 ]; then
		echo '<p class="debug">[ DEBUG ] $AUDIO: '$AUDIO'<br />'
		echo '                 [ DEBUG ] $OUTPUT: '$OUTPUT'<br />'
		echo '                 [ DEBUG ] $ALSA_PARAMS: '$ALSA_PARAMS'<br />'
		echo '                 [ DEBUG ] $DT_MODE: '$DT_MODE'</p>'
	fi

		if [ "$AUDIO" = "USB" ]; then
		STRING1='INFO: USB is chosen. Please check that the OUTPUT field is correct. Press Ok to check, and then reboot'
		SCRIPT1='squeezelite.cgi'
		pcp_confirmation_required
		fi

	pcp_squeezelite_start
	pcp_save_to_config
	pcp_read_chosen_audio
	[ $DEBUG -eq 1 ] && pcp_table_middle && pcp_textarea_inform "Updated config.cfg" "cat $CONFIGCFG" 380
	pcp_backup
fi

pcp_table_middle
pcp_go_back_button
pcp_table_end

pcp_footer
pcp_copyright

[ $CHANGED ] && pcp_reboot_required

echo '</body>'
echo '</html>'