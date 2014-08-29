#!/bin/sh
. pcp-functions
pcp_variables
. $CONFIGCFG

echo '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">'
echo '<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">'
echo ''
echo '<head>'
echo '  <meta http-equiv="Cache-Control" content="no-cache" />'
echo '  <meta http-equiv="Pragma" content="no-cache" />'
echo '  <meta http-equiv="Expires" content="0" />'
echo '  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
echo '  <title>pCP - Choose output</title>'
echo '  <meta name="author" content="Steen" />'
echo '  <meta name="description" content="Choose output" />'
echo '  <link rel="stylesheet" type="text/css" href="../css/piCorePlayer.css" />'
echo '</head>'
echo ''
echo '<body>'

pcp_banner
pcp_running_script
pcp_httpd_query_string

# Decode variables using httpd, add quotes
AUDIO=`sudo /usr/local/sbin/httpd -d \"$AUDIO\"`

# Save variable $AUDIO to the config file
sudo sed -i "s/\(AUDIO *=*\).*/\1$AUDIO/" $CONFIGCFG

if [ $DEBUG = 1 ]; then
	echo '<p class="debug">[ DEBUG ] QUERY_STRING: '$QUERY_STRING'<br />'
	echo '                 [ DEBUG ] AUDIO: '$AUDIO'<br />'
	echo '                 [ DEBUG ] OUTPUT: '$OUTPUT'</p>'
fi

##### Needs work #####
# Could we just stop Squeezelite for everything? and start again at the end?
#####
# if using hifiberry DAC or Digi then stop player before removing the modules
if [ $OUTPUT = hw:CARD=sndrpihifiberry ]; then
	echo '<p class="info">[ INFO ] Stopping Squeezelite because HiFiBerry module will be manipulated.</p>'
	echo '<p class="warning">[ WARNING ] You will need to restart Squeezelite from the Main Page.</p>'
	pcp_squeezelite_stop
fi 
if [ $OUTPUT = hw:CARD=sndrpiiqaudioda ]; then
	echo '<p class="info">[ INFO ] Stopping Squeezelite because IQaudIO module will be manipulated.</p>'
    echo '<p class="warning">[ WARNING ] You will need to restart Squeezelite from the Main Page.</p>'
	pcp_squeezelite_stop
fi
sleep 1
######################

# Set the default settings
case "$AUDIO" in
	\"Analog*)
		echo '<p class="info">[ INFO ] Setting '$AUDIO'</p>'
		pcp_disable_i2s
		sudo ./disablehdmi.sh
		OUTPUT="sysdefault:CARD=ALSA"
		ALSA_PARAMS="80:::0"
		sudo sed -i "s/\(OUTPUT *=*\).*/\1$OUTPUT/" $CONFIGCFG
		sudo sed -i "s/\(ALSA_PARAMS *=*\).*/\1$ALSA_PARAMS/" $CONFIGCFG
		;;
	\"HDMI*)
		echo '<p class="info">[ INFO ] Setting '$AUDIO'</p>'
		pcp_disable_i2s
		sudo ./enablehdmi.sh
		OUTPUT="sysdefault:CARD=ALSA"
		ALSA_PARAMS="::32:0"
		sudo sed -i "s/\(OUTPUT *=*\).*/\1$OUTPUT/" $CONFIGCFG
		sudo sed -i "s/\(ALSA_PARAMS *=*\).*/\1$ALSA_PARAMS/" $CONFIGCFG
		;;
	\"USB*)
		echo '<p class="info">[ INFO ] Setting '$AUDIO'</p>'
		pcp_disable_i2s
		sudo ./disablehdmi.sh
		OUTPUT=" "
		ALSA_PARAMS="80:4::"
		sudo sed -i "s/\(OUTPUT *=*\).*/\1$OUTPUT/" $CONFIGCFG
		sudo sed -i "s/\(ALSA_PARAMS *=*\).*/\1$ALSA_PARAMS/" $CONFIGCFG
		;;
	\"I2SDAC*)
		echo '<p class="info">[ INFO ] Setting '$AUDIO'</p>'
		pcp_enable_i2s_dac
		sudo ./disablehdmi.sh
		OUTPUT="hw:CARD=sndrpihifiberry"
		ALSA_PARAMS="80:4::"
		sudo sed -i "s/\(OUTPUT *=*\).*/\1$OUTPUT/" $CONFIGCFG
		sudo sed -i "s/\(ALSA_PARAMS *=*\).*/\1$ALSA_PARAMS/" $CONFIGCFG
		;;
	\"I2SDIG*)
		echo '<p class="info">[ INFO ] Setting '$AUDIO'</p>'
		pcp_enable_i2s_digi
		sudo ./disablehdmi.sh
		OUTPUT="hw:CARD=sndrpihifiberry"
		ALSA_PARAMS="80:4::"
		sudo sed -i "s/\(OUTPUT *=*\).*/\1$OUTPUT/" $CONFIGCFG
		sudo sed -i "s/\(ALSA_PARAMS *=*\).*/\1$ALSA_PARAMS/" $CONFIGCFG
		;;
	\"IQaudio*)
		echo '<p class="info">[ INFO ] Setting '$AUDIO'</p>'
		pcp_enable_iqaudio_dac
		sudo ./disablehdmi.sh
		OUTPUT="hw:CARD=sndrpiiqaudioda"
		ALSA_PARAMS="80:4::"
		sudo sed -i "s/\(OUTPUT *=*\).*/\1$OUTPUT/" $CONFIGCFG
		sudo sed -i "s/\(ALSA_PARAMS *=*\).*/\1$ALSA_PARAMS/" $CONFIGCFG
		;;
	*)
		echo '<p class="error">[ ERROR ] Error setting '$AUDIO'</p>'
		;;
esac

pcp_show_config_cfg
pcp_backup
pcp_go_back_button

echo '</body>'
echo '</html>'
