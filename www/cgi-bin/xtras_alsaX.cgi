#!/bin/sh

# Version: 7.0.0 2020-05-21

. pcp-functions

CARDS=$(cat /proc/asound/card*/id)
NO_OF_CARDS=$(echo $CARDS | wc -w )

pcp_html_head "xtras_alsa" "GE"

pcp_controls
pcp_navbar
pcp_httpd_query_string
pcp_remove_query_string

#=========================================================================================
# 
#-----------------------------------------------------------------------------------------
pcp_view_asound_state() {
	if [ -f /var/lib/alsa/asound.state ]; then
		pcp_textarea "Current /var/lib/alsa/asound.state" "cat /var/lib/alsa/asound.state" 18
	else
		pcp_textarea "Current /var/lib/alsa/asound.state" "echo '[ WARN ] /var/lib/alsa/asound.state missing.'" 5
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
		pcp_infobox_begin
		pcp_backup
		pcp_infobox_end
	;;
	Custom)
		:
	;;
	View)
		:
	;;
	Delete)
		sudo mv /var/lib/alsa/asound.state /var/lib/alsa/asound.state~
	;;
esac

COLUMN3_1="col-sm-2"
COLUMN3_2="col-sm-3"
COLUMN3_3="col-sm-7"
#----------------------------------------------------------------------------------------
echo '  <form name="alsa" action="'$0'" method="get">'
echo '    <div class="'$BORDER'">'
pcp_heading5 "Advanced Linux Sound Architecture (ALSA)"
#-----------------------------------------Card-------------------------------------------
pcp_incr_id
echo '      <div class="row mx-1">'
echo '        <div class="'$COLUMN3_1'">'
echo '          <p>Sound card</p>'
echo '        </div>'
echo '        <div class="input-group '$COLUMN3_2'">'
echo '          <select class="custom-select custom-select-sm" name="CARD">'

                  for VALUE in $CARDS
                  do
                    echo '<option value="'$VALUE'">'$VALUE'</option>'
                  done
  
echo '          </select>'
echo '        </div>'
echo '        <div class="'$COLUMN3_3'">'
echo '          <p>Select card&nbsp;&nbsp;'
echo '            <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
echo '          </p>'
echo '          <div id="dt'$ID'" class="'$COLLAPSE'">'
echo '            <p>The RPi built-in sound card is named ALSA. This can cause some confusion '
echo '               with Advanced Linux Sound Architecture (ALSA).</p>'
echo '            <p>Some USB sound cards used a rather generic name Device.</p>' 
echo '          </div>'
echo '        </div>'
echo '      </div>'
#--------------------------------------Volume--------------------------------------------
pcp_incr_id
echo '      <div class="row mx-1">'
echo '        <div class="'$COLUMN3_1'">'
echo '          <p>Volume</p>'
echo '        </div>'
echo '        <div class="form-group '$COLUMN3_2'">'
echo '          <input class="form-control form-control-sm" type="text" name="VOL" value="'$VOL'">'
echo '        </div>'
echo '        <div class="'$COLUMN3_3'">'
echo '          <p>Specify the volume for card&nbsp;&nbsp;'
echo '            <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
echo '          </p>'
echo '          <div id="dt'$ID'" class="'$COLLAPSE'">'
echo '            <p>The volume range will be different depending on the sound card.
                     Check Limits: under sounds Card details.</p>'
