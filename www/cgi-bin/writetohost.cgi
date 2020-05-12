#!/bin/sh

# Version: 7.0.0 2020-05-12

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
#  - pcp.cfg
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

REDIRECT_WAIT=5

pcp_navbar
pcp_httpd_query_string

pcp_heading5 "Changing hostname"

pcp_infobox_begin
pcp_message INFO "Host is now: $HOST" "html"
pcp_mount_bootpart
pcp_write_to_host
pcp_umount_bootpart
pcp_save_to_config
pcp_backup
pcp_infobox_end

if [ $DEBUG -eq 1 ]; then
	REDIRECT_WAIT=30
	echo '<hr>'
	pcp_heading5 "Debug information"
	pcp_mount_bootpart
	pcp_textarea "Current $CMDLINETXT" "cat $CMDLINETXT" 7
	pcp_umount_bootpart
	pcp_textarea "Current hostname" "hostname" 2
	pcp_textarea "Current /proc/cmdline" "cat /proc/cmdline" 10
	pcp_textarea "Current /etc/hostname" "cat /etc/hostname" 5
	pcp_textarea "Current /etc/hosts" "cat /etc/hosts" 20
	pcp_textarea "Current /opt/bootsync.sh" "cat /opt/bootsync.sh" 10
	pcp_textarea "Current pcp.cfg" "cat $PCPCFG" 20
	pcp_textarea "ps " "ps | grep -v grep | grep udhcpc" 5
fi

pcp_redirect_button "Go to Tweaks" "tweaks.cgi" $REDIRECT_WAIT
pcp_reboot_required
pcp_html_end
