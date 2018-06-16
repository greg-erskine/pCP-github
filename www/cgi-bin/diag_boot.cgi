#!/bin/sh
# Boot diagnostics script

# Version: 4.0.0 2018-05-16

. pcp-functions

# Local variables
LOG="${LOGDIR}/pcp_diag_boot.log"

pcp_html_head "Boot Diagnostics" "GE"

pcp_banner
pcp_diagnostics
pcp_running_script
pcp_log_header $0

echo "This shows the boot process, starting with the initial init and going through to the the tc profile and ashrc files." >> $LOG
echo "" >> $LOG

#=========================================================================================
# Generate links to boot files.
#-----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Index</legend>'
echo '          <table class="bggrey percent100">'
pcp_start_row_shade
pcp_toggle_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td>'
echo '                <p>This shows the boot process, starting with the initial init and going through to the the '
echo '                   tc profile and ashrc files. A log file <b>pcp_diag_boot.log</b> is also created.</p>'
echo '                <ol>'
echo '                  <li><a href="#01">/init</a></li>'
echo '                  <li><a href="#02">/sbin/init</a></li>'
echo '                  <li><a href="#03">/etc/init.d/rcS</a></li>'
echo '                  <li><a href="#04">/etc/init.d/tc-config</a></li>'
echo '                  <li><a href="#05">/etc/init.d/dhcp.sh</a></li>'
echo '                  <li><a href="#06">/etc/init.d/settime.sh</a></li>'
echo '                  <li><a href="#07">/usr/bin/getTime.sh</a></li>'
echo '                  <li><a href="#08">/opt/bootsync.sh</a></li>'
echo '                  <li><a href="#09">/opt/bootlocal.sh</a></li>'
echo '                  <li><a href="#10">/home/tc/www/cgi-bin/pcp_startup.sh</a></li>'
echo '                  <li><a href="#11">/home/tc/.profile</a></li>'
echo '                  <li><a href="#12">/home/tc/.ashrc</a></li>'
echo '                  <li><a href="#13">/etc/init.d/tc-functions</a></li>'
echo '                  <li><a href="#14">/proc/cmdline</a></li>'
echo '                  <li><a href="#15">/opt/eth0.sh</a></li>'
echo '                  <li><a href="#16">/opt/wlan0.sh</a></li>'
echo '                </ol>'
echo '              </td>'
echo '            </tr>'
echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'

#=========================================================================================
# Boot files in order of execution.
#-----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Boot files</legend>'
echo '          <table class="bggrey percent100">'
pcp_start_row_shade
pcp_toggle_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td>'
echo '                <div id="01">'
                        pcp_textarea_inform "" "cat /init" 300 log
echo '                </div>'
echo '                <div id="02">'
                        pcp_textarea_inform "" "ls -al /sbin/init" 60 log
echo '                </div>'
echo '                <div id="03">'
                        pcp_textarea_inform "" "cat /etc/init.d/rcS" 240 log
echo '                </div>'
echo '                <div id="04">'
                        pcp_textarea_inform "" "cat /etc/init.d/tc-config" 600 log
echo '                </div>'
echo '                <div id="05">'
                        pcp_textarea_inform "" "cat /etc/init.d/dhcp.sh" 120 log
echo '                </div>'
echo '                <div id="06">'
                        pcp_textarea_inform "" "cat /etc/init.d/settime.sh" 120 log
echo '                </div>'
echo '                <div id="07">'
                        pcp_textarea_inform "" "cat /usr/bin/getTime.sh" 120 log
echo '                </div>'
echo '                <div id="08">'
                        pcp_textarea_inform "" "cat /opt/bootsync.sh" 120 log
echo '                </div>'
echo '                <div id="09">'
                        pcp_textarea_inform "" "cat /opt/bootlocal.sh" 110 log
echo '                </div>'
echo '                <div id="10">'
                        pcp_textarea_inform "" "cat /home/tc/www/cgi-bin/pcp_startup.sh" 600 log
echo '                </div>'
echo '                <div id="11">'
                        pcp_textarea_inform "" "cat /home/tc/.profile" 530 log
echo '                </div>'
echo '                <div id="12">'
                        pcp_textarea_inform "" "cat /home/tc/.ashrc" 410 log
echo '                </div>'
echo '              </td>'
echo '            </tr>'
echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'

#=========================================================================================
# Various files called during the boot process from the boot files.
#-----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Additional boot files</legend>'
echo '          <table class="bggrey percent100">'
pcp_start_row_shade
pcp_toggle_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td>'
echo '                <p>Additional files that are run during the boot process.</p>'
echo '                   Additional files that are run during the boot process.' >> $LOG
echo '                <div id="13">'
                        pcp_textarea_inform  "" "cat /etc/init.d/tc-functions" 600 log
echo '                </div>'
echo '                <div id="14">'
                        pcp_textarea_inform "" "cat /proc/cmdline" 100 log
echo '                </div>'
echo '                <div id="15">'
                        if [ -f "/opt/eth0.sh" ]; then
                            pcp_textarea_inform "" "cat /opt/eth0.sh" 150 log
                        else
                            pcp_textarea_inform "/opt/eth0.sh" "echo File does not exist." 30 log
                        fi
echo '                </div>'
echo '                <div id="16">'
                        if [ -f "/opt/wlan0.sh" ]; then
                            pcp_textarea_inform "" "cat /opt/wlan0.sh" 150 log
                        else
                            pcp_textarea_inform "/opt/wlan0.sh" "echo File does not exist." 30 log
                        fi
echo '                </div>'
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
