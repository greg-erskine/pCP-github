#!/bin/sh

# Version: 3.10 2017-01-06
#	First version to control volume and eventaully filter on soundcards - so we can avoid to use alsamixer via ssh. SBP.

. pcp-soundcard-functions
. pcp-functions
pcp_variables

. $CONFIGCFG
# Save copy of variable value from config.cfg so it is not overwritten with default values
ORIG_AUDIO="$AUDIO"
ORIG_CARD="$CARD"
ORIG_OUTPUT="$OUTPUT"
ORIG_ALSA_PARAMS="$ALSA_PARAMS"

pcp_html_head "Sound card controls" "SBP"

pcp_controls
pcp_banner
pcp_navigation
pcp_running_script
pcp_httpd_query_string

pcp_selected_soundcontrol
#pcp_soundcontrol
pcp_generic_card_control

#========================================ACTIONS=========================================
case "$ACTION" in
	Test)
		sudo amixer -c $CARD sset $SSET $VoIinputName'%' >/dev/null 2>&1
		[ x"$FILTER1" != x"" ] && sudo amixer -c $CARD sset "$DSP" "$FILTER" >/dev/null 2>&1
		pcp_selected_soundcontrol
		pcp_generic_card_control
	;;
	Backup)
		AUDIO="$ORIG_AUDIO"
		CARD="$ORIG_CARD"
		OUTPUT="$ORIG_OUTPUT"
		ALSA_PARAMS="$ORIG_ALSA_PARAMS"
		ALSAlevelout="Custom"
		pcp_save_to_config
		sudo alsactl store
		pcp_backup
	;;
	0dB)
		sudo amixer -c $CARD sset $SSET 0dB >/dev/null 2>&1
		pcp_selected_soundcontrol
#		pcp_soundcontrol
		pcp_generic_card_control
	;;	
	Select)
		AUDIO="$ORIG_AUDIO"
		CARD="$ORIG_CARD"
		OUTPUT="$ORIG_OUTPUT"
		ALSA_PARAMS="$ORIG_ALSA_PARAMS"
		pcp_save_to_config
		#pcp_soundcontrol
		pcp_read_chosen_audio
		pcp_backup
		pcp_reboot_required
	;;
esac
#----------------------------------------------------------------------------------------

#======================================DEBUG=============================================
if [ $DEBUG -eq 1 ]; then
	echo '<!-- Start of debug info -->'
	echo '<p class="debug">[ DEBUG ] Audiocard is:   '$AUDIO'<br />'
	echo '                 [ DEBUG ] sset is:        '$SSET'<br />'
	echo '                 [ DEBUG ] dsp:            '$DSP'<br />'
	echo '                 [ DEBUG ] dtoverlay is:   '$DTOVERLAY'<br />'
	echo '                 [ DEBUG ] Generic card is:'$GENERIC_CARD'<br />'
	echo '                 [ DEBUG ] Parameter1 is:'  $PARAMS1'<br />'
	echo '                 [ DEBUG ] Parameter2 is:'  $PARAMS2'<br />'
	echo '                 [ DEBUG ] Parameter3 is:'  $PARAMS3'<br />'
	echo '                 [ DEBUG ] Parameter4 is:'  $PARAMS4'<br />'
	echo '                 [ DEBUG ] Parameter5 is:'  $PARAMS5'<br />'
	echo '                 [ DEBUG ] filter1:        '$FILTER1'<br />'
	echo '                 [ DEBUG ] filter2:        '$FILTER2'<br />'
	echo '                 [ DEBUG ] filter3:        '$FILTER3'<br />'
	echo '                 [ DEBUG ] filter4:        '$FILTER4'<br />'
	echo '                 [ DEBUG ] filter5:        '$FILTER5'<br />'
	echo '                 [ DEBUG ] Actual vol is:  '$ACTUAL_VOL'<br />'
	echo '                 [ DEBUG ] Actual db is:   '$ACTUAL_DB'<br />'
	echo '                 [ DEBUG ] Actual Filter:  '$ACTUAL_FILTER'<br />'
	echo '                 [ DEBUG ] Check1 is:      '$FILTER1_CHECK'<br />'
	echo '                 [ DEBUG ] Check2 is:      '$FILTER2_CHECK'<br />'
	echo '                 [ DEBUG ] Check3 is:      '$FILTER3_CHECK'<br />'
	echo '                 [ DEBUG ] Check4 is:      '$FILTER4_CHECK'<br />'
	echo '                 [ DEBUG ] Check5 is:      '$FILTER5_CHECK'</p>'
	echo '<!-- End of debug info -->'
