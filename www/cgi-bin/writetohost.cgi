#!/bin/sh

# Version: 0.03 2015-12-03 GE
#	Added more debug information.
#	PROBLEM: udhcpc uses box.

# Version: 0.02 2014-12-10 GE
#	Using pcp_html_head now.
#	HTML5 formatting.

# Version: 0.01 2014-08-06 SBP
#   Original version.

. pcp-functions
pcp_variables

pcp_html_head "Write Hostname" "SBP" "15" "tweaks.cgi"

pcp_banner
pcp_running_script
pcp_httpd_query_string
echo '<p class="info">[ INFO ] Host is now: '$HOST'</p>'
pcp_mount_mmcblk0p1
pcp_write_to_host
pcp_umount_mmcblk0p1
pcp_save_to_config
pcp_backup

if [ $DEBUG = 1 ]; then
	pcp_textarea "Current hostname" "hostname" 50
	pcp_textarea "Current /etc/hostname" "cat /etc/hostname" 50
	pcp_textarea "Current /opt/bootsync.sh" "cat /opt/bootsync.sh" 100
	pcp_textarea "Current /etc/hosts" "cat /etc/hosts" 180
	pcp_textarea "Current config.cfg" "cat $CONFIGCFG" 380
	pcp_textarea "ps " "ps | grep -v grep | grep udhcpc" 100
fi

pcp_reboot_required
pcp_go_back_button

echo '</body>'
echo '</html>'