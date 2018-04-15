#!/bin/sh
# Raspberry Pi diagnostics script

# Version: 4.0.0 2018-04-15
#	Fixed log file name. GE.
#  Changed repo to new server. PH.

# Version: 3.20 2017-03-08
#	Fixed pcp-xxx-functions issues. GE.

# Version: 3.10 2017-01-06
#	Changed to using pcp_log_header. GE.
#	Changed to using pcp_green_tick, pcp_red_cross. GE.
#	Changes for Squeezelite extension. PH.
#	removed squeezelite size. GE.

# Version: 0.01 2014-10-22
#	Original. GE.

. pcp-functions
. pcp-rpi-functions
. pcp-pastebin-functions

pcp_html_head "Raspberry Pi Diagnostics" "GE"

pcp_banner
pcp_diagnostics
pcp_running_script

LOG="${LOGDIR}/pcp_diag_rpi.log"

#=========================================================================================
# Add information to log file.
#-----------------------------------------------------------------------------------------
pcp_add_to_log() {
	START="====================> Start <===================="
	END="=====================> End <====================="

	pcp_log_header $0

	echo "Raspberry Pi" >> $LOG
	echo  ============ >> $LOG
	echo  >> $LOG
	echo "Model: $(pcp_rpi_model)" >> $LOG
	echo "Revision: $(pcp_rpi_revision)" >> $LOG
	echo "PCB Revision: $(pcp_rpi_pcb_revision)" >> $LOG
	echo "Memory: $(pcp_rpi_memory)" >> $LOG
	echo "Shortname: $(pcp_rpi_shortname)" >> $LOG
	echo "CPU Temperature: $(pcp_rpi_thermal_temp degrees)" >> $LOG
	echo "eth0 IP: $(pcp_diag_rpi_eth0_ip)" >> $LOG
	echo "wlan0 IP: $(pcp_diag_rpi_wlan0_ip)" >> $LOG
	echo "LMS IP: $(pcp_diag_rpi_lmsip)" >> $LOG
	echo "Uptime: $(pcp_uptime_days)" >> $LOG
	echo "Physical MAC: $(pcp_diag_rpi_eth0_mac_address)" >> $LOG
	echo "Wireless MAC: $(pcp_diag_rpi_wlan0_mac_address)" >> $LOG
	echo "Configuration MAC: $(pcp_diag_rpi_config_mac_address)" >> $LOG
	echo "Controls MAC: $(pcp_controls_mac_address)" >> $LOG
	echo  >> $LOG

	echo "Squeezelite" >> $LOG
	echo  =========== >> $LOG
	echo  >> $LOG
	echo "Version: $(pcp_squeezelite_version)" >> $LOG
	echo "Build options: $BUILD" >> $LOG
	if [ $(pcp_squeezelite_status) -eq 0 ]; then
		echo "Squeezelite running." >> $LOG
	else
		echo  "Squeezelite not running." >> $LOG
	fi
	echo  >> $LOG

	echo "piCorePlayer" >> $LOG
	echo  ============ >> $LOG
	echo  >> $LOG
	echo "Version: $(pcp_picoreplayer_version)" >> $LOG
	echo "pCP name: $NAME" >> $LOG
	echo "Hostname: $HOST" >> $LOG
	echo  >> $LOG

	echo "piCore" >> $LOG
	echo  ====== >> $LOG
	echo  >> $LOG
	echo "Version: $(pcp_picore_version)" >> $LOG
	echo "Linux release: $(pcp_linux_release)" >> $LOG
	if [ $(pcp_internet_accessible) -eq 0 ]; then
		echo "Internet found." >> $LOG
	else
		echo "Internet not found." >> $LOG
	fi
	if [ $(pcp_pcp_repo_accessible) -eq 0 ]; then
		echo "pCP repo accessible." >> $LOG
	else
		echo "pCP repo not accessible." >> $LOG
	fi
}

# Maybe able to simplify the following routines?
pcp_diag_rpi_eth0_mac_address() {
	RESULT=$(pcp_eth0_mac_address)
	[ x"" = x"$RESULT" ] && echo "None" || echo $RESULT
}

pcp_diag_rpi_wlan0_mac_address() {
	RESULT=$(pcp_wlan0_mac_address)
	[ x"" = x"$RESULT" ] && echo "None" || echo $RESULT
}

pcp_diag_rpi_config_mac_address() {
	RESULT=$(pcp_config_mac_address)
	[ x"" = x"$RESULT" ] && echo "Not set" || echo $RESULT
}

pcp_diag_rpi_eth0_ip() {
	RESULT=$(pcp_eth0_ip)
	[ x"" = x"$RESULT" ] && echo "None" || echo $RESULT
}

pcp_diag_rpi_wlan0_ip() {
	RESULT=$(pcp_wlan0_ip)
	[ x"" = x"$RESULT" ] && echo "None" || echo $RESULT
}

pcp_diag_rpi_lmsip() {
	RESULT=$(pcp_lmsip)
	[ x"" = x"$RESULT" ] && echo "None" || echo $RESULT
}

