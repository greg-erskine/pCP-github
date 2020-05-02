#!/bin/sh
# Boot diagnostics script

# Version: 7.0.0 2020-05-02

. pcp-functions

# Local variables
LOG="${LOGDIR}/pcp_diag_boot_process.log"

pcp_html_head "Boot Diagnostics" "GE"

pcp_diagnostics
pcp_log_header $0

echo "This shows the boot process, starting with the initial init and going through to the the tc profile and ashrc files." >> $LOG
echo "" >> $LOG

#=========================================================================================
# Generate links to boot files.
#-----------------------------------------------------------------------------------------
ID=0

echo '  <div class="row">'
echo '    This shows the boot process, starting with the initial init and going through to the the '
echo '    tc profile and ashrc files. A log file <b>pcp_diag_boot.log</b> is also created.'
echo '    <ol>'

pcp_incr_id; echo '      <li><a href="#ta'$ID'">/init</a></li>'
pcp_incr_id; echo '      <li><a href="#ta'$ID'">/sbin/init</a></li>'
pcp_incr_id; echo '      <li><a href="#ta'$ID'">/etc/inittab</a></li>'
pcp_incr_id; echo '      <li><a href="#ta'$ID'">/etc/init.d/rcS</a></li>'
pcp_incr_id; echo '      <li><a href="#ta'$ID'">/etc/init.d/tc-config</a></li>'
pcp_incr_id; echo '      <li><a href="#ta'$ID'">/etc/init.d/dhcp.sh</a></li>'
pcp_incr_id; echo '      <li><a href="#ta'$ID'">/etc/init.d/settime.sh</a></li>'
pcp_incr_id; echo '      <li><a href="#ta'$ID'">/usr/bin/getTime.sh</a></li>'
pcp_incr_id; echo '      <li><a href="#ta'$ID'">/opt/bootsync.sh</a></li>'
pcp_incr_id; echo '      <li><a href="#ta'$ID'">/opt/bootlocal.sh</a></li>'
pcp_incr_id; echo '      <li><a href="#ta'$ID'">/usr/local/etc/init.d/pcp_startup.sh</a></li>'
pcp_incr_id; echo '      <li><a href="#ta'$ID'">/home/tc/.profile</a></li>'
pcp_incr_id; echo '      <li><a href="#ta'$ID'">/home/tc/.ashrc</a></li>'
             echo '    </ol>'
pcp_incr_id; echo '    <ol start="'$ID'">' 
             echo '      <li><a href="#ta'$ID'">/etc/init.d/tc-functions</a></li>'
pcp_incr_id; echo '      <li><a href="#ta'$ID'">/etc/init.d/busybox-aliases</a></li>'
pcp_incr_id; echo '      <li><a href="#ta'$ID'">/proc/cmdline</a></li>'
pcp_incr_id; echo '      <li><a href="#ta'$ID'">/opt/eth0.sh</a></li>'
pcp_incr_id; echo '      <li><a href="#ta'$ID'">/opt/wlan0.sh</a></li>'
             echo '    </ol>'
             echo '  </div>'

#=========================================================================================
# Boot files in order of execution.
#-----------------------------------------------------------------------------------------
ID=0
#echo '  <div class="row">'
echo '    <h5>Boot files</h5>'

pcp_incr_id; pcp_textarea "" "cat /init" 10 log
pcp_incr_id; pcp_textarea "" "ls -al /sbin/init" 2 log
pcp_incr_id; pcp_textarea "" "cat /etc/inittab" 10 log
pcp_incr_id; pcp_textarea "" "cat /etc/init.d/rcS" 80 log
pcp_incr_id; pcp_textarea "" "cat /etc/init.d/tc-config" 20 log
pcp_incr_id; pcp_textarea "" "cat /etc/init.d/dhcp.sh" 4 log
pcp_incr_id; pcp_textarea "" "cat /etc/init.d/settime.sh" 4 log
pcp_incr_id; pcp_textarea "" "cat /usr/bin/getTime.sh" 4 log
pcp_incr_id; pcp_textarea "" "cat /opt/bootsync.sh" 4 log
pcp_incr_id; pcp_textarea "" "cat /opt/bootlocal.sh" 4 log

pcp_incr_id
if [ -f /home/tc/www/cgi-bin/pcp_startup.sh ]; then
  pcp_textarea "" "cat /home/tc/www/cgi-bin/pcp_startup.sh" 20 log
elif [ -f /usr/local/etc/init.d/pcp_startup ]; then
  pcp_textarea "" "cat /usr/local/etc/init.d/pcp_startup.sh" 20 log
fi

pcp_incr_id; pcp_textarea "" "cat /home/tc/.profile" 20 log
pcp_incr_id; pcp_textarea "" "cat /home/tc/.ashrc" 20 log

#=========================================================================================
# Various files called during the boot process from the boot files.
#-----------------------------------------------------------------------------------------
echo '    <h5>Additional boot files</h5>'

echo '    <p>Additional files that are run during the boot process.</p>'
echo '    additional files that are run during the boot process.' >> $LOG

pcp_incr_id; pcp_textarea "" "cat /etc/init.d/tc-functions" 20 log
pcp_incr_id; pcp_textarea "" "cat /etc/init.d/busybox-aliases" 10 log
pcp_incr_id; pcp_textarea "" "cat /proc/cmdline" 6 log

pcp_incr_id
if [ -f "/opt/eth0.sh" ]; then
  pcp_textarea "" "cat /opt/eth0.sh" 5 log
else
  pcp_textarea "/opt/eth0.sh" "echo File does not exist." 2 log
fi

pcp_incr_id
if [ -f "/opt/wlan0.sh" ]; then
  pcp_textarea "" "cat /opt/wlan0.sh" 4 log
else
  pcp_textarea "/opt/wlan0.sh" "echo File does not exist." 3 log
fi

echo '  </div>'

pcp_footer
pcp_copyright
echo '</div>'
echo '</body>'
echo '</html>'
