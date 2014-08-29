#!/bin/sh
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

# Decode variables using httpd, no quotes
TIMEZONE=`sudo /usr/local/sbin/httpd -d $TIMEZONE`

[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Timezone: '$TIMEZONE'</p>'

echo "TZ="$TIMEZONE > /etc/sysconfig/timezone
unset TZ
[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] System time: '$(date)'</p>'
export TZ=$TIMEZONE
[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Local time:  '$(date)'</p>'

if [ -f /opt/.filetool.lst ]; then
	grep timezone /opt/.filetool.lst 1>&2
	result=$?
	if [ $result = 0 ]; then
		echo '<p class="debug">[ DEBUG ] timezone exists in /opt/.filetool.lst: '$result'</p>'
	else
		echo '<p class="debug">[ DEBUG ] timezone does not exist in /opt/.filetool.lst: '$result'</p>'
		sudo echo "etc/sysconfig/timezone" >> /opt/.filetool.lst
	fi
fi
pcp_backup
pcp_reboot_button
pcp_go_back_button

echo '</body>'
echo '</html>'
