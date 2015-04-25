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
pcp_xtras
pcp_running_script
pcp_refresh_button

if [ $DEBUG = 1 ]; then
	echo '<p class="debug">[ DEBUG ] LMS IP: '$(pcp_lmsip)'<br />'
	echo '                 [ DEBUG ] MAC: '$(pcp_controls_mac_address)'</p>'
fi

#========================================================================================
echo '<h1>pcp-lms-functions tests</h1>'

echo '<div>'

echo '<h2>Select list of squeezelite player</h2>'
echo '<select name="pCPplayers">'
echo '<p>'$(pcp_lms_players squeezelite)'</p>'
echo '</select>'

echo '<h2>Artists:</h2>'
echo '<p>Artists: '$(pcp_lms_artists)'</p>'

echo '<br />'

echo '<p>Mode: '$(pcp_lms_mode)'</p>'
echo '<p>Time: '$(pcp_lms_time)'</p>'
echo '<p>Genre: '$(pcp_lms_genre)'</p>'
echo '<p>Artist: '$(pcp_lms_artist)'</p>'
echo '<p>Album: '$(pcp_lms_album)'</p>'
echo '<p>Title: '$(pcp_lms_title)'</p>'
echo '<p>Duration: '$(pcp_lms_duration)'</p>'
echo '<p>Remote: '$(pcp_lms_remote)'</p>'
echo '<p>Current_title: '$(pcp_lms_current_title)'</p>'
echo '<p>Path: '$(pcp_lms_path)'</p>'
echo '<p>Player count: '$(pcp_lms_player_count)'</p>'
echo '<p>Player id: '$(pcp_lms_player_id)'</p>'
echo '<p>Player uuid: '$(pcp_lms_player_uuid)'</p>'
echo '<p>Player name: '$(pcp_lms_player_name)'</p>'
echo '<p>Player ip: '$(pcp_lms_player_ip)'</p>'
echo '<p>Player model: '$(pcp_lms_player_model)'</p>'
echo '<p>Player isplayer: '$(pcp_lms_player_isplayer)'</p>'
echo '<p>Player displaytype: '$(pcp_lms_player_displaytype)'</p>'
echo '<p>Player canpoweroff: '$(pcp_lms_player_canpoweroff)'</p>'
echo '<p>Signalstrength: '$(pcp_lms_signalstrength)'</p>'
echo '<p>Name: '$(pcp_lms_name)'</p>'
echo '<p>Connected: '$(pcp_lms_connected)'</p>'

echo '<p>info_total_genres: '$(pcp_lms_info_total_genres)'</p>'
echo '<p>info_total_artists: '$(pcp_lms_info_total_artists)'</p>'
echo '<p>info_total_albums: '$(pcp_lms_info_total_albums)'</p>'
echo '<p>info_total_songs: '$(pcp_lms_info_total_songs)'</p>'


echo '<p>Show: '$(pcp_lms_show)'</p>'

echo '</div>'

#===============================================================
echo '<h1>Old functions</h1>'

echo '<br />'
echo '<div>'
echo '<img src="http://'$(pcp_lmsip)':9000/music/current/cover.jpg" alt="Currently playing" style="height:250px; width:250px; border:1px solid black;"/>'
echo '</div>'
echo '<br />'

pcp_footer

echo '</body>'
echo '</html>'

exit

#========================================================================================
echo '<h1>Playlist experiment</h1>'

PLAYLISTS=`( echo "$(pcp_controls_mac_address) playlists 0 5"; echo "exit" ) | nc $(pcp_lmsip) 9090 | sed 's/ /\+/g'`

echo '#1<br />'
echo $PLAYLISTS
echo '<br /><br />'

PLAYLISTS=`sudo $HTPPD -d $PLAYLISTS`

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