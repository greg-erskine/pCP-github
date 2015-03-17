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
	JIVELITE=`sudo /usr/local/sbin/httpd -d \"$JIVELITE\"`
	NAME=`sudo /usr/local/sbin/httpd -d $NAME`
	OUTPUT=`sudo /usr/local/sbin/httpd -d $OUTPUT`
	ALSA_PARAMS=`sudo /usr/local/sbin/httpd -d $ALSA_PARAMS`
	BUFFER_SIZE=`sudo /usr/local/sbin/httpd -d $BUFFER_SIZE`
	_CODEC=`sudo /usr/local/sbin/httpd -d $_CODEC`
	PRIORITY=`sudo /usr/local/sbin/httpd -d $PRIORITY`
	MAX_RATE=`sudo /usr/local/sbin/httpd -d $MAX_RATE`
	UPSAMPLE=`sudo /usr/local/sbin/httpd -d $UPSAMPLE`
	MAC_ADDRESS=`sudo /usr/local/sbin/httpd -d $MAC_ADDRESS`
	SERVER_IP=`sudo /usr/local/sbin/httpd -d $SERVER_IP`
	LOGLEVEL=`sudo /usr/local/sbin/httpd -d $LOGLEVEL`
	LOGFILE=`sudo /usr/local/sbin/httpd -d $LOGFILE`
	DSDOUT=`sudo /usr/local/sbin/httpd -d $DSDOUT`
	VISUALISER=`sudo /usr/local/sbin/httpd -d $VISUALISER`
	CLOSEOUT=`sudo /usr/local/sbin/httpd -d $CLOSEOUT`
	OTHER=`sudo /usr/local/sbin/httpd -d $OTHER`

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