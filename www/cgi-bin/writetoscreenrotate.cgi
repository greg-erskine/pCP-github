#!/bin/sh

# Version: 3.5.1 2018-04-02
#	Added pcp_redirect_button. GE.

# Version: 3.21 2017-05-20
#	Changed to allow booting from USB on RPi3. PH.

# Version: 3.20 2017-03-08
#	Fixed pcp-xxx-functions issues. GE.

# Version: 3.12 2017-02-26
#	Updated to default rotation to 0. GE.
#	Brown ribbon cable to bottom. GE.

# Version: 3.10 2017-01-06
#	Enhanced formatting. GE.

# Version: 0.01 2015-10-06
#	Original. SBP.

. pcp-functions

pcp_html_head "Write to config.cfg" "SBP"

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