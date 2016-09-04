#!/bin/sh

# Version: 0.02 2016-05-09 GE
#	Fixed SCREENROTATE variable (YES/NO).

# Version: 0.01 2015-10-06 SBP
#	Original.

. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "Write to config.cfg" "SBP" "15" "tweaks.cgi"

pcp_banner
pcp_running_script
pcp_httpd_query_string
pcp_save_to_config

#========================================================================================
# Write to mmcblk0p1/config.txt
#----------------------------------------------------------------------------------------
case "$SCREENROTATE" in
	yes)
		pcp_mount_mmcblk0p1
		sed -i '/lcd_rotate=2/d' $CONFIGTXT
		sudo echo 'lcd_rotate=2' >> $CONFIGTXT
		pcp_umount_mmcblk0p1
	;;
	no)
		pcp_mount_mmcblk0p1
		sed -i '/lcd_rotate=2/d' $CONFIGTXT
		pcp_umount_mmcblk0p1
	;;
	*)
		echo '[ ERROR ] Error setting $SCREENROTATE to '$SCREENROTATE
	;;
esac

. $CONFIGCFG

pcp_show_config_cfg
pcp_backup
pcp_reboot_required
pcp_go_back_button

echo '</body>'
echo '</html>'