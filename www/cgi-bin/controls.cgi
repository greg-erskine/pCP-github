#!/bin/sh

# Version: 0.05 2014-12-11 GE
#	HTML5 formatting.

# Version: 0.04 2014-10-02 GE
#	Added variable $SERVER_IP_NO_PORT.

# Version: 0.03 2014-09-09 GE
#	Removed $LMSIP using $SERVER_IP instead.

# Version: 0.02 2014-07-18 GE
# 	Added support for wireless connection, pcp_controls_mac_address.

# Version: 0.01 2014-06-27 GE
#	Original.

. pcp-lms-functions

. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "Controls" "GE"

#====================================Fix=================================================

#echo '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">'
#echo '<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">'
#echo ''
#echo '<head>'
#echo '  <meta http-equiv="Cache-Control" content="no-cache" />'
#echo '  <meta http-equiv="Pragma" content="no-cache" />'
#echo '  <meta http-equiv="Expires" content="0" />'
#echo '  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
#echo '  <title>pCP - Controls</title>'
#echo '  <meta name="author" content="Steen" />'
#echo '  <meta name="description" content="Controls" />'
#echo '  <link rel="stylesheet" type="text/css" href="../css/piCorePlayer.css" />'
#echo '  <script language="Javascript" src="../js/piCorePlayer.js"></script>'
#echo '</head>'
#echo ''

[ $DEBUG = 1 ] && echo '<body>' || echo '<body onload="javascript:location.href=document.referrer;">'

#====================================Fix=================================================

[ $DEBUG = 1 ] && pcp_controls && pcp_banner && pcp_navigation && pcp_running_script

pcp_httpd_query_string

PLAYER_MAC=$(pcp_controls_mac_address)
SERVER_IP_NO_PORT=`echo $SERVER_IP | awk -F: '{ print $1 }'`

if [ $DEBUG = 1 ]; then
	echo '<p class="debug">[ DEBUG ] Command: '$COMMAND'<br />'
	echo '                 [ DEBUG ] LMS IP address: '$SERVER_IP'<br />'
	echo '                 [ DEBUG ] LMS IP no port: '$SERVER_IP_NO_PORT'<br />'
	echo '                 [ DEBUG ] $MAC_ADDRESS: '$MAC_ADDRESS'<br />'
	echo '                 [ DEBUG ] Physical MAC: '$(pcp_eth0_mac_address)'<br />'
	echo '                 [ DEBUG ] Wireless MAC: '$(pcp_wlan0_mac_address)'<br />'
	echo '                 [ DEBUG ] $PLAYER_MAC: '$PLAYER_MAC'</p>'
fi

case $COMMAND in
	random_tracks)
		pcp_lms_randomplay
		;;
	volume_up)
		pcp_lms_volume_up
		;;
	volume_down)
		pcp_lms_volume_down
		;;
	track_next)
		pcp_lms_next
		;;
	track_prev)
		pcp_lms_prev
		;;
	play)
		pcp_lms_play
		;;
	stop)
	    pcp_lms_stop
		;;
esac

[ $DEBUG = 1 ] && pcp_footer

echo '</body>'
echo '</html>'