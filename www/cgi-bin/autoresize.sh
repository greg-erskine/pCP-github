#!/bin/sh

# Version: 3.03 2016-10-05
#	Added selectable partition size. SBP.

# Version: 0.01 2015-11-27 GE
#	Original version.

SCRATCH="/home/tc"
DEBUG=TRUE

[ $DEBUG ] && fdisk -l /dev/mmcblk0

#========================================================================================
# fdisk routine
#----------------------------------------------------------------------------------------
pcp_fdisk() {
	[ $DEBUG ] && clear
	LAST_PARTITION_NUM=$(fdisk -l /dev/mmcblk0 | tail -n 1 | sed 's/  */ /g' | cut -d' ' -f 1 | cut -c14)
	PARTITION_START=$(fdisk -l /dev/mmcblk0 | tail -n 1 | sed 's/  */ /g' | cut -d' ' -f 2)
	P2_SIZE="+${PARTITION_SIZE}M"

	echo 'Last partition:  '$LAST_PARTITION_NUM
	echo 'Partition start: '$PARTITION_START
	echo 'Partition size:  '$P2_SIZE

	fdisk /dev/mmcblk0 <<EOF
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
	sudo resize2fs /dev/mmcblk0p2
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