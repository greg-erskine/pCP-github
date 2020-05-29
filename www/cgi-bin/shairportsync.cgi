#!/bin/sh

# Version: 7.0.0 2020-05-29

. pcp-functions
. pcp-soundcard-functions

pcp_html_head "Shairport-sync" "SBP"

SHAIRPORT_CONFIG="$PCPCFG"
SECTION_NAME=SHAIRPORTSYNC

pcp_navbar
pcp_httpd_query_string

#========================================================================================
# Initial setup routines.
# - Primary install will use default settings from DAC definitions.
#----------------------------------------------------------------------------------------
pcp_shairportsettings_to_config() {
	pcp_write_var_to_config SHAIRPORT_OUT "$SHAIRPORT_OUT"
	pcp_write_var_to_config SHAIRPORT_CONTROL "$SHAIRPORT_CONTROL"
	pcp_backup "text"
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
	pcp_debug_variables "html" SHAIRPORT_VERSION SHAIRPORT_OUT SHAIRPORT_CONTROL \
		OUTPUT SHAIRPORTSYNC_SHAIRPORT SHAIRPORT
}
pcp_debug_information

#========================================================================================
# Main
#----------------------------------------------------------------------------------------
case "$ACTION" in
	Start)
		pcp_shairport_start
	;;
	Stop)
		pcp_shairport_stop
		sleep 1
	;;
	Restart)
		pcp_shairport_stop
		sleep 1
		pcp_shairport_start
	;;
	Default)
		pcp_selected_soundcontrol
		pcp_message INFO "Writing to ${SHAIRPORT_CONFIG}..." "text"
		pcp_shairportsettings_to_config
	;;
	Save)
		pcp_message INFO "Writing to ${SHAIRPORT_CONFIG}..." "text"
		pcp_shairportsettings_to_config
	;;
	*)
		ACTION="Initial"
	;;
esac

. /$SHAIRPORT_CONFIG

COLUMN3_1="col-sm-3"
COLUMN3_2="col-sm-9"
#========================================================================================
pcp_border_begin
pcp_heading5 "Shairport-sync Settings"
echo '    <form name="settings" action="'$0'" method="get">'
#--------------------------------shairport-sync output name------------------------------
pcp_incr_id
echo '      <div class="row mx-1">'
echo '        <div class="'$COLUMN3_1'">'
echo '          <input class="form-control form-control-sm"'
echo '                 type="text"'
echo '                 name="SHAIRPORT_OUT"'
echo '                 value="'$SHAIRPORT_OUT'"'
echo '          >'
echo '        </div>'
echo '        <div class="'$COLUMN3_2'">'
echo '          <p>Set name of Shairport-sync output device&nbsp;&nbsp;'
pcp_helpbadge
echo '          </p>'
echo '          <div id="dt'$ID'" class="'$COLLAPSE'">'
echo '            <p>If not changed Shairport-sync output device will be the default DAC specific values.</p>'
echo '            <p>If equalizer is enabled use equal as output device name.</p>'
echo '            <p>Please experiment if default settings are wrong.</p>'
echo '          </div>'
echo '        </div>'
echo '      </div>'
#------------------------------shairport-sync control name-------------------------------
pcp_incr_id
echo '      <div class="row mx-1">'
echo '        <div class="'$COLUMN3_1'">'
echo '          <input class="form-control form-control-sm"'
echo '                 type="text"'
echo '                 name="SHAIRPORT_CONTROL"'
echo '                 value="'$SHAIRPORT_CONTROL'"'
echo '          >'
echo '        </div>'
echo '        <div class="'$COLUMN3_2'">'
echo '          <p>Set name of Output control used for Shairport-sync&nbsp;&nbsp;'
pcp_helpbadge
echo '          </p>'
echo '          <div id="dt'$ID'" class="'$COLLAPSE'">'
echo '            <p>Often the control name is Digital or PCM or left empty.</p>'
echo '            <p>If not changed Shairport-sync will use the default DAC specific values.</p>'
echo '            <p>If equalizer is enabled, the control name should be left empty.</p>'
echo '            <p>Please experiment if default settings are wrong.</p>'
echo '          </div>'
echo '        </div>'
echo '      </div>'
#----------------------------------------Default-----------------------------------------
pcp_incr_id
echo '      <div class="row mx-1">'
echo '        <div class="col-2">'
echo '          <input class="'$BUTTON'"'
echo '                 type="submit"'
echo '                 name="ACTION"'
echo '                 value="Default"'
echo '                 title="Default Settings"'
echo '          />'
echo '        </div>'
echo '        <div class="col-1"></div>'
echo '        <div class="col-9">'
echo '          <p>Load default Shairport-sync settings for your DAC&nbsp;&nbsp;'
pcp_helpbadge
echo '          </p>'
echo '          <div id="dt'$ID'" class="'$COLLAPSE'">'
echo '            <p>If needed change the settings and restart Shairport-sync to test the new settings.</p>'
echo '            <p>Remember to save your settings... and restart Shairport-sync</p>'
echo '          </div>'
echo '        </div>'
echo '      </div>'
#------------------------------------------Save------------------------------------------
pcp_incr_id
echo '      <div class="row mx-1 mb-2">'
echo '        <div class="col-2">'
echo '          <input class="'$BUTTON'"'
echo '                 type="submit"'
echo '                 name="ACTION"'
echo '                 value="Save"'
echo '                 title="Save Shairport-sync settings"'
echo '          >'
echo '        </div>'
echo '      </div>'
#----------------------------------------------------------------------------------------
echo '    </form>'
pcp_border_end
#----------------------------------------------------------------------------------------

