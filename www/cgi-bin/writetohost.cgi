#!/bin/sh

# Version: 3.10 2017-01-06
#	Enhanced formatting. GE.

# Version: 0.03 2015-12-05 GE
#	Added more debug information.
#	Added reboot required button.

# Version: 0.02 2014-12-10 GE
#	Using pcp_html_head now.
#	HTML5 formatting.

# Version: 0.01 2014-08-06 SBP
#	Original version.

#========================================================================================
# The hostname is set during the boot process. It needs to be set before the network is
# started otherwise udhcpc will use the default hostname "box".
#
# Default hostname values:
# - piCore       : box
# - piCorePlayer : piCorePlayer
#
# The best option is setting the hostname in cmdline.txt, therefore a reboot is required.
#
# You need to check the following to ensure the hostname is fully implemented:
#  - /etc/hostname
#  - /etc/hosts
#  - /opt/bootsync.sh				: sethostname piCorePlayer, default value if missing from cmdline.txt
#  - config.cfg
#  - /mnt/mmcblk0p1/cmdline.txt		: hostname set here, overwrites all other methods
#  - /proc/cmdline.txt				: set after reboot
#  - $CMDLINE						: set after reboot
#  - linux prompt
#  - udhcpc - eth0
#  - udhcpc - wlan0
#
# The extensive debug information should give most of the above information.
# ---------------------------------------------------------------------------------------

. pcp-functions
pcp_variables

pcp_html_head "Write Hostname" "SBP" "10" "tweaks.cgi"

pcp_banner
pcp_running_script
pcp_httpd_query_string

pcp_table_top "Changing hostname"
echo '<p class="info">[ INFO ] Host is now: '$HOST'</p>'
pcp_mount_mmcblk0p1
pcp_write_to_host
[ $DEBUG -eq 1 ] && pcp_textarea_inform "Current /mnt/mmcblk0p1/cmdline.txt" "cat /mnt/mmcblk0p1/cmdline.txt" 70
pcp_umount_mmcblk0p1
pcp_save_to_config
pcp_backup

if [ $DEBUG -eq 1 ]; then
	pcp_textarea_inform "Current hostname" "hostname" 20
	pcp_textarea_inform "Current /proc/cmdline" "cat /proc/cmdline" 100
	pcp_textarea_inform "Current /etc/hostname" "cat /etc/hostname" 50
	pcp_textarea_inform "Current /etc/hosts" "cat /etc/hosts" 180
	pcp_textarea_inform "Current /opt/bootsync.sh" "cat /opt/bootsync.sh" 100
	pcp_textarea_inform "Current config.cfg" "cat $CONFIGCFG" 380
	pcp_textarea_inform "ps " "ps | grep -v grep | grep udhcpc" 50
fi

pcp_table_middle
pcp_go_back_button
pcp_table_end
pcp_footer
pcp_copyright
pcp_reboot_required

echo '</body>'
echo '</html>'