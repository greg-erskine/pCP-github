#!/bin/sh
# Boot diagnostics script

# Version: 0.04 2015-04-28 GE
#	Minor updates.

# Version: 0.03 2015-03-31 GE
#	Added /usr/local/bin/wifi.sh
#	Added navigation links at top of page.

# Version: 0.02 2015-03-07 GE
#	Minor updates.

# version: 0.01 2014-10-22 GE
#	Original.

. pcp-functions
pcp_variables

# Local variables
START="====================> Start <===================="
END="=====================> End <====================="
LOG="/tmp/diagboot.log"
(echo $0; date) > $LOG
echo "This shows the boot process, starting with the initial init and going through to the the tc profile and ashrc files." >> $LOG

pcp_html_head "Boot Diagnostics" "GE"

pcp_footer
pcp_banner
pcp_diagnostics
pcp_running_script
pcp_mode_lt_5

#=========================================================================================
# Boot files in order of execution
#-----------------------------------------------------------------------------------------
echo '<p>This shows the boot process, starting with the initial init and going through to the the '
echo '   tc profile and ashrc files. A log file <b>/tmp/diagboot.log</b> is also created.</p>'

echo '<ol>'
echo '	<li><a href="#01">/init</a></li>'
echo '	<li><a href="#02">/sbin/init</a></li>'
echo '	<li><a href="#03">/etc/init.d/rcS</a></li>'
echo '	<li><a href="#04">/etc/init.d/tc-config</a></li>'
echo '	<li><a href="#05">/opt/bootsync.sh</a></li>'
echo '	<li><a href="#06">/opt/bootlocal.sh</a></li>'
echo '	<li><a href="#07">/home/tc/www/cgi-bin/do_rebootstuff.sh</a></li>'
echo '	<li><a href="#08">/home/tc/.profile</a></li>'
echo '	<li><a href="#09">/home/tc/.ashrc</a></li>'
echo '	<li><a href="#10">/etc/init.d/tc-functions</a></li>'
echo '	<li><a href="#11">/proc/cmdline</a></li>'
echo '	<li><a href="#12">/usr/local/bin/wifi.sh</a></li>'
echo '</ol>'

echo '<p id="01"></p>'
pcp_textarea "" "cat /init" 300 log
echo '<p id="02"></p>'
pcp_textarea "" "ls -al /sbin/init" 60 log
echo '<p id="03"></p>'
pcp_textarea "" "cat /etc/init.d/rcS" 240 log
echo '<p id="04"></p>'
pcp_textarea "" "cat /etc/init.d/tc-config" 600 log
echo '<p id="05"></p>'
pcp_textarea "" "cat /opt/bootsync.sh" 120 log
echo '<p id="06"></p>'
pcp_textarea "" "cat /opt/bootlocal.sh" 110 log
echo '<p id="07"></p>'
pcp_textarea "" "cat /home/tc/www/cgi-bin/do_rebootstuff.sh" 600 log
echo '<p id="08"></p>'
pcp_textarea "" "cat /home/tc/.profile" 530 log
echo '<p id="09"></p>'
pcp_textarea "" "cat /home/tc/.ashrc" 410 log

#=========================================================================================
# Files called from various boot files
#-----------------------------------------------------------------------------------------
echo '<p>Additional files that are run during the boot process that may be of interest</p>'

echo '<p id="10"></p>'
pcp_textarea "" "cat /etc/init.d/tc-functions" 600 log
echo '<p id="11"></p>'
pcp_textarea "" "cat /proc/cmdline" 100 log
echo '<p id="12"></p>'
pcp_textarea "" "cat /usr/local/bin/wifi.sh" 500 log

echo '<br />'
echo '<br />'

pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'