#========================================================================================
pcp_border_begin
pcp_heading5 "Control of Shairport-sync"
echo '    <form name="buttons" action="'$0'" method="get">'
#----------------------------------Shairport-sync Indication-----------------------------
pcp_main_shairport_indication() {

	if [ $(pcp_shairport_status) -eq 0 ]; then
		pcp_green_tick "running"
	else
		pcp_red_cross "not running"
	fi

	pcp_incr_id
	echo '      <div class="row mx-1">'
	echo '        <div class="col-1 text-sm-right">'
	echo '          <p>'$INDICATOR'</p>'
	echo '        </div>'
	echo '        <div class="col-11">'
	echo '          <p>Shairport-sync is '$STATUS'&nbsp;&nbsp;'
	pcp_helpbadge
	echo '          </p>'
	echo '          <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '            <ul>'
	echo '              <li>'$(pcp_bi_check)' = Shairport-sync running.</li>'
	echo '              <li>'$(pcp_bi_x)' = Shairport-sync not running.</li>'
	echo '            </ul>'
	echo '            <p><b>Note:</b></p>'
	echo '            <ul>'
	echo '              <li>Shairport-sync must be running for music to play from iDevices.</li>'
	echo '            </ul>'
	echo '          </div>'
	echo '        </div>'
	echo '      </div>'
}
pcp_main_shairport_indication
#----------------------------------------------------------------------------------------

if ! [ "$STATUS" = "running" ]; then
	#-----------------------------------Start button-------------------------------------
	echo '              <div class="row mx-1 mb-2">'
	echo '                <div class="col-2">'
	echo '                  <input class="'$BUTTON'"'
	echo '                         type="submit"'
	echo '                         name="ACTION"'
	echo '                         value="Start"'
	echo '                         title="Start Shairport-sync"'
	echo '                  />'
	echo '                </div>'
	echo '              </div>'
	#------------------------------------------------------------------------------------
else
	#--------------------------------Stop/Restart button---------------------------------
	echo '              <div class="row mx-1 mb-2">'
	echo '                <div class="col-2">'
	echo '                  <input class="'$BUTTON'"'
	echo '                         type="submit"'
	echo '                         name="ACTION"'
	echo '                         value="Stop"'
	echo '                         title="Stop Shairport-sync"'
	echo '                  />'
	echo '                </div>'
	echo '                <div class="col-2">'
	echo '                  <input class="'$BUTTON'"'
	echo '                         type="submit"'
	echo '                         name="ACTION"'
	echo '                         value="Restart"'
	echo '                         title="Restart Shairport-sync"'
	echo '                  />'
	echo '                </div>'
	echo '              </div>'
	#------------------------------------------------------------------------------------
fi
echo '          </form>'
pcp_border_end
#----------------------------------------------------------------------------------------

if [ "$STATUS" = "running" ]; then
	#------------------------------------------------------------------------------------
	echo '                <p>'"$(ps -eo args | grep shairport-sync | grep -v grep)"'</p>'
	#------------------------------------------------------------------------------------
fi

pcp_html_end
exit
