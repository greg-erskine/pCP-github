#!/bin/sh

# Version: 5.0.0 2019-03-01

. pcp-functions
. pcp-soundcard-functions

pcp_html_head "Shairport-sync" "SBP"

SHAIRPORT_CONFIG="$PCPCFG"
SECTION_NAME=SHAIRPORTSYNC

pcp_banner
pcp_navigation
pcp_running_script
pcp_httpd_query_string

#========================================================================================
# Initial setup routines.
# - Primary install will use default settings from DAC definitions.
#----------------------------------------------------------------------------------------
pcp_shairportsettings_to_config() {
	pcp_write_var_to_config SHAIRPORT_OUT "$SHAIRPORT_OUT"
	pcp_write_var_to_config SHAIRPORT_CONTROL "$SHAIRPORT_CONTROL"
	pcp_backup
}

pcp_shairport_default() {
	if [ "$SHAIRPORT_OUT" = "Please change" ]; then
		pcp_selected_soundcontrol
		pcp_shairportsettings_to_config
	fi
}
pcp_shairport_default

#========================================================================================
# Debug information
#----------------------------------------------------------------------------------------
SHAIRPORT_VERSION=$(/usr/local/sbin/shairport-sync -V)

pcp_debug_information() {
	if [ $DEBUG -eq 1 ]; then
		pcp_table_top "Debug information"
		echo '<!-- Start of debug info -->'
		pcp_debug_variables "html" SHAIRPORT_VERSION SHAIRPORT_OUT SHAIRPORT_CONTROL \
		OUTPUT SHAIRPORTSYNC_SHAIRPORT SHAIRPORT
		echo '<!-- End of debug info -->'
		pcp_table_end
	fi
}
pcp_debug_information

#========================================================================================
# Main
#----------------------------------------------------------------------------------------
case "$ACTION" in
	Start)
		pcp_table_top "Starting Shairport-sync"
		pcp_shairport_start
		pcp_table_end
	;;
	Stop)
		pcp_table_top "Stopping Shairport-sync"
		pcp_shairport_stop
		pcp_table_end
		sleep 1
	;;
	Restart)
		pcp_table_top "Restarting Shairport-sync"
		pcp_shairport_stop
		sleep 1
		pcp_shairport_start
		pcp_table_end
	;;
	Default)
		pcp_table_top "Setting defaults for Shairport-sync"
		pcp_selected_soundcontrol
		echo '[ INFO ] Writing to '${SHAIRPORT_CONFIG}'...'
		pcp_shairportsettings_to_config
		pcp_table_end
	;;
	Save)
		pcp_table_top "Starting Shairport-sync"
		echo '[ INFO ] Writing to '${SHAIRPORT_CONFIG}'...'
		pcp_shairportsettings_to_config
		pcp_table_end
	;;
	*)
		ACTION="Initial"
	;;
esac

. /$SHAIRPORT_CONFIG

COLUMN1="column210 center"
#========================================================================================
# Shairport-sync settings table
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Shairport-sync Settings</legend>'
echo '          <form name="settings" action="'$0'" method="get">'
echo '            <table class="bggrey percent100">'
#----------------------------------------------------------------------------------------

#--------------------------------shairport-sync output name------------------------------
pcp_incr_id
pcp_start_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="'$COLUMN1'">'
echo '                  <input class="large15"'
echo '                         type="text"'
echo '                         name="SHAIRPORT_OUT"'
echo '                         value="'$SHAIRPORT_OUT'"'
echo '                  >'
echo '                </td>'
echo '                <td>'
echo '                  <p>Set name of Shairport-sync output device&nbsp;&nbsp;'
echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                  </p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <p>If not changed Shairport-sync output device will be the default DAC specific values.</p>'
echo '                    <p>If equalizer is enabled use equal as output device name.</p>'
echo '                    <p>Please experiment if default settings are wrong.</p>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'
#----------------------------------------------------------------------------------------

#------------------------------shairport-sync control name-------------------------------
pcp_incr_id
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="'$COLUMN1'">'
echo '                  <input class="large15"'
echo '                         type="text"'
echo '                         name="SHAIRPORT_CONTROL"'
echo '                         value="'$SHAIRPORT_CONTROL'"'
echo '                  >'
echo '                </td>'
echo '                <td>'
echo '                  <p>Set name of Output control used for Shairport-sync&nbsp;&nbsp;'
echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                  </p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <p>Often the control name is Digital or PCM or left empty.</p>'
echo '                    <p>If not changed Shairport-sync will use the default DAC specific values.</p>'
echo '                    <p>If equalizer is enabled, the control name should be left empty.</p>'
echo '                    <p>Please experiment if default settings are wrong.</p>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'
#----------------------------------------------------------------------------------------

