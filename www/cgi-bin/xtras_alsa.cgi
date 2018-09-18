#!/bin/sh

# Version: 4.0.1 2018-09-19

. pcp-functions
#. $CONFIGCFG

CARDS=$(cat /proc/asound/card*/id)
NO_OF_CARDS=$(echo $CARDS | wc -w )

pcp_html_head "xtras_alsa" "GE"

pcp_controls
pcp_banner
pcp_navigation
pcp_running_script
pcp_httpd_query_string

#=========================================================================================
# 
#-----------------------------------------------------------------------------------------
pcp_view_asound_state() {
	if [ -f /var/lib/alsa/asound.state ]; then
		pcp_textarea_inform "Current /var/lib/alsa/asound.state" "cat /var/lib/alsa/asound.state" 180
	else
		pcp_textarea_inform "Current /var/lib/alsa/asound.state" "echo '[ WARN ] /var/lib/alsa/asound.state missing.'" 50
	fi
}

case "$ACTION" in
	Save)
		sudo amixer -c $CARD -- sset PCM $UNMUTE $VOL >/dev/null 2>&1
		sudo amixer -c ALSA cset name='PCM Playback Route' $HDMI >/dev/null 2>&1
	;;
	Store)
		sudo alsactl store
	;;
	Restore)
		sudo alsactl restore
	;;
	Backup)
		pcp_backup
	;;
	Custom)
		echo
	;;
	View)
		echo
	;;
	Delete)
		sudo mv /var/lib/alsa/asound.state /var/lib/alsa/asound.state~
	;;
esac

#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>ALSA</legend>'
echo '          <table class="bggrey percent100">'
echo '            <form name="alsa" action="'$0'" method="get">'
#-----------------------------------------Card-------------------------------------------
pcp_incr_id
pcp_start_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="column150">'
echo '                  <p>Sound card</p>'
echo '                </td>'
echo '                <td class="column210">'
echo '                  <select name="CARD">'

                          for VALUE in $CARDS
                          do
                            echo '<option value="'$VALUE'">'$VALUE'</option>'
                          done
  
echo '                  </select>'
echo '                </td>'
echo '                <td>'
echo '                  <p>Select card&nbsp;&nbsp;'
echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                  </p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <p>Card</p>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'
#--------------------------------------Volume-------------------------------
pcp_incr_id
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="column150">'
echo '                  <p>Volume</p>'
echo '                </td>'
echo '                <td class="column210">'
echo '                  <input class="large15" type="text" name="VOL" value="'$VOL'">'
echo '                </td>'
echo '                <td>'
echo '                  <p>Specify the volume for card&nbsp;&nbsp;'
echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                  </p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <p>Volume</p>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'
#--------------------------------------Unmute---------------------------------------------
pcp_incr_id
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="column150">'
echo '                  <p>Unmute/mute</p>'
echo '                </td>'
echo '                <td class="column210">'
echo '                  <input class="small1" type="radio" name="UNMUTE" value="unmute" checked>Umute&nbsp;'
echo '                  <input class="small1" type="radio" name="UNMUTE" value="mute">Mute'
echo '                </td>'
echo '                <td>'
echo '                  <p>Unmute/mute card&nbsp;&nbsp;'
echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                  </p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <ul>'
echo '                      <li>Unmute or mute.</li>'
echo '                    </ul>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'
#--------------------------------------Analog/HDMI---------------------------------------
pcp_incr_id
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="column150">'
echo '                  <p>Analog/HDMI</p>'
echo '                </td>'
echo '                <td class="column210">'
echo '                  <input class="small1" type="radio" name="HDMI" value="1" checked>Analog&nbsp;'
echo '                  <input class="small1" type="radio" name="HDMI" value="2">HDMI'
echo '                </td>'
echo '                <td>'
echo '                  <p>Select Analog/HDMI&nbsp;&nbsp;'
echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                  </p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <ul>'
echo '                      <li>Select Anlog or HDMI output for on-board sound card.</li>'
echo '                    </ul>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'
#----------------------------------------------------------------------------------------
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td>'
echo '                  <input type="submit" name="ACTION" value="Save">'
eecho '                </td>'
echo '              </tr>'
#----------------------------------------------------------------------------------------
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td>'
echo '                  <textarea class="inform" style="height:220px">'

                          echo Number of soundcards: $NO_OF_CARDS

                          for VALUE in $CARDS
                          do
                            echo ------------------------------------------------------------------------------
                            echo CARD=$VALUE
                            amixer -c $VALUE -- sget PCM
                            echo
                          done

echo '                  </textarea>'
echo '                </td>'
#----------------------------------------------------------------------------------------
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td>'
echo '                  <input type="submit" name="ACTION" value="Store">'
echo '                  <input type="submit" name="ACTION" value="Restore">'
echo '                  <input type="submit" name="ACTION" value="Backup">'
echo '                  <input type="submit" name="ACTION" value="Custom">'
echo '                  <input type="submit" name="ACTION" value="View">'
echo '                  <input type="submit" name="ACTION" value="Delete">'
echo '                </td>'
echo '              </tr>'
#----------------------------------------------------------------------------------------
if [ "$ACTION" = "View" ] || [ "$ACTION" = "Delete" ]; then
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td>'
	                        pcp_view_asound_state
	echo '                </td>'
	echo '              </tr>'
fi
#----------------------------------------------------------------------------------------
echo '            </form>'
echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------

pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'