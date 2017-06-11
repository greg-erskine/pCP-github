#!/bin/sh

# Version: 3.21 2017-06-10
#	Changed vfat mounts.  PH.
#	Fixed util-linux button download function. PH
#	Changed to allow booting from USB on RPI3. PH.
#	Support multiple USB mounts. PH

# Version: 3.20 2017-03-31
#	Revisions to pcp_lms_set_slimconfig function. PH.
#	Fixed pcp-xxx-functions issues. GE.
#	Updates for vfat mount permissions. PH

# Version: 3.10 2017-01-06
#	Added support for GPT disks. PH.

# Version: 2.06 2016-06-04 PH
#	Made CIFS User and Password Optional
#	Error trap on setting LMS Cache to a fat based device.

# Version: 0.01 2016-04-14 PH
#	Original version.

. pcp-functions
. pcp-lms-functions

# Store the original values so we can see if they are changed
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
REBOOT_REQUIRED="0"

#========================================================================================================
# Routines
#--------------------------------------------------------------------------------------------------------

pcp_move_LMS_cache() {
	sudo cp -avr $1 $2 >/dev/null 2>&1
	[ "$?" = "0" ] && sudo rm -rf $1 || echo '<p class="error">[ ERROR ] File Copy Error.</p>'

	#Remove old Symlinks to the data location.  Will be recreated when LMS is started.
	sudo rm -f /usr/local/slimserver/Cache
	sudo rm -f /usr/local/slimserver/prefs
	sync
}

pcp_do_umount () {
	if [ -d $1 ]; then
		df | grep -qws $1
		if [ "$?" = "0" ]; then
			umount $1
			if [ "$?" = "0" ]; then
				echo '<p class="info">[ INFO ] Mount '$1' Unmounted.</p>' 
			else
				echo '<p class="error">[ERROR] Mount point '$1' is Busy, Reboot will be required.</p>'
				echo '<p class="error">[ERROR] Diskmount Options Saved Reboot to Mount.</p>'
				REBOOT_REQUIRED="1"
			fi
		else
			echo '<p class="info">[ INFO ] New Mount Point '$1' is not in use.</p>' 
		fi
	fi
}

#========================================================================================
# Mounts section
#----------------------------------------------------------------------------------------
#Only do something if variable is changed
pcp_table_top "Write to mount"
[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] MOUNTTYPE is: '$MOUNTTYPE'</p>'

if [ "${ACTION}" = "gptfdisk" ]; then 
	MOUNTTYPE="skip"
	EXTN="util-linux.tcz"
	if [ -f $PACKAGEDIR/$EXTN ]; then
		pcp_textarea_inform "none" "sudo -u tc pcp-load -i $EXTN" 50
		echo $EXTN >> $ONBOOTLST
	else
		pcp_textarea_inform "none" "sudo -u tc pcp-load -wi $EXTN" 50
	fi
fi

