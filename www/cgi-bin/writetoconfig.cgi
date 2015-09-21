#!/bin/sh

# Version: 0.05 2015-09-21 SBP
#	Removed httpd decoding.
#	Added pcp_restart_required.

# Version: 0.04 2015-01-23 SBP
#	Added CLOSEOUT.
#	Removed debugging code.
#	Removed adding quotes when decoding variables.
#	Added pcp_reset, pcp_restore.

# Version: 0.03 2014-12-12 GE
#	HTML5 format.
#	Minor mods.

# Version: 0.02 2014-08-22 SBP
#	Changed the back button to absolute path back to Squeezelite.cgi. Otherwise we would go in circles.

# Version: 0.01 2014-06-25 GE
#	Original.

. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "Write to config.cfg" "SBP" "15" "squeezelite.cgi"

pcp_banner
pcp_running_script
pcp_httpd_query_string

#========================================================================================
# Reset configuration
#----------------------------------------------------------------------------------------
pcp_reset() {
	pcp_reset_config_to_defaults
}

#========================================================================================
# Restore configuration
#
# Note: Assumes a backup onto USB stick exists.
#----------------------------------------------------------------------------------------
pcp_restore() {
	pcp_mount_device sda1
	. /mnt/sda1/newconfig.cfg
	pcp_umount_device sda1
	pcp_save_to_config
}

#========================================================================================
# Main
#----------------------------------------------------------------------------------------
case $SUBMIT in
	Save)
		pcp_save_to_config
		;;
	Reset*)
		pcp_reset
		;;
	Restore*)
		pcp_restore
		;;
	*)
		echo '<p class="error">[ ERROR ] Invalid case argument.</p>'
		;;
esac

. $CONFIGCFG

pcp_show_config_cfg
pcp_backup
pcp_go_back_button

pcp_restart_required

echo '</body>'
echo '</html>'