#!/bin/sh

# Version: 4.0.0 2018-06-15

. pcp-functions
. pcp-soundcard-functions


SHAIRPORT_CONFIG="$PCPCFG"

unset BACKUP_REQUIRED REBOOT_REQUIRED 

pcp_html_head "Shairport-sync" "SBP"
SECTION_NAME=SHAIRPORTSYNC           #   <------- Specific for each plugin

pcp_banner
pcp_navigation
pcp_running_script
pcp_httpd_query_string
#pcp_soundcontrol

#FAIL_MSG="ok"

#========================================================================================================
# Initial setup routines. So primary install will use default settings from DAC definitions
#--------------------------------------------------------------------------------------------------------
pcp_shairportsettings_to_config(){
		pcp_write_var_to_config SHAIRPORT_OUT "$SHAIRPORT_OUT"
		pcp_write_var_to_config SHAIRPORT_CONTROL $SHAIRPORT_CONTROL
}

pcp_shairport_default(){
	if [ "$SHAIRPORT_OUT" = "Please change" ]; then
		pcp_selected_soundcontrol
		pcp_shairportsettings_to_config
		pcp_backup
	fi
}
pcp_shairport_default


#========================================================================================
# Do a backup if required
#----------------------------------------------------------------------------------------
pcp_backup_if_required() {
	if [ $BACKUP_REQUIRED ]; then
		echo '<table class="bggrey">'
		echo '  <tr>'
		echo '    <td>'
		echo '      <div class="row">'
		echo '        <fieldset>'
		echo '          <legend>Backup required</legend>'
		echo '          <table class="bggrey percent100">'
		pcp_start_row_shade
		echo '            <tr class="'$ROWSHADE'">'
		echo '              <td>'
		echo '                <textarea class="inform" style="height:40px">'
		                        pcp_backup_nohtml
		                        [ $? -eq 0 ] || FAIL_MSG="Backup failed."
		echo '                </textarea>'
		echo '              </td>'
		echo '            </tr>'
		echo '          </table>'
		echo '        </fieldset>'
		echo '      </div>'
		echo '    </td>'
		echo '  </tr>'
		echo '</table>'
	fi
}

#========================================================================================
# Generate status message and finish html page
#----------------------------------------------------------------------------------------
pcp_html_end() {
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Status</legend>'
	echo '          <table class="bggrey percent100">'
	pcp_start_row_shade
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td>'
#	echo '                <p>'$FAIL_MSG'</p>'
	echo ' 		<p><b>Shairport is using these settings:</b></p>'
	echo ' 		 '"$(ps -eo args | grep /usr/local/sbin/shairport-sync | grep -v grep)"' </p>'
	echo '              </td>'
	echo '            </tr>'
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'

	pcp_footer
	pcp_copyright
	pcp_remove_query_string

	echo '</body>'
	echo '</html>'
	[ "$REBOOT_REQUIRED" ] && pcp_reboot_required
	exit
}


#========================================================================================
# Main		<==== GE. This section is a little weird - Borrowed from LIRC page working good (SBP).
#----------------------------------------------------------------------------------------
case "$ACTION" in
	Start)
		ACTION=$ACTION
		pcp_shairport_start
	;;
	Stop)
		ACTION=$ACTION
		pcp_shairport_stop
	;;
	Restart)
		ACTION=$ACTION
		pcp_shairport_restart
	;;
	Default)
		ACTION=$ACTION
		pcp_selected_soundcontrol
		echo '[ INFO ] Write to $SHAIRPORT_CONFIG... '
		pcp_shairportsettings_to_config
		#pcp_save_to_config
		pcp_backup
	;;
	Save)
		ACTION=$ACTION
		echo '[ INFO ] Write to $SHAIRPORT_CONFIG... '
		pcp_shairportsettings_to_config
		#pcp_save_to_config
		pcp_backup
	;;
	Select)
		ACTION=$ACTION
		echo '[ INFO ] Write to $SHAIRPORT_CONFIG... '
		pcp_save_to_config
	;;
	*)
		ACTION="Initial"
	;;
esac



