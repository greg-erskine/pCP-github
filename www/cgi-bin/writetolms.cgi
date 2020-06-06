#!/bin/sh

# Version: 7.0.0 2020-06-06

. pcp-functions

# Store the original values so we can see if they are changed
ORIG_LMSERVER="$LMSERVER"

pcp_html_head "Write LMS settings" "SBP"

pcp_navbar
pcp_httpd_query_string

WGET="/bin/busybox wget"
LMS_UPDATE_LOG="/var/log/slimserver/LMS_update.log"

# Only offer reboot option if needed
REBOOT_REQUIRED=0

#========================================================================================================
# Routines
#--------------------------------------------------------------------------------------------------------
pcp_enable_lms() {
	# $1 - format

	FORMAT=$1
	pcp_message INFO "Enabling automatic start of LMS..." $FORMAT
	[ $DEBUG -eq 1 ] && pcp_message DEBUG "LMS is added to onboot.lst" $FORMAT
	sudo sed -i '/slimserver.tcz/d' $ONBOOTLST
	sudo echo 'slimserver.tcz' >> $ONBOOTLST
}

pcp_disable_lms() {
	# $1 - format

	FORMAT=$1
	pcp_message INFO "Disabling automatic start of LMS..." $FORMAT
#	sudo /usr/local/etc/init.d/slimserver stop >/dev/null 2>&1
	sudo sed -i '/slimserver.tcz/d' $ONBOOTLST
}

pcp_lms_update() {
	# The -m option will force an update no matter what.  We need to remove that option after testing.
	# Update checks and frequency are set within LMS, and will write /tmp/slimupdate/update_url when there is an update to be done.
	sudo lms-update.sh -r -u 2>&1 | sudo tee -a "$LMS_UPDATE_LOG"   
}

pcp_restore_LMS_cache() {
	sudo /usr/local/etc/init.d/slimserver stop
	sudo rm -rf $TCEMNT/tce/slimserver/Cache/
	sudo rm -rf $TCEMNT/tce/slimserver/prefs/
	pcp_message INFO "LMS is now using SD card to store its values..." "text"
	pcp_message INFO "LMS will automatically rescan your library again..." "text"
	pcp_message INFO "" "text" "-n"
	sudo /usr/local/etc/init.d/slimserver start
}

case "$ACTION" in
	#========================================================================================
	# LMS Statup section
	#----------------------------------------------------------------------------------------
	# Only do something if variable is changed
	Startup)
		pcp_heading5 "LMS Server Auto Start"
		pcp_infobox_begin
		pcp_message INFO "LMS is set to: $LMSERVER" "text"
		if [ "$ORIG_LMSERVER" != "$LMSERVER" -a "$UPDATE" = "" ]; then
			[ $DEBUG -eq 1 ] && pcp_message DEBUG "ORIG_LMS is: $ORIG_LMSERVER" "text"
			[ $DEBUG -eq 1 ] && pcp_message DEBUG "LMS is: $LMSERVER" "text"
			case "$LMSERVER" in
				yes)
					pcp_message INFO "Automatic start of LMS is enabled." "text"
					pcp_enable_lms "text"
				;;
				no)
					pcp_message INFO "Automatic start of LMS is disabled." "text"
					pcp_disable_lms "text"
				;;
				*)
					pcp_message ERROR "LMS selection invalid: $LMSERVER" "text"
				;;
			esac
			pcp_save_to_config
			pcp_backup "text"
		else
			pcp_message INFO "LMS Server Auto Start unchanged." "text"
		fi
		pcp_infobox_end
	;;
	#========================================================================================
	# Update of LMS section
	#----------------------------------------------------------------------------------------
	Update)
		pcp_heading5 "LMS Server Updating"
		[ $DEBUG -eq 1 ] && pcp_message DEBUG "UPDATE is: $UPDATE" "text"
		pcp_infobox_begin
		pcp_message INFO "LMS is updating. It will take a few minutes" "text"
		pcp_lms_update
		pcp_infobox_end
	;;
esac

[ $DEBUG -eq 1 ] && pcp_textarea "Current $ONBOOTLST" "cat $ONBOOTLST" 15
[ $DEBUG -eq 1 ] && pcp_textarea "Current $PCPCFG" "cat $PCPCFG" 15

[ $REBOOT_REQUIRED -eq 1 ] && pcp_reboot_required

pcp_redirect_button "Go to LMS" "lms.cgi" 15

pcp_html_end