echo '            <p>For example: The built-in sound card has Limits: -10239 to 400</p>'
echo '            <p>Where -10239 equals -102.39dB, 400 equals 4.00dB so 0 equals 0.00dB</p>'
echo '          </div>'
echo '        </div>'
echo '      </div>'
#--------------------------------------Unmute--------------------------------------------
pcp_incr_id
echo '      <div class="row mx-1">'
echo '        <div class="'$COLUMN3_1'">'
echo '          <p>Unmute/mute</p>'
echo '        </div>'
echo '        <div class="'$COLUMN3_2'">'
echo '          <input id="rad1" type="radio" name="UNMUTE" value="unmute" checked>'
echo '          <label for="rad1">Umute&nbsp;&nbsp;</label>'
echo '          <input id="rad2" type="radio" name="UNMUTE" value="mute">'
echo '          <label for="rad2">Mute</label>'
echo '        </div>'
echo '        <div class="'$COLUMN3_3'">'
echo '          <p>Unmute/mute card&nbsp;&nbsp;'
echo '            <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
echo '          </p>'
echo '          <div id="dt'$ID'" class="'$COLLAPSE'">'
echo '            <ul>'
echo '              <li>Unmute or mute.</li>'
echo '            </ul>'
echo '          </div>'
echo '        </div>'
echo '      </div>'
#--------------------------------------Analog/HDMI---------------------------------------
pcp_incr_id
echo '      <div class="row mx-1">'
echo '        <div class="'$COLUMN3_1'">'
echo '          <p>Analog/HDMI</p>'
echo '        </div>'
echo '        <div class="'$COLUMN3_2'">'
echo '          <input id="rad3" type="radio" name="HDMI" value="1" checked>'
echo '          <label for="rad3">Analog&nbsp;&nbsp;</label>'
echo '          <input id="rad4" type="radio" name="HDMI" value="2">'
echo '          <label for="rad4">HDMI</label>'
echo '        </div>'
echo '        <div class="'$COLUMN3_3'">'
echo '          <p>Select Analog/HDMI&nbsp;&nbsp;'
echo '            <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
echo '          </p>'
echo '          <div id="dt'$ID'" class="'$COLLAPSE'">'
echo '            <ul>'
echo '              <li>Select Anlog or HDMI output for built-in sound card.</li>'
echo '            </ul>'
echo '          </div>'
echo '        </div>'
echo '      </div>'
#----------------------------------------------------------------------------------------
echo '      <div class="row mx-1">'
echo '        <div class="col-2">'
echo '          <input class="'$BUTTON'" type="submit" name="ACTION" value="Save">'
echo '        </div>'
echo '      </div>'
#----------------------------------------------------------------------------------------
echo '<hr>'
#----------------------------------------------------------------------------------------
pcp_incr_id
echo '      <div class="col-12">'
echo '        <p>Sound cards details&nbsp;&nbsp;'
echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
echo '        </p>'
echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
echo '          <div class="row">'
echo '            <div class="col-12">'
echo '              <pre>'

                    echo Number of soundcards: $NO_OF_CARDS

                    for VALUE in $CARDS
                    do
                      echo ------------------------------------------------------------------------------
                      echo CARD=$VALUE
                      amixer -c $VALUE -- sget PCM
                      echo
                    done

echo '              </pre>'
echo '            </div>'
echo '          </div>'
echo '        </div>'
echo '      </div>'
#----------------------------------------------------------------------------------------
echo '      <div class="row mx-1">'
echo '        <div class="col-2">'
echo '          <input class="'$BUTTON'" type="submit" name="ACTION" value="Store" title="Store asound.state">'
echo '        </div>'
echo '        <div class="col-2">'
echo '          <input class="'$BUTTON'" type="submit" name="ACTION" value="Restore" title="Restore asound.state">'
echo '        </div>'
echo '        <div class="col-2">'
echo '          <input class="'$BUTTON'" type="submit" name="ACTION" value="View" title="View asound.state">'
echo '        </div>'
echo '        <div class="col-2">'
echo '          <input class="'$BUTTON'" type="submit" name="ACTION" value="Delete" title="Delete asound.state">'
echo '        </div>'
echo '        <div class="col-2">'
echo '          <input class="'$BUTTON'" type="submit" name="ACTION" value="Backup" title="Backup pcp.cfg">'
echo '        </div>'
#echo '        <div class="col-2">'
#echo '          <input class="'$BUTTON'" type="submit" name="ACTION" value="Custom">'
#echo '        </div>'
echo '      </div>'
#----------------------------------------------------------------------------------------
echo '<hr>'
#----------------------------------------------------------------------------------------
if [ "$ACTION" = "View" ] || [ "$ACTION" = "Delete" ]; then
	echo '      <div class="row mx-1">'
	echo '        <div class="col-12">'
	                pcp_view_asound_state
	echo '        </div>'
	echo '      </div>'
fi
#----------------------------------------------------------------------------------------
echo '    </div>'
echo '  </form>'
#----------------------------------------------------------------------------------------

pcp_html_end
exit