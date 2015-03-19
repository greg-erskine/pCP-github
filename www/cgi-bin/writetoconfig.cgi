#!/bin/sh

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
# Save configuration
#----------------------------------------------------------------------------------------

pcp_save() {
	# Decode Squeezelite variables using httpd
	# ----------------------------------------
	NAME=`sudo $HTPPD -d $NAME`
	OUTPUT=`sudo $HTPPD -d $OUTPUT`
	ALSA_PARAMS=`sudo $HTPPD -d $ALSA_PARAMS`
	BUFFER_SIZE=`sudo $HTPPD -d $BUFFER_SIZE`
	_CODEC=`sudo $HTPPD -d $_CODEC`
	PRIORITY=`sudo $HTPPD -d $PRIORITY`
	MAX_RATE=`sudo $HTPPD -d $MAX_RATE`
	UPSAMPLE=`sudo $HTPPD -d $UPSAMPLE`
	MAC_ADDRESS=`sudo $HTPPD -d $MAC_ADDRESS`
	SERVER_IP=`sudo $HTPPD -d $SERVER_IP`
	LOGLEVEL=`sudo $HTPPD -d $LOGLEVEL`
	LOGFILE=`sudo $HTPPD -d $LOGFILE`
	DSDOUT=`sudo $HTPPD -d $DSDOUT`
	VISUALISER=`sudo $HTPPD -d $VISUALISER`
	CLOSEOUT=`sudo $HTPPD -d $CLOSEOUT`
	OTHER=`sudo $HTPPD -d $OTHER`
	JIVELITE=`sudo $HTPPD -d $JIVELITE`

	# Save the variables to the config file
	# -------------------------------------
	pcp_save_to_config
}





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
		pcp_save
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

echo '</body>'
echo '</html>'