#!/bin/sh

# Version: 5.0.0 2019-04-20

. pcp-functions
. pcp-soundcard-functions
. pcp-lms-functions

# Save copy of variable values so it is not overwritten with default values
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

unset REBOOT_REQUIRED

pcp_selected_soundcontrol
pcp_generic_card_control

# Check for built-in soundcard
cat /proc/asound/cards | grep -q bcm2835
ACTUAL_ONBOARD_STATUS=$?
[ $ACTUAL_ONBOARD_STATUS -eq 0 ] && ONBOARD_SND="On" || ONBOARD_SND="Off"
[ "$ONBOARD_SND" = "On" ] && ONBOARD_SOUND_CHECK="checked" || ONBOARD_SOUND_CHECK=""

#========================================ACTIONS=========================================
if [ "$ACTION" != "" ]; then
	pcp_table_top "Setting Alsa"
	echo '                <textarea class="inform" style="height:60px">'
fi
case "$ACTION" in
	Save)
		echo '[ INFO ] Setting Alsa mixer.'
		#Special case for rpi card to allow for setting 0db
		if [ $CARD = "ALSA" -a $VolInputName -eq 96 ]; then
			sudo amixer -c $CARD sset $SSET 0db >/dev/null 2>&1
		else
			sudo amixer -c $CARD sset $SSET $VolInputName'%' >/dev/null 2>&1
		fi

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
		#----------------------------Allo Katana Specific Controls-----------------------
		if [ $CARD = "Katana" ]; then
			sudo amixer -c $CARD sset Deemphasis "$DEEM" >/dev/null 2>&1
		fi
		#----------------------------Allo Piano Plus Dac Controls------------------------
		case "$PIANOSUBMODE" in
			"2.0") sudo amixer -c $CARD sset 'Subwoofer mode' "$PIANOSUBMODE" >/dev/null 2>&1;;
			Dual*) sudo amixer -c $CARD sset 'Dual Mode' "$PIANOSUBMODE" >/dev/null 2>&1;;
			"2.1"|"2.2")
				df | grep -q "allo-piano"
				if [ $? -eq 0 ]; then
					sudo amixer -c $CARD sset 'Subwoofer mode' "$PIANOSUBMODE" >/dev/null 2>&1
				else
					echo '<p class="error">[ERROR] firmware-allo-piano.tcz not loaded for the selected mode.</p>'
				fi
			;;
			*);;
		esac
		[ "$PIANOLOWPASS" != "" ] && sudo amixer -c $CARD sset 'Lowpass' "$PIANOLOWPASS" >/dev/null 2>&1
		[ "$VolInputSubName" != "" ] && sudo amixer -c $CARD sset "Subwoofer" $VolInputSubName'%' >/dev/null 2>&1
		#--------------------------------------------------------------------------------
		pcp_generic_card_control

		AUDIO="$ORIG_AUDIO"
		OUTPUT="$ORIG_OUTPUT"
		ALSA_PARAMS="$ORIG_ALSA_PARAMS"
		ALSAlevelout="Custom"
		pcp_save_to_config
		echo '[ INFO ] Saving Alsa State.'
		sudo alsactl store
		pcp_backup "nohtml"
	;;
	0dB)
		echo '[ INFO ] Setting volume to 0dB.'
		sudo amixer -c $CARD sset $SSET 0dB >/dev/null 2>&1
		pcp_generic_card_control
		ALSAlevelout="Custom"
		pcp_save_to_config
		echo '[ INFO ] Saving Alsa State.'
		sudo alsactl store
		pcp_backup "nohtml"
	;;
	4dB)
		echo '[ INFO ] Setting volume to 4dB.'
		sudo amixer -c $CARD sset $SSET 4dB >/dev/null 2>&1
		pcp_generic_card_control
		ALSAlevelout="Custom"
		pcp_save_to_config
		echo '[ INFO ] Saving Alsa State.'
		sudo alsactl store
		pcp_backup "nohtml"
	;;
	Select)
		echo '[ INFO ] Setting soundcard driver parameters.'
		AUDIO="$ORIG_AUDIO"
		CARD="$ORIG_CARD"
		OUTPUT="$ORIG_OUTPUT"
		ALSA_PARAMS="$ORIG_ALSA_PARAMS"
		pcp_save_to_config
		pcp_read_chosen_audio
		pcp_backup "nohtml"
		REBOOT_REQUIRED=TRUE
	;;
	Onboard)
		# Check for changes in onboard status as we don't want to mount and umount if not needed
		SELECTED_BOARD="On"
		[ x"$ONBOARD" = x"" ] && SELECTED_BOARD="Off"
		if [ "$ONBOARD_SND" != "$SELECTED_BOARD" ]; then
			pcp_mount_bootpart_nohtml >/dev/null 2>&1
			if [ "$ONBOARD" = "On" ]; then
				echo '[ INFO ] Enabling RPi Built-in Audio.'
				pcp_re_enable_analog
			else
				echo '[ INFO ] Disabling RPi Built-in Audio.'
				pcp_disable_analog
				sudo rmmod snd_bcm2835
			fi
			# This page should not be changing ALSA_PARAMS.
			ALSA_PARAMS="$ORIG_ALSA_PARAMS"
			pcp_umount_bootpart_nohtml
			pcp_save_to_config
			pcp_backup "nohtml"
			REBOOT_REQUIRED=TRUE
		fi
	;;
	Reset)
		echo '[ INFO ] Removing alsa saved states.'
		rm -f /var/lib/alsa/asound.state
		touch /var/lib/alsa/asound.state
		ALSAlevelout="Default"
		pcp_save_to_config
		pcp_backup "nohtml"
	;;
