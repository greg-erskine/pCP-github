#!/bin/sh

# Version: 6.0.0 2019-06-05

SCRATCH="/home/tc"
#DEBUG=TRUE

TCEDEV="/dev/$(readlink /etc/sysconfig/tcedir | cut -d '/' -f3)"
BOOTDEV=${TCEDEV%%?}1

case $BOOTDEV in
	*/sd?*) DEVICE=${BOOTDEV%%?} ;;
	*mmcblk*) DEVICE=${BOOTDEV%%??} ;;
	*) [ $DEBUG ] echo "ERROR in device" ;;
esac

#========================================================================================
# fdisk function
#
# $ fdisk -l
# Disk /dev/mmcblk0: 3724 MB, 3904897024 bytes, 7626752 sectors
# 119168 cylinders, 4 heads, 16 sectors/track
# Units: cylinders of 64 * 512 = 32768 bytes
# 
# Device       Boot StartCHS    EndCHS        StartLBA     EndLBA    Sectors  Size Id Type
# /dev/mmcblk0p1    128,0,1     127,3,16          8192      73727      65536 32.0M  c Win95 FAT32 (LBA)
# /dev/mmcblk0p2    128,0,1     639,3,16         73728     172031      98304 48.0M 83 Linux
#
#       f 1           f 2         f 3            f 4         f 5
#----------------------------------------------------------------------------------------
pcp_fdisk_part2() {
	PART2_START=$(fdisk -l $DEVICE | tail -n 1 | sed 's/  */ /g' | cut -d' ' -f 4)

	echo
	echo 'Partition 2 - fdisk'
	echo 'Partition 2 start: '$PART2_START
	echo 'Partition 2 size: '$PART2_SIZE

	fdisk -u $DEVICE <<EOF
p
d
2
n
p
2
$PART2_START
$PART2_SIZE
p
w
EOF
}

pcp_fdisk_part3() {
	PART2_END=$(fdisk -l $DEVICE | tail -n 1 | sed 's/  */ /g' | cut -d' ' -f 5)
	PART3_START=$((PART2_END + 1))

	echo
	echo 'Partition 3 - fdisk'
	echo 'Partition 2 end: '$PART2_END
	echo 'Partition 3 start: '$PART3_START

	fdisk -u $DEVICE <<EOF
n
p
3
$PART3_START

p
w
EOF
}

#========================================================================================
# resize2fs routines
#----------------------------------------------------------------------------------------
pcp_resize2fs_part2() {
	[ $DEBUG ] && clear
	echo 'resize2fs partition 2 can take a couple of minutes. Please wait...'
	sudo resize2fs $TCEDEV
	[ $DEBUG ] && pcp_pause
}

pcp_pause() {
	read -n1 -r -p "Press any key to continue..." KEY
	echo
}

#========================================================================================
# Main
#----------------------------------------------------------------------------------------
if [ -f ${SCRATCH}/fdisk_part2_required ]; then
	[ $DEBUG ] && clear
	. ${SCRATCH}/fdisk_part2_required
	PARTITION_SIZE=$SIZE
	if [ "$PARTITION_SIZE" = "" ]; then
		PART2_SIZE=""
	else
		PART2_SIZE="+${PARTITION_SIZE}M"
	fi

	echo
	echo "==============================================================================="
	echo "Resizing partition 2 using fdisk..."
	echo "-------------------------------------------------------------------------------"
	echo "Please wait. System will reboot when ready."
	pcp_fdisk_part2
	rm -f ${SCRATCH}/fdisk_part2_required
	sleep 1
	if [ ! -f ${SCRATCH}/fdisk_part2_required ]; then
		touch ${SCRATCH}/resize2fs_part2_required
		sudo filetool.sh -b
		sync; sync
		sleep 1
		[ $DEBUG ] && pcp_pause
		echo "-------------------------------------------------------------------------------"
		sudo reboot
	fi
	exit
fi

if [ -f ${SCRATCH}/resize2fs_part2_required ]; then
	[ $DEBUG ] && clear
	echo
	echo "==============================================================================="
	echo "Resizing partition 2 using resize2fs..."
	echo "-------------------------------------------------------------------------------"
	echo "Please wait. System will reboot when ready."
	pcp_resize2fs_part2
	rm -f ${SCRATCH}/resize2fs_part2_required
	sleep 1
	if [ ! -f ${SCRATCH}/resize2fs_part2_required ]; then
		sudo filetool.sh -b
		sync; sync
		sleep 1
		[ $DEBUG ] && pcp_pause
		echo "-------------------------------------------------------------------------------"
		sudo reboot
	fi
	exit
fi

if [ -f ${SCRATCH}/fdisk_part3_required ]; then
	[ $DEBUG ] && clear
	echo
	echo "==============================================================================="
	echo "Creating partition 3 using fdisk..."
	echo "-------------------------------------------------------------------------------"
	echo "Please wait. System will reboot when ready."
	pcp_fdisk_part3
	rm -f ${SCRATCH}/fdisk_part3_required
	sleep 1
	if [ ! -f ${SCRATCH}/fdisk_part3_required ]; then
		touch ${SCRATCH}/mkfs_part3_required
		sudo filetool.sh -b
		sync; sync
		sleep 1
		[ $DEBUG ] && pcp_pause
		echo "-------------------------------------------------------------------------------"
		sudo reboot
	fi
	exit
fi

if [ -f ${SCRATCH}/mkfs_part3_required ]; then
	[ $DEBUG ] && clear
	echo
	echo "==============================================================================="
	echo "Formatting partition 3 using mkfs.ext4..."
	echo "-------------------------------------------------------------------------------"
	echo "Please wait. System will reboot when ready."
	mkfs.ext4 -L "PCP_DATA" /dev/mmcblk0p3
	rm -f ${SCRATCH}/mkfs_part3_required
	sleep 1
	if [ ! -f ${SCRATCH}/mkfs_part3_required ]; then
		sudo filetool.sh -b
		sync; sync
		sleep 1
		[ $DEBUG ] && pcp_pause
		echo "-------------------------------------------------------------------------------"
		sudo reboot
	fi
	exit
fi

echo ""
echo "Autoresize.sh skipped..."
exit
