#!/bin/sh

# Version: 7.0.0 2020-05-09

. pcp-functions
. pcp-soundcard-functions

# Store the original values so we can see if they are changed.
ORIG_AUDIO="$AUDIO"
ORIG_ALSA_PARAMS="$ALSA_PARAMS"

pcp_httpd_query_string
[ "$FROM_PAGE" = "" ] && FROM_PAGE="squeezelite.cgi"

pcp_html_head "Choose output" "SBP"

pcp_navbar
pcp_remove_query_string
pcp_httpd_query_string

#----------------------------------------------------------------------------------------
COLUMN1="col-3"
pcp_heading5 "Choose output"

[ $DEBUG -eq 1 ] &&
pcp_debug_variables "html" QUERY_STRING AUDIO OUTPUT DTOVERLAY PARAMS1 PARAMS2 PARAMS3 \
                           PARAMS4 PARAMS5 OUTPUT ALSA_PARAMS DT_MODE

if [ "$ORIG_AUDIO" = "$AUDIO" ]; then
	pcp_message INFO "Audio output unchanged, still $AUDIO." "html"
	if [ "$DEFAULTS" = "yes" ]; then
		pcp_message INFO "Setting default ALSA parameters." "html"
		pcp_squeezelite_stop "html"
		pcp_soundcontrol
		pcp_squeezelite_start "html"
		pcp_save_to_config
	else
		pcp_message INFO "Nothing to do." "html"
		unset CHANGED
	fi
else
	pcp_message INFO "Audio output changed from $ORIG_AUDIO to $AUDIO." "html"
	# The next line is needed to clear OUTPUT from here when selecting USB.
	# Whereas when pcp_read_chosen_audio is called from pcp_startup.sh it should use the correct USB OUTPUT from newpcp.
	USBOUTPUT=""
	CHANGED=TRUE
fi

# Only do something if $AUDIO variable has changed.
if [ $CHANGED ]; then
	pcp_squeezelite_stop "html"
	pcp_soundcontrol

	[ "$DEFAULTS" = "no" ] && ALSA_PARAMS=$ORIG_ALSA_PARAMS

	# To save the default dt-overlay parameter (PARAMS1) in pcp.cfg
	# Needed as PARAM1 is the value saved in pcp.cfg
	PARAM1="$PARAMS1"

	# Set the default settings
	pcp_message INFO "Setting Audio output to $AUDIO." "html"

	# If ALSA equalizer is chosen output it should always be equal.
	[ "$ALSAeq" = "yes" ] && OUTPUT="equal"

	# If ALSA equalizer is chosen then the card number in ALSA equalizer part of asound.conf should be updated if another card is chosen.
	# Determination of the number of the current sound card.

	# If output is analog or HDMI then find the number of the used ALSA card.
	if [ "$AUDIO" = "Analog" ] || [ "$AUDIO" = "HDMI" ]; then
		CARDNO=$(sudo cat /proc/asound/cards | grep '\[' | grep 'ALSA' | awk '{print $1}')
	fi

	# If output is different from analog or HDMI then find the number of the non-ALSA card.
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
		STRING1='INFO: USB is chosen. Check that the OUTPUT field is correct. Press [OK] to check, and then reboot.'
		SCRIPT1='squeezelite.cgi'
		pcp_confirmation_required
	fi

	pcp_squeezelite_start "html"
	pcp_save_to_config
	pcp_read_chosen_audio
	pcp_backup "html"
fi

echo '<div class="mt-3">'
pcp_redirect_button "Go Back" "$FROM_PAGE" 15
echo '<div>'

[ $CHANGED ] && pcp_reboot_required

pcp_html_end
