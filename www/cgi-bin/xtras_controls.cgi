#!/bin/sh

# Version: 0.01 2014-10-22 GE
#	Original.

. pcp-lms-functions
. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "Controls Adv" "GE"

#pcp_favorites
pcp_controls
pcp_banner
pcp_navigation
pcp_running_script
pcp_refresh_button

if [ $DEBUG = 1 ]; then
	echo '<p class="debug">[ DEBUG ] LMS IP: '$(pcp_lmsip)'<br />'
	echo '                 [ DEBUG ] MAC: '$(pcp_controls_mac_address)'</p>'
fi

#========================================================================================
echo '<h1>pcp-lms-functions experiment</h1>'

echo '<div>'

echo '<p>Connected: '$(pcp_lms_is_connected)'</p>'

echo '<p>Player count: '$(pcp_lms_get_player_count)'</p>'
echo '<p>Artist: '$(pcp_lms_get_artist)'</p>'
echo '<p>Title: '$(pcp_lms_get_title)'</p>'
echo '<p>Album: '$(pcp_lms_get_album)'</p>'

echo '<p>Show: '$(pcp_lms_show)'</p>'


#pcp_lms_next


echo '</div>'

#===============================================================
echo '<h1>Old functions</h1>'

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

exit

#========================================================================================
echo '<h1>User Commands experiment</h1>' 

echo 	'<textarea rows="20">'

pcp_user_commands

echo 	'</textarea>'

for i in 1 2
do
set -x
USER_COMMAND_$i=`sudo /usr/local/sbin/httpd -d $USER_COMMAND_$i`
echo $USER_COMMAND_${i}
eval "$USER_COMMAND_${i}"
echo "<br />"

done

exit

#========================================================================================
echo '<h1>Playlist experiment</h1>'

PLAYLISTS=`( echo "$(pcp_controls_mac_address) playlists 0 5"; echo "exit" ) | nc $(pcp_lmsip) 9090 | sed 's/ /\+/g'`

echo '#1<br />'
echo $PLAYLISTS
echo '<br /><br />'

PLAYLISTS=`sudo /usr/local/sbin/httpd -d $PLAYLISTS`

echo '#2<br />'
echo $PLAYLISTS
echo '<br /><br />'

echo '#3<br />'
echo '<br />'
echo '<select name="PLAYLISTS">'


SEARCH="Affirmation"

PLAYLISTS=`echo $PLAYLISTS | awk -v search=$SEARCH '
BEGIN {
	RS="id:"
	FS=":"
	i = 0
}
#main
{
	split($1,c," ")
	id[i]=c[1]
	playlist[i]=$2
	i++
}
END {
	for (j=1; j<NR; j++) {
		printf "<option value=\"%s\" id=\"%10s\">%s - %s</option>",id[j],id[j],id[j],playlist[j]
	}
	printf "</select><p>Search: %s</p>", search
} ' `

echo $PLAYLISTS
echo '</select>'


echo '<br /><br />'

#------------------------------------------------------------------------------


echo '<br />'
echo '<br />'

exit