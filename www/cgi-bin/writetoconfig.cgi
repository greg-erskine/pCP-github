#!/bin/sh

# Version: 0.02 2014-08-22 SBP
#	Changed the back button to absolute path back to Squeezelite.cgi. Otherwise we would go in circles

# Version: 0.01 2014-06-25 GE
#	Original.


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
echo '  <title>pCP - Write to config.cfg</title>'
echo '  <meta name="author" content="Steen" />'
echo '  <meta name="description" content="Write to configuration file" />'
echo '  <link rel="stylesheet" type="text/css" href="../css/piCorePlayer.css" />'
echo '</head>'
echo ''
echo '<body>'
echo ''

pcp_controls
pcp_banner
pcp_navigation
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
	echo '<code>[ INFO ] '$QUERY_STRING'</code>'
	echo '<h2>[ DEBUG ] Parameters from decoded $QUERY_STRING</h2>'
	echo '<code>NAME=.'$NAME'.<br />'
	echo 'OUTPUT=.'$OUTPUT'.<br />'
	echo 'ALSA_PARAMS=.'$ALSA_PARAMS'.<br />'
	echo 'BUFFER_SIZE=.'$BUFFER_SIZE'.<br />'
	echo 'CODEC=.'$_CODEC'.<br />'
	echo 'PRIORITY=.'$PRIORITY'.<br />'
	echo 'MAX_RATE=.'$MAX_RATE'.<br />'
	echo 'UPSAMPLE=.'$UPSAMPLE'.<br />'
	echo 'MAC_ADDRESS=.'$MAC_ADDRESS'.<br />'
	echo 'SERVER_IP=.'$SERVER_IP'.<br />'
	echo 'LOGLEVEL=.'$LOGLEVEL'.<br />'
	echo 'LOGFILE=.'$LOGFILE'.<br />'
	echo 'DSDOUT=.'$DSDOUT'.<br />'
	echo 'VISULIZER=.'$VISULIZER'.<br />'
	echo 'OTHER=.'$OTHER'.<br />'
	echo '</code>'
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
	echo '<h2>[ DEBUG ] Parameters after reading config file</h2>'
	echo '<code>NAME=.'$NAME'.<br />'
	echo 'OUTPUT=.'$OUTPUT'.<br />'
	echo 'ALSA_PARAMS=.'$ALSA_PARAMS'.<br />'
	echo 'BUFFER_SIZE=.'$BUFFER_SIZE'.<br />'
	echo 'CODEC=.'$_CODEC'.<br />'
	echo 'PRIORITY=.'$PRIORITY'.<br />'
	echo 'MAX_RATE=.'$MAX_RATE'.<br />'
	echo 'UPSAMPLE=.'$UPSAMPLE'.<br />'
	echo 'MAC_ADDRESS=.'$MAC_ADDRESS'.<br />'
	echo 'SERVER_IP=.'$SERVER_IP'.<br />'
	echo 'LOGLEVEL=.'$LOGLEVEL'.<br />'
	echo 'LOGFILE=.'$LOGFILE'.<br />'
	echo 'DSDOUT=.'$DSDOUT'.<br />'
	echo 'VISULIZER=.'$VISULIZER'.<br />'
	echo 'OTHER=.'$OTHER'.<br />'
	echo '</code>'
fi

pcp_show_config_cfg
pcp_backup

#We needed a static link to squeezelite.cgi otherwise the go back button would go in circles if coming from usboption.cgi
#pcp_go_back_button
echo '<FORM METHOD="LINK" ACTION="squeezelite.cgi"><INPUT TYPE="submit" VALUE="Go back"></FORM>'

echo '</body>'
echo '</html>'
