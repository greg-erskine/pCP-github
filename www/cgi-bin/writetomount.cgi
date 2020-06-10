#!/bin/sh

# Version: 7.0.0 2020-06-10

. pcp-functions
. pcp-lms-functions

# Store the original values so we can see if they are changed
ORIG_LMSDATA="$LMSDATA"

pcp_html_head "Write to Disk Mounts" "PH"

pcp_navbar
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
	[ $? -eq 0 ] && sudo rm -rf $1 || pcp_message ERROR "File Copy Error." "text"

	# Remove old Symlinks to the data location.  Will be recreated when LMS is started.
	sudo rm -f /usr/local/slimserver/Cache
	sudo rm -f /usr/local/slimserver/prefs
	sync
}

pcp_do_umount () {
	if [ -d $1 ]; then
		df | grep -qws $1
		if [ $? -eq 0 ]; then
			umount $1
			if [ $? -eq 0 ]; then
				pcp_message INFO "Mount $1 Unmounted." "text"
			else
				pcp_message ERROR "Mount point $1 is Busy, Reboot will be required." "text"
				pcp_message ERROR "Diskmount Options Saved, Reboot to Mount." "text"
				REBOOT_REQUIRED=1
			fi
		else
			pcp_message INFO "New Mount Point $1 is not in use." "text"
		fi
	fi
}

#========================================================================================
# Mounts section
#----------------------------------------------------------------------------------------
pcp_heading5 "Write to mount"
pcp_infobox_begin
pcp_debug_variables "text" MOUNTTYPE

case ${ACTION} in
	gptfdisk) 
		MOUNTTYPE="skip"
		EXTN="util-linux.tcz"
		if [ -f $PACKAGEDIR/$EXTN ]; then
			pcp_textarea "none" "sudo -u tc pcp-load -i $EXTN" 5
			echo $EXTN >> $ONBOOTLST
		else
			pcp_textarea "none" "sudo -u tc pcp-load -wi $EXTN" 5
		fi
	;;
	Permissions)
		MOUNTTYPE="skip"
		ALLPARTS=$(mount | grep -e "/dev/\(sd[a-z][1-9]\|mmcblk0p[3-9]\)" | cut -d ' ' -f3)
		for I in $ALLPARTS; do
			# Do not show the boot Drive
			if [ "$I" != "${BOOTMNT}" -a "$I" != "${TCEMNT}" ]; then
				pcp_message INFO "Setting write permissions on $I." "text"
				find $I -type d | grep -v "lost+found" | xargs -r chmod 755
				find $I -type d | grep -v "lost+found" | xargs -r chown tc.staff
				find $I -not -type d | xargs -r chmod 664
			fi
		done
	;;
esac

