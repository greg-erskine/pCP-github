#!/bin/sh

# Version: 3.21 2017-07-15
#	Added Analogue and Analogue Boost, Alsa Simple Controls. SBP.
#	Added Mixer controls for Allo Piano Plus. PH.
#	Added HTML formatting. PH.

# Version: 3.20 2017-03-13
#	Fixed pcp-xxx-functions issues. GE.
#	Added Extra Text fields. SBP

# Version: 3.10 2017-01-06
#	First version to control volume and eventaully filter on soundcards - so we can avoid to use alsamixer via ssh. SBP.

. pcp-functions
. pcp-soundcard-functions
. pcp-lms-functions

# Save copy of variable value from config.cfg so it is not overwritten with default values
ORIG_AUDIO="$AUDIO"
ORIG_CARD="$CARD"
ORIG_OUTPUT="$OUTPUT"
ORIG_ALSA_PARAMS="$ALSA_PARAMS"

pcp_html_head "Sound card controls" "SBP"

pcp_picoreplayers_toolbar
pcp_controls
pcp_banner
pcp_navigation
pcp_running_script
[ $DEBUG -eq 0 ] && pcp_remove_query_string
pcp_httpd_query_string

pcp_selected_soundcontrol
#pcp_soundcontrol
pcp_generic_card_control

#Check for onboard soundcard presence: 
aplay -l | grep bcm2835 >/dev/null 2>&1 
ACTUAL_ONBOARD_STATUS=$?
[ $ACTUAL_ONBOARD_STATUS = 0 ] && ONBOARD_SND=On || ONBOARD_SND=Off
[ $ONBOARD_SND = On ] && ONBOARD_SOUND_CHECK=checked || ONBOARD_SOUND_CHECK="" 

#========================================ACTIONS=========================================
case "$ACTION" in
	Test)
		sudo amixer -c $CARD sset $SSET $VoIinputName'%' >/dev/null 2>&1
		[ x"$FILTER1" != x"" ] && sudo amixer -c $CARD sset "$DSP" "$FILTER" >/dev/null 2>&1
		
		if [ x"$SMCFILTER1" = x"" ]; then
			sudo amixer -c $CARD sset 'Analogue' 0 >/dev/null 2>&1
		else 
			sudo amixer -c $CARD sset 'Analogue' $SMCFILTER1 >/dev/null 2>&1
		fi

		if [ x"$SMCFILTER2" = x"" ]; then 
			sudo amixer -c $CARD sset 'Analogue Playback Boost' 0 >/dev/null 2>&1
		else
			sudo amixer -c $CARD sset 'Analogue Playback Boost' $SMCFILTER2 >/dev/null 2>&1
		fi
# -------------------Allo Piano Plus Dac Controls--------------------
		case "$PIANOSUBMODE" in
			"2.0") sudo amixer -c $CARD sset 'Subwoofer mode' "$PIANOSUBMODE" > /dev/null 2>&1;;
			Dual*) sudo amixer -c $CARD sset 'Dual Mode' "$PIANOSUBMODE" > /dev/null 2>&1;;
			"2.1"|"2.2")
				df | grep -q "allo-piano"
				if [ $? -eq 0 ]; then
					sudo amixer -c $CARD sset 'Subwoofer mode' "$PIANOSUBMODE" > /dev/null 2>&1
				else
					echo '<p class="error">[ERROR] firmware-allo-piano.tcz not loaded for the selected mode.</p>'
				fi
			;;
			*);;
		esac
		[ "$PIANOLOWPASS" != "" ] && sudo amixer -c $CARD sset 'Lowpass' "$PIANOLOWPASS" >/dev/null 2>&1
		[ "$VoIinputSubName" != "" ] && sudo amixer -c $CARD sset "Subwoofer" $VoIinputSubName'%' >/dev/null 2>&1
# -------------------Allo Piano Plus Dac Controls--------------------
		pcp_generic_card_control
	;;
	Backup)
		sudo amixer -c $CARD sset $SSET $VoIinputName'%' >/dev/null 2>&1
		[ "$VoIinputSubName" != "" ] && sudo amixer -c $CARD sset "Subwoofer" $VoIinputSubName'%' >/dev/null 2>&1
		[ x"$FILTER1" != x"" ] && sudo amixer -c $CARD sset "$DSP" "$FILTER" >/dev/null 2>&1
		pcp_generic_card_control
		AUDIO="$ORIG_AUDIO"
