#!/bin/sh

# Version: 4.0.0 2018-06-15

. pcp-functions

# Store the original values so we can see if they are changed
ORIG_LMSERVER="$LMSERVER"

pcp_html_head "Write LMS settings" "SBP"

pcp_banner
pcp_running_script
pcp_httpd_query_string

WGET="/bin/busybox wget"
LMS_UPDATE_LOG="/var/log/slimserver/LMS_update.log"

# Only offer reboot option if needed
REBOOT_REQUIRED=0

#========================================================================================================
# Routines
#--------------------------------------------------------------------------------------------------------
pcp_enable_lms() {
	echo '<p class="info">[ INFO ] Enabling automatic start of LMS...</p>'
	[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] LMS is added to onboot.lst</p>'
	sudo sed -i '/slimserver.tcz/d' $ONBOOTLST
	sudo echo 'slimserver.tcz' >> $ONBOOTLST
}

pcp_disable_lms() {
	echo '<p class="info">[ INFO ] Disabling automatic start of LMS...</p>'
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
	echo '<p class="info">[ INFO ] LMS is now using SD-card to store its values...</p>'
	echo '<p class="info">[ INFO ] LMS will automatically rescan your library again...</p>'
	sudo /usr/local/etc/init.d/slimserver start
}

case "$ACTION" in
	#========================================================================================
	# LMS Statip section
	#----------------------------------------------------------------------------------------
	# Only do something if variable is changed
	Startup)
		if [ "$ORIG_LMSERVER" != "$LMSERVER" -a "$UPDATE" = "" ]; then
			pcp_table_top "LMS Server Auto Start"
			echo '<p class="info">[ INFO ] LMS is set to: '$LMSERVER'</p>'
			[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] ORIG_LMS is: '$ORIG_LMSERVER'</p>'
			[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] LMS is: '$LMSERVER'</p>'

			case "$LMSERVER" in
				yes)
					echo '<p class="info">[ INFO ] Automatic start of LMS is enabled.</p>'
					pcp_enable_lms
				;;
				no)
					echo '<p class="info">[ INFO ] Automatic start of LMS is disabled</p>'
					pcp_disable_lms
				;;
				*)
					echo '<p class="error">[ ERROR ] LMS selection invalid: '$LMSERVER'</p>'
				;;
			esac
			pcp_save_to_config
			pcp_backup
		else
			pcp_table_top "LMS Server Auto Start"
			echo '<p class="info">[ INFO ] LMS variable unchanged.</p>'
		fi
	;;
	#========================================================================================
	# Update of LMS section
	#----------------------------------------------------------------------------------------
	Update)
		[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] UPDATE is: '$UPDATE'</p>'
		pcp_table_top "LMS Server Updating"
		echo '<p class="info">[ INFO ] LMS is updating. It will take a few minutes.</p>'
		echo '<textarea class="inform" style="height:200px">'
		pcp_lms_update
		echo '</textarea>'
	;;
esac

#echo '<hr>'

[ $DEBUG -eq 1 ] && pcp_textarea "Current $ONBOOTLST" "cat $ONBOOTLST" 150
[ $DEBUG -eq 1 ] && pcp_textarea "Current $PCPCFG" "cat $PCPCFG" 150

[ $REBOOT_REQUIRED -eq 1 ] && pcp_reboot_required

pcp_table_middle
pcp_redirect_button "Go to LMS" "lms.cgi" 15
pcp_table_end
pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'
