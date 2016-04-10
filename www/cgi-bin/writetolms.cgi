#!/bin/sh

# Version: 0.02 2016-03-19 GE
#	Fixed sourceforge redirection issue.
#	Updated slimserver extension names   PH
#	Added LMS update function   SBP


# Version: 0.01 2016-01-30 SBP
#	Original version.

. pcp-functions
pcp_variables

# Store the original values so we can see if they are changed
ORIG_LMSERVER="$LMSERVER"
ORIG_SAMBA="$SAMBA"

pcp_html_head "Write LMS settings" "SBP" "15" "lms.cgi"

pcp_banner
pcp_running_script
pcp_httpd_query_string

#LMS="slimserver*"
SAMBA="samba.tcz"
WGET="/bin/busybox wget"
LMSUPDATELOG=/tmp/updateLMS.txt

# Only offer reboot option if needed
REBOOT_REQUIRED=0

#========================================================================================================
# Routines
#--------------------------------------------------------------------------------------------------------

pcp_enable_lms() {
	echo '<p class="info">[ INFO ] Enabling automatic start of LMS...</p>'
	[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] LMS is added to onboot.lst</p>'
	sudo sed -i '/slimserver.tcz/d' /mnt/mmcblk0p2/tce/onboot.lst
	sudo echo 'slimserver.tcz' >> /mnt/mmcblk0p2/tce/onboot.lst
}

pcp_disable_lms() {
	echo '<p class="info">[ INFO ] Disabling automatic start of LMS...</p>'
#	sudo /usr/local/etc/init.d/slimserver stop >/dev/null 2>&1
	sudo sed -i '/slimserver.tcz/d' /mnt/mmcblk0p2/tce/onboot.lst
}

pcp_lms_update() {
	sudo lms-update.sh -r -m -u > "$LMSUPDATELOG" 2>&1
}

pcp_move_LMS_cache() {
	sudo /usr/local/etc/init.d/slimserver stop
	sudo cp -avr /mnt/mmcblk0p2/tce/slimserver/Cache/ /mnt/$MOUNTPOINT/
	sudo rm -rf /mnt/mmcblk0p2/tce/slimserver/Cache/
	sudo ln -s /mnt/$MOUNTPOINT/Cache/ /mnt/mmcblk0p2/tce/slimserver/

	sudo cp -avr /mnt/mmcblk0p2/tce/slimserver/prefs/ /mnt/$MOUNTPOINT/
	sudo rm -rf /mnt/mmcblk0p2/tce/slimserver/prefs/
	sudo ln -s /mnt/$MOUNTPOINT/prefs/ /mnt/mmcblk0p2/tce/slimserver/
	echo '<p class="info">[ INFO ] LMS is now using the attached Media drive to store its values...</p>'
	sudo /usr/local/etc/init.d/slimserver start
}


pcp_restore_LMS_cache() {
	sudo /usr/local/etc/init.d/slimserver stop
	sudo rm -rf /mnt/mmcblk0p2/tce/slimserver/Cache/
	sudo rm -rf /mnt/mmcblk0p2/tce/slimserver/prefs/
	echo '<p class="info">[ INFO ] LMS is now using SD-card to store its values...</p>'
	echo '<p class="info">[ INFO ] LMS will automatically rescan your libaryis again...</p>'
	sudo /usr/local/etc/init.d/slimserver start
}



#========================================================================================
# LMS section
#----------------------------------------------------------------------------------------
# Only do something if variable is changed
if [ $ORIG_LMSERVER != $LMSERVER ]; then
	echo '<p class="info">[ INFO ] LMS is set to: '$LMSERVER'</p>'
	[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] ORIG_LMS is: '$ORIG_LMSERVER'</p>'
	[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] LMS is: '$LMSERVER'</p>'

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
	[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] UPDATE is: '$UPDATE'</p>'
	case "$UPDATE" in
		Update)
			echo '<p class="info">[ INFO ] LMS is updating. It will take a few minutes.</p>'
			pcp_lms_update
			pcp_textarea "Log from latest LMS update $LMSUPDATELOG" "cat $LMSUPDATELOG" 150
			;;
	esac


#========================================================================================
# Move LMS cache and prefs section
#----------------------------------------------------------------------------------------
	[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] CACHE_SD is: '$CACHE_SDE'</p>'
	case "$CACHE_SD" in
		SDcard)
			echo '<p class="info">[ INFO ] Moving LMS Cache and prefs to attached media drive.</p>'
			pcp_move_LMS_cache
			;;
		Media)
			echo '<p class="info">[ INFO ] Restoring LMS cache and prefs location to SD-card.</p>'
			pcp_restore_LMS_cache
			;;
		
	esac





echo '<hr>'
pcp_save_to_config
pcp_backup

[ $DEBUG = 1 ] && pcp_textarea "Current $ONBOOTLST" "cat $ONBOOTLST" 150
[ $DEBUG = 1 ] && pcp_textarea "Current $CONFIGCFG" "cat $CONFIGCFG" 150

[ $REBOOT_REQUIRED = 1 ] && pcp_reboot_required

pcp_go_back_button

echo '</body>'
echo '</html>'