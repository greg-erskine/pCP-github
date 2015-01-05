#!/bin/sh

# Version: 0.01 2014-10-22 GE
#	Original.

. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "Controls Adv" "GE"

pcp_controls
pcp_banner
pcp_navigation
pcp_running_script
pcp_refresh_button

if [ $DEBUG = 1 ]; then
	echo '<p class="debug">[ DEBUG ] LMS IP: '$(pcp_lmsip)'<br />'
	echo '                 [ DEBUG ] MAC: '$(pcp_controls_mac_address)'</p>'
fi

pcp_lms_get_xxx() {
	RESULT=`( echo "$(pcp_controls_mac_address) $1"; echo "exit" ) | nc $(pcp_lmsip) 9090 | sed 's/ /\+/g' | sed 's/id/<br>id/g'`
	echo `sudo /usr/local/sbin/httpd -d $RESULT`
}


PLAYERS=$(pcp_lms_get_xxx "playlists 0 200")
echo '<div>'
echo '<p>Players: '$PLAYERS'</p>'
echo '</div>'

CONNECTED=$(pcp_lms_get "connected")
echo '<div>'
echo '<p>Connected: '$CONNECTED'</p>'
echo '</div>'

ARTIST=$(pcp_lms_get "artist")
echo '<div>'
echo '<p>Artist: '$ARTIST'</p>'
echo '</div>'

TITLE=$(pcp_lms_get "title")
echo '<div>'
echo '<p>Song: '$TITLE'</p>'
echo '</div>'

ALBUM=$(pcp_lms_get "album")
echo '<div>'
echo '<p>Album: '$ALBUM'</p>'
echo '</div>'

INFORMATION="$ARTIST - $TITLE - $ALBUM"
echo '<br />'
echo '<div style="width: 400px; border:1px solid black; ">'
echo '<marquee behavior="scroll" direction="left">'$INFORMATION'</marquee>'
echo '</div>'
echo '<br />'

echo '<div>'
echo '<img src="http://'$(pcp_lmsip)':9000/music/current/cover.jpg" alt="Currently playing" style="height: 250px; width: 250px; border:1px solid black;"/>'
echo '</div>'

echo '<br />'

pcp_footer

echo '</body>'
echo '</html>'