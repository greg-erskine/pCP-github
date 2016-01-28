#!/bin/sh

# Version: 0.01 2016-01-29 GE
#	Original version.

. pcp-functions
pcp_variables
. $CONFIGCFG

SET_EQUAL="sudo amixer -D equal cset numid="
BAND=1
PRESETS=0
i=1

# Labels for equalizer bands
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

pcp_html_head "xtras alsaequal" "GE"

pcp_controls
pcp_banner
pcp_navigation
pcp_running_script
pcp_httpd_query_string

#========================================================================================
# Routines
#----------------------------------------------------------------------------------------
pcp_load_equaliser() {
	for VALUE in $RANGE
	do
		${SET_EQUAL}$BAND $VALUE >/dev/null 2>&1
		BAND=$(($BAND + 1))
	done
}

#----------------------------------------------------------------------------------------
if [ -f /home/tc/.alsaequal.presets ]; then
	PRESETS=1
	. /home/tc/.alsaequal.presets
	PRESET_NAMES=$(cat /home/tc/.alsaequal.presets | awk -F= '{print $1}')
fi

case $ACTION in
	Test)
		RANGE="$R1 $R2 $R3 $R4 $R5 $R6 $R7 $R8 $R9 $R10"
		;;
	Backup)
		RANGE="$R1 $R2 $R3 $R4 $R5 $R6 $R7 $R8 $R9 $R10"
		pcp_backup >/dev/null 2>&1
		;;
	Reset)
		RANGE="66 66 66 66 66 66 66 66 66 66"
		;;
esac

pcp_load_equaliser

# Determine if alsaequalizer is loaded
CURRENT_EQ_SETTINGS=$(sudo amixer -D equal contents | grep ": values" | awk -F"," '{print $2}')

if [ x"" = x"$CURRENT_EQ_SETTINGS" ]; then
	echo '<p class="error">[ ERROR ] Alsa equalizer package is not loaded...</p>'
	echo '<p class="info">[ INFO ] Please try to reboot.</p>'
	sleep 1
	pcp_reboot_required
fi

#-----------------------------Manual Equalizer Adjustment--------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Manual Equalizer Adjustment</legend>'
#----------------------------------------------------------------------------------------
pcp_incr_id
echo '          <table class="bggrey percent100">'
echo '            <form name="manual_adjust" action="'$0'" method="get">'
pcp_start_row_shade

for VALUE in $CURRENT_EQ_SETTINGS
do
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td>'
	echo '                  <p style="height:12px"><input class="large36" type="range" name="R'$i'" value="'$VALUE'" min="0" max="100">&nbsp;&nbsp;'$(eval "echo \$LB$i")'</p>'
	echo '                </td>'
	echo '              </tr>'
	i=$((i + 1))
done

echo '              <tr class="'$ROWSHADE'">'
echo '                <td>'
echo '                  <p style="height:10px"></p>'
echo '                </td>'
echo '              </tr>'

pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td>'
echo '                  <input type="submit" name="ACTION" value="Test">'
echo '                  <input type="submit" name="ACTION" value="Backup">'
echo '                  <input type="submit" name="ACTION" value="Reset">'
echo '                </td>'
echo '              </tr>'
echo '              <tr class="'$ROWSHADE'">'
echo '                <td>'
echo '                  <p><b>10-band equalizer&nbsp;&nbsp;</b>'
echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                  </p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <p>Use the sliders to adjust the soundstage, then</p>'
echo '                    <ul>'
echo '                      <li><b>Test</b> - The changes will be written to ALSA, so you can hear the effects.</li>'
echo '                      <li><b>Backup</b> - The equalizer settings are backed up to make them available after a reboot.</li>'
echo '                      <li><b>Reset</b> - Set the equalizer to the defaults settings.</li>'
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

#--------------------------------------Presets-------------------------------------------
if [ $PRESETS = 1 ]; then
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Presets</legend>'
	#----------------------------------------------------------------------------------------
	pcp_incr_id
	echo '          <table class="bggrey percent100">'
	echo '            <form name="presets" action="'$0'" method="get">'
	pcp_start_row_shade
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
	echo '                  <p>Select one of your preset&nbsp;&nbsp;</b>'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Use [Test] and [Backup] after selecting preset to make it permanent.</p>'
	echo '                    <p>Presets are:</p>'
	echo '                    <ul>'
	echo '                      <li>An advanced feature that requires some linux skills to maintain.</li>'
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
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'" >'
	echo '                <td colspan=3>'
	echo '                  <input type="submit" name="ACTION" value="Preset">'
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
fi
#----------------------------------------------------------------------------------------

pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'