#========================================================================================
# Shairport Sync table
#----------------------------------------------------------------------------------------

# Function to check the SHAIRPORT radio button according to common_plugin.cfg file
	. /$SHAIRPORT_CONFIG
	case "$SHAIRPORT" in
		yes) SHAIRPORTyes="checked" ;;
		no) SHAIRPORTno="checked" ;;
	esac

pcp_enable_shairport(){
	#-------------------------------------------Start table--------------------------------
	#------------------------------------------Still not in use--------------------------
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Enable Shairport-sync at startup</legend>'
	echo '          <table class="bggrey percent100">'
	echo '            <form name="main" action="'$0'" method="get">'


	#-------------------------------------------Shairport--------------------------------
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>Shairport-sync</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="small1" type="radio" name="SHAIRPORT" value="yes" '$SHAIRPORTyes'>Yes&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
	echo '                  <input class="small1" type="radio" name="SHAIRPORT" value="no" '$SHAIRPORTno'>No'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Use Shairport-sync to stream from iDevices&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Automatically start Shairport when pCP starts to stream audio from your iDevice to pCP.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'

	#------------------------------------------Enable------------------------------------------
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center" colspan="3">'
	echo '                  <input type="submit"'
	echo '                         name="ACTION"'
	echo '                         value="Select"'
	echo '                         title="Enable Shairport_sync"'
	echo '                  />'
	echo '                </td>'
	echo '              </tr>'
	
	#----------------------------------------------------------------------------------------

	echo '            </table>'
	echo '          </fieldset>'
	echo '        </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
}
#pcp_enable_shairport


	#========================================================================================
	# Shairport-sync Settings table
	#----------------------------------------------------------------------------------------
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Shairport-sync Settings</legend>'
	echo '          <table class="bggrey percent100">'
	echo '            <form name="settings" action="'$0'" method="get">'
	#----------------------------------------------------------------------------------------


	#------------------------------------------shairport-sync output name-----------------------------------
	# shairport-sync output name
	#-----------------------------------------------------------------------------------------
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column210 center">'
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
	echo '                    <p>If not changed Shairport output device will be the default DAC specific values.</p>'
	echo '                    <p>If equalizer is enabled use equal as output device name.</p>'
	echo '                    <p>Please experiment if default settings are wrong.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	#----------------------------------------------------------------------------------------

	
	#------------------------------------------shairport-sync control name---------------------------------
	# Name of shairport-sync control device name 
	#----------------------------------------------------------------------------------------
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column210 center">'
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
	echo '                    <p>If not changed Shairport sync will use the default DAC specific values.</p>'
	echo '                    <p>If equalizer is enabled the control name should be left empty.</p>'
	echo '                    <p>Please experiment if default settings are wrong.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	#----------------------------------------------------------------------------------------
	

	#------------------------------------------Save------------------------------------------
	
		pcp_incr_id
		pcp_toggle_row_shade
		echo '              <tr class="'$ROWSHADE'">'
		echo '                <td class="column150 center" colspan="3">'
		echo '                  <input type="submit"'
		echo '                         name="ACTION"'
		echo '                         value="Default"'
		echo '                         title="Default Settings"'
		echo '                  />'
		echo '                <td>'
		echo '                  <p>Load default Shairport-sync settings for your DAC&nbsp;&nbsp;'
		echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
		echo '                  </p>'
		echo '                  <div id="'$ID'" class="less">'
		echo '                    <p>If needed change the settings and restart Shairport-sync to test the new settings.</p>'
		echo '                    <p>Remember to save your settings.... And restart Shairport-sync</p>'
		echo '                  </div>'
		echo '                </td>'
		echo '              </tr>'
		pcp_incr_id
		pcp_toggle_row_shade
		echo '              <tr class="'$ROWSHADE'">'
		echo '                <td class="column150 center" colspan="3">'
		echo '                  <input type="submit"'
		echo '                         name="ACTION"'
		echo '                         value="Save"'
		echo '                         title="Save Shairport settings"'
		echo '                  />'
		echo '                </td>'
		echo '              </tr>'



	#----------------------------------------------------------------------------------------
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
#----------------------------------------------------------------------------------------


