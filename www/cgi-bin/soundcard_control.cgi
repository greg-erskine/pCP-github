#!/bin/sh

# Version: 3.03 2016-01-10 SBP
#	First version to control volume and eventaul filter on soundcards - so we can avoid to use alsamixer via ssh.

. pcp-functions
pcp_variables
. $CONFIGCFG


pcp_html_head "Sound card controls" "SBP"

pcp_controls
pcp_banner
pcp_navigation
pcp_running_script
pcp_httpd_query_string


#====================================================
#To find the controls:
# amixer -c 0 scontrols
# aplay -l
#===================================================

#========================================================================================
# Routines
# Needs to be populated for each soundcard. Some is without filter options.
# USB cards will probably never be supported this way as they are so different 
#----------------------------------------------------------------------------------------

pcp_soundcontrol (){
#Generic procedure:

	case "$AUDIO" in
		Analog)
			CARD='ALSA'
			SSET='PCM'
			ACTUAL_VOL=$(amixer -c $CARD sget $SSET | grep "Mono: Playback" | awk '{ print $4 }' | tr -d "[]%")
			ACTUAL_DB=$(amixer -c $CARD sget $SSET | grep "Mono: Playback" | awk '{ print $5 }' | tr -d "[]")

 
		;;
		HDMI)
			
		;;
		USB)
			
		;;
		I2SDAC)
			
		;;
		I2SGENERIC)
			
		;;
		I2SDIG)
			
		;;
		I2SAMP)
			
		;;
		IQaudio)
			
		;;
		I2SpIQAMP)
			
		;;
		I2SpDAC)
			
		;;
		I2SpDIG)
			
		;;
		I2SpDIGpro)
			
		;;
		I2SpIQaudIO)
			CARD='IQaudIODAC'
			SSET='Digital'
			DSP='DSP Program,0'
			FILTER1='Low latency IIR with de-emphasis'
			FILTER2='FIR interpolation with de-emphasis'
			FILTER3='High attenuation with de-emphasis'
			FILTER4='Fixed process flow'
			FILTER5='Ringing-less low latency FIR'
			ACTUAL_VOL=$(amixer -c $CARD sget $SSET | grep "Right: Playback" | awk '{ print $5 }' | tr -d "[]%")
			ACTUAL_DB=$(amixer -c $CARD sget $SSET | grep "Right: Playback" | awk '{ print $6 }' | tr -d "[]")
			ACTUAL_FILTER=$(amixer -c $CARD sget 'DSP Program,0' | grep "Item0:" | awk '{ print $2 }' | tr -d "'")

				case "$DSPFILTER" in
						FILTER1) FILTER='Low latency IIR with de-emphasis' ;;
						FILTER2) FILTER='FIR interpolation with de-emphasis' ;;
						FILTER3) FILTER='High attenuation with de-emphasis' ;;
						FILTER4) FILTER='Fixed process flow' ;;
						FILTER5) FILTER='Ringing-less low latency FIR' ;;
				esac

				#Logic to make checked radiobuttons - should be done for each sound card: 
				pcp_filtercheck (){
				FILTER1_CHECK=""
				FILTER2_CHECK=""
				FILTER3_CHECK=""
				FILTER4_CHECK=""
				FILTER5_CHECK=""
					case "$ACTUAL_FILTER" in
						Low) FILTER1_CHECK="checked" ;;
						FIR) FILTER2_CHECK="checked" ;;
						High) FILTER3_CHECK="checked" ;;
						Fixed) FILTER4_CHECK="checked" ;;	
						Ringing-less) FILTER5_CHECK="checked" ;;
					esac
				}
				pcp_filtercheck
		;;

		I2SpIQaudIOdigi)

			
		;;
		justboomdac)
			
		;;
		justboomdigi)
			
		;;
		raspidac3)
			
		;;
		rpi_dac)
			
		;;
		LOCO_dac)

		;;

		*)
			echo '[ ERROR ] Error setting $AUDIO to '$AUDIO
		;;
	esac
}
pcp_soundcontrol

#========================== ACTIONS=======================================
case "$ACTION" in
	Test)
	sudo amixer -c $CARD sset $SSET $VoIinputName'%' >/dev/null 2>&1
	[ x"$FILTER1" != x"" ] && sudo amixer -c $CARD sset "$DSP" "$FILTER"
	pcp_soundcontrol
	;;

	Backup)
		ALSAlevelout="Custom"
		pcp_save_to_config
		sudo alsactl store
		pcp_backup >/dev/null 2>&1
	;;
esac
#----------------------------------------------------------------------------

#==========================DEBUG=============================================
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
	echo '                 [ DEBUG ] Check1 is:       '$FILTER1_CHECK'<br />'
	echo '                 [ DEBUG ] Check2 is:       '$FILTER2_CHECK'<br />'
	echo '                 [ DEBUG ] Check3 is:       '$FILTER3_CHECK'<br />'
	echo '                 [ DEBUG ] Check4 is:       '$FILTER4_CHECK'<br />'
	echo '                 [ DEBUG ] Check5 is:       '$FILTER5_CHECK'<br />'
	echo '<!-- End of debug info -->'
fi
#----------------------------------------------------------------------------------------



#==========================Adjustment of Soundcard======================================
pcp_sound_card_table (){
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
pcp_toggle_row_shade
echo '    <label for="VoIinputid">Volume</label>'
echo '    <input type="range" name="VoIinputName" id="VoIinputid" value='"$ACTUAL_VOL"' min="1" max="100" oninput="VoIOutputid.value = VoIinputid.value">'
echo '    <output name="VolOutputName" id="VoIOutputid">'"$ACTUAL_VOL"'</output>&nbsppct of max. This equals: <b>'"$ACTUAL_DB"'</b>'

#-------------------------------------------DSP Filter options--------------------------------
#Only show these options if a filters are an option for current sound card. 
pcp_incr_id
pcp_start_row_shade
[ x"$FILTER1" != x"" ] && echo '  <p><b>DSP filter options&nbsp;&nbsp;</b><br>'
[ x"$FILTER1" != x"" ] && echo '  <input type="radio" name="DSPFILTER" value="FILTER1" '"$FILTER1_CHECK"'><label for="FILTER1"> '"$FILTER1"'</label><br>'
[ x"$FILTER2" != x"" ] && echo '  <input type="radio" name="DSPFILTER" value="FILTER2" '"$FILTER2_CHECK"'><label for="FILTER2"> '"$FILTER2"'</label><br>'
[ x"$FILTER3" != x"" ] && echo '  <input type="radio" name="DSPFILTER" value="FILTER3" '"$FILTER3_CHECK"'><label for="FILTER3"> '"$FILTER3"'</label><br>'
[ x"$FILTER4" != x"" ] && echo '  <input type="radio" name="DSPFILTER" value="FILTER4" '"$FILTER4_CHECK"'><label for="FILTER4P"> '"$FILTER4"'</label><br>'
[ x"$FILTER5" != x"" ] && echo '  <input type="radio" name="DSPFILTER" value="FILTER5" '"$FILTER5_CHECK"'><label for="FILTER5"> '"$FILTER5"'</label><br>'
#----------------------------------------------------------------------------------------------
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td>'
echo '                  <input type="submit" name="ACTION" value="Test">'
echo '                  <input type="submit" name="ACTION" value="Backup">'
#echo '                  <input type="submit" name="ACTION" value="Reset">'
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
}
#----------------------------------------------------------------------------------------

pcp_sound_card_table

pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'