fi

#========================================================================================
# Below is the blocks that builds the table
#----------------------------------------------------------------------------------------

#--------------ALSA volume options-------------------------------------------------------
# Only show this if ALSA volume control is possible
pcp_soundcard_volume_options() {
if [ x"$ACTUAL_VOL" != x"" ]; then
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="column100">'
echo '                  <p><b>Output Level</b></p>'
echo '                </td>'
echo '                <td>'
echo '                  <p style="height:12px">'
echo '                    <input class="large36"'
echo '                           id="VoIinputid"'
echo '                           type="range"'
echo '                           name="VoIinputName"'
echo '                           value='"$ACTUAL_VOL"''
echo '                           min="1"'
echo '                           max="100"'
echo '                           oninput="VoIOutputid.value = VoIinputid.value">'
echo '                  </p>'
echo '                </td>'
echo '                <td>'
echo '                  <output name="VolOutputName" id="VoIOutputid">'"$ACTUAL_VOL"'</output>&nbsppct of max. This equals: <b>'"$ACTUAL_DB"'</b>'
echo '                </td>'
echo '              </tr>'
fi
}

#--------------------------------------DSP Filter options--------------------------------
# Only show these options if filters are an option for current sound card.
pcp_soundcard_DSP_options() {
if [ x"$FILTER1" != x"" ]; then
pcp_toggle_row_shade
[ x"$FILTER1" != x"" ] && echo ' <p><b>DSP filter options:&nbsp;&nbsp;</b><br>'
[ x"$FILTER1" != x"" ] && echo ' <input type="radio" name="DSPFILTER" value="FILTER1" '"$FILTER1_CHECK"'><label for="FILTER1"> '"$FILTER1"'</label><br>'
[ x"$FILTER2" != x"" ] && echo ' <input type="radio" name="DSPFILTER" value="FILTER2" '"$FILTER2_CHECK"'><label for="FILTER2"> '"$FILTER2"'</label><br>'
[ x"$FILTER3" != x"" ] && echo ' <input type="radio" name="DSPFILTER" value="FILTER3" '"$FILTER3_CHECK"'><label for="FILTER3"> '"$FILTER3"'</label><br>'
[ x"$FILTER4" != x"" ] && echo ' <input type="radio" name="DSPFILTER" value="FILTER4" '"$FILTER4_CHECK"'><label for="FILTER4"> '"$FILTER4"'</label><br>'
[ x"$FILTER5" != x"" ] && echo ' <input type="radio" name="DSPFILTER" value="FILTER5" '"$FILTER5_CHECK"'><label for="FILTER5"> '"$FILTER5"'</label><br>'
#----------------------------------------------------------------------------------------
fi
pcp_toggle_row_shade
}

#--------------------------------------Show Buttons for Volume selection-------------------
# Only show this if ALSA volume control is possible

pcp_Volume_filter_buttons() {
if [ x"$ACTUAL_VOL" != x"" ]; then
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td>'
echo '                  <input type="submit" name="ACTION" value="Test">'
echo '                  <input type="submit" name="ACTION" value="Backup">'
echo '                  <input type="submit" name="ACTION" value="0dB">'
echo '                </td>'
echo '              </tr>'

pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td>'
echo '                  <p><b>Alsa Output level&nbsp;&nbsp;</b>'
echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                  </p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <p>Use the sliders to adjust the output level, then</p>'
echo '                    <ul>'
echo '                      <li><b>Test</b> - The changes will be written to ALSA, so you can hear the effects.</li>'
echo '                      <li><b>Backup</b> - The output settings are backed up to make them available after a reboot.</li>'
echo '                      <li><b>0dB Button</b> - Force outout level to 0dB.</li>'
echo '                    </ul>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'
fi
#echo '            </form>'
#echo '          </table>'
}

