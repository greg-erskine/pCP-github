#!/bin/sh


# Version: 3.03 2016-10-11
#	First version to control volume and eventaully filter on soundcards - so we can avoid to use alsamixer via ssh. SBP.

. pcp-soundcard-functions
. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "Sound card controls" "SBP"

pcp_controls
pcp_banner
pcp_navigation
pcp_running_script
pcp_httpd_query_string

pcp_soundcontrol


#========================================ACTIONS=========================================
case "$ACTION" in
	Test)
		sudo amixer -c $CARD sset $SSET $VoIinputName'%' >/dev/null 2>&1
		[ x"$FILTER1" != x"" ] && sudo amixer -c $CARD sset "$DSP" "$FILTER" >/dev/null 2>&1
		pcp_soundcontrol
	;;
	Backup)
		ALSAlevelout="Custom"
		pcp_save_to_config
		sudo alsactl store
		pcp_backup
	;;
	0dB)
		sudo amixer -c $CARD sset $SSET 0dB >/dev/null 2>&1
		pcp_soundcontrol
	;;
esac
#----------------------------------------------------------------------------------------


#======================================DEBUG=============================================
if [ $DEBUG -eq 1 ]; then
	echo '<!-- Start of debug info -->'
	echo '<p class="debug">[ DEBUG ] Audiocard is:   '$AUDIO'<br />'
	echo '                 [ DEBUG ] sset is:        '$SSET'<br />'
	echo '                 [ DEBUG ] dsp:            '$DSP'<br />'
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
#----------------------------------------------------------------------------------------

#===============================Adjustment of Soundcard==================================
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Soundcard Adjustment for: '"$CARD"'</legend>'
#----------------------------------------------------------------------------------------
pcp_incr_id
echo '          <table class="bggrey percent100">'
echo '            <form name="manual_adjust" action="'$0'" method="get">'
pcp_start_row_shade
#----------------------------------------------------------------------------------------

#Show this if no ALSA controls are avaiable
no_pcp_soundcard_options(){
echo $TEXT
echo '                  <input type="submit" name="ACTION" value="Backup">'
echo '                </td>'
echo '              </tr>'
echo '            </form>'
echo '          </table>'
#----------------------------------------------------------------------------------------
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
}


#----------------------------------------------------------------------------------------
#Show this if ALSA controls are avaiable
pcp_soundcard_options () {
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="column100">'
echo '                  <p>Volume</p>'
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

#--------------------------------------DSP Filter options--------------------------------
# Only show these options if filters are an option for current sound card.
pcp_start_row_shade
[ x"$FILTER1" != x"" ] && echo ' <p><b>DSP filter options&nbsp;&nbsp;</b><br>'
[ x"$FILTER1" != x"" ] && echo ' <input type="radio" name="DSPFILTER" value="FILTER1" '"$FILTER1_CHECK"'><label for="FILTER1"> '"$FILTER1"'</label><br>'
[ x"$FILTER2" != x"" ] && echo ' <input type="radio" name="DSPFILTER" value="FILTER2" '"$FILTER2_CHECK"'><label for="FILTER2"> '"$FILTER2"'</label><br>'
[ x"$FILTER3" != x"" ] && echo ' <input type="radio" name="DSPFILTER" value="FILTER3" '"$FILTER3_CHECK"'><label for="FILTER3"> '"$FILTER3"'</label><br>'
[ x"$FILTER4" != x"" ] && echo ' <input type="radio" name="DSPFILTER" value="FILTER4" '"$FILTER4_CHECK"'><label for="FILTER4P"> '"$FILTER4"'</label><br>'
[ x"$FILTER5" != x"" ] && echo ' <input type="radio" name="DSPFILTER" value="FILTER5" '"$FILTER5_CHECK"'><label for="FILTER5"> '"$FILTER5"'</label><br>'
#----------------------------------------------------------------------------------------
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
echo '                      <li><b>Backup</b> - =dB button will set outout at 0dB.</li>'
echo '                    </ul>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'
echo '            </form>'
echo '          </table>'
#----------------------------------------------------------------------------------------
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------
}

[ x"$TEXT" != x"" ] && no_pcp_soundcard_options || pcp_soundcard_options 

pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'