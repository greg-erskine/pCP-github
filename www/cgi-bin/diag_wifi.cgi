#!/bin/sh
# Wifi diagnostics script

# Version: 0.01 2015-08-20 GE
#	Original.

. pcp-rpi-functions
. pcp-functions
pcp_variables

# Local variables


pcp_html_head "Wifi Diagnostics" "GE"

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
echo '          <legend>Wifi</legend>'
echo '          <table class="bggrey percent100">'
#----------------------------------------------------------------------------------------
pcp_start_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td class="column150">'
echo '                <p>Wifi:</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>'$WIFI'</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p></p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p></p>'
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
echo '                <p>SSID:</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>'$SSID'</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p></p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p></p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p></p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p></p>'
echo '              </td>'
echo '            </tr>'
#----------------------------------------------------------------------------------------
pcp_toggle_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td class="column150">'
echo '                <p>Password:</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>'$PASSWORD'</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p></p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p></p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p></p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>'$(pcp_uptime_seconds)'</p>'
echo '              </td>'
echo '            </tr>'
----------------------------------------------------------------------------------------
if [ $(pcp_uptime_seconds) -lt 86400 ]; then
  IMAGE="green.png"
  STATUS="No reboot required."
else
  IMAGE="red.png"
  STATUS="Reboot recommended."
fi

pcp_toggle_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td class="column300">'
echo '                <p>Your piCorePlayer has not been reboot for:</p>'
echo '              </td>'
echo '              <td class="column300">'
echo '                <p>'$(pcp_uptime_days)'</p>'
echo '              </td>'
echo '              <td class="column300">'
echo '                <p><img src="../images/'$IMAGE'" alt="'$STATUS'">&nbsp;&nbsp;'$STATUS'</p>'
echo '              </td>'
echo '            </tr>'
#----------------------------------------------------------------------------------------
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
# Generate wifi report file in /tmp.
#-----------------------------------------------------------------------------------------
LOG="/tmp/pcp_diagwifi.log"

echo Report $0 generated on $(date) > $LOG
cat /etc/motd >> $LOG
echo >> $LOG

echo ========================================================================================= >> $LOG
echo "Wifi:        "$WIFI >> $LOG
echo "SSID:        "$SSID >> $LOG
echo "Password:    "$PASSWORD >> $LOG
echo "MAC address: "$(pcp_wlan0_mac_address) >> $LOG
echo "Uptime:      "$(pcp_uptime_days) >> $LOG
echo ========================================================================================= >> $LOG
echo >> $LOG

echo "dmesg" >> $LOG
echo ========================================================================================= >> $LOG
dmesg >> $LOG
echo >> $LOG

echo "lsmod" >> $LOG
echo ========================================================================================= >> $LOG
lsmod >> $LOG
echo >> $LOG

echo "lsusb" >> $LOG
echo ========================================================================================= >> $LOG
lsusb >> $LOG
echo >> $LOG

echo "iwconfig" >> $LOG
echo ========================================================================================= >> $LOG
iwconfig wlan0 >> $LOG
echo >> $LOG

echo "iwlist" >> $LOG
echo ========================================================================================= >> $LOG
iwlist wlan0 scan >> $LOG
echo >> $LOG
