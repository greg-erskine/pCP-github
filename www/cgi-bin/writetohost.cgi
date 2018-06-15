#!/bin/sh

# Version: 4.0.0 2018-06-15

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

pcp_html_head "Write Hostname" "SBP" "10" "tweaks.cgi"

pcp_banner
pcp_running_script
pcp_httpd_query_string

pcp_table_top "Changing hostname"
echo '<p class="info">[ INFO ] Host is now: '$HOST'</p>'
pcp_mount_bootpart
pcp_write_to_host

[ $DEBUG -eq 1 ] && pcp_textarea_inform "Current $CMDLINETXT" "cat $CMDLINETXT" 70

pcp_umount_bootpart
pcp_save_to_config
pcp_backup

if [ $DEBUG -eq 1 ]; then
	pcp_textarea_inform "Current hostname" "hostname" 20
	pcp_textarea_inform "Current /proc/cmdline" "cat /proc/cmdline" 100
	pcp_textarea_inform "Current /etc/hostname" "cat /etc/hostname" 50
	pcp_textarea_inform "Current /etc/hosts" "cat /etc/hosts" 180
	pcp_textarea_inform "Current /opt/bootsync.sh" "cat /opt/bootsync.sh" 100
	pcp_textarea_inform "Current pcp.cfg" "cat $PCPCFG" 380
	pcp_textarea_inform "ps " "ps | grep -v grep | grep udhcpc" 50
fi

pcp_table_middle
pcp_redirect_button "Go to Tweaks" "tweaks.cgi" 5
pcp_table_end
pcp_footer
pcp_copyright
pcp_reboot_required

echo '</body>'
echo '</html>'