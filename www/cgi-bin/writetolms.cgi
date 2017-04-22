#!/bin/sh

# Version: 3.20 2017-03-08
#	Fixed pcp-xxx-functions issues. GE.

# Version: 3.10 2016-12-23
#	Remove references to SAMBA in this routine. PH.

# Version: 2.05 2016-04-15
#	Fixed sourceforge redirection issue. GE.
#	Updated slimserver extension names. PH.
#	Added LMS update function. SBP.

# Version: 0.01 2016-01-30 SBP
#	Original version.

. pcp-functions

# Store the original values so we can see if they are changed
ORIG_LMSERVER="$LMSERVER"

pcp_html_head "Write LMS settings" "SBP" "15" "lms.cgi"

pcp_banner
pcp_running_script
pcp_httpd_query_string

WGET="/bin/busybox wget"
LMSUPDATELOG="/tmp/updateLMS.txt"					#<---- MAKE RIGHT DIRECTORY???
#LMSUPDATELOG="${LOGDIR}/pcp_updateLMS.log"			# GE. Can we make the log file dir/name this?

# Only offer reboot option if needed
REBOOT_REQUIRED=0

#========================================================================================================
# Routines
#--------------------------------------------------------------------------------------------------------
pcp_enable_lms() {
	echo '<p class="info">[ INFO ] Enabling automatic start of LMS...</p>'
	[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] LMS is added to onboot.lst</p>'
	sudo sed -i '/slimserver.tcz/d' /mnt/mmcblk0p2/tce/onboot.lst
	sudo echo 'slimserver.tcz' >> /mnt/mmcblk0p2/tce/onboot.lst
}

pcp_disable_lms() {
	echo '<p class="info">[ INFO ] Disabling automatic start of LMS...</p>'
#	sudo /usr/local/etc/init.d/slimserver stop >/dev/null 2>&1
	sudo sed -i '/slimserver.tcz/d' /mnt/mmcblk0p2/tce/onboot.lst
}

pcp_lms_update() {
	# The -m option will force an update no matter what.  We need to remove that option after testing.
	# Update checks and frequency are set within LMS, and will write /tmp/slimupdate/update_url when there is an update to be done.
	sudo lms-update.sh -r -u > "$LMSUPDATELOG" 2>&1  
}

pcp_restore_LMS_cache() {
	sudo /usr/local/etc/init.d/slimserver stop
	sudo rm -rf /mnt/mmcblk0p2/tce/slimserver/Cache/
	sudo rm -rf /mnt/mmcblk0p2/tce/slimserver/prefs/
	echo '<p class="info">[ INFO ] LMS is now using SD-card to store its values...</p>'
	echo '<p class="info">[ INFO ] LMS will automatically rescan your library again...</p>'
	sudo /usr/local/etc/init.d/slimserver start
}

#========================================================================================
# LMS section
#----------------------------------------------------------------------------------------
# Only do something if variable is changed
if [ "$ORIG_LMSERVER" != "$LMSERVER" ]; then
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
else
	echo '<p class="info">[ INFO ] LMS variable unchanged.</p>'
fi

#========================================================================================
# Update of LMS section
#----------------------------------------------------------------------------------------
[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] UPDATE is: '$UPDATE'</p>'
case "$UPDATE" in
	Update)
		echo '<p class="info">[ INFO ] LMS is updating. It will take a few minutes.</p>'
		pcp_lms_update
		pcp_textarea "Log from latest LMS update $LMSUPDATELOG" "cat $LMSUPDATELOG" 150
	;;
esac

echo '<hr>'
pcp_save_to_config
pcp_backup

[ $DEBUG -eq 1 ] && pcp_textarea "Current $ONBOOTLST" "cat $ONBOOTLST" 150
[ $DEBUG -eq 1 ] && pcp_textarea "Current $CONFIGCFG" "cat $CONFIGCFG" 150

[ $REBOOT_REQUIRED -eq 1 ] && pcp_reboot_required

pcp_go_back_button

echo '</body>'
echo '</html>'