#!/bin/sh
# Boot diagnostics script

# Version: 4.2.0 2019-01-14

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

ID=0
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
pcp_incr_id
echo '                  <li><a href="#'$ID'">/init</a></li>'
pcp_incr_id
echo '                  <li><a href="#'$ID'">/sbin/init</a></li>'
pcp_incr_id
echo '                  <li><a href="#'$ID'">/etc/inittab</a></li>'
pcp_incr_id
echo '                  <li><a href="#'$ID'">/etc/init.d/rcS</a></li>'
pcp_incr_id
echo '                  <li><a href="#'$ID'">/etc/init.d/tc-config</a></li>'
pcp_incr_id
echo '                  <li><a href="#'$ID'">/etc/init.d/dhcp.sh</a></li>'
pcp_incr_id
echo '                  <li><a href="#'$ID'">/etc/init.d/settime.sh</a></li>'
pcp_incr_id
echo '                  <li><a href="#'$ID'">/usr/bin/getTime.sh</a></li>'
pcp_incr_id
echo '                  <li><a href="#'$ID'">/opt/bootsync.sh</a></li>'
pcp_incr_id
echo '                  <li><a href="#'$ID'">/opt/bootlocal.sh</a></li>'
pcp_incr_id
echo '                  <li><a href="#'$ID'">/home/tc/www/cgi-bin/pcp_startup.sh</a></li>'
pcp_incr_id
echo '                  <li><a href="#'$ID'">/home/tc/.profile</a></li>'
pcp_incr_id
echo '                  <li><a href="#'$ID'">/home/tc/.ashrc</a></li>'
echo '                </ol>'
pcp_incr_id
echo '                <ol start="'$ID'">' 
echo '                  <li><a href="#'$ID'">/etc/init.d/tc-functions</a></li>'
pcp_incr_id
echo '                  <li><a href="#'$ID'">/etc/init.d/busybox-aliases</a></li>'
pcp_incr_id
echo '                  <li><a href="#'$ID'">/proc/cmdline</a></li>'
pcp_incr_id
echo '                  <li><a href="#'$ID'">/opt/eth0.sh</a></li>'
pcp_incr_id
echo '                  <li><a href="#'$ID'">/opt/wlan0.sh</a></li>'
echo '                </ol>'
echo '              </td>'
echo '            </tr>'
echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'

ID=0
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
pcp_incr_id
echo '                <div id="'$ID'">'
                        pcp_textarea_inform "" "cat /init" 300 log
echo '                </div>'
pcp_incr_id
echo '                <div id="'$ID'">'
                        pcp_textarea_inform "" "ls -al /sbin/init" 60 log
echo '                </div>'
pcp_incr_id
echo '                <div id="'$ID'">'
                        pcp_textarea_inform "" "cat /etc/inittab" 260 log
echo '                </div>'
pcp_incr_id
echo '                <div id="'$ID'">'
                        pcp_textarea_inform "" "cat /etc/init.d/rcS" 240 log
echo '                </div>'
pcp_incr_id
echo '                <div id="'$ID'">'
                        pcp_textarea_inform "" "cat /etc/init.d/tc-config" 600 log
echo '                </div>'
pcp_incr_id
echo '                <div id="'$ID'">'
                        pcp_textarea_inform "" "cat /etc/init.d/dhcp.sh" 120 log
echo '                </div>'
pcp_incr_id
echo '                <div id="'$ID'">'
                        pcp_textarea_inform "" "cat /etc/init.d/settime.sh" 120 log
echo '                </div>'
pcp_incr_id
echo '                <div id="'$ID'">'
                        pcp_textarea_inform "" "cat /usr/bin/getTime.sh" 120 log
echo '                </div>'
pcp_incr_id
echo '                <div id="'$ID'">'
                        pcp_textarea_inform "" "cat /opt/bootsync.sh" 120 log
echo '                </div>'
pcp_incr_id
echo '                <div id="'$ID'">'
                        pcp_textarea_inform "" "cat /opt/bootlocal.sh" 110 log
echo '                </div>'
pcp_incr_id
echo '                <div id="'$ID'">'
                        pcp_textarea_inform "" "cat /home/tc/www/cgi-bin/pcp_startup.sh" 600 log
echo '                </div>'
pcp_incr_id
echo '                <div id="'$ID'">'
                        pcp_textarea_inform "" "cat /home/tc/.profile" 530 log
echo '                </div>'
pcp_incr_id
echo '                <div id="'$ID'">'
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
pcp_incr_id
echo '                <div id="'$ID'">'
                        pcp_textarea_inform  "" "cat /etc/init.d/tc-functions" 600 log
echo '                </div>'
pcp_incr_id
echo '                <div id="'$ID'">'
                        pcp_textarea_inform  "" "cat /etc/init.d/busybox-aliases" 300 log
echo '                </div>'
pcp_incr_id
echo '                <div id="'$ID'">'
                        pcp_textarea_inform "" "cat /proc/cmdline" 100 log
echo '                </div>'
pcp_incr_id
echo '                <div id="'$ID'">'
                        if [ -f "/opt/eth0.sh" ]; then
                            pcp_textarea_inform "" "cat /opt/eth0.sh" 150 log
                        else
                            pcp_textarea_inform "/opt/eth0.sh" "echo File does not exist." 30 log
                        fi
echo '                </div>'
pcp_incr_id
echo '                <div id="'$ID'">'
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