#--------------------------------------Parameter options--------------------------------

# Logic that will show options as checked if defined in config.cfg
[ x"$SPARAMS1" != x"" ] && PARAMS1_CHECK="checked"
[ x"$SPARAMS2" != x"" ] && PARAMS2_CHECK="checked"
[ x"$SPARAMS3" != x"" ] && PARAMS3_CHECK="checked"
[ x"$SPARAMS4" != x"" ] && PARAMS4_CHECK="checked"
[ x"$SPARAMS5" != x"" ] && PARAMS5_CHECK="checked"

# Only show these options if Parameters for dtoverlay are an option for current sound card.
pcp_soundcard_parameter_options() {
. $CONFIGCFG
if [ x"$PARAMS1" != x"" ] || [ x"$PARAMS2" != x"" ] || [ x"$PARAMS3" != x"" ] || [ x"$PARAMS4" != x"" ] || [ x"$PARAMS5" != x"" ]; then            #....... CAN PROBABLY BE MADE SMARTER
pcp_incr_id
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td>'
echo ' <p><b>Dtoverlay parameter options:&nbsp;&nbsp;</b><br>'
[ x"$PARAMS1" != x"" ] && echo ' <input type="checkbox" name="PARAM1" value='"$PARAMS1"' '"$PARAMS1_CHECK"'><label for="PARAMS1"> '"$PARAMS1"'</label><br>'
[ x"$PARAMS2" != x"" ] && echo ' <input type="checkbox" name="PARAM2" value='"$PARAMS2"' '"$PARAMS2_CHECK"'><label for="PARAMS2"> '"$PARAMS2"'</label><br>'
[ x"$PARAMS3" != x"" ] && echo ' <input type="checkbox" name="PARAM3" value='"$PARAMS3"' '"$PARAMS3_CHECK"'><label for="PARAMS3"> '"$PARAMS3"'</label><br>'
[ x"$PARAMS4" != x"" ] && echo ' <input type="checkbox" name="PARAM4" value='"$PARAMS4"' '"$PARAMS4_CHECK"'><label for="PARAMS4"> '"$PARAMS4"'</label><br>'
[ x"$PARAMS5" != x"" ] && echo ' <input type="checkbox" name="PARAM5" value='"$PARAMS5"' '"$PARAMS5_CHECK"'><label for="PARAMS5"> '"$PARAMS5"'</label><br>'
#----------------------------------------------------------------------------------------
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td>'
echo '                  <input type="submit" name="ACTION" value="Select">'
echo '                </td>'
echo '              </tr>'
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td>'
echo '                  <p><b>Parameters available for your DAC&nbsp;&nbsp;</b>'
echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                  </p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <p>Select the parameters you want to add to dtoverlay for your DAC. <b>Then a reboot is needed.</b></p>'
echo '                    <ul>'
echo '                      <li>'"$TEXT"'</li>'
echo '                    </ul>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'
fi
}

#========================================================================================
# Build the Table
#----------------------------------------------------------------------------------------
pcp_table_top "Soundcard Adjustment for: $LISTNAME"
echo '            <form name="manual_adjust" action="'$0'" method="get">'
pcp_start_row_shade
pcp_incr_id

[ "$GENERIC_CARD" = "TI51XX" ] || [ "$GENERIC_CARD" = "ONBOARD" ] && pcp_soundcard_DSP_options && pcp_soundcard_volume_options && pcp_Volume_filter_buttons && pcp_soundcard_parameter_options

[ "$GENERIC_CARD" = "ES9023" ] && pcp_soundcard_DSP_options && pcp_soundcard_volume_options && pcp_Volume_filter_buttons && pcp_soundcard_parameter_options

[ x"$GENERIC_CARD" = x"" ] && echo "$TEXT"

pcp_table_end
#-----------------------------------------------------------------------------------------

pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'