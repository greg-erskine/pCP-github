#!/bin/sh

# Version: 0.03 2014-09-04 GE
#	Moved code to pcp_set_timezone routine.

# Version: 0.01 2014-06-24 GE
#	Original.

. pcp-functions
pcp_variables

echo '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">'
echo '<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">'
echo ''
echo '<head>'
echo '  <meta http-equiv="Cache-Control" content="no-cache" />'
echo '  <meta http-equiv="Pragma" content="no-cache" />'
echo '  <meta http-equiv="Expires" content="0" />'
echo '  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
echo '  <meta http-equiv="Refresh" content="15; url=tweaks.cgi">'
echo '  <title>pCP - Set Timezone</title>'
echo '  <meta name="author" content="Steen" />'
echo '  <meta name="description" content="Set Timezone" />'
echo '  <link rel="stylesheet" type="text/css" href="../css/piCorePlayer.css" />'
echo '  <script language="Javascript" src="../js/piCorePlayer.js"></script>'
echo '</head>'
echo ''
echo '<body>'

pcp_banner
pcp_running_script
pcp_httpd_query_string

# Save the encoded parameter to the config file, with quotes
sudo sed -i "s/\(TIMEZONE=\).*/\1\"$TIMEZONE\"/" $CONFIGCFG

# Decode variables using httpd, no quotes
TIMEZONE=`sudo /usr/local/sbin/httpd -d $TIMEZONE`

[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Timezone: '$TIMEZONE'</p>'

pcp_set_timezone

[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Local time:  '$(date)'</p>'

pcp_backup
pcp_reboot_button
pcp_go_back_button

echo '</body>'
echo '</html>'