case "$MOUNTTYPE" in
	localdisk)
		# READ Conf file
		if [ -f ${USBMOUNTCONF} ]; then
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
				[ $DEBUG -eq 1 ] && pcp_message DEBUG "I,J =$I,$J" "text"
				ORIGUU=$(eval echo "\${ORIG_MOUNTUUID${J}}")
				ORIGPNT=$(eval echo "\${ORIG_MOUNTPOINT${J}}")
				ORIGENA=$(eval echo "\${ORIG_USBDISK${J}}")
				if [ "$THISUU" = "$ORIGUU" ]; then
					FOUND=1
					[ $DEBUG -eq 1 ] && pcp_message DEBUG "ORIG UU is: $ORIGUU" "text"
					[ $DEBUG -eq 1 ] && pcp_message DEBUG "This UU is: $THISUU" "text"
					[ $DEBUG -eq 1 ] && pcp_message DEBUG "ORIG_USBDISK is: $ORIGENA" "text"
					[ $DEBUG -eq 1 ] && pcp_message DEBUG "This USBDISK is: $THISENA" "text"
					[ $DEBUG -eq 1 ] && pcp_message DEBUG "ORIG_MOUNTPOINT is: $ORIGPNT" "text"
					[ $DEBUG -eq 1 ] && pcp_message DEBUG "This MOUNTPOINT is: $THISPNT" "text"
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
			[ $DEBUG -eq 1 ] && pcp_message DEBUG "MOUNTUUID${I} is: $NEWUU" "text"
			[ $DEBUG -eq 1 ] && pcp_message DEBUG "ORIG_USBDISK${I} is: $OLDENA" "text"
			[ $DEBUG -eq 1 ] && pcp_message DEBUG "USBDISK${I} is: $NEWENA" "text"
			[ $DEBUG -eq 1 ] && pcp_message DEBUG "ORIG_MOUNTPOINT${I} is: $OLDPNT" "text"
			[ $DEBUG -eq 1 ] && pcp_message DEBUG "MOUNTPOINT${I} is: $NEWPNT" "text"
			[ $DEBUG -eq 1 ] && pcp_message DEBUG "MOUNT CHANGED${I}=$CHANGED" "text"
			if [ $CHANGED -eq 0 ]; then
				pcp_message INFO "Mount options unchanged for Disk $NEWUU." "text"
			else
				MNTCHANGED=1
				pcp_message INFO "Mount options have changed for Disk $NEWUU." "text"
				pcp_message INFO "Mount Point is set to: $NEWPNT" "text"
				if [ "$OLDPNT" != "" ]; then
					pcp_message INFO "Unmounting Old Mount Point: /mnt/$OLDPNT." "text"
					pcp_do_umount /mnt/$OLDPNT
				fi
				if [ $CHANGED -eq 1 -a $REBOOT_REQUIRED -eq 0 ]; then
					if [ "$NEWENA" != "" ]; then
						pcp_message INFO "Checking new Mount Point." "text"
						pcp_do_umount /mnt/$NEWPNT
						if [ $REBOOT_REQUIRED -eq 0 ]; then
							[ ! -d /mnt/$NEWPNT ] && mkdir -p /mnt/$NEWPNT
							chown tc.staff /mnt/$NEWPNT
							chmod 755 /mnt/$NEWPNT
							DEVICE=$(blkid -U $NEWUU)
							FSTYPE=$(blkid -U $NEWUU | xargs -I {} blkid {} -s TYPE | awk -F"TYPE=" '{print $NF}' | tr -d "\"")
							case "$FSTYPE" in
								ntfs)
									pcp_message INFO "Checking to make sure NTFS is not mounted." "text"
									umount $DEVICE
									OPTIONS="-v -t ntfs-3g -o permissions,noatime"
								;;
								vfat|fat32)
									# if Filesystem support installed, use utf-8 charset for fat.
									df | grep -qs ntfs
									[ $? -eq 0 ] && CHARSET=",iocharset=utf8" || CHARSET=""
									umount $DEVICE  # need to unmount vfat incase 1st mount is not utf8
									OPTIONS="-v -t vfat -o noauto,users,noatime,exec,umask=000,flush${CHARSET}"
								;;
								exfat)
									CHARSET=",iocharset=utf8"
									umount $DEVICE  # need to unmount incase 1st mount is not utf8
									OPTIONS="-v -o noauto,users,noatime,exec,umask=000,flush,uid=1001,gid=50${CHARSET}"
								;;
								*)
									OPTIONS="-v -o noatime"
								;;
							esac
							pcp_message INFO "Mounting Disk." "text"
							case "$FSTYPE" in
								exfat) [ $DEBUG -eq 1 ] && pcp_message DEBUG "Mount Line is: mount.exfat $OPTIONS $DEVICE /mnt/$NEWPNT" "text"
									pcp_message INFO "" "text" "-n"
									modprobe fuse
									mount.exfat $OPTIONS $DEVICE /mnt/$NEWPNT
								;;
								*) [ $DEBUG -eq 1 ] && pcp_message DEBUG "Mount Line is: mount $OPTIONS --uuid $NEWUU /mnt/$NEWPNT" "text"
									pcp_message INFO "" "text" "-n"
									mount $OPTIONS --uuid $NEWUU /mnt/$NEWPNT
								;;
							esac
							if [ $? -eq 0 ]; then
								pcp_message INFO "Disk Mounted Successfully." "text"
							else
								pcp_message ERROR "Disk Mount Error, Try to Reboot." "text"
								REBOOT_REQUIRED=1
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
			pcp_backup "text"
		fi
	;;
	networkshare)
		NETMNTCHANGED=0
		NN=0
		# cifs does not automatically load arc4, which is in the dependencies needed for SMB3 to work
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
			[ $DEBUG -eq 1 ] && pcp_message DEBUG "CHECK is: $CHECK" "text"
			[ $DEBUG -eq 1 ] && pcp_message DEBUG "ORIG_CHECK is: $ORIG_CHECK" "text"
			[ $DEBUG -eq 1 ] && pcp_message DEBUG "NETENABLE${I} is: $ENABLE" "text"
			[ $DEBUG -eq 1 ] && pcp_message DEBUG "ORIG_NETENABLE${I} is: $OLDENABLE" "text"
			[ $DEBUG -eq 1 ] && pcp_message DEBUG "NETMOUNTPOINT${I} is: $PNT" "text"
			[ $DEBUG -eq 1 ] && pcp_message DEBUG "ORIG_NETMOUNTPOINT${I} is: $OLDPNT" "text"
			[ $DEBUG -eq 1 ] && pcp_message DEBUG "NETMOUNTIP${I} is: $IP" "text"
			[ $DEBUG -eq 1 ] && pcp_message DEBUG "ORIG_NETMOUNTIP${I} is: $OLDIP" "text"
			[ $DEBUG -eq 1 ] && pcp_message DEBUG "NETMOUNTSHARE${I} is: $SHARE" "text"
			[ $DEBUG -eq 1 ] && pcp_message DEBUG "ORIG_NETMOUNTSHARE${I} is: $OLDSHARE" "text"
			[ $DEBUG -eq 1 ] && pcp_message DEBUG "NETMOUNTFSTYPE${I} is: $FSTYPE" "text"
			[ $DEBUG -eq 1 ] && pcp_message DEBUG "ORIG_NETMOUNTFSTYPE${I} is: $OLDFSTYPE" "text"
			[ $DEBUG -eq 1 ] && pcp_message DEBUG "NETMOUNTUSER${I} is: $USER" "text"
			[ $DEBUG -eq 1 ] && pcp_message DEBUG "ORIG_NETMOUNTUSER${I} is: $OLDUSER" "text"
			[ $DEBUG -eq 1 ] && pcp_message DEBUG "NETMOUNTPASS${I} is: $PASS" "text"
			[ $DEBUG -eq 1 ] && pcp_message DEBUG "ORIG_NETMOUNTPASS${I} is: $OLDPASS" "text"
			[ $DEBUG -eq 1 ] && pcp_message DEBUG "NETMOUNTOPTIONS${I} is: $OPTIONS" "text"
			[ $DEBUG -eq 1 ] && pcp_message DEBUG "ORIG_NETMOUNTOPTIONS${I} is: $OLDOPTIONS" "text"
			if [ "$ORIG_CHECK" = "$CHECK" ]; then
				[ "$CHECK" != "" ] && pcp_message INFO "Mount configuration unchanged for $IP:/$SHARE" "text"
			else
				NETMNTCHANGED=1
				pcp_message INFO "Mount configuration changed for $IP:/$SHARE" "text"
				if [ "$OLDPNT" != "" ]; then
					pcp_message INFO "Unmounting Old Mount Point: /mnt/$OLDPNT." "text"
					pcp_do_umount /mnt/$OLDPNT
				fi
				if [ "$ENABLE" != "" -a $REBOOT_REQUIRED -eq 0 ]; then
					pcp_message INFO "Checking new Mount Point /mnt/$PNT." "text"
					pcp_do_umount /mnt/$PNT
					pcp_message INFO "Mounting Disk." "text"
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
					pcp_message INFO "mount $MNTCMD" "text"
					/bin/sh -c "mount ${MNTCMD}"
					if [ $? -eq 0 ]; then
						pcp_message INFO "Disk Mounted Successfully." "text"
					else
						pcp_message ERROR "Disk Mount Error, Try to Reboot." "text"
						REBOOT_REQUIRED=1
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
						J=$((J-1)) # Decrement the counter written to the conf file
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
			pcp_backup "text"
		fi
	;;
	slimconfig)
		pcp_debug_variables "text" ORIG_LMSDATA LMSDATA

		if [ "$ORIG_LMSDATA" = "$LMSDATA" ]; then
			pcp_message INFO "LMS Data directory unchanged for $LMSDATA." "text"
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
						cifs) pcp_message WARN "CIFS partitions may not work with LMS Cache." "text";;
						*);;
					esac
				;;
				default) MNT="$TCEMNT/tce/slimserver";;
			esac

			pcp_debug_variables "text" ORIG_MNT MNT DEV FSTYPE BADFORMAT

			if [ "$BADFORMAT" = "no" ]; then
				pcp_message INFO "Setting LMS Data Directory to $MNT." "text"
				pcp_lms_set_slimconfig CACHE $MNT
				pcp_save_to_config
				pcp_backup "text"
				echo
				if [ "$ACTION" = "Move" ]; then
					#========================================================================================
					# Move LMS cache and prefs section
					#----------------------------------------------------------------------------------------
					WASRUNNING=0
					if [ $(pcp_lms_status) -eq 0 ]; then
						WASRUNNING=1
						pcp_message INFO "Stopping LMS..." "text"
						pcp_message INFO "" "text" "-n"
						/usr/local/etc/init.d/slimserver stop
					fi
					if [ -d $ORIG_MNT ]; then
						pcp_message INFO "Moving Data from $ORIG_MNT to $MNT" "text"
						pcp_move_LMS_cache $ORIG_MNT $MNT
						pcp_message OK "DONE" "text"
					fi
					[ $WASRUNNING -eq 1 ] && (pcp_message INFO "Starting LMS" "text"; /usr/local/etc/init.d/slimserver start)
				fi
			else
				pcp_message ERROR "Unsupported partition type detected ($FSTYPE), please use a NTFS or Linux partition type for Cache storage. (i.e. ext4)" "text"
			fi
		fi
	;;
	skip)
	;;
	*)
		pcp_message ERROR "Web Page Error, No MountType Submitted" "text"
	;;
esac

pcp_infobox_end

if [ $DEBUG -eq 1 ]; then
	pcp_hr
	pcp_textarea "Current $USBMOUNTCONF" "cat $USBMOUNTCONF" 10
	pcp_textarea "Current $NETMOUNTCONF" "cat $NETMOUNTCONF" 10
	pcp_textarea "Current $PCPCFG" "cat $PCPCFG" 10
fi

[ $REBOOT_REQUIRED -eq 1 ] && pcp_reboot_required

pcp_redirect_button "Go to LMS" "lms.cgi" 100

pcp_html_end
exit
