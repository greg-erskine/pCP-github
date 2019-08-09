#!/bin/sh

# Version: 6.0.0 2019-08-09

. pcp-functions

pcp_html_head "xtras ALSA equal" "GE"

pcp_controls
pcp_banner
pcp_navigation
pcp_httpd_query_string

SET_EQUAL="sudo amixer -D equal cset numid="
BAND=1
PRESETS=0
i=1

#========================================================================================
# Labels for equalizer bands
#----------------------------------------------------------------------------------------
LB1="31 Hz"
LB2="63 Hz"
LB3="125 Hz"
LB4="250 Hz"
LB5="500 Hz"
LB6="1 kHz"
LB7="2 kHz"
LB8="4 kHz"
LB9="8 kHz"
LB10="16 kHz"

if [ -f /home/tc/.alsaequal.presets ]; then
	PRESETS=1
	. /home/tc/.alsaequal.presets
	PRESET_NAMES=$(cat /home/tc/.alsaequal.presets | awk -F= '{print $1}')
fi

case "$ACTION" in
	Test)
		RANGE="$R1 $R2 $R3 $R4 $R5 $R6 $R7 $R8 $R9 $R10"
	;;
	Save)
		RANGE="$R1 $R2 $R3 $R4 $R5 $R6 $R7 $R8 $R9 $R10"
		pcp_backup >/dev/null 2>&1
	;;
	Reset)
		RANGE="66 66 66 66 66 66 66 66 66 66"
	;;
esac

for VALUE in $RANGE
do
	${SET_EQUAL}$BAND $VALUE >/dev/null 2>&1
	BAND=$((BAND+1))
done

# Determine if ALSA equalizer is loaded
CURRENT_EQ_SETTINGS=$(sudo amixer -D equal contents | grep ": values" | awk -F"," '{print $2}')

if [ x"" = x"$CURRENT_EQ_SETTINGS" ]; then
	pcp_table_top "Error"
	pcp_message ERROR "ALSA Equalizer is not loaded." "html"
	pcp_message INFO "Load ALSA Equalizer from the [Tweaks] page." "html"
	pcp_table_end
	pcp_html_end
fi

#-----------------------------Manual Equalizer Adjustment--------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Manual Equalizer Adjustment</legend>'
echo '          <table class="bggrey percent100">'
echo '            <form name="manual_adjust" action="'$0'" method="get">'
#----------------------------------------------------------------------------------------
pcp_start_row_shade
for VALUE in $CURRENT_EQ_SETTINGS
do
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="small2">'
	echo '                  <output name="P'$i'" id="P'$i'" for="R'$i'">'$VALUE'</output>'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p style="height:12px">'
	echo '                    <input class="large36"'
	echo '                           type="range"'
	echo '                           id="R'$i'"'
	echo '                           name="R'$i'"'
	echo '                           value="'$VALUE'"'
	echo '                           min="0"'
	echo '                           max="100"'
	echo '                           oninput="P'$i'.value=R'$i'.value"'
	echo '                    >&nbsp;&nbsp;&nbsp;'$(eval "echo \$LB$i")
	echo '                  </p>'
	echo '                </td>'
	echo '              </tr>'
	i=$((i+1))
done
#----------------------------------------------------------------------------------------
echo '              <tr class="'$ROWSHADE'">'
echo '                <td>'
echo '                  <p style="height:0px"></p>'
echo '                </td>'
echo '              </tr>'
#----------------------------------------------------------------------------------------
pcp_table_padding
#----------------------------------------------------------------------------------------
echo '              <tr class="'$ROWSHADE'">'
echo '                <td>'
echo '                  <input type="submit" name="ACTION" value="Save">'
echo '                  <input type="submit" name="ACTION" value="Reset">'
echo '                  <input type="submit" name="ACTION" value="Test">'
echo '                </td>'
echo '              </tr>'
#----------------------------------------------------------------------------------------
pcp_incr_id
echo '              <tr class="'$ROWSHADE'">'
echo '                <td>'
echo '                  <p><b>10-band equalizer&nbsp;&nbsp;</b>'
echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                  </p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <p>Use the sliders to adjust the soundstage, then</p>'
echo '                    <ul>'
echo '                      <li><b>Save</b> - The equalizer settings are saved to make them available after a reboot.</li>'
echo '                      <li><b>Test</b> - The changes will be written to ALSA, so you can hear the effects.</li>'
echo '                      <li><b>Reset</b> - Set the equalizer to the defaults settings.</li>'
echo '                    </ul>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'
#----------------------------------------------------------------------------------------
echo '            </form>'
echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------

#--------------------------------------Presets-------------------------------------------
if [ $PRESETS -eq 1 ]; then
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Presets</legend>'
	echo '          <table class="bggrey percent100">'
	echo '            <form name="presets" action="'$0'" method="get">'
	#------------------------------------------------------------------------------------
	pcp_start_row_shade
	pcp_incr_id
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>Preset</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <select class="large16" name="RANGE">'

	for VALUE in $PRESET_NAMES
	do
		echo '                    <option value="'$(eval "echo \$$VALUE")'">'$VALUE'</option>'
	done

	echo '                  </select>'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Select one of your presets&nbsp;&nbsp;</b>'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Use [Save] and [Test] after selecting preset to make it permanent.</p>'
	echo '                    <p>Presets are:</p>'
	echo '                    <ul>'
	echo '                      <li>An advanced feature that requires some Linux skills to maintain.</li>'
	echo '                      <li>Stored in the file $HOME/.alsaequal.presets</li>'
	echo '                      <li>Edited using a text editor such as vi.</li>'
	echo '                      <li>The format of the presets file is important, i.e.</li>'
	echo '                      <ul>'
	echo '                        <li>RESET="66 66 66 66 66 66 66 66 66 66"</li>'
	echo '                        <li>The name of the preset is a simple single word, no spaces.</li>'
	echo '                        <li>There are 10 values between 0 and 100, enclosed in double quotes.</li>'
	echo '                      </ul>'
	echo '                    </ul>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	#------------------------------------------------------------------------------------
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td colspan="3">'
	echo '                  <input type="submit" name="ACTION" value="Use Preset">'
	echo '                </td>'
	echo '              </tr>'
	#------------------------------------------------------------------------------------
	echo '            </form>'
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
fi
#----------------------------------------------------------------------------------------

pcp_html_end