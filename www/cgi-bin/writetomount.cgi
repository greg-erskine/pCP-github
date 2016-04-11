#!/bin/sh

# Version: 0.01 2016-04-05 PH
#	Original version.

. pcp-functions
. pcp-lms-functions
pcp_variables

# Store the original values so we can see if they are changed
ORIG_MOUNTPOINT="$MOUNTPOINT"
ORIG_MOUNTUUID="$MOUNTUUID"
ORIG_NETMOUNT1POINT="$NETMOUNT1POINT"
ORIG_NETMOUNT1="$NETMOUNT1"
ORIG_NETMOUNT1IP="$NETMOUNT1IP"
ORIG_NETMOUNT1SHARE="$NETMOUNT1SHARE"
ORIG_NETMOUNT1FSTYPE="$NETMOUNT1FSTYPE"
ORIG_NETMOUNT1USER="$NETMOUNT1USER"
ORIG_NETMOUNT1PASS="$NETMOUNT1PASS"
ORIG_NETMOUNT1OPTIONS="$NETMOUNT1OPTIONS"
ORIG_LMSDATA="$LMSDATA"

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

pcp_set_slimconfig(){
	CFG="/home/tc/.slimserver.cfg"
	rm -rf $CFG
	echo "CACHE=$1/Cache" >> $CFG
	echo "PREFS=$1/prefs" >> $CFG
}

pcp_move_LMS_cache() {
	sudo cp -avr $1 $2 >/dev/null 2>&1

	[ $? = 0 ] && sudo rm -rf $1 || echo '<p class="error">[ ERROR ] File Copy Error.</p>'
	
	#Remove old Symlinks to the data location.  Will be recreated when LMS is started.
	sudo rm -f /usr/local/slimserver/Cache
	sudo rm -f /usr/local/slimserver/prefs
	sync
}


DEBUG=0
#========================================================================================
# Mounts section
#----------------------------------------------------------------------------------------
#Only do something if variable is changed

[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] ORIG_MOUNTPOINT is: '$ORIG_MOUNTPOINT'</p>'
[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] MOUNTPOINT is: '$MOUNTPOINT'</p>'
[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] ORIG_MOUNTUUID is: '$ORIG_MOUNTUUID'</p>'
[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] MOUNTUUID is: '$MOUNTUUID'</p>'

[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] MOUNTTYPE is: '$MOUNTTYPE'</p>'


case "$MOUNTTYPE" in
	localdisk)
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
	;;
	networkshare)
		[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] ORIG_NETMOUNT1 is: '$ORIG_NETMOUNT1'</p>'
		[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] NETMOUNT1 is: '$NETMOUNT1'</p>'

		if [ "$ORIG_NETMOUNT1" = "$NETMOUNT1" ]; then
			echo '<p class="info">[ INFO ] Mount Enabled Unchanged.</p>'
		else
			echo '<p class="info">[ INFO ] Mount Enabled Mounting.</p>'
			if [ "$NETMOUNT1" = "no" ]; then
				umount /mnt/$NETMOUNT1POINT
			else
				[ ! -d /mnt/$NETMOUNT1POINT ] && mkdir -p /mnt/$NETMOUNT1POINT
				echo '<p class="info">[INFO] mount -t '$NETMOUNT1FSTYPE' -o username='$NETMOUNT1USER',password='$NETMOUNT1PASS','$NETMOUNT1OPTIONS' //'$NETMOUNT1IP'/'$NETMOUNT1SHARE' /mnt/'$NETMOUNT1POINT'</p>'
				mount -v -t $NETMOUNT1FSTYPE -o username=$NETMOUNT1USER,password=$NETMOUNT1PASS,$NETMOUNT1OPTIONS //$NETMOUNT1IP/$NETMOUNT1SHARE /mnt/$NETMOUNT1POINT
			fi
			pcp_save_to_config
			pcp_backup
		fi
	;;
	slimconfig)
		[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] ORIG_LMSDATA is: '$ORIG_LMSDATA'</p>'
		[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] LMSDATA is: '$LMSDATA'</p>'
		
		if [ "$ORIG_LMSDATA" = "$LMSDATA" ]; then
			echo '<p class="info">[ INFO ] LMS Data directory Unchanged.</p>'
		else
			case "$ORIG_LMSDATA" in
				usbmount) ORIG_MNT="/mnt/$MOUNTPOINT/slimserver";;
				netmount1) ORIG_MNT="/mnt/$NETMOUNT1POINT/slimserver";;
				default) ORIG_MNT="/mnt/mmcblk0p2/tce/slimserver";;
			esac
			case "$LMSDATA" in
				usbmount) MNT="/mnt/$MOUNTPOINT/slimserver";;
				netmount1) MNT="/mnt/$NETMOUNT1POINT/slimserver";;
				default) MNT="/mnt/mmcblk0p2/tce/slimserver";;
			esac
			echo '<p class="info">[ INFO ] Setting LMS Data Directory to '$MNT'.</p>'
			pcp_set_slimconfig $MNT
			pcp_save_to_config
			pcp_backup
			echo ''
			
			#========================================================================================
			# Move LMS cache and prefs section
			#----------------------------------------------------------------------------------------
			WASRUNNING=0
			if [ $(pcp_lms_status) = 0 ]; then
				WASRUNNING=1
				echo '<p class="info">[ INFO ] Stopping LMS</p>'
				/usr/local/etc/init.d/slimserver stop
			fi
			if [ -d $ORIG_MNT ]; then
				echo '<p class="info">[ INFO ] Moving Data from '$ORIG_MNT' to '$MNT'</p>'
				pcp_move_LMS_cache $ORIG_MNT $MNT
			fi
			[ $WASRUNNING = 1 ] && (echo '<p class="info">[ INFO ] Starting LMS</p>';/usr/local/etc/init.d/slimserver start)
		fi	
	;;
	*)
		echo '<p class="error">[ERROR] No MountType Submitted</p>'
	;;
esac

echo '<hr>'

[ $DEBUG = 1 ] && pcp_textarea "Current $CONFIGCFG" "cat $CONFIGCFG" 150

[ $REBOOT_REQUIRED = 1 ] && pcp_reboot_required

pcp_go_back_button

echo '</body>'
echo '</html>'