esac
if [ "$ACTION" != "" ]; then
	echo '                </textarea>'
	pcp_table_end
	[ $REBOOT_REQUIRED ] && pcp_reboot_required
fi
#----------------------------------------------------------------------------------------

#======================================DEBUG=============================================
if [ $DEBUG -eq 1 ]; then
	echo '<!-- Start of debug info -->'
	pcp_debug_variables "html" AUDIO CARD SSET DSP DTOVERLAY GENERIC_CARD \
		PARAMS1 PARAMS2 PARAMS3 PARAMS4 PARAMS5 \
		FILTER1 FILTER2 FILTER3 FILTER4 FILTER5 FILTER6 FILTER7 \
		TEXT1 TEXT2 TEXT3 TEXT4 TEXT5 \
		ACTUAL_VOL ACTUAL_DB ACTUAL_FILTER FILTER \
		FILTER1_CHECK FILTER2_CHECK FILTER3_CHECK FILTER4_CHECK FILTER5_CHECK FILTER6_CHECK FILTER7_CHECK \
		DEEMPHASIS DEEM1 DEEM2 DEEM3 DEEM4 DEEM1_CHECK DEEM2_CHECK DEEM3_CHECK DEEM4_CHECK ALSA_PARAMS
	echo '<!-- End of debug info -->'
fi

row_padding() {
	echo '            <tr class="padding '$ROWSHADE'">'
	echo '              <td colspan="3">'
	echo '              </td>'
	echo '            </tr>'
}

#========================================================================================
# Below is the blocks that builds the table
#----------------------------------------------------------------------------------------
COL1="column120 center"
COL2=""

#========================================================================================
# DSP Filter options
# - Only show these options if filters are an option for current sound card.
#----------------------------------------------------------------------------------------
pcp_soundcard_DSP_options() {
	if [ x"$FILTER1" != x"" ]; then
		pcp_incr_id
		echo '                <p><b>DSP filter options:</b></p>'
		echo '              </td>'
		echo '            </tr>'
		I=1
		while [ $I -le $NUMFILTERS ]; do
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

#========================================================================================
# Simple Mixer Controls analoque volume options
# - Only show these options if filters are an option for current sound card.
#----------------------------------------------------------------------------------------
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
		echo '              <td class="'$COL2'" colspan="2">'
		echo '                <p>Toggle a 6dB increase on analog output level</p>'
		echo '              </td>'
		echo '            </tr>'
		if [ x"$SMC_ANALOGUE_BOOST" != x"" ]; then
			echo '            <tr class="'$ROWSHADE'_tight">'
			echo '              <td class="'$COL1'">'
			echo '                <input type="checkbox" name="SMCFILTER2" value="1" '"$SMC_ANALOGUE_BOOST_CHECK"'>'
			echo '              </td>'
			echo '              <td class="'$COL2'" colspan="2">'
			echo '                <p>Toggle a 0.80dB increase on analog output level</p>'
			echo '              </td>'
			echo '            </tr>'
		fi
		row_padding
		pcp_toggle_row_shade
	fi
}