#		CARD="$ORIG_CARD"   ORIG_CARD is always = "" since it is set at the beginning before the card.conf is read....not sure what this was intended for.
		OUTPUT="$ORIG_OUTPUT"
		ALSA_PARAMS="$ORIG_ALSA_PARAMS"
		ALSAlevelout="Custom"
		pcp_save_to_config
		sudo alsactl store
		pcp_backup
	;;
	0dB)
		sudo amixer -c $CARD sset $SSET 0dB >/dev/null 2>&1
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
	Onboard)
		#Check for changes in onboard status as we dont want to mount and umount if not needed
		SELECTED_BOARD=On
		[ x"$ONBOARD" = x"" ] && SELECTED_BOARD=Off
		if [ "$ONBOARD_SND" != "$SELECTED_BOARD" ]; then 
		pcp_mount_bootpart_nohtml >/dev/null 2>&1
			if [ "$ONBOARD" = "On" ]; then 
				pcp_re_enable_analog
				else
				pcp_disable_analog
				sudo rmmod snd_bcm2835 
			fi
		pcp_umount_bootpart
		pcp_save_to_config
		pcp_backup
		pcp_reboot_required
		fi
	;;

esac
#----------------------------------------------------------------------------------------

#======================================DEBUG=============================================
if [ $DEBUG -eq 1 ]; then
	echo '<!-- Start of debug info -->'
	echo '<p class="debug">[ DEBUG ] Audiocard is:   '$AUDIO'<br />'
	echo '                 [ DEBUG ] card is:        '$CARD'<br />'
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
	echo '                 [ DEBUG ] TEXT1 is:       '$TEXT1'<br />'
	echo '                 [ DEBUG ] TEXT2 is:       '$TEXT2'<br />'
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

row_padding() {
	echo '            <tr class="padding '$ROWSHADE'">'
	echo '              <td></td>'
	echo '              <td></td>'
	echo '            </tr>'
}

#========================================================================================
# Below is the blocks that builds the table
#----------------------------------------------------------------------------------------
COL1="column120 center"
COL2=""

#--------------------------------------DSP Filter options--------------------------------
# Only show these options if filters are an option for current sound card.
pcp_soundcard_DSP_options() {
	if [ x"$FILTER1" != x"" ]; then
		pcp_incr_id
		echo '                <p><b>DSP filter options:</b></p>'
		echo '              </td>'
		echo '            </tr>'
		I=1
		while [ $I -le 5 ]; do
			if [ "$(eval echo "\${FILTER${I}}")" != "" ]; then
				echo '            <tr class="'$ROWSHADE'_tight">'
				echo '              <td class="'$COL1'">'
				echo '                <input type="radio" name="DSPFILTER" value="FILTER'$I'" '$(eval echo \${FILTER${I}_CHECK})'>'
				echo '              </td>'
				echo '              <td class="'$COL2'">'
				echo '                <p>'$(eval echo \${FILTER${I}})'</p>'
				echo '              </td>'
				echo '            </tr>'
			fi
			I=$((I+1))
		done
	row_padding
	pcp_toggle_row_shade
	fi
}

#--------------------------------------Simple Mixer Controls analoque volume options--------------------------------
# Only show these options if filters are an option for current sound card.
pcp_soundcard_SMC_Analogue_options() {
	if [ x"$SMC_ANALOGUE" != x"" ]; then
		echo '            <tr class="'$ROWSHADE'_tight">'
		echo '              <td class="colspan 3">'
		echo '                <p><b>Simple Mixer Controls:&nbsp;&nbsp;</b></p>'
		echo '              </td>'
		echo '            </tr>'
		echo '            <tr class="'$ROWSHADE'_tight">'
		echo '              <td class="'$COL1'">'
		echo '                <input type="checkbox" name="SMCFILTER1" value="1" '"$SMC_ANALOGUE_CHECK"'>'
		echo '              </td>'
		echo '              <td class="'$COL2'">'
		echo '                <p>Toggle a 6 dB increase on analogue output level</p>'
		echo '              </td>'
		echo '            </tr>'
		if [ x"$SMC_ANALOGUE_BOOST" != x"" ]; then
			echo '            <tr class="'$ROWSHADE'_tight">'
			echo '              <td class="'$COL1'">'
			echo '                <input type="checkbox" name="SMCFILTER2" value="1" '"$SMC_ANALOGUE_BOOST_CHECK"'>'
			echo '              </td>'
			echo '              <td class="'$COL2'">'
			echo '                <p>Toggle a 0.80 dB increase on analogue output level</p>'
			echo '              </td>'
			echo '            </tr>'
		fi
		row_padding
		pcp_toggle_row_shade
	fi
}