#========================================================================================
	# Shairport-sync Start,stop/restart table
	#----------------------------------------------------------------------------------------
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Control of Shairport-sync</legend>'
	echo '          <table class="bggrey percent100">'
	echo '            <form name="settings" action="'$0'" method="get">'
	#----------------------------------------------------------------------------------------


#------------------------------------Shairport Indication--------------------------------
pcp_main_shairport_indication() {

	if [ $(pcp_shairport_status) -eq 0 ]; then
		pcp_green_tick "running"
	else
		pcp_red_cross "not running"
	fi


	pcp_incr_id
	pcp_toggle_row_shade
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150 center">'
	echo '                <p class="'$CLASS'">'$INDICATOR'</p>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>Shairport is '$STATUS'&nbsp;&nbsp;'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <ul>'
	echo '                    <li><span class="indicator_green">&#x2714;</span> = Shairport running.</li>'
	echo '                    <li><span class="indicator_red">&#x2718;</span> = Shairport not running.</li>'
	echo '                  </ul>'
	echo '                  <p><b>Note:</b></p>'
	echo '                  <ul>'
	echo '                    <li>Shairport must be running for music to play from iDevices.</li>'
	echo '                  </ul>'
	echo '                </div>'
	echo '              </td>'
	echo '            </tr>'
}

pcp_main_shairport_indication && pcp_main_padding
#----------------------------------------------------------------------------------------



	#------------------------------------------Buttons------------------------------------------

		pcp_incr_id
		pcp_toggle_row_shade
		echo '              <tr class="'$ROWSHADE'">'
		echo '                <td class="column150 center" colspan="3">'
		echo '                  <input type="submit"'
		echo '                         name="ACTION"'
		echo '                         value="Start"'
		echo '                         title="Start Shairport-sync"'
		echo '                  />'
		echo '                </td>'
		echo '              </tr>'

		pcp_incr_id
		pcp_toggle_row_shade
		echo '              <tr class="'$ROWSHADE'">'
		echo '                <td class="column150 center" colspan="3">'
		echo '                  <input type="submit"'
		echo '                         name="ACTION"'
		echo '                         value="Stop"'
		echo '                         title="Stop Shairport-sync"'
		echo '                  />'
		echo '              </tr>'

		pcp_incr_id
		pcp_toggle_row_shade
		echo '              <tr class="'$ROWSHADE'">'
		echo '                <td class="column150 center" colspan="3">'
		echo '                  <input type="submit"'
		echo '                         name="ACTION"'
		echo '                         value="Restart"'
		echo '                         title="Restart Shairport-sync"'
		echo '                  />'
		echo '              </tr>'


	#----------------------------------------------------------------------------------------
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
#----------------------------------------------------------------------------------------


if [ $DEBUG -eq 1 ]; then
	pcp_table_top "Debug"
	echo '<!-- Start of debug info -->'
	echo '<p class="debug">[ DEBUG ] $SHAIRPORT_OUT: '$SHAIRPORT_OUT'<br />'
	echo '                 [ DEBUG ] $SH_OUTPUT: '$SH_OUTPUT'<br />'
	echo '                 [ DEBUG ] $OUTPUT: '$OUTPUT'<br />'
	echo '                 [ DEBUG ] $SHAIRPORT_CONTROL: '$SHAIRPORT_CONTROL'<br />'
	echo '                 [ DEBUG ] $SH_CONTROL: '$SH_CONTROL'<br />'
	echo '                 [ DEBUG ] $SSET: '$SSET'<br />'
	echo '                 [ DEBUG ] $SHAIRPORTSYNC_SHAIRPORT: '$SHAIRPORTSYNC_SHAIRPORT'<br />'
	echo '                 [ DEBUG ] $SHAIRPORT: '$SHAIRPORT'<br />'
	echo '                 [ DEBUG ] $SHAIRPORTyes: '$SHAIRPORTyes'<br />'
	echo '                 [ DEBUG ] $SHAIRPORTno: '$SHAIRPORTno'</p>'
	pcp_table_end
fi

pcp_backup_if_required
pcp_html_end