#========================================================================================
# Deemphasis settings - Currently only for Katana
#----------------------------------------------------------------------------------------
pcp_soundcard_Deemphasis_options() {
	pcp_incr_id
	echo '            <tr class="'$ROWSHADE'_tight">'
	echo '              <td class="colspan 3">'
	echo '                <p><b>Deemphasis options:</b></p>'
	echo '              </td>'
	echo '            </tr>'
	I=1
	while [ $I -le $NUMDEEM ]; do
		if [ "$(eval echo "\${DEEM${I}}")" != "" ]; then
			echo '            <tr class="'$ROWSHADE'_tight">'
			echo '              <td class="'$COL1'">'
			echo '                <input type="radio" name="DEEMPHASIS" value="DEEM'$I'" '$(eval echo \${DEEM${I}_CHECK})'>'
			echo '              </td>'
			echo '              <td class="'$COL2'">'
			echo '                <p>'$(eval echo \${DEEM${I}})'</p>'
			echo '              </td>'
			echo '            </tr>'
		fi
		I=$((I+1))
	done
	row_padding
	pcp_toggle_row_shade
}

#========================================================================================
# Allo Piano Plus Custom Controls
#----------------------------------------------------------------------------------------
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
	echo '              <td class="'$COL2'" colspan="2">'
	echo '                <p>Subwoofer Mode.&nbsp;&nbsp;'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <p>Set the Mode of the Dual Dacs</p>'
	echo '                  <ul>'
	echo '                    <li><b>2.0</b> - Subwoofer Outputs are not used. All frequencies sent to Left/Right connectors</li>'
	echo '                    <li><b>2.1</b> - Subwoofer Mono Output. Use crossover frequency to control.</li>'
	echo '                    <li><b>2.2</b> - Subwoofer Stereo Output. Use crossover frequency to control.</li>'
	echo '                    <li><b>Dual-Stereo</b> - All Frequencies are sent to both DACS. All Connectors Active.</li>'
	echo '                    <li><b>Dual-Mono</b> - Left and Right channels are split between DACs. LEFT and SUB Right are used.</li>'
	echo '                    <li>2.1 and 2.2 modes require firmware-allo-piano.tcz from the piCorePlayer Repository using the <a href="/cgi-bin/xtras_extensions.cgi?MYMIRROR=https%3A%2F%2Frepo.picoreplayer.org%2Frepo%2F&SUBMIT=Set">Extension Browser</a>.</li>'
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
			# Lowpass frequencies from 60 to 200, in increments of 10
			I=60
			while [ $I -le 200 ]; do
				[ "$LOWPASS" = "$I" ] && SELECT="selected" || SELECT=""
				echo '                  <option value="'$I'" '$SELECT'>'$I'</option>'
				I=$((I+10))
			done
			echo '                </select>'
			echo '              </td>'
			echo '              <td class="'$COL2'" colspan="2">'
			echo '                <p>Set the Subwoofer Crossover Frequency when in 2.1 or 2.2 mode.</p>'
			echo '              </td>'
			echo '            </tr>'
		;;
	esac
	case $SUBMODE in
		2.0|Dual-Mono|Dual-Stereo) VOLTEXT="Master ";;
		*)
			SUBVOLTEXT="Sub Output Level"
			VOLTEXT="Primary "
			ACTUAL_SUB_VOL=$(amixer -c $CARD sget "Subwoofer" | grep "Right: Playback" | awk '{ print $5 }' | tr -d "[]%")
			ACTUAL_SUB_DB=$(amixer -c $CARD sget "Subwoofer" | grep "Right: Playback" | awk '{ print $6 }' | tr -d "[]")
			echo '            <tr class="'$ROWSHADE'">'
			echo '              <td class="'$COL1'">'
			echo '                <p><b>'$SUBVOLTEXT'</b></p>'
			echo '              </td>'
			echo '              <td>'
			echo '                <p style="height:12px">'
			echo '                  <input class="large36"'
			echo '                         id="VolInputSubId"'
			echo '                         type="range"'
			echo '                         name="VolInputSubName"'
			echo '                         value='"$ACTUAL_SUB_VOL"''
			echo '                         min="1"'
			echo '                         max="100"'
			echo '                         oninput="VolOutputSubId.value = VolInputSubId.value">'
			echo '                </p>'
			echo '              </td>'
			echo '              <td>'
			echo '                <output name="VolOutputSubName" id="VolOutputSubId">'"$ACTUAL_SUB_VOL"'</output>&nbsp;pct of max. <b>Current:</b> '"$ACTUAL_SUB_DB"''
			echo '              </td>'
			echo '            </tr>'
		;;
	esac
	row_padding
	pcp_toggle_row_shade
}

