#!/bin/sh
# Raspberry Pi diagnostics script

# Version: 0.05 2015-07-04 GE
#	More updates.

# Version: 0.04 2015-04-28 GE
#	More minor updates.

# Version: 0.03 2015-03-07 GE
#	Added internet and sourceforge accessible.

# Version: 0.02 2015-02-06 GE
#	Reformatted.

# Version: 0.01 2014-10-22 GE
#	Original.

. pcp-rpi-functions
. pcp-functions
pcp_variables

# Local variables
START="====================> Start <===================="
END="=====================> End <====================="
LOG="/tmp/pcp_diagrpi.log"
(echo $0; date) > $LOG
cat /etc/motd >> $LOG

pcp_html_head "RasPi Diagnostics" "GE"

pcp_banner
pcp_diagnostics
pcp_running_script

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
#----------------------------------------------------------------------------------------
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
echo '                <p>'$(pcp_rpi_thermal_temp)'</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>Physical MAC:</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>'$(pcp_eth0_mac_address)'</p>'
echo '              </td>'
echo '            </tr>'
#----------------------------------------------------------------------------------------
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
echo '                <p>'$(pcp_eth0_ip)'</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>Wireless MAC:</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>'$(pcp_wlan0_mac_address)'</p>'
echo '              </td>'
echo '            </tr>'
#----------------------------------------------------------------------------------------
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
echo '                <p>'$(pcp_wlan0_ip)'</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>Configuration MAC:</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>'$(pcp_config_mac_address)'</p>'
echo '              </td>'
echo '            </tr>'
#----------------------------------------------------------------------------------------
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
echo '                <p>'$(pcp_lmsip)'</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>Controls MAC:</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>'$(pcp_controls_mac_address)'</p>'
echo '              </td>'
echo '            </tr>'
#----------------------------------------------------------------------------------------
pcp_toggle_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td class="column150">'
echo '                <p>Uptime:</p>'
echo '              </td>'
echo '              <td colspan="4">'
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
if [ $(pcp_squeezelite_status) = 0 ]; then
	IMAGE="green.png"
	STATUS="Running..."
else
	IMAGE="red.png"
	STATUS="Not running!!"
fi

echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Squeezelite</legend>'
echo '          <table class="bggrey percent100">'
pcp_start_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td class="column150">'
echo '                <p class="centre"><img src="../images/'$IMAGE'" alt="'$STATUS'"></p>'
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
echo '                <p>Compile version:</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>'$(pcp_which_squeezelite)'</p>'
echo '              </td>'
echo '            </tr>'
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
echo '              <td class="column150">'
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

                    if [ $(pcp_internet_accessible) = 0 ]; then
                      IMAGE="green.png"
                      STATUS="Internet found..."
                    else
                      IMAGE="red.png"
                      STATUS="Internet not found!!"
                    fi

echo '              <td class="column150">'
echo '                <p class="centre"><img src="../images/'$IMAGE'" alt="'$STATUS'"></p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>'$STATUS'</p>'
echo '              </td>'

                    if [ $(pcp_sourceforge_accessible) = 0 ]; then
                      IMAGE="green.png"
                      STATUS="Sourceforge accessible..."
                    else
                      IMAGE="red.png"
                      STATUS="Sourceforge not accessible!!"
                    fi

echo '              <td class="column150">'
echo '                <p class="centre"><img src="../images/'$IMAGE'" alt="'$STATUS'"></p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>'$STATUS'</p>'
echo '              </td>'

echo '              <td class="column150">'
echo '                <p></p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p></p>'
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

echo '</body>'
echo '</html>'

#=========================================================================================
# Add information to log file.
#-----------------------------------------------------------------------------------------
echo "[ INFO ] Rev: $(pcp_rpi_revision)" >> $LOG
echo "[ INFO ] Model: $(pcp_rpi_model)" >> $LOG
echo "[ INFO ] PCB rev: $(pcp_rpi_pcb_revision)" >> $LOG
echo "[ INFO ] memory: $(pcp_rpi_memory)" >> $LOG

[ $(pcp_rpi_is_model_A) = 0 ]     && echo "[ INFO ] model A: Yes" >> $LOG  || echo "[ INFO ] model A: No" >> $LOG
[ $(pcp_rpi_is_model_B) = 0 ]     && echo "[ INFO ] model B: Yes" >> $LOG  || echo "[ INFO ] model B: No" >> $LOG
[ $(pcp_rpi_is_model_Bplus) = 0 ] && echo "[ INFO ] model B+: Yes" >> $LOG || echo "[ INFO ] model B+: No" >> $LOG