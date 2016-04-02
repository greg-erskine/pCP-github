#!/bin/sh

# Version: 0.01 2016-04-02 PH
#	Original version.

. pcp-functions
pcp_variables

# Store the original values so we can see if they are changed
ORIG_MOUNTPOINT="$MOUNTPOINT"
ORIG_MOUNTUUID="$MOUNTUUID"

pcp_html_head "Write to Disk Mounts" "PH" 

pcp_banner
pcp_running_script
pcp_httpd_query_string

WGET="/bin/busybox wget"

# Only offer reboot option if needed
REBOOT_REQUIRED=0

#========================================================================================================
# Routines
#--------------------------------------------------------------------------------------------------------

DEBUG=0
#========================================================================================
# Mounts section
#----------------------------------------------------------------------------------------
#Only do something if variable is changed
[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] ORIG_MOUNTPOINT is: '$ORIG_MOUNTPOINT'</p>'
[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] MOUNTPOINT is: '$MOUNTPOINT'</p>'
[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] ORIG_MOUNTUUID is: '$ORIG_MOUNTUUID'</p>'
[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] MOUNTUUID is: '$MOUNTUUID'</p>'

if [ "$ORIG_MOUNTPOINT" = "$MOUNTPOINT" -a "$ORIG_MOUNTUUID" = "$MOUNTUUID" ]; then
	echo '<p class="info">[ INFO ] Mount Options Unchanged.</p>'
else
	echo '<p class="info">[ INFO ] Mount Point is set to: '$MOUNTPOINT'</p>'
	echo '<p class="info">[ INFO ] Mount UUID is set to: '$MOUNTUUID'</p>'

	if [ -d /mnt/$ORIG_MOUNTPOINT ]; then
		echo '<p class="info">[ INFO ] Checking if Disk was Mounted.</p>'
		mount | grep -q /mnt/$ORIG_MOUNTPOINT
		[ $? = 0 ] && umount /mnt/$ORIG_MOUNTPOINT || echo '<p class="info">[ INFO ] Old Mount Mount was not Mounted.</p>'
		[ $? = 0 ] && echo '<p class="info">[ INFO ] Disk Unmounted.</p>' || (echo '<p class="error">[ERROR] Disk Busy, Reboot will be required.</p>'; REBOOT_REQUIRED=1)
	fi
	if [ -d /mnt/$MOUNTPOINT ]; then
		echo '<p class="info">[ INFO ] Checking new Mount Point.</p>'
		mount | grep -q /mnt/$MOUNTPOINT
		[ $? = 0 ] && umount /mnt/$MOUNTPOINT || echo '<p class="info">[ INFO ] New Mount Mount was not Mounted.</p>'
		[ $? = 0 ] && echo '<p class="info">[ INFO ] Disk Unmounted.</p>' || (echo '<p class="error">[ERROR] New MountPoint in Use, Reboot will be required/</p>'; REBOOT_REQUIRED=1)
	fi
	if [ $MOUNTUUID != "no" ]; then
		echo '<p class="info">[ INFO ] Mounting Disk.</p>'
		[ ! -d /mnt/$MOUNTPOINT ] && mkdir -p /mnt/$MOUNTPOINT
		mount --uuid $MOUNTUUID /mnt/$MOUNTPOINT
		[ $? = 0 ] && echo '<p class="info">[ INFO ] Disk Mounted.</p>' || (echo '<p class="error">[ERROR] Disk Mount Error, Try to Reboot.</p>'; REBOOT_REQUIRED=1)
	fi

	pcp_save_to_config
	pcp_backup
fi

echo '<hr>'

[ $DEBUG = 1 ] && pcp_textarea "Current $CONFIGCFG" "cat $CONFIGCFG" 150

[ $REBOOT_REQUIRED = 1 ] && pcp_reboot_required

pcp_go_back_button

echo '</body>'
echo '</html>'