#========================================================================================
# ALSA volume options
# - Only show this if ALSA volume control is possible.
#----------------------------------------------------------------------------------------
pcp_soundcard_volume_options() {
	if [ x"$ACTUAL_VOL" != x"" ]; then
		echo '            <tr class="'$ROWSHADE'">'
		echo '              <td class="'$COL1'">'
		echo '                <p><b>'${VOLTEXT}'Output Level</b></p>'
		echo '              </td>'
		echo '              <td>'
		echo '                <p style="height:12px">'
		echo '                  <input class="large36"'
		echo '                         id="VolInputId"'
		echo '                         type="range"'
		echo '                         name="VolInputName"'
		echo '                         value='"$ACTUAL_VOL"''
		echo '                         min="1"'
		echo '                         max="100"'
		echo '                         oninput="VolOutputId.value = VolInputId.value;">'
		echo '                </p>'
		echo '              </td>'
		echo '              <td>'
		echo '                <output name="VolOutputName" id="VolOutputId">'"$ACTUAL_VOL"'</output>&nbsp;pct of max. <b>Current:</b> '"$ACTUAL_DB"''
		echo '              </td>'
		echo '            </tr>'
		row_padding
		pcp_toggle_row_shade
	fi
}

#========================================================================================
# Show Buttons for Volume selection
# - Only show this if ALSA volume control is possible.
#----------------------------------------------------------------------------------------
pcp_volume_filter_buttons() {
	if [ x"$ACTUAL_VOL" != x"" ]; then
		pcp_incr_id
		echo '            <tr class="'$ROWSHADE'">'
		echo '              <td class="column120 center">'
		echo '                <input type="submit" name="ACTION" value="Save">'
		echo '              </td>'
		echo '              <td class="column120 center">'
		echo '                <input type="submit" name="ACTION" value="0dB">'
		echo '              </td>'
		if [ $CARD = "ALSA" ]; then
			echo '              <td class="column120 center">'
			echo '                <input type="submit" name="ACTION" value="4dB">'
			echo '              </td>'
		fi
		echo '              <td>'
		echo '                <p>'
		echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
		echo '                </p>'
		echo '                <div id="'$ID'" class="less">'
		echo '                  <p>Use above control(s) to set the ALSA mixer, then</p>'
		echo '                  <ul>'
		echo '                    <li><b>Save</b> - The output setting(s) are saved up to make them available after a reboot.</li>'
		echo '                    <li><b>0dB</b> - Set output level to 0dB.</li>'
		if [ $CARD = "ALSA" ]; then
			echo '                    <li><b>4dB</b> - Set output level to 4dB (100%).</li>'
		fi
		echo '                  </ul>'
		echo '                </div>'
		echo '              </td>'
		echo '            </tr>'
		row_padding
	fi
}

