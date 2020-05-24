#!/bin/sh

# Version: 7.0.0 2020-05-24

# Title: LMS CLI test
# Description: Display LMS 

. pcp-functions
. pcp-lms-functions

pcp_html_head "LMS CLI test" "GE"

pcp_controls
pcp_xtras
pcp_httpd_query_string

if [ $DEBUG -eq 1 ]; then
	pcp_message DEBUG "LMS IP: $(pcp_lmsip)" "html"
	pcp_message DEBUG "MAC: $(pcp_controls_mac_address)" "html"
fi

COLUMN3_1="col-sm-2"
COLUMN3_2="col-sm-3"
COLUMN3_3="col-sm-7"
#========================================================================================
# Main
#----------------------------------------------------------------------------------------
echo '  <div class="'$BORDER'">'
pcp_heading5 "Select LMS"
echo '    <form name="new-lms-ip" action="'$0'" method="get">'
#----------------------------------------------------------------------------------------
pcp_incr_id
echo '      <div class="row mx-1">'
echo '         <div class="'$COLUMN3_1'">'
echo '           <input class="'$BUTTON'" type="submit" name="SUBMIT" value="Connect">'
echo '         </div>'
echo '         <div class="input-group '$COLUMN3_2'">'

if which find_servers >/dev/null 2>&1; then
	echo '           <select class="custom-select custom-select-sm" name="NEWLMSIP">'
	find_servers | sed -e 's|(||' -e 's|)||' | awk '{ printf "<option value=%s>%s</option>\n", $2, $1 }'
	echo '           </select>'
else
	pcp_message ERROR "find_servers missing." "html"
fi

echo '         </div>'
echo '         <div class="'$COLUMN3_3'">'
echo '           <p>Connect to LMS&nbsp;&nbsp;'
pcp_helpbadge
echo '           </p>'
echo '           <div id="dt'$ID'" class="'$COLLAPSE'">'
echo '             <p>This will connect piCorePlayer to selected LMS.</p>'
echo '           </div>'
echo '         </div>'
echo '       </div>'
#----------------------------------------------------------------------------------------
echo '    </form>'
echo '  </div>'

[ "$SUBMIT" = "Connect" ] && pcp_lms_connect "$NEWLMSIP"

#========================================================================================
# LMS functions
#----------------------------------------------------------------------------------------

#--------------------------------------pcp_lms_players-----------------------------------
pcp_heading5 "Squeezelite players: (pcp_lms_players squeezelite)" hr
PLAYERDATA=$(pcp_lms_players squeezelite)
echo '<p>'$PLAYERDATA'</p>'

PLAYERS=$(echo "$PLAYERDATA" | awk -F",1 " '{ for(i=1;i<=NF;i++) { printf "<p>%s</p>%s", $i, "\n"} }')
echo $PLAYERS

#--------------------------------------pcp_lms_player_status-----------------------------
pcp_heading5 "Status: (pcp_lms_player_status)" hr
echo '<p>'$(pcp_lms_player_status)'</p>'

#--------------------------------------pcp_lms_artists-----------------------------------
pcp_heading5 "Artists: (pcp_lms_artists)" hr
echo '<p><b>Note:</b> Limited to first 20 artists.</p>'
echo '<p>'$(pcp_lms_artists 20)'</p>'
echo '<br />'

#--------------------------------------pcp_lms_mode--------------------------------------
pcp_heading5 "Mode: (pcp_lms_mode)" hr
echo '<p>'$(pcp_lms_mode)'</p>'

#--------------------------------------pcp_lms_time--------------------------------------
pcp_heading5 "Time: (pcp_lms_time)" hr
echo '<p>'$(pcp_lms_time)'</p>'

#--------------------------------------pcp_lms_genre--------------------------------------
pcp_heading5 "Genre: (pcp_lms_genre)" hr
echo '<p>'$(pcp_lms_genre)'</p>'

#--------------------------------------pcp_lms_artist------------------------------------
pcp_heading5 "Artist: (pcp_lms_artist)" hr
echo '<p>'$(pcp_lms_artist)'</p>'

#--------------------------------------pcp_lms_album-------------------------------------
pcp_heading5 "Album: (pcp_lms_album)" hr
echo '<p>'$(pcp_lms_album)'</p>'

#--------------------------------------pcp_lms_title-------------------------------------
pcp_heading5 "Title: (pcp_lms_title)" hr
echo '<p>'$(pcp_lms_title)'</p>'

#--------------------------------------pcp_lms_duration----------------------------------
pcp_heading5 "Duration: (pcp_lms_duration)" hr
echo '<p>'$(pcp_lms_duration)'</p>'

