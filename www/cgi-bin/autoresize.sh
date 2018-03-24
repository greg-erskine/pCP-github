#!/bin/sh

# Version: 3.50 2017-11-06
#	Fixed for changed format of fdisk (BusyBox v1.27.2). PH.

# Version: 3.21 2017-05-20
#	Changed to allow booting from USB on RPI3. PH.

# Version: 3.10 2017-01-06
#	Added selectable partition size. SBP.

# Version: 0.01 2015-11-27 GE
#	Original version.

SCRATCH="/home/tc"
#DEBUG=TRUE

TCEDEV="/dev/$(readlink /etc/sysconfig/tcedir | cut -d '/' -f3)"
BOOTDEV=${TCEDEV%%?}1

case $BOOTDEV in
	*/sd?*)
		[ $DEBUG ] && fdisk -l ${BOOTDEV%%?}
		DEVICE=${BOOTDEV%%?}
	;;
	*mmcblk*)
		[ $DEBUG ] && fdisk -l ${BOOTDEV%%??}
		DEVICE=${BOOTDEV%%??}
	;;
	*)
		[ $DEBUG ] echo "ERROR in device"
	;;
esac

#========================================================================================
# fdisk routine
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
#   Field 1         Field 2      Field 3         Field 4
#----------------------------------------------------------------------------------------
pcp_fdisk() {
	[ $DEBUG ] && clear
	LAST_PARTITION_NUM=$(fdisk -l $DEVICE | tail -n 1 | sed 's/  */ /g' | cut -d' ' -f 1 | awk '$0=$NF' FS=)
	PARTITION_START=$(fdisk -l $DEVICE | tail -n 1 | sed 's/  */ /g' | cut -d' ' -f 4)
	P2_SIZE="+${PARTITION_SIZE}M"

	echo 'Last partition:  '$LAST_PARTITION_NUM
	echo 'Partition start: '$PARTITION_START
	echo 'Partition size:  '$P2_SIZE

	fdisk -u $DEVICE <<EOF
p
d
$LAST_PARTITION_NUM
n
p
$LAST_PARTITION_NUM
$PARTITION_START
$P2_SIZE
w
EOF
	[ $DEBUG ] && pcp_pause
}

#========================================================================================
# resize2fs routine
#----------------------------------------------------------------------------------------
pcp_resize2fs() {
	[ $DEBUG ] && clear
	echo 'resize2fs can take a couple of minutes. Please wait...'
	sudo resize2fs $TCEDEV
	[ $DEBUG ] && pcp_pause
}

pcp_pause() {
	read -n1 -r -p "Press any key to continue..." KEY
}

#========================================================================================
# Main
#----------------------------------------------------------------------------------------
if [ -f ${SCRATCH}/partition_size.cfg ]; then
	. ${SCRATCH}/partition_size.cfg
	PARTITION_SIZE=$SIZE
	echo "partition_size.cfg file found"
else
	PARTITION_SIZE=""
	echo "partition_size.cfg file not found and whole SD card will be used."
fi

if [ -f ${SCRATCH}/fdisk_required ]; then
	echo "Resizing partition using fdisk..."
	pcp_fdisk
	rm -f ${SCRATCH}/fdisk_required
	rm -f ${SCRATCH}/partition_size.cfg
	sleep 1
	if [ ! -f ${SCRATCH}/fdisk_required ]; then
		touch ${SCRATCH}/resize2fs_required
		sudo filetool.sh -b
		sync; sync
		sleep 1
		sudo reboot
	fi
	exit
fi

if [ -f ${SCRATCH}/resize2fs_required ]; then
	echo "Resizing partition using resize2fs...Please wait. System will reboot when ready"
	pcp_resize2fs
	rm -f ${SCRATCH}/resize2fs_required
	sleep 1
	if [ ! -f ${SCRATCH}/resize2fs_required ]; then
		sudo filetool.sh -b
		sync; sync
		sleep 1
		sudo reboot
	fi
	exit
fi

echo "Autoresize.sh skipped..."