pcp_reset_alsactl() {
	pcp_toggle_row_shade
	pcp_incr_id
	pcp_table_top "Reset ALSA Configuration" "colspan=\"3\""
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column120 center">'
	echo '                <input type="submit" name="ACTION" value="Reset">'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>Reset saved alsa settings&nbsp;&nbsp;'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <p>After reset, you will need to resave mixer settings.</p>'
	echo '                </div>'
	echo '              </td>'
	echo '            </tr>'
	row_padding
	pcp_table_end
}


#========================================================================================
# Parameter options
# - Only show these options if Parameters for dtoverlay are an option for current
#   sound card.
#----------------------------------------------------------------------------------------
pcp_soundcard_parameter_options() {
	. $PCPCFG
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
		#--------------------------------------------------------------------------------
		pcp_table_middle
		echo '                <button type="submit" name="ACTION" value="Select">Save</button>'
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
			eval CHK="\${TEXT${I}}"
			if [ x"$CHK" != x ]; then
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

#========================================================================================
# Enable/disable built-in analoq sound
#----------------------------------------------------------------------------------------
pcp_disable_enable_builtin_sound() {
	if [ "$GENERIC_CARD" != "ONBOARD" ]; then
		pcp_start_row_shade
		pcp_incr_id
		pcp_table_top "Raspberry Pi Built-in Audio"
		echo '                <p><b>Enable/disable built-in audio (after a reboot)</b></p>'
		pcp_table_middle "class=\"column120 center\""
		echo '                <p><input type="checkbox" name="ONBOARD" value="On" '"$ONBOARD_SOUND_CHECK"'>'
		echo '              </td>'
		echo '              <td colspan="2">'
		echo '                <p>When checked - built-in audio is enabled&nbsp;&nbsp;'
		echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
		echo '                </p>'
		echo '                <div id="'$ID'" class="less">'
		echo '                  <p>Enable (with check) or disable (no check) the built-in audio. <b>Then a reboot is needed.</b></p>'
		echo '                </div>'
		pcp_table_middle "class=\"column120 center\""
		echo '                <button type="submit" name="ACTION" value="Onboard">Save</button>'
		pcp_table_end
	fi
}

#========================================================================================
# Build the table
#----------------------------------------------------------------------------------------
echo '<form name="manual_adjust" action="'$0'" method="get">'
pcp_start_row_shade
pcp_incr_id
pcp_table_top "ALSA Mixer Adjustment for: $LISTNAME" "colspan=\"3\""

if [ "$GENERIC_CARD" = "TI51XX" ] || [ "$GENERIC_CARD" = "ONBOARD" ] || [ "$GENERIC_CARD" = "HIFIBERRY_AMP" ]; then
	pcp_soundcard_DSP_options
	pcp_soundcard_SMC_Analogue_options
	[ "$AUDIO" = "allo_piano_dac_plus" ] && pcp_allo_piano_plus_custom_controls
	pcp_soundcard_volume_options
	pcp_volume_filter_buttons
	pcp_soundcard_parameter_options
fi

if [ "$GENERIC_CARD" = "Katana" ]; then
	pcp_soundcard_DSP_options
	pcp_soundcard_Deemphasis_options
	pcp_soundcard_volume_options
	pcp_volume_filter_buttons
	pcp_soundcard_parameter_options
fi

if [ "$GENERIC_CARD" = "ES9023" ]; then
	pcp_soundcard_DSP_options
	pcp_soundcard_volume_options
	pcp_volume_filter_buttons
	pcp_soundcard_parameter_options
fi

[ x"$GENERIC_CARD" = x"" ] && echo "$TEXT"

# HTML formatting Cleanup for built-in audio setting only
if [ "$GENERIC_CARD" = "ONBOARD" ]; then
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td colspan="3">'
fi
pcp_table_end

pcp_reset_alsactl

pcp_disable_enable_builtin_sound
echo '</form>'
#----------------------------------------------------------------------------------------

pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'
