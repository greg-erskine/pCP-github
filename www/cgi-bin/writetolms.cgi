#!/bin/sh

# Version: 0.02 2016-03-13 GE
#	Fixed sourceforge redirection issue.
#	Updated slimserver extension names   PH

# Version: 0.01 2016-01-30 SBP
#	Original version.

. pcp-functions
pcp_variables

# Store the original values so we can see if they are changed
ORIG_LMSERVER="$LMSERVER"
ORIG_SAMBA="$SAMBA"

pcp_html_head "Write to Audio Tweak" "SBP" "15" "tweaks.cgi"

pcp_banner
pcp_running_script
pcp_httpd_query_string

#LMS="slimserver*"
SAMBA="samba.tcz"
WGET="/bin/busybox wget"

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

#========================================================================================
# LMS section
#----------------------------------------------------------------------------------------
 Only do something if variable is changed
if [ $ORIG_LMSERVER != $LMSERVER ]; then
	REBOOT_REQUIRED=1
	echo '<hr>'
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
	echo '<hr>'
else
	echo '<p class="info">[ INFO ] LMS variable unchanged.</p>'
fi


echo '<hr>'
pcp_save_to_config
pcp_backup

[ $DEBUG = 1 ] && pcp_textarea "Current $ONBOOTLST" "cat $ONBOOTLST" 150
[ $DEBUG = 1 ] && pcp_textarea "Current $CONFIGCFG" "cat $CONFIGCFG" 150

[ $REBOOT_REQUIRED = 1 ] && pcp_reboot_required

pcp_go_back_button

echo '</body>'
echo '</html>'