#!/bin/sh

# Version: 4.0.0 2018-04-17
#	fuse.ko does not load automatically for exfat mounts. PH.

# Version: 3.5.0 2017-12-27
#	Load arc4 if doing a network mount, as it does not automatically load. PH.

# Version: 3.22 2017-09-10
#	Changed Netmounts to support shares with spaces. PH.
#	Added checkbox to clear unused netmount conf entries. PH.
#	Added exFat support. PH.

# Version: 3.21 2017-06-18
#	Changed vfat mounts.  PH.
#	Fixed util-linux button download function. PH.
#	Changed to allow booting from USB on RPI3. PH.
#	Support multiple USB mounts. PH.
#	Support multiple Network mounts. PH.

# Version: 3.20 2017-03-31
#	Revisions to pcp_lms_set_slimconfig function. PH.
#	Fixed pcp-xxx-functions issues. GE.
#	Updates for vfat mount permissions. PH.

# Version: 3.10 2017-01-06
#	Added support for GPT disks. PH.

# Version: 0.01 2016-04-14
#	Original version. PH.

. pcp-functions
. pcp-lms-functions

# Store the original values so we can see if they are changed
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

pcp_move_LMS_cache() {
	DEST=$(echo "$2" | sed 's/slimserver//')
	sudo cp -avr $1 $DEST >/dev/null 2>&1
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
				[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] I,J ='$I','$J'</p>'
				ORIGUU=$(eval echo "\${ORIG_MOUNTUUID${J}}")
				ORIGPNT=$(eval echo "\${ORIG_MOUNTPOINT${J}}")
				ORIGENA=$(eval echo "\${ORIG_USBDISK${J}}")
				if [ "$THISUU" = "$ORIGUU" ]; then
					FOUND=1
					[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] ORIG UU is: '$ORIGUU'</p>'
					[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] This UU is: '$THISUU'</p>'
					[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] ORIG_USBDISK is: '$ORIGENA'</p>'
					[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] This USBDISK is: '$THISENA'</p>'
					[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] ORIG_MOUNTPOINT is: '$ORIGPNT'</p>'
					[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] This MOUNTPOINT is: '$THISPNT'</p>'
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
			[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] MOUNTUUID'${I}' is: '$NEWUU'</p>'
			[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] ORIG_USBDISK'${I}' is: '$OLDENA'</p>'
			[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] USBDISK'${I}' is: '$NEWENA'</p>'
			[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] ORIG_MOUNTPOINT'${I}' is: '$OLDPNT'</p>'
			[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] MOUNTPOINT'${I}' is: '$NEWPNT'</p>'
			[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] MOUNT CHANGED'${I}'='$CHANGED'</p>'
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
								exfat)
									CHARSET=",iocharset=utf8"
									umount $DEVICE  # need to unmount incase 1st mount is not utf8
									OPTIONS="-v -o noauto,users,exec,umask=000,flush,uid=1001,gid=50${CHARSET}"
								;;
								*)
									OPTIONS="-v"
								;;
							esac
							echo '<p class="info">[ INFO ] Mounting Disk.</p>'
							case "$FSTYPE" in
								exfat) [ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] Mount Line is: mount.exfat '$OPTIONS' '$DEVICE' /mnt/'$NEWPNT'</p>'
									echo '<p class="info">[ INFO ] '
									modprobe fuse
									mount.exfat $OPTIONS $DEVICE /mnt/$NEWPNT
								;;
								*) [ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] Mount Line is: mount '$OPTIONS' --uuid '$NEWUU' /mnt/'$NEWPNT'</p>'
									echo '<p class="info">[ INFO ] '
									mount $OPTIONS --uuid $NEWUU /mnt/$NEWPNT
								;;
							esac
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
		NETMNTCHANGED=0
		NN=0
		#cifs does not automatically load arc4, which is in the dependancies needed for SMB3 to work
		modprobe arc4
		# Process the $QUERY_STRING Not decoding NETMOUNTSHAREs
		eval $(echo "$QUERY_STRING" | awk -F'&' '{ for(i=1;i<=NF;i++) { if ($i ~ /^NETMOUNTSHARE/) printf "%s\"\n",$i} }' | sed 's/=/="/')
		if [ -f  ${NETMOUNTCONF} ]; then
			while read LINE; do
				case $LINE in
					[*) NN=$((NN+1));;
					*NETENABLE*) TST=$(pcp_trimval "${LINE}"); [ "$TST" = "no" ] && TST=""; eval ORIG_NETENABLE${NN}="$TST";;
					*MOUNTPOINT*) eval ORIG_NETMOUNTPOINT${NN}=$(pcp_trimval "${LINE}");;
					*MOUNTIP*) eval ORIG_NETMOUNTIP${NN}=$(pcp_trimval "${LINE}");;
					*MOUNTSHARE*) eval ORIG_NETMOUNTSHARE${NN}=$(pcp_trimval "${LINE}");;
					*FSTYPE*) eval ORIG_NETMOUNTFSTYPE${NN}=$(pcp_trimval "${LINE}");;
					*PASS*) eval ORIG_NETMOUNTPASS${NN}=$(pcp_trimval "${LINE}");;
					*USER*) eval ORIG_NETMOUNTUSER${NN}=$(pcp_trimval "${LINE}");;
					*MOUNTOPTIONS*) eval ORIG_NETMOUNTOPTIONS${NN}=$(echo "${LINE}" | awk -F= '{ st = index($0,"=");print substr($0,st+1)}');;
					*);;
				esac
			done < $NETMOUNTCONF
		fi

		I=1
		while [ $I -le $NUMNET ]; do
			ENABLE=$(eval echo \${NETENABLE${I}})
			PNT=$(eval echo \${NETMOUNTPOINT${I}})
			IP=$(eval echo \${NETMOUNTIP${I}})
			SHARE=$(eval echo \${NETMOUNTSHARE${I}})
			FSTYPE=$(eval echo \${NETMOUNTFSTYPE${I}})
			USER=$(eval echo \${NETMOUNTUSER${I}})
			PASS=$(eval echo \${NETMOUNTPASS${I}})
			OPTIONS=$(eval echo \${NETMOUNTOPTIONS${I}})

			OLDENABLE=$(eval echo \${ORIG_NETENABLE${I}})
			OLDPNT=$(eval echo \${ORIG_NETMOUNTPOINT${I}})
			OLDIP=$(eval echo \${ORIG_NETMOUNTIP${I}})
			OLDSHARE=$(eval echo \${ORIG_NETMOUNTSHARE${I}})
			OLDFSTYPE=$(eval echo \${ORIG_NETMOUNTFSTYPE${I}})
			OLDUSER=$(eval echo \${ORIG_NETMOUNTUSER${I}})
			OLDPASS=$(eval echo \${ORIG_NETMOUNTPASS${I}})
			OLDOPTIONS=$(eval echo \${ORIG_NETMOUNTOPTIONS${I}})

			ORIG_CHECK="${OLDENABLE}${OLDPNT}${OLDIP}${OLDSHARE}${OLDFSTYPE}${OLDUSER}${OLDPASS}${OLDOPTIONS}"
			CHECK="${ENABLE}${PNT}${IP}${SHARE}${FSTYPE}${USER}${PASS}${OPTIONS}"
			[ "$CHECK" = "nfs" -o "$CHECK" = "cifs" ] && CHECK=""
			[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] CHECK is: '$CHECK'</p>'
			[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] ORIG_CHECK is: '$ORIG_CHECK'</p>'
			[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] NETENABLE'${I}' is: '$ENABLE'</p>'
			[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] ORIG_NETENABLE'${I}' is: '$OLDENABLE'</p>'
			[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] NETMOUNTPOINT'${I}' is: '$PNT'</p>'
			[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] ORIG_NETMOUNTPOINT'${I}' is: '$OLDPNT'</p>'
			[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] NETMOUNTIP'${I}' is: '$IP'</p>'
			[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] ORIG_NETMOUNTIP'${I}' is: '$OLDIP'</p>'
			[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] NETMOUNTSHARE'${I}' is: '$SHARE'</p>'
			[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] ORIG_NETMOUNTSHARE'${I}' is: '$OLDSHARE'</p>'
			[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] NETMOUNTFSTYPE'${I}' is: '$FSTYPE'</p>'
			[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] ORIG_NETMOUNTFSTYPE'${I}' is: '$OLDFSTYPE'</p>'
			[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] NETMOUNTUSER'${I}' is: '$USER'</p>'
			[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] ORIG_NETMOUNTUSER'${I}' is: '$OLDUSER'</p>'
			[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] NETMOUNTPASS'${I}' is: '$PASS'</p>'
			[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] ORIG_NETMOUNTPASS'${I}' is: '$OLDPASS'</p>'
			[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] NETMOUNTOPTIONS'${I}' is: '$OPTIONS'</p>'
			[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] ORIG_NETMOUNTOPTIONS'${I}' is: '$OLDOPTIONS'</p>'
			if [ "$ORIG_CHECK" = "$CHECK" ]; then
				[ "$CHECK" != "" ] && echo '<p class="info">[ INFO ] Mount configuration unchanged for '$IP':/'$SHARE'</p>'
			else
				NETMNTCHANGED=1
				echo '<p class="info">[ INFO ] Mount configuration changed for '$IP':/'$SHARE'</p>'
				if [ "$OLDPNT" != "" ]; then
					echo '<p class="info">[ INFO ] Unmounting Old Mount Point: /mnt/'$OLDPNT'.</p>'
					pcp_do_umount /mnt/$OLDPNT
				fi
				if [ "$ENABLE" != "" -a "$REBOOT_REQUIRED" = "0" ]; then
					echo '<p class="info">[ INFO ] Checking new Mount Point /mnt/'$PNT'.</p>'
					pcp_do_umount /mnt/$PNT
					echo '<p class="info">[ INFO ] Mounting Disk.</p>'
					[ ! -d /mnt/$PNT ] && mkdir -p /mnt/$PNT
					case "$FSTYPE" in
						cifs)
							OPTS=""
							[ "$USER" != "" ] && OPTS="${OPTS}username=${USER},"
							[ "$PASS" != "" ] && OPTS="${OPTS}password=${PASS},"
							OPTS="${OPTS}${OPTIONS}"
							MNTCMD="-v -t $FSTYPE -o $OPTS //$IP/\"$(${HTTPD} -f -d $SHARE)\" /mnt/$PNT"
						;;
						nfs)
							OPTS="addr=${IP},nolock,${OPTIONS}"
							MNTCMD="-v -t $FSTYPE -o $OPTS $IP:\"$(${HTTPD} -f -d $SHARE)\" /mnt/$PNT"
						;;
					esac
					echo '<p class="info">[INFO] mount '$MNTCMD'</p>'
					/bin/sh -c "mount ${MNTCMD}"
					if [ $? -eq 0 ]; then
						echo '<p class="info">[ INFO ] Disk Mounted Successfully.</p>'
					else
						echo '<p class="error">[ERROR] Disk Mount Error, Try to Reboot.</p>'
						REBOOT_REQUIRED="1"
					fi
				fi
			fi
			I=$((I+1))
		done

		if [ $NETMNTCHANGED -eq 1 -o "$CLEARUNUSED" = "yes" ]; then
			rm -f $NETMOUNTCONF
			I=1
			J=1
			while [ $I -le $NUMNET ]; do
				if [ "$(eval echo \${NETMOUNTPOINT${I}})" != "" ]; then
					ENABLE=$(eval echo \${NETENABLE${I}})
					if [ "$ENABLE" = "" -a "$CLEARUNUSED" = "yes" ]; then
						J=$((J-1)) #Decrement the Counter written to the conf file
					else
						[ "$ENABLE" = "" ] && ENABLE="no"
						echo "[$J]" >> $NETMOUNTCONF
						echo "NETENABLE=$ENABLE" >> $NETMOUNTCONF
						eval echo "NETMOUNTPOINT=\${NETMOUNTPOINT${I}}" >> $NETMOUNTCONF
						eval echo "NETMOUNTIP=\${NETMOUNTIP${I}}" >> $NETMOUNTCONF
						eval echo "NETMOUNTSHARE=\${NETMOUNTSHARE${I}}" >> $NETMOUNTCONF
						eval echo "NETMOUNTFSTYPE=\${NETMOUNTFSTYPE${I}}" >> $NETMOUNTCONF
						eval echo "NETMOUNTUSER=\${NETMOUNTUSER${I}}" >> $NETMOUNTCONF
						eval echo "NETMOUNTPASS=\${NETMOUNTPASS${I}}" >> $NETMOUNTCONF
						eval echo "NETMOUNTOPTIONS=\${NETMOUNTOPTIONS${I}}" >> $NETMOUNTCONF
					fi
				fi
				I=$((I+1))
				J=$((J+1))
			done
			pcp_backup
		fi
	;;
	slimconfig)
		[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] ORIG_LMSDATA is: '$ORIG_LMSDATA'</p>'
		[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] LMSDATA is: '$LMSDATA'</p>'

		if [ "$ORIG_LMSDATA" = "$LMSDATA" ]; then
			echo '<p class="info">[ INFO ] LMS Data directory Unchanged.</p>'
		else
			case "$ORIG_LMSDATA" in
				usb:*) DEV=$(blkid | grep ${ORIG_LMSDATA:4} | cut -d ':' -f1)
					TMP=$(mount | grep -w $DEV | cut -d ' ' -f3)
					ORIG_MNT="$TMP/slimserver"
				;;
				net:*) ORIG_MNT="${ORIG_LMSDATA:4}/slimserver";;
				default) ORIG_MNT="$TCEMNT/tce/slimserver";;
			esac
			BADFORMAT="no"
			case "$LMSDATA" in
				usb:*) DEV=$(blkid | grep ${LMSDATA:4} | cut -d ':' -f1)
					TMP=$(mount | grep -w $DEV | cut -d ' ' -f3)
					MNT="$TMP/slimserver"
					FSTYPE=$(blkid -U ${LMSDATA:4} | xargs -I {} blkid {} -s TYPE | awk -F"TYPE=" '{print $NF}' | tr -d "\"")
					case $FSTYPE in
						msdos|fat|vfat|fat32) BADFORMAT="yes";;
						*) BADFORMAT="no";;
					esac
				;;
				net:*)
					MNT="${LMSDATA:4}/slimserver"
					FSTYPE=$(mount | grep -w ${LMSDATA:4} | cut -d ' ' -f5)
					case "$FSTYPE" in
						cifs)echo '<p class="warn">[ WARN ] CIFS partitions may not work with LMS Cache.</p>';;
						*);;
					esac
				;;
				default) MNT="$TCEMNT/tce/slimserver";;
			esac
			[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] ORIG_MNT is: '$ORIG_MNT'</p>'
			[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] MNT is: '$MNT'</p>'
			[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] DEV is: '$DEV'</p>'
			[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] FSTYPE is: '$FSTYPE'</p>'
			[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] BADFORMAT is: '$BADFORMAT'</p>'

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
						echo '<p class="ok">[  OK  ] DONE</p>'
					fi
					[ "$WASRUNNING" = "1" ] && (echo '<p class="info">[ INFO ] Starting LMS</p>';/usr/local/etc/init.d/slimserver start)
				fi
			else
				echo '<p class="error">[ERROR] Unsupported partition type detected ('$FSTYPE'), please use a ntfs or linux partition type for Cache storage. (i.e. ext4)</p>'
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

[ $DEBUG -eq 1 ] && pcp_textarea "Current $USBMOUNTCONF" "cat $USBMOUNTCONF" 150
[ $DEBUG -eq 1 ] && pcp_textarea "Current $NETMOUNTCONF" "cat $NETMOUNTCONF" 150
[ $DEBUG -eq 1 ] && pcp_textarea "Current $CONFIGCFG" "cat $CONFIGCFG" 150

[ "$REBOOT_REQUIRED" = "1" ] && pcp_reboot_required

pcp_table_middle
pcp_go_back_button
pcp_table_end
pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'
