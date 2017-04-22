#!/bin/sh

# Version: 3.20 2017-03-08
#	Fixed pcp-xxx-functions issues. GE.

# Version: 3.10 2017-01-06
#	Enhanced format. GE.
#	Set mmap=1 for all configurations. GE.

# Version: 3.02 2016-09-19
#	Added Hifiberry Digi+ Pro support. SBP.
#	Fixed problem with selection of certain cards. GE/SBP.

# Version: 3.00 2016-07-04
#	Added new DACs - justboomdigi, justboomdac, dionaudio-loco. SBP.

# Version: 0.01 SBP
#	Original.

. pcp-functions
. pcp-soundcard-functions
#. $CONFIGCFG

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
	echo '                 [ DEBUG ] $DTOVERLAY: '$DTOVERLAY'<br />'
	echo '                 [ DEBUG ] $PARAMS1: '$PARAMS1'<br />'
	echo '                 [ DEBUG ] $PARAMS2: '$PARAMS2'<br />'
	echo '                 [ DEBUG ] $PARAMS3: '$PARAMS3'<br />'
	echo '                 [ DEBUG ] $PARAMS4: '$PARAMS4'<br />'
	echo '                 [ DEBUG ] $PARAMS5: '$PARAMS5'<br />'
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

	

		if [ "$AUDIO" = "USB" ]; then
		STRING1='INFO: USB is chosen. Please check that the OUTPUT field is correct. Press Ok to check, and then reboot'
		SCRIPT1='squeezelite.cgi'
		pcp_confirmation_required
		fi

	pcp_squeezelite_start
	pcp_save_to_config
	pcp_read_chosen_audio
if [ $DEBUG -eq 1 ]; then
		echo '<p class="debug">[ DEBUG ] $AUDIO: '$AUDIO'<br />'
		echo '                 [ DEBUG ] $OUTPUT: '$OUTPUT'<br />'
		echo '                 [ DEBUG ] $ALSA_PARAMS: '$ALSA_PARAMS'<br />'
		echo '                 [ DEBUG ] $DTOVERLAY: '$DTOVERLAY'<br />'
		echo '                 [ DEBUG ] $PARAMS1: '$PARAMS1'<br />'
		echo '                 [ DEBUG ] $PARAMS2: '$PARAMS2'<br />'
		echo '                 [ DEBUG ] $PARAMS3: '$PARAMS3'<br />'
		echo '                 [ DEBUG ] $PARAMS4: '$PARAMS4'<br />'
		echo '                 [ DEBUG ] $PARAMS5: '$PARAMS5'<br />'
		echo '                 [ DEBUG ] $DT_MODE: '$DT_MODE'</p>'
	fi
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