case "$MOUNTTYPE" in
	localdisk)
		#	READ Conf file
		if [ -f  ${USBMOUNTCONF} ]; then
			SC=0
			while read LINE; do
				case $LINE in
					[*)SC=$((SC+1));;
					*USBDISK*) eval ORIG_USBDISK${SC}=$(pcp_trimval "${LINE}");;
					*POINT*) eval ORIG_MOUNTPOINT${SC}=$(pcp_trimval "${LINE}");;
					*UUID*) eval ORIG_MOUNTUUID${SC}=$(pcp_trimval "${LINE}");;
					*);;
				esac
			done < $USBMOUNTCONF
		fi
		
		# Match ORIG values from config to current set passed on HTML
		MNTCHANGED=0
		I=1
		while [ $I -le $NUMDRIVES ]; do
			eval MNTCHANGED${I}=0
			THISUU=$(eval echo "\${MOUNTUUID${I}}")
			THISPNT=$(eval echo "\${MOUNTPOINT${I}}")
			THISENA=$(eval echo "\${USBDISK${I}}")
			J=1
			FOUND=0
			while [ $J -le $SC ]; do
				[ "$DEBUG" = "1" ] && echo '<p class="debug">[ DEBUG ] I,J ='$I','$J'</p>'
				ORIGUU=$(eval echo "\${ORIG_MOUNTUUID${J}}")
				ORIGPNT=$(eval echo "\${ORIG_MOUNTPOINT${J}}")
				ORIGENA=$(eval echo "\${ORIG_USBDISK${J}}")
				if [ "$THISUU" = "$ORIGUU" ]; then
					FOUND=1
					[ "$DEBUG" = "1" ] && echo '<p class="debug">[ DEBUG ] ORIG UU is: '$ORIGUU'</p>'
					[ "$DEBUG" = "1" ] && echo '<p class="debug">[ DEBUG ] This UU is: '$THISUU'</p>'
					[ "$DEBUG" = "1" ] && echo '<p class="debug">[ DEBUG ] ORIG_USBDISK is: '$ORIGENA'</p>'
					[ "$DEBUG" = "1" ] && echo '<p class="debug">[ DEBUG ] This USBDISK is: '$THISENA'</p>'
					[ "$DEBUG" = "1" ] && echo '<p class="debug">[ DEBUG ] ORIG_MOUNTPOINT is: '$ORIGPNT'</p>'
					[ "$DEBUG" = "1" ] && echo '<p class="debug">[ DEBUG ] This MOUNTPOINT is: '$THISPNT'</p>'
					if [ "$THISPNT" != "$ORIGPNT" -o "$THISENA" != "$ORIGENA" ]; then
						MNTCHANGED=1
						eval MNTCHANGED${I}=1
						eval OLDMOUNTPOINT${I}=$ORIGPNT
						eval OLDUSBDISK${I}=$ORIGENA
					fi
					J=$SC
				fi
				J=$((J+1))
			done
			[ $FOUND -eq 0 -a "$THISENA" != "" ] && eval MNTCHANGED${I}=1
			I=$((I+1))
		done
		I=1
		while [ $I -le $NUMDRIVES ]; do
			NEWUU=$(eval echo "\${MOUNTUUID${I}}")
			NEWENA=$(eval echo "\${USBDISK${I}}")
			NEWPNT=$(eval echo "\${MOUNTPOINT${I}}")
			OLDENA=$(eval echo "\${OLDUSBDISK${I}}")
			OLDPNT=$(eval echo "\${OLDMOUNTPOINT${I}}")
			CHANGED=$(eval echo "\${MNTCHANGED${I}}")
			[ "$DEBUG" = "1" ] && echo '<p class="debug">[ DEBUG ] MOUNTUUID'${I}' is: '$NEWUU'</p>'
			[ "$DEBUG" = "1" ] && echo '<p class="debug">[ DEBUG ] ORIG_USBDISK'${I}' is: '$OLDENA'</p>'
			[ "$DEBUG" = "1" ] && echo '<p class="debug">[ DEBUG ] USBDISK'${I}' is: '$NEWENA'</p>'
			[ "$DEBUG" = "1" ] && echo '<p class="debug">[ DEBUG ] ORIG_MOUNTPOINT'${I}' is: '$OLDPNT'</p>'
			[ "$DEBUG" = "1" ] && echo '<p class="debug">[ DEBUG ] MOUNTPOINT'${I}' is: '$NEWPNT'</p>'
			[ "$DEBUG" = "1" ] && echo '<p class="debug">[ DEBUG ] MOUNT CHANGED'${I}'='$CHANGED'</p>'
			if [ $CHANGED -eq 0 ]; then
				echo '<p class="info">[ INFO ] Mount Options Unchanged for Disk '$NEWUU'.</p>'
			else
				MNTCHANGED=1
				echo '<p class="info">[ INFO ] Mount options have changed for Disk '$NEWUU'.</p>'
				echo '<p class="info">[ INFO ] Mount Point is set to: '$NEWPNT'</p>'
				if [ "$OLDPNT" != "" ]; then
					echo '<p class="info">[ INFO ] Unmounting Old Mount Point: /mnt/'$OLDPNT'.</p>'
					pcp_do_umount /mnt/$OLDPNT
				fi
				if [ $CHANGED -eq 1 -a "$REBOOT_REQUIRED" = "0" ]; then
					if [ "$NEWENA" != "" ]; then
						echo '<p class="info">[ INFO ] Checking new Mount Point.</p>'
						pcp_do_umount /mnt/$NEWPNT 
						if [ "$REBOOT_REQUIRED" = "0" ]; then
							[ ! -d /mnt/$NEWPNT ] && mkdir -p /mnt/$NEWPNT
							DEVICE=$(blkid -U $NEWUU)
							FSTYPE=$(blkid -U $NEWUU | xargs -I {} blkid {} -s TYPE | awk -F"TYPE=" '{print $NF}' | tr -d "\"")
							case "$FSTYPE" in
								ntfs) 
									echo '<p class="info">[ INFO ] Checking to make sure NTFS is not mounted.</p>'
									umount $DEVICE
									OPTIONS="-v -t ntfs-3g -o permissions"
								;;
								vfat|fat32)
									#if Filesystem support installed, use utf-8 charset for fat.
									df | grep -qs ntfs
									[ "$?" = "0" ] && CHARSET=",iocharset=utf8" || CHARSET=""
									umount $DEVICE  # need to unmount vfat incase 1st mount is not utf8
									OPTIONS="-v -t vfat -o noauto,users,exec,umask=000,flush${CHARSET}"
								;;
								*)
									OPTIONS="-v"
								;;
							esac
							echo '<p class="info">[ INFO ] Mounting Disk.</p>'
							[ "$DEBUG" = "1" ] && echo '<p class="debug">[ DEBUG ] Mount Line is: mount '$OPTIONS' --uuid '$NEWUU' /mnt/'$NEWPNT'</p>'
							echo '<p class="info">[ INFO ] '
							mount $OPTIONS --uuid $NEWUU /mnt/$NEWPNT
							if [ $? -eq 0 ]; then
								echo '</p><p class="info">[ INFO ] Disk Mounted Successfully.</p>'
							else
								echo '</p><p class="error">[ERROR] Disk Mount Error, Try to Reboot.</p>'
								REBOOT_REQUIRED="1"
							fi
						fi
					fi
				fi
			fi
			I=$((I+1))
		done
		
		if [ $MNTCHANGED -eq 1 ]; then
			rm -f $USBMOUNTCONF
			I=1
			while [ $I -le $NUMDRIVES ]
			do
				if [ $(eval echo \${MOUNTUUID${I}}) != "" ]; then
					echo "[$I]" >> $USBMOUNTCONF
					eval echo "USBDISK=\${USBDISK${I}}" >> $USBMOUNTCONF
					eval echo "MOUNTPOINT=\${MOUNTPOINT${I}}" >> $USBMOUNTCONF
					eval echo "MOUNTUUID=\${MOUNTUUID${I}}" >> $USBMOUNTCONF
				fi
				I=$((I+1))
			done
			pcp_backup
		fi
	;;
	networkshare)
		[ "$DEBUG" = "1" ] && echo '<p class="debug">[ DEBUG ] ORIG_NETMOUNT1 is: '$ORIG_NETMOUNT1'</p>'
		[ "$DEBUG" = "1" ] && echo '<p class="debug">[ DEBUG ] NETMOUNT1 is: '$NETMOUNT1'</p>'
		[ "$DEBUG" = "1" ] && echo '<p class="debug">[ DEBUG ] ORIG_NETMOUNT1 is: '$ORIG_NETMOUNT1POINT'</p>'
		[ "$DEBUG" = "1" ] && echo '<p class="debug">[ DEBUG ] NETMOUNT1 is: '$NETMOUNT1POINT'</p>'

		ORIG_CHECK="${ORIG_NETMOUNT1POINT}${ORIG_NETMOUNT1}${ORIG_NETMOUNT1IP}${ORIG_NETMOUNT1SHARE}${ORIG_NETMOUNT1FSTYPE}${ORIG_NETMOUNT1USER}${ORIG_NETMOUNT1PASS}${ORIG_NETMOUNT1OPTIONS}"
		CHECK="${NETMOUNT1POINT}${NETMOUNT1}${NETMOUNT1IP}${NETMOUNT1SHARE}${NETMOUNT1FSTYPE}${NETMOUNT1USER}${NETMOUNT1PASS}${NETMOUNT1OPTIONS}"

		if [ "$ORIG_CHECK" = "$CHECK" ]; then
			echo '<p class="info">[ INFO ] Mount configuration unchanged.</p>'
		else
			echo '<p class="info">[ INFO ] Checking Old Mount Point.</p>'
			pcp_do_umount /mnt/$ORIG_NETMOUNT1POINT
			if [ "$NETMOUNT1" != "no" -a "$REBOOT_REQUIRED" = "0" ]; then
				echo '<p class="info">[ INFO ] Checking new Mount Point.</p>'
				pcp_do_umount /mnt/$NETMOUNT1POINT 

				if [ "$REBOOT_REQUIRED" = "0" ]; then
					echo '<p class="info">[ INFO ] Mounting Disk.</p>'
					[ ! -d /mnt/$NETMOUNT1POINT ] && mkdir -p /mnt/$NETMOUNT1POINT
					case "$NETMOUNT1FSTYPE" in
						cifs)
							OPTIONS=""
							[ "$NETMOUNT1USER" != "" ] && OPTIONS="${OPTIONS}username=${NETMOUNT1USER},"
							[ "$NETMOUNT1PASS" != "" ] && OPTIONS="${OPTIONS}password=${NETMOUNT1PASS},"
							OPTIONS="${OPTIONS}${NETMOUNT1OPTIONS}"
							MNTCMD="-v -t $NETMOUNT1FSTYPE -o $OPTIONS //$NETMOUNT1IP/$NETMOUNT1SHARE /mnt/$NETMOUNT1POINT"
						;;
						nfs)
							OPTIONS="addr=${NETMOUNT1IP},nolock,${NETMOUNT1OPTIONS}"
							MNTCMD="-v -t $NETMOUNT1FSTYPE -o $OPTIONS $NETMOUNT1IP:$NETMOUNT1SHARE /mnt/$NETMOUNT1POINT"
						;;
					esac
					echo '<p class="info">[INFO] mount '$MNTCMD'</p>'
					mount $MNTCMD
					if [ $? -eq 0 ]; then
						echo '<p class="info">[ INFO ] Disk Mounted Successfully.</p>'
					else
						echo '<p class="error">[ERROR] Disk Mount Error, Try to Reboot.</p>'
						REBOOT_REQUIRED="1"
					fi
				fi
			fi
			pcp_save_to_config
			pcp_backup
		fi
	;;
	slimconfig)
		[ "$DEBUG" = "1" ] && echo '<p class="debug">[ DEBUG ] ORIG_LMSDATA is: '$ORIG_LMSDATA'</p>'
		[ "$DEBUG" = "1" ] && echo '<p class="debug">[ DEBUG ] LMSDATA is: '$LMSDATA'</p>'

		if [ "$ORIG_LMSDATA" = "$LMSDATA" ]; then
			echo '<p class="info">[ INFO ] LMS Data directory Unchanged.</p>'
		else
			case "$ORIG_LMSDATA" in
				usb:*) DEV=$(blkid | grep ${ORIG_LMSDATA:5} | cut -d ':' -f1)
					TMP=$(mount | grep -w $DEV | cut -d ' ' -f3)
					ORIG_MNT="$TMP/slimserver"
				;;
				netmount1) ORIG_MNT="/mnt/$NETMOUNT1POINT/slimserver";;
				default) ORIG_MNT="$TCEMNT/tce/slimserver";;
			esac
			BADFORMAT="no"
			case "$LMSDATA" in
				usb:*) DEV=$(blkid | grep ${LMSDATA:4} | cut -d ':' -f1)
					TMP=$(mount | grep -w $DEV | cut -d ' ' -f3)
					MNT="$TMP/slimserver"
					FSTYPE=$(blkid -U $MOUNTUUID | xargs -I {} blkid {} -s TYPE | awk -F"TYPE=" '{print $NF}' | tr -d "\"")
					case $FSTYPE in
						msdos|fat|vfat|fat32)BADFORMAT="yes";;
						*)BADFORMAT="no";;
					esac
					;;
				netmount1)
					MNT="/mnt/$NETMOUNT1POINT/slimserver"
					FSTYPE=$NETMOUNT1FSTYPE
					case "$FSTYPE" in
						cifs)echo '<p class="warn">[ WARN ] CIFS partitions may not work with LMS Cache.</p>';;
						*);;
					esac
					;;
				default) MNT="$TCEMNT/tce/slimserver";;
			esac

			if [ "$BADFORMAT" = "no" ]; then
				echo '<p class="info">[ INFO ] Setting LMS Data Directory to '$MNT'.</p>'
				pcp_lms_set_slimconfig CACHE $MNT
				pcp_save_to_config
				pcp_backup
				echo ''

				if [ "$ACTION" = "Move" ]; then
					#========================================================================================
					# Move LMS cache and prefs section
					#----------------------------------------------------------------------------------------
					WASRUNNING="0"
					if [ "$(pcp_lms_status)" = "0" ]; then
						WASRUNNING="1"
						echo '<p class="info">[ INFO ] Stopping LMS</p>'
						/usr/local/etc/init.d/slimserver stop
					fi
					if [ -d $ORIG_MNT ]; then
						echo '<p class="info">[ INFO ] Moving Data from '$ORIG_MNT' to '$MNT'</p>'
						pcp_move_LMS_cache $ORIG_MNT $MNT
					fi
					[ "$WASRUNNING" = "1" ] && (echo '<p class="info">[ INFO ] Starting LMS</p>';/usr/local/etc/init.d/slimserver start)
				fi
			else
				echo '<p class="error">[ERROR] Unsupported partition type detected ('$FSTYPE'), please use a ntfs or linux partition type for Cache storate. (i.e. ext4)</p>'
			fi
		fi
	;;
	skip)
	;;
	*)
		echo '<p class="error">[ERROR] Web Page Error, No MountType Submitted</p>'
	;;
esac

echo '<hr>'

[ "$DEBUG" = "1" ] && pcp_textarea "Current $USBMOUNTCONF" "cat $USBMOUNTCONF" 150
[ "$DEBUG" = "1" ] && pcp_textarea "Current $CONFIGCFG" "cat $CONFIGCFG" 150

[ "$REBOOT_REQUIRED" = "1" ] && pcp_reboot_required

pcp_table_middle
pcp_go_back_button
pcp_table_end
pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'