#========================================================================================
# Raspberry Pi
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Raspberry Pi</legend>'
echo '          <table class="bggrey percent100">'
#-------------------------------------Row 1----------------------------------------------
pcp_start_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td class="column150">'
echo '                <p>Model:</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>'$(pcp_rpi_model)'</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>CPU Temperature:</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>'$(pcp_rpi_thermal_temp degrees)'</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>Physical MAC:</p>'
echo '              </td>'
echo '              <td>'
echo '                <p>'$(pcp_diag_rpi_eth0_mac_address)'</p>'
echo '              </td>'
echo '            </tr>'
#-------------------------------------Row 2----------------------------------------------
pcp_toggle_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td class="column150">'
echo '                <p>Revison:</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>'$(pcp_rpi_revision)'</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>eth0 IP:</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>'$(pcp_diag_rpi_eth0_ip)'</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>Wireless MAC:</p>'
echo '              </td>'
echo '              <td>'
echo '                <p>'$(pcp_diag_rpi_wlan0_mac_address)'</p>'
echo '              </td>'
echo '            </tr>'
#-------------------------------------Row 3----------------------------------------------
pcp_toggle_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td class="column150">'
echo '                <p>PCB Revison:</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>'$(pcp_rpi_pcb_revision)'</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>wlan0 IP:</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>'$(pcp_diag_rpi_wlan0_ip)'</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>Configuration MAC:</p>'
echo '              </td>'
echo '              <td>'
echo '                <p>'$(pcp_diag_rpi_config_mac_address)'</p>'
echo '              </td>'
echo '            </tr>'
#-------------------------------------Row 4----------------------------------------------
pcp_toggle_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td class="column150">'
echo '                <p>Memory:</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>'$(pcp_rpi_memory)'</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>LMS IP:</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>'$(pcp_diag_rpi_lmsip)'</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>Controls MAC:</p>'
echo '              </td>'
echo '              <td>'
echo '                <p>'$(pcp_controls_mac_address)'</p>'
echo '              </td>'
echo '            </tr>'
#-------------------------------------Row 5----------------------------------------------
pcp_toggle_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td class="column150">'
echo '                <p>Shortname:</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>'$(pcp_rpi_shortname)'</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>Uptime:</p>'
echo '              </td>'
echo '              <td colspan="3">'
echo '                <p>'$(pcp_uptime_days)'</p>'
echo '              </td>'
echo '            </tr>'
#----------------------------------------------------------------------------------------
echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'

#========================================================================================
# Squeezelite
#----------------------------------------------------------------------------------------
BUILD=$(sudo ${SQLT_BIN} -? | grep "Build options" | awk -F": " '{print $2}')

if [ $(pcp_squeezelite_status) -eq 0 ]; then
	pcp_green_tick "Running."
else
	pcp_red_cross "Not running."
fi

echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Squeezelite</legend>'
echo '          <table class="bggrey percent100">'
#-------------------------------------Row 1----------------------------------------------
pcp_start_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td class="column150 center">'
echo '                <p class="'$CLASS'">'$INDICATOR'</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>'$STATUS'</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>Version:</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>'$(pcp_squeezelite_version)'</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p></p>'
echo '              </td>'
echo '              <td>'
echo '                <p></p>'
echo '              </td>'
echo '            </tr>'
#-------------------------------------Row 2----------------------------------------------
pcp_toggle_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td class="column150 center">'
echo '                <p>Build options:</p>'
echo '              </td>'
echo '              <td colspan="5">'
echo '                <p>'$BUILD'</p>'
echo '              </td>'
echo '            </tr>'
#----------------------------------------------------------------------------------------
echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'

#========================================================================================
# piCorePlayer
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>piCorePlayer</legend>'
echo '          <table class="bggrey percent100">'
pcp_start_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td class="column150">'
echo '                <p>Version:</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>'$(pcp_picoreplayer_version)'</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>pCP name:</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>'$NAME'</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>Hostname:</p>'
echo '              </td>'
echo '              <td>'
echo '                <p>'$HOST'</p>'
echo '              </td>'
echo '            </tr>'
echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'

#========================================================================================
# piCore
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>piCore</legend>'
echo '          <table class="bggrey percent100">'
pcp_start_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td class="column150">'
echo '                <p>Version:</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>'$(pcp_picore_version)'</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>Linux release:</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>'$(pcp_linux_release)'</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p></p>'
echo '              </td>'
echo '              <td>'
echo '                <p></p>'
echo '              </td>'
echo '            </tr>'
echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'

#========================================================================================
# internet
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Internet</legend>'
echo '          <table class="bggrey percent100">'
pcp_start_row_shade
echo '            <tr class="'$ROWSHADE'">'

                    if [ $(pcp_internet_accessible) -eq 0 ]; then
                        pcp_green_tick "Internet found."
                    else
                        pcp_red_cross "Internet not found."
                    fi

echo '              <td class="column150 center">'
echo '                <p class="'$CLASS'">'$INDICATOR'</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>'$STATUS'</p>'
echo '              </td>'

                    if [ $(pcp_pcp_repo_accessible) -eq 0 ]; then
                        pcp_green_tick "pCP repo accessible."
                    else
                        pcp_red_cross "pCP repo not accessible."
                    fi

echo '              <td class="column150 center">'
echo '                <p class="'$CLASS'">'$INDICATOR'</p>'
echo '              </td>'
echo '              <td>'
echo '                <p>'$STATUS'</p>'
echo '              </td>'

echo '            </tr>'
echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'

[ $MODE -ge $MODE_DEVELOPER ] && pcp_pastebin_button "Raspberry-Pi"

pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'

pcp_add_to_log
