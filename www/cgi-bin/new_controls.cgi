#!/bin/sh

# Version: 0.02 2014-07-18 GE
# 	Added support for wireless connection, pcp_controls_mac_address.
#
# Version: 0.01 2014-06-27 GE
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
echo '  <title>pCP - Controls</title>'
echo '  <meta name="author" content="Steen" />'
echo '  <meta name="description" content="Controls" />'
echo '  <link rel="stylesheet" type="text/css" href="../css/piCorePlayer.css" />'
echo '  <script language="Javascript" src="../js/piCorePlayer.js"></script>'
echo '</head>'
echo ''

[ $DEBUG = 1 ] && echo '<body>' || echo '<body onload="javascript:location.href=document.referrer;">'

[ $DEBUG = 1 ] && pcp_controls && pcp_banner && pcp_navigation && pcp_running_script

pcp_httpd_query_string

PLAYER_MAC=$(pcp_controls_mac_address)

if [ $DEBUG = 1 ]; then
	echo '<p class="debug">[ DEBUG ] Command: '$COMMAND'<br />'
	echo '                 [ DEBUG ] $MAC_ADDRESS: '$MAC_ADDRESS'<br />'
	echo '                 [ DEBUG ] Physical MAC: '$(pcp_eth0_mac_address)'<br />'
	echo '                 [ DEBUG ] $PLAYER_MAC: '$PLAYER_MAC'<br />'
	echo '                 [ DEBUG ] LMS IP address: '$LMSIP'</p>'
fi

# $LMSIP, the LMS server ip address, needs to be manually set in pcp-functions
case $COMMAND in
	random_tracks)
		echo "$PLAYER_MAC randomplay tracks" | telnet $LMSIP:9090
		;;
	volume_up)
		echo "$PLAYER_MAC mixer volume +5" | telnet $LMSIP:9090
		;;
	volume_down)
		echo "$PLAYER_MAC mixer volume -5" | telnet $LMSIP:9090
		;;		
	track_next)
		echo "$PLAYER_MAC playlist index +1" | telnet $LMSIP:9090
		;;
	track_prev)
		echo "$PLAYER_MAC playlist index -1" | telnet $LMSIP:9090
		;;
	play)
		echo "$PLAYER_MAC play" | telnet $LMSIP:9090
		;;
	stop)
	    echo "$PLAYER_MAC stop" | telnet $LMSIP:9090
		;;		
esac

[ $DEBUG = 1 ] && pcp_footer

echo '</body>'
echo '</html>'
