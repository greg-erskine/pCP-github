#!/bin/sh

# Version: 4.0.0 2018-08-11

. pcp-functions

pcp_html_head "Write to config.txt" "SBP"

pcp_banner
pcp_running_script
pcp_httpd_query_string

pcp_save_to_config

#========================================================================================
# Write to BOOTMNT/config.txt
#----------------------------------------------------------------------------------------
pcp_table_top "Rotate screen"
echo '<p class="info">[ INFO ] Setting screen rotate to '$SCREENROTATE'</p>'

case "$SCREENROTATE" in
	0|no)
		pcp_mount_bootpart
		sed -i "s/\(lcd_rotate=\).*/\10/" $CONFIGTXT
		pcp_umount_bootpart
	;;
	180|yes)
		pcp_mount_bootpart
		sed -i "s/\(lcd_rotate=\).*/\12/" $CONFIGTXT
		pcp_umount_bootpart
	;;
	*)
		echo '<p class="error">[ ERROR ] Error setting screen rotate to '$SCREENROTATE'</p>'
	;;
esac

pcp_backup
pcp_table_middle
pcp_redirect_button "Go to Tweaks" "tweaks.cgi" 10
pcp_table_end

pcp_footer
pcp_copyright
pcp_reboot_required

echo '</body>'
echo '</html>'