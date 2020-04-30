#!/bin/sh
# Boot diagnostics script

# Version: 7.0.0 2020-04-30

. pcp-functions

# Local variables
LOG="${LOGDIR}/pcp_diag_boot_process.log"

pcp_html_head "Boot Diagnostics" "GE"

pcp_diagnostics
pcp_log_header $0

echo "This shows the boot process, starting with the initial init and going through to the the tc profile and ashrc files." >> $LOG
echo "" >> $LOG

ID=0
#=========================================================================================
# Generate links to boot files.
#-----------------------------------------------------------------------------------------
echo '              <div class="row">'
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
echo '                  <li><a href="#'$ID'">/usr/local/etc/init.d/pcp_startup.sh</a></li>'
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
echo '              </div>'

ID=0
#=========================================================================================
# Boot files in order of execution.
#-----------------------------------------------------------------------------------------

echo '      <div class="row">'
echo '          <h5>Boot files</h5>'

pcp_incr_id
echo '                <div id="'$ID'">'
                        pcp_textarea_inform "" "cat /init" 10 log
echo '                </div>'
pcp_incr_id
echo '                <div id="'$ID'">'
                        pcp_textarea_inform "" "ls -al /sbin/init" 2 log
echo '                </div>'
pcp_incr_id
echo '                <div id="'$ID'">'
                        pcp_textarea_inform "" "cat /etc/inittab" 10 log
echo '                </div>'
pcp_incr_id
echo '                <div id="'$ID'">'
                        pcp_textarea_inform "" "cat /etc/init.d/rcS" 80 log
echo '                </div>'
pcp_incr_id
echo '                <div id="'$ID'">'
                        pcp_textarea_inform "" "cat /etc/init.d/tc-config" 20 log
echo '                </div>'
pcp_incr_id
echo '                <div id="'$ID'">'
                        pcp_textarea_inform "" "cat /etc/init.d/dhcp.sh" 4 log
echo '                </div>'
pcp_incr_id
echo '                <div id="'$ID'">'
                        pcp_textarea_inform "" "cat /etc/init.d/settime.sh" 4 log
echo '                </div>'
pcp_incr_id
echo '                <div id="'$ID'">'
                        pcp_textarea_inform "" "cat /usr/bin/getTime.sh" 4 log
echo '                </div>'
pcp_incr_id
echo '                <div id="'$ID'">'
                        pcp_textarea_inform "" "cat /opt/bootsync.sh" 4 log
echo '                </div>'
pcp_incr_id
echo '                <div id="'$ID'">'
                        pcp_textarea_inform "" "cat /opt/bootlocal.sh" 4 log
echo '                </div>'
pcp_incr_id
echo '                <div id="'$ID'">'
if [ -f /home/tc/www/cgi-bin/pcp_startup.sh ]; then
                        pcp_textarea_inform "" "cat /home/tc/www/cgi-bin/pcp_startup.sh" 20 log
elif [ -f /usr/local/etc/init.d/pcp_startup ]; then
                        pcp_textarea_inform "" "cat /usr/local/etc/init.d/pcp_startup.sh" 20 log
echo '                </div>'
pcp_incr_id
echo '                <div id="'$ID'">'
                        pcp_textarea_inform "" "cat /home/tc/.profile" 20 log
echo '                </div>'
pcp_incr_id
echo '                <div id="'$ID'">'
                        pcp_textarea_inform "" "cat /home/tc/.ashrc" 20 log
echo '                </div>'

echo '      </div>'


#=========================================================================================
# Various files called during the boot process from the boot files.
#-----------------------------------------------------------------------------------------

echo '      <div class="row">'
echo '          <h5>Additional boot files</h5>'

echo '                <p>Additional files that are run during the boot process.</p>'
echo '                   Additional files that are run during the boot process.' >> $LOG
pcp_incr_id
echo '                <div id="'$ID'"></div>'
                        pcp_textarea_inform  "" "cat /etc/init.d/tc-functions" 20 log

pcp_incr_id
echo '                <div id="'$ID'"></div>'
                        pcp_textarea_inform  "" "cat /etc/init.d/busybox-aliases" 10 log

pcp_incr_id
echo '                <div id="'$ID'">'
                        pcp_textarea_inform "" "cat /proc/cmdline" 30 log
echo '                </div>'
pcp_incr_id
echo '                <div id="'$ID'">'
                        if [ -f "/opt/eth0.sh" ]; then
                            pcp_textarea_inform "" "cat /opt/eth0.sh" 5 log
                        else
                            pcp_textarea_inform "/opt/eth0.sh" "echo File does not exist." 2 log
                        fi
echo '                </div>'
pcp_incr_id
echo '                <div id="'$ID'">'
                        if [ -f "/opt/wlan0.sh" ]; then
                            pcp_textarea_inform "" "cat /opt/wlan0.sh" 4 log
                        else
                            pcp_textarea_inform "/opt/wlan0.sh" "echo File does not exist." 3 log
                        fi
echo '                </div>'
echo '         </div>'

pcp_footer
pcp_copyright
echo '         </div>'

echo '</body>'
echo '</html>'