#--------------------------------------pcp_lms_remote------------------------------------
pcp_heading5 "Remote: (pcp_lms_remote)" hr
echo '<p>'$(pcp_lms_remote)'</p>'

#--------------------------------------pcp_lms_current_title-----------------------------
pcp_heading5 "Current_title: (pcp_lms_current_title)" hr
echo '<p>'$(pcp_lms_current_title)'</p>'

#--------------------------------------pcp_lms_path--------------------------------------
pcp_heading5 "Path: (pcp_lms_path)" hr
echo '<p>'$(pcp_lms_path)'</p>'

#--------------------------------------pcp_lms_player_count------------------------------
pcp_heading5 "Player count: (pcp_lms_player_count)" hr
echo '<p>'$(pcp_lms_player_count)'</p>'

#--------------------------------------pcp_lms_player_id---------------------------------
pcp_heading5 "Player id: (pcp_lms_player_id)" hr
echo '<p>'$(pcp_lms_player_id)'</p>'

#--------------------------------------pcp_lms_player_uuid-------------------------------
pcp_heading5 "Player uuid: (pcp_lms_player_uuid)" hr
echo '<p>'$(pcp_lms_player_uuid)'</p>'

#--------------------------------------pcp_lms_player_name-------------------------------
pcp_heading5 "Player name: (pcp_lms_player_name)" hr
echo '<p>'$(pcp_lms_player_name)'</p>'

#--------------------------------------pcp_lms_player_ip---------------------------------
pcp_heading5 "Player ip: (pcp_lms_player_ip)" hr
echo '<p>'$(pcp_lms_player_ip)'</p>'

#--------------------------------------pcp_lms_player_model------------------------------
pcp_heading5 "Player model: (pcp_lms_player_model)" hr
echo '<p>'$(pcp_lms_player_model)'</p>'

#--------------------------------------pcp_lms_player_isplayer---------------------------
pcp_heading5 "Player isplayer: (pcp_lms_player_isplayer)" hr
echo '<p>'$(pcp_lms_player_isplayer)'</p>'

#--------------------------------------pcp_lms_player_displaytype------------------------
pcp_heading5 "Player displaytype: (pcp_lms_player_displaytype)" hr
echo '<p>'$(pcp_lms_player_displaytype)'</p>'

#--------------------------------------pcp_lms_player_canpoweroff------------------------
pcp_heading5 "Player canpoweroff: (pcp_lms_player_canpoweroff)" hr
echo '<p>'$(pcp_lms_player_canpoweroff)'</p>'

#--------------------------------------pcp_lms_signalstrength----------------------------
pcp_heading5 "Signalstrength: (pcp_lms_signalstrength)" hr
echo '<p>'$(pcp_lms_signalstrength)'</p>'

#--------------------------------------pcp_lms_name--------------------------------------
pcp_heading5 "Name: (pcp_lms_name)" hr
echo '<p>'$(pcp_lms_name)'</p>'

#--------------------------------------pcp_lms_connected---------------------------------
pcp_heading5 "Connected: (pcp_lms_connected)" hr
echo '<p>'$(pcp_lms_connected)'</p>'

#--------------------------------------pcp_lms_info_total_genres-------------------------
pcp_heading5 "info_total_genres: (pcp_lms_info_total_genres)" hr
echo '<p>'$(pcp_lms_info_total_genres)'</p>'

#--------------------------------------pcp_lms_info_total_artists------------------------
pcp_heading5 "info_total_artists: (pcp_lms_info_total_artists)" hr
echo '<p>'$(pcp_lms_info_total_artists)'</p>'

#--------------------------------------pcp_lms_info_total_albums-------------------------
pcp_heading5 "info_total_albums: (pcp_lms_info_total_albums)" hr
echo '<p>'$(pcp_lms_info_total_albums)'</p>'

#--------------------------------------pcp_lms_info_total_songs--------------------------
pcp_heading5 "info_total_songs: (pcp_lms_info_total_songs)" hr
echo '<p>'$(pcp_lms_info_total_songs)'</p>'

#--------------------------------------pcp_lms_show--------------------------------------
pcp_heading5 "Show: (pcp_lms_show)" hr
echo '<p>'$(pcp_lms_show)'</p>'

#===============================================================

[ x"" = x"$LMSWEBPORT" ] && LMSPORT=9000 || LMSPORT=$LMSWEBPORT
echo '<br />'
echo '<div>'
echo '<img src="http://'$(pcp_lmsip)':'${LMSPORT}$(pcp_lms_show)'" alt="Currently playing" style="height:250px; width:250px; border:1px solid black;"/>'
echo '</div>'
echo '<br />'

pcp_html_end
exit