pcp_allo_piano_plus_custom_controls(){
	SUBMODE=$(amixer -c $CARD sget "Subwoofer mode" | grep "Item0" | awk -F\' '{print $2}')
	[ $DEBUG -eq 1 ] && echo '<p class="error">[MODE] Submode='$SUBMODE':</p>'
	[ "$SUBMODE" = "None" ] && SUBMODE=$(amixer -c $CARD sget "Dual Mode" | grep "Item0" | awk -F\' '{print $2}')
	[ $DEBUG -eq 1 ] && echo '<p class="error">[MODE] Dual Mode='$SUBMODE':</p>'
	LOWPASS=$(amixer -c $CARD sget "Lowpass" | grep "Item0" | awk -F\' '{print $2}')

	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="colspan 3">'
	echo '                <p><b>Piano Plus Custom Mixer Controls:</b></p>'
	echo '              </td>'
	echo '            </tr>'
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="'$COL1'">'
	echo '                <select class="large10" name="PIANOSUBMODE" >'
	for I in "2.0" "2.1" "2.2" "Dual-Stereo" "Dual-Mono"; do
		[ "$SUBMODE" = "$I" ] && SELECT="selected" || SELECT=""
		echo '                  <option value="'$I'" '$SELECT'>'$I'</option>'
	done
	echo '                </select>'
	echo '              </td>'
	echo '              <td class="'$COL2'">'
	echo '                <p>Subwoofer Mode.&nbsp;&nbsp'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <p>Set the Mode of the Dual Dacs</p>'
	echo '                  <ul>'
	echo '                    <li><b>2.0</b> - Subwoofer Outputs are not used. All frequencies sent to Left/Right connectors</li>'
	echo '                    <li><b>2.1</b> - Subwoofer Mono Output.  Use crossover frequency to control.</li>'
	echo '                    <li><b>2.2</b> - Subwoofer Stereo Output.  Use crossover frequency to control.</li>'
	echo '                    <li><b>Dual-Stereo</b> - All Frequencies are sent to both DACS.  All Connectors Active</li>'
	echo '                    <li><b>Dual-Mono</b> - Left and Right channels are split between DACs.  LEFT and SUB Right are used.</li>'
	echo '                    <li>2.1 and 2.2 modes require firmware-allo-piano.tcz from the piCorePlayer Repository using the <a href="/cgi-bin/xtras_extensions.cgi?MYMIRROR=http%3A%2F%2Fpicoreplayer.sourceforge.net%2Ftcz_repo%2F&SUBMIT=Set">Extension Browser</a>.</li>'
	echo '                  </ul>'
	echo '                </div>'
	echo '                </p>'
	echo '              </td>'
	echo '            </tr>'
	case $SUBMODE in
		2.1|2.2)
			echo '            <tr class="'$ROWSHADE'">'
			echo '              <td class="'$COL1'">'
			echo '                <select class="large10" name="PIANOLOWPASS" >'
			I=60    #Lowpass frequencies from 60 to 200, in increments of 10
			while [ $I -le 200 ]; do
				[ "$LOWPASS" = "$I" ] && SELECT="selected" || SELECT=""
				echo '                  <option value="'$I'" '$SELECT'>'$I'</option>'
				I=$((I+10))
			done
			echo '                </select>'
			echo '              </td>'
			echo '              <td class="'$COL2'">'
			echo '                <p>Set the Subwoofer Crossover Frequency when in 2.1 or 2.2 mode.</p>'
			echo '              </td>'
			echo '            </tr>'
			SUBVOLTEXT="Sub Output Level"
			VOLTEXT="L/R "
		;;
		Dual-Mono)SUBVOLTEXT="Right Output Level"; VOLTEXT="LEFT ";;
		Dual-Stereo)SUBVOLTEXT="Sub L/R Output Level"; VOLTEXT="L/R ";
	esac
	case $SUBMODE in
		2.0);;
		*)
			ACTUAL_SUB_VOL=$(amixer -c $CARD sget "Subwoofer" | grep "Right: Playback" | awk '{ print $5 }' | tr -d "[]%")
			ACTUAL_SUB_DB=$(amixer -c $CARD sget "Subwoofer" | grep "Right: Playback" | awk '{ print $6 }' | tr -d "[]")
			echo '            <tr class="'$ROWSHADE'">'
			echo '              <td class="'$COL1'">'
			echo '                <p><b>'$SUBVOLTEXT'</b></p>'
			echo '              </td>'
			echo '              <td>'
			echo '                <p style="height:12px">'
			echo '                  <input class="large36"'
			echo '                         id="VoIinputSubid"'
			echo '                         type="range"'
			echo '                         name="VoIinputSubName"'
			echo '                         value='"$ACTUAL_SUB_VOL"''
			echo '                         min="1"'
			echo '                         max="100"'
			echo '                         oninput="VoIOutputSubid.value = VoIinputSubid.value">'
			echo '                </p>'
			echo '              </td>'
			echo '              <td>'
			echo '                <output name="VolOutputSubName" id="VoIOutputSubid">'"$ACTUAL_SUB_VOL"'</output>&nbsppct of max. This equals: <b>'"$ACTUAL_SUB_DB"'</b>'
			echo '              </td>'
			echo '            </tr>'
		;;
	esac
	row_padding
	pcp_toggle_row_shade
}