#----------------------------------------Default-----------------------------------------
pcp_incr_id
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="'$COLUMN1'">'
echo '                  <input type="submit"'
echo '                         name="ACTION"'
echo '                         value="Default"'
echo '                         title="Default Settings"'
echo '                  />'
echo '                </td>'
echo '                <td>'
echo '                  <p>Load default Shairport-sync settings for your DAC&nbsp;&nbsp;'
echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                  </p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <p>If needed change the settings and restart Shairport-sync to test the new settings.</p>'
echo '                    <p>Remember to save your settings... and restart Shairport-sync</p>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'
#----------------------------------------------------------------------------------------

#------------------------------------------Save------------------------------------------
pcp_incr_id
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="'$COLUMN1'" colspan="2">'
echo '                  <input type="submit"'
echo '                         name="ACTION"'
echo '                         value="Save"'
echo '                         title="Save Shairport-sync settings"'
echo '                  />'
echo '                </td>'
echo '              </tr>'
#----------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------
echo '            </table>'
echo '          </form>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------

COLUMN1="column210 center"
#========================================================================================
# Shairport-sync Start,stop/restart table
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Control of Shairport-sync</legend>'
echo '          <form name="buttons" action="'$0'" method="get">'
echo '            <table class="bggrey percent100">'
#----------------------------------------------------------------------------------------

#----------------------------------Shairport-sync Indication-----------------------------
pcp_main_shairport_indication() {

	if [ $(pcp_shairport_status) -eq 0 ]; then
		pcp_green_tick "running"
	else
		pcp_red_cross "not running"
	fi

	pcp_incr_id
	pcp_toggle_row_shade
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="'$COLUMN1'">'
	echo '                <p class="'$CLASS'">'$INDICATOR'</p>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>Shairport-sync is '$STATUS'&nbsp;&nbsp;'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <ul>'
	echo '                    <li><span class="indicator_green">&#x2714;</span> = Shairport-sync running.</li>'
	echo '                    <li><span class="indicator_red">&#x2718;</span> = Shairport-sync not running.</li>'
	echo '                  </ul>'
	echo '                  <p><b>Note:</b></p>'
	echo '                  <ul>'
	echo '                    <li>Shairport-sync must be running for music to play from iDevices.</li>'
	echo '                  </ul>'
	echo '                </div>'
	echo '              </td>'
	echo '            </tr>'
}
pcp_main_shairport_indication
#----------------------------------------------------------------------------------------

if ! [ "$STATUS" = "running" ]; then
	#-----------------------------------Start button-------------------------------------
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COLUMN1'" colspan="2">'
	echo '                  <input type="submit"'
	echo '                         name="ACTION"'
	echo '                         value="Start"'
	echo '                         title="Start Shairport-sync"'
	echo '                  />'
	echo '                </td>'
	echo '              </tr>'
	#------------------------------------------------------------------------------------
else
	#--------------------------------Stop/Restart button---------------------------------
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td>'
	echo '                  <input type="submit"'
	echo '                         name="ACTION"'
	echo '                         value="Stop"'
	echo '                         title="Stop Shairport-sync"'
	echo '                  />'
	echo '                </td>'
	echo '                <td>'
	echo '                  <input type="submit"'
	echo '                         name="ACTION"'
	echo '                         value="Restart"'
	echo '                         title="Restart Shairport-sync"'
	echo '                  />'
	echo '                </td>'
	echo '              </tr>'
	#------------------------------------------------------------------------------------
fi
echo '            </table>'
echo '          </form>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------

if [ "$STATUS" = "running" ]; then
	#------------------------------------------------------------------------------------
	pcp_table_top "Shairport-sync is using these settings:"
	echo '                <p>'"$(ps -eo args | grep shairport-sync | grep -v grep)"'</p>'
	pcp_table_end
	#------------------------------------------------------------------------------------
fi

pcp_footer
pcp_copyright
pcp_remove_query_string

echo '</body>'
echo '</html>'
exit
