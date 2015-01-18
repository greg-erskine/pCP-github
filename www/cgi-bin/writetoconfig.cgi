#!/bin/sh

# Version: 0.03 2014-12-12 GE
#	HTML5 format.
#	Minor mods.

# Version: 0.02 2014-08-22 SBP
#	Changed the back button to absolute path back to Squeezelite.cgi. Otherwise we would go in circles.

# Version: 0.01 2014-06-25 GE
#	Original.

. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "Write Write to config.cfg" "SBP" "15" "squeezelite.cgi"

pcp_banner
pcp_running_script
pcp_httpd_query_string

# Decode variables using httpd, add quotes
NAME=`sudo /usr/local/sbin/httpd -d \"$NAME\"`
OUTPUT=`sudo /usr/local/sbin/httpd -d \"$OUTPUT\"`
ALSA_PARAMS=`sudo /usr/local/sbin/httpd -d \"$ALSA_PARAMS\"`
BUFFER_SIZE=`sudo /usr/local/sbin/httpd -d \"$BUFFER_SIZE\"`
_CODEC=`sudo /usr/local/sbin/httpd -d \"$_CODEC\"`
PRIORITY=`sudo /usr/local/sbin/httpd -d \"$PRIORITY\"`
MAX_RATE=`sudo /usr/local/sbin/httpd -d \"$MAX_RATE\"`
UPSAMPLE=`sudo /usr/local/sbin/httpd -d \"$UPSAMPLE\"`
MAC_ADDRESS=`sudo /usr/local/sbin/httpd -d \"$MAC_ADDRESS\"`
SERVER_IP=`sudo /usr/local/sbin/httpd -d \"$SERVER_IP\"`
LOGLEVEL=`sudo /usr/local/sbin/httpd -d \"$LOGLEVEL\"`
LOGFILE=`sudo /usr/local/sbin/httpd -d \"$LOGFILE\"`
DSDOUT=`sudo /usr/local/sbin/httpd -d \"$DSDOUT\"`
VISULIZER=`sudo /usr/local/sbin/httpd -d \"$VISULIZER\"`
OTHER=`sudo /usr/local/sbin/httpd -d \"$OTHER\"`

if [ $DEBUG = 1 ]; then
	echo '<p class="debug">[ DEBUG ] Parameters after decoding + . added<br /><br />'
	echo '                 [ DEBUG ] NAME=.'$NAME'.<br />'
	echo '                 [ DEBUG ] OUTPUT=.'$OUTPUT'.<br />'
	echo '                 [ DEBUG ] ALSA_PARAMS=.'$ALSA_PARAMS'.<br />'
	echo '                 [ DEBUG ] BUFFER_SIZE=.'$BUFFER_SIZE'.<br />'
	echo '                 [ DEBUG ] CODEC=.'$_CODEC'.<br />'
	echo '                 [ DEBUG ] PRIORITY=.'$PRIORITY'.<br />'
	echo '                 [ DEBUG ] MAX_RATE=.'$MAX_RATE'.<br />'
	echo '                 [ DEBUG ] UPSAMPLE=.'$UPSAMPLE'.<br />'
	echo '                 [ DEBUG ] MAC_ADDRESS=.'$MAC_ADDRESS'.<br />'
	echo '                 [ DEBUG ] SERVER_IP=.'$SERVER_IP'.<br />'
	echo '                 [ DEBUG ] LOGLEVEL=.'$LOGLEVEL'.<br />'
	echo '                 [ DEBUG ] LOGFILE=.'$LOGFILE'.<br />'
	echo '                 [ DEBUG ] DSDOUT=.'$DSDOUT'.<br />'
	echo '                 [ DEBUG ] VISULIZER=.'$VISULIZER'.<br />'
	echo '                 [ DEBUG ] OTHER=.'$OTHER'.</p>'
fi

# Save the parameters to the config file
sudo sed -i "s/\(NAME=\).*/\1$NAME/" $CONFIGCFG
sudo sed -i "s/\(OUTPUT=\).*/\1$OUTPUT/" $CONFIGCFG
sudo sed -i "s/\(ALSA_PARAMS=\).*/\1$ALSA_PARAMS/" $CONFIGCFG
sudo sed -i "s/\(BUFFER_SIZE=\).*/\1$BUFFER_SIZE/" $CONFIGCFG
sudo sed -i "s/\(_CODEC=\).*/\1$_CODEC/" $CONFIGCFG
sudo sed -i "s/\(PRIORITY=\).*/\1$PRIORITY/" $CONFIGCFG
sudo sed -i "s/\(MAX_RATE=\).*/\1$MAX_RATE/" $CONFIGCFG
sudo sed -i "s/\(UPSAMPLE=\).*/\1$UPSAMPLE/" $CONFIGCFG
sudo sed -i "s/\(MAC_ADDRESS=\).*/\1$MAC_ADDRESS/" $CONFIGCFG
sudo sed -i "s/\(SERVER_IP=\).*/\1$SERVER_IP/" $CONFIGCFG
sudo sed -i "s/\(LOGLEVEL=\).*/\1$LOGLEVEL/" $CONFIGCFG
sudo sed -i "s/\(LOGFILE=\).*/\1$LOGFILE/" $CONFIGCFG
sudo sed -i "s/\(DSDOUT=\).*/\1$DSDOUT/" $CONFIGCFG
sudo sed -i "s/\(VISULIZER=\).*/\1$VISULIZER/" $CONFIGCFG
sudo sed -i "s/\(OTHER=\).*/\1$OTHER/" $CONFIGCFG

. $CONFIGCFG

if [ $DEBUG = 1 ]; then
	echo '<p class="debug">[ DEBUG ] Parameters after reading config file + . added<br /><br />'
	echo '                 [ DEBUG ] NAME=.'$NAME'.<br />'
	echo '                 [ DEBUG ] OUTPUT=.'$OUTPUT'.<br />'
	echo '                 [ DEBUG ] ALSA_PARAMS=.'$ALSA_PARAMS'.<br />'
	echo '                 [ DEBUG ] BUFFER_SIZE=.'$BUFFER_SIZE'.<br />'
	echo '                 [ DEBUG ] CODEC=.'$_CODEC'.<br />'
	echo '                 [ DEBUG ] PRIORITY=.'$PRIORITY'.<br />'
	echo '                 [ DEBUG ] MAX_RATE=.'$MAX_RATE'.<br />'
	echo '                 [ DEBUG ] UPSAMPLE=.'$UPSAMPLE'.<br />'
	echo '                 [ DEBUG ] MAC_ADDRESS=.'$MAC_ADDRESS'.<br />'
	echo '                 [ DEBUG ] SERVER_IP=.'$SERVER_IP'.<br />'
	echo '                 [ DEBUG ] LOGLEVEL=.'$LOGLEVEL'.<br />'
	echo '                 [ DEBUG ] LOGFILE=.'$LOGFILE'.<br />'
	echo '                 [ DEBUG ] DSDOUT=.'$DSDOUT'.<br />'
	echo '                 [ DEBUG ] VISULIZER=.'$VISULIZER'.<br />'
	echo '                 [ DEBUG ] OTHER=.'$OTHER'.</p>'
fi

pcp_show_config_cfg
pcp_backup

pcp_go_back_button

echo '</body>'
echo '</html>'