#--------------ALSA volume options-------------------------------------------------------
# Only show this if ALSA volume control is possible
pcp_soundcard_volume_options() {
	if [ x"$ACTUAL_VOL" != x"" ]; then
		echo '            <tr class="'$ROWSHADE'">'
		echo '              <td class="'$COL1'">'
		echo '                <p><b>'${VOLTEXT}'Output Level</b></p>'
		echo '              </td>'
		echo '              <td>'
		echo '                <p style="height:12px">'
		echo '                  <input class="large36"'
		echo '                         id="VoIinputid"'
		echo '                         type="range"'
		echo '                         name="VoIinputName"'
		echo '                         value='"$ACTUAL_VOL"''
		echo '                         min="1"'
		echo '                         max="100"'
		echo '                         oninput="VoIOutputid.value = VoIinputid.value">'
		echo '                </p>'
		echo '              </td>'
		echo '              <td>'
		echo '                <output name="VolOutputName" id="VoIOutputid">'"$ACTUAL_VOL"'</output>&nbsppct of max. This equals: <b>'"$ACTUAL_DB"'</b>'
		echo '              </td>'
		echo '            </tr>'
		row_padding
		pcp_toggle_row_shade
	fi
}

#--------------------------------------Show Buttons for Volume selection-------------------
# Only show this if ALSA volume control is possible

pcp_Volume_filter_buttons() {
	if [ x"$ACTUAL_VOL" != x"" ]; then
		pcp_incr_id
		echo '            <tr class="'$ROWSHADE'">'
		echo '              <td class="column120 center">'
		echo '                <button type="submit" name="ACTION" value="Test">Set Mixer</button>'
		echo '              </td>'
		echo '              <td class="column120 center">'
		echo '                <input type="submit" name="ACTION" value="Backup">'
		echo '              </td>'
		echo '              <td class="column120 center">'
		[ x"$ACTUAL_DB" != x"" ] && echo '                <input type="submit" name="ACTION" value="0dB">'
		echo '              </td>'
		echo '              <td>'
		echo '                <p><b>&nbsp;&nbsp;</b>'
		echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
		echo '                </p>'
		echo '                <div id="'$ID'" class="less">'
		echo '                  <p>Use above controls to set the alsa mixer, then</p>'
		echo '                  <ul>'
		echo '                    <li><b>Set Mixer</b> - All above values will be written to ALSA, so you can hear the effects.</li>'
		echo '                    <li><b>Backup</b> - The output settings are backed up to make them available after a reboot.</li>'
		echo '                    <li><b>0dB Button</b> - Force outout level to 0dB.</li>'
		echo '                  </ul>'
		echo '                </div>'
		echo '              </td>'
		echo '            </tr>'
		row_padding
	fi
}

