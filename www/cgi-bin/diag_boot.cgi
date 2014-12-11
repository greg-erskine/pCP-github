#!/bin/sh
# Boot diagnostics script

# version: 0.01 2014-10-22 GE
#	Orignal.

. pcp-functions
pcp_variables

# Local variables
START="====================> Start <===================="
END="=====================> End <====================="
LOG="/tmp/diagboot.log"
(echo $0; date) > $LOG

pcp_html_head "Boot Diagnostics" "GE"

if [ $MODE -lt 5 ]; then
	echo '</body>'
	echo '</html>'
	exit 1
fi

pcp_banner
pcp_navigation
pcp_refresh_button

#=========================================================================================
# Boot files in order of execution
#-----------------------------------------------------------------------------------------
echo '<p>This shows the boot process, starting with the initial init and going through to the the '
echo '   tc profile and ashrc files. A log file /tmp/diagboot.log is also created.</p>'

pcp_textarea "" "cat /init" 300 log
pcp_textarea "" "ls -al /sbin/init" 60 log
pcp_textarea "" "cat /etc/init.d/rcS" 240 log
pcp_textarea "" "cat /etc/init.d/tc-config" 600 log
pcp_textarea "" "cat /opt/bootsync.sh" 120 log
pcp_textarea "" "cat /opt/bootlocal.sh" 110 log
pcp_textarea "" "cat /home/tc/www/cgi-bin/do_rebootstuff.sh" 600 log
pcp_textarea "" "cat /home/tc/.profile" 530 log
pcp_textarea "" "cat /home/tc/.ashrc" 410 log

#=========================================================================================
# Files called from various boot files
#-----------------------------------------------------------------------------------------
echo '<p>Additional files that are run during the boot process that may be of interest</p>'

pcp_textarea "" "cat /etc/init.d/tc-functions" 600 log
pcp_textarea "" "cat /proc/cmdline" 100 log

pcp_refresh_button
pcp_footer

echo '</body>'
echo '</html>'