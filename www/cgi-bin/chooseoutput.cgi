#!/bin/sh

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

# Decode variables using httpd
AUDIO=`sudo $HTPPD -d $AUDIO`

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
		pcp_disable_i2s
		sudo ./disablehdmi.sh
		OUTPUT="sysdefault:CARD=ALSA"
		ALSA_PARAMS="80:::0"
		;;
	HDMI*)
		pcp_disable_i2s
		sudo ./enablehdmi.sh
		OUTPUT="sysdefault:CARD=ALSA"
		ALSA_PARAMS="::32:0"
		;;
	USB*)
		pcp_disable_i2s
		sudo ./disablehdmi.sh
		OUTPUT=""
		ALSA_PARAMS="80:4::"
		;;
	I2SDAC*)
		pcp_enable_i2s_dac
		sudo ./disablehdmi.sh
		OUTPUT="hw:CARD=sndrpihifiberry"
		ALSA_PARAMS="80:4::"
		;;
	I2SDIG*)
		pcp_enable_i2s_digi
		sudo ./disablehdmi.sh
		OUTPUT="hw:CARD=sndrpihifiberry"
		ALSA_PARAMS="80:4::"
		;;
	I2SAMP*)
		pcp_enable_i2s_amp
		sudo ./disablehdmi.sh
		OUTPUT="hw:CARD=sndrpihifiberry"
		ALSA_PARAMS="80:4::"
		;;
	IQaudio*)
		pcp_enable_iqaudio_dac
		sudo ./disablehdmi.sh
		OUTPUT="hw:CARD=IQaudIODAC"
		ALSA_PARAMS="80:4::"
		;;
	I2SpDAC*)
		pcp_enable_hifiberry_dac_p
		sudo ./disablehdmi.sh
		OUTPUT="hw:CARD=sndrpihifiberry"
		ALSA_PARAMS="80:4::"
		;;	
	I2SpDIG*)
		pcp_enable_i2s_digi
		sudo ./disablehdmi.sh
		OUTPUT="hw:CARD=sndrpihifiberry"
		ALSA_PARAMS="80:4::"
		;;
	I2SpIQaudIO*)
		pcp_enable_iqaudio_dac
		sudo ./disablehdmi.sh
		OUTPUT="hw:CARD=IQaudIODAC"
		ALSA_PARAMS="80:4::"
		;;
	*)
		echo '[ ERROR ] Error setting $AUDIO to '$AUDIO
		;;
esac

echo '</textarea>'

if [ $DEBUG = 1 ]; then
	echo '<p class="debug">[ DEBUG ] $AUDIO: '$AUDIO'<br />'
	echo '                 [ DEBUG ] $OUTPUT: '$OUTPUT'<br />'
	echo '                 [ DEBUG ] $ALSA_PARAMS: '$ALSA_PARAMS'</p>'
fi

# Save variable to the config file, add quotes
sudo sed -i "s/\(AUDIO *=*\).*/\1\"$AUDIO\"/" $CONFIGCFG
sudo sed -i "s/\(OUTPUT *=*\).*/\1\"$OUTPUT\"/" $CONFIGCFG
sudo sed -i "s/\(ALSA_PARAMS *=*\).*/\1\"$ALSA_PARAMS\"/" $CONFIGCFG

pcp_textarea "" "cat $CONFIGCFG" 380

pcp_squeezelite_start

pcp_backup
pcp_go_back_button

echo '</body>'
echo '</html>'