#--------------------------------------Parameter options--------------------------------
# Only show these options if Parameters for dtoverlay are an option for current sound card.
pcp_soundcard_parameter_options() {
	. $CONFIGCFG
	if [ "${PARAMS1}${PARAMS2}${PARAMS3}${PARAMS4}${PARAMS5}" != "" ]; then
		pcp_table_end
		pcp_incr_id
		pcp_start_row_shade
		pcp_table_top "Dtoverlay parameter options"
		I=1
		while [ $I -le 5 ]; do
			[ "$(eval echo "\${SPARAMS${I}}")" != "" ] && eval PARAMS${I}_CHECK="checked"
			[ "$(eval echo "\${PARAMS${I}}")" != "" ] && echo '                <input type="checkbox" name="PARAM'$I'" value='$(eval echo \${PARAMS${I}})' '$(eval echo \${PARAMS${I}_CHECK})'><label for="PARAMS'$I'"> '$(eval echo \${PARAMS${I}})'</label><br>'
			I=$((I+1))
		done
		#----------------------------------------------------------------------------------------
		pcp_table_middle
		echo '                <input type="submit" name="ACTION" value="Select">'
	fi

	if [ x"$TEXT1" != x ]; then 
		pcp_table_middle
		pcp_incr_id
		echo '                <p><b>Parameters and notes for your DAC&nbsp;&nbsp;</b>'
		echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
		echo '                </p>'
		echo '                <div id="'$ID'" class="less">'
		echo '                  <p>Select the parameters you want to add to dtoverlay for your DAC. <b>Then a reboot is needed.</b></p>'
		echo '                  <ul>'
		I=1
		while true; do
			eval TEST="\${TEXT${I}}"
			if [ x"$TEST" != x ]; then 
				echo -n '                    <li>'
				eval echo -n "\${TEXT${I}}"
				echo '</li>'
				I=$((I+1))
			else
				break
			fi
		done
		echo '                  </ul>'
		echo '                </div>'
	fi
}

#--------------------------------------Enable/disable build-in analoq sound-------------------
# Enable/diable onboard sound
pcp_disable_enable_buildin_sound() {
	if [ "$GENERIC_CARD" != "ONBOARD" ]; then
		pcp_start_row_shade
		pcp_incr_id
		pcp_table_top "Raspberry Pi Builtin Audio" "colspan=\"2\""
		echo '                <p><b>Enable/disable onboard soundcard (after a reboot)&nbsp;&nbsp;</b></p>'
		pcp_table_middle "class=\"column120 center\""
		echo '                <p><input type="checkbox" name="ONBOARD" value="On" '"$ONBOARD_SOUND_CHECK"'>'
		echo '              </td>'
		echo '              <td class="column420">'
		echo '                <p>When checked - Onboard soundcard is always enabled.&nbsp;&nbsp;'
		echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
		echo '                </p>'
		echo '                <div id="'$ID'" class="less">'
		echo '                  <p>Enable (whith check) or disasable (no check) the onboard analoq soundcard. <b>Then a reboot is needed.</b></p>'
		echo '                </div>'
		pcp_table_middle "class=\"column120 center\""
		echo '                <button type="submit" name="ACTION" value="Onboard">Save</button>'
		pcp_table_end
	fi
}

#========================================================================================
# Build the Table
#----------------------------------------------------------------------------------------
echo '<form name="manual_adjust" action="'$0'" method="get">'
pcp_start_row_shade
pcp_incr_id
pcp_table_top "Alsa Mixer Adjustment for: $LISTNAME" "colspan=\"2\""

if [ "$GENERIC_CARD" = "TI51XX" ] || [ "$GENERIC_CARD" = "ONBOARD" ] || [ "$GENERIC_CARD" = "HIFIBERRY_AMP" ]; then 
	pcp_soundcard_DSP_options
	pcp_soundcard_SMC_Analogue_options
	[ "$AUDIO" = "allo_piano_dac_plus" ] && pcp_allo_piano_plus_custom_controls
	pcp_soundcard_volume_options
	pcp_Volume_filter_buttons 
	pcp_soundcard_parameter_options
fi

[ "$GENERIC_CARD" = "ES9023" ] && pcp_soundcard_DSP_options && pcp_soundcard_volume_options && pcp_Volume_filter_buttons && pcp_soundcard_parameter_options

[ x"$GENERIC_CARD" = x"" ] && echo "$TEXT"

# HTML Formatting Cleanup for Onboard Audio setting only.
[ "$GENERIC_CARD" = "ONBOARD" ] && ( echo '            <tr class="'$ROWSHADE'">'; echo '              <td>' )
pcp_table_end

pcp_disable_enable_buildin_sound
echo '</form>'
#-----------------------------------------------------------------------------------------

pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'
