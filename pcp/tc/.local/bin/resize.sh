#!/bin/sh -x

# Version: 0.01 2015-11-25 GE
#   Original version.

fdisk -l /dev/mmcblk0
HOUSE=/home/tc

#========================================================================================
# fdisk routine
#----------------------------------------------------------------------------------------
pcp_fdisk() {

	LAST_PARTITION_NUM=$(fdisk -l /dev/mmcblk0 | tail -n 1 | sed 's/  */ /g' | cut -d' ' -f 1 | cut -c14)
	PARTITION_START=$(fdisk -l /dev/mmcblk0 | tail -n 1 | sed 's/  */ /g' | cut -d' ' -f 2)

	echo 'Last partition:  '$LAST_PARTITION_NUM
	echo 'Partition start: '$PARTITION_START

	fdisk /dev/mmcblk0 <<EOF
p
d
$LAST_PARTITION_NUM
n
p
$LAST_PARTITION_NUM
$PARTITION_START

w
p
EOF
}

#========================================================================================
# resize2fs routine
#----------------------------------------------------------------------------------------
pcp_resize2fs() {
	echo 'resize2fs can take a couple of minutes. Please wait...'
	sudo resize2fs /dev/mmcblk0p2
}

#========================================================================================
# Main
#----------------------------------------------------------------------------------------

if [ -f $HOUSE/fdisk_required ]; then
	echo "Resizing partition using fdisk..."
	pcp_fdisk
	rm -f $HOUSE/fdisk_required
	touch $HOUSE/resize2fs_required
	sudo filetool.sh -b
	sudo reboot
	exit
fi

if [ -f $HOUSE/resize2fs_required ]; then
	echo "Resizing partition using resize2fs..."
	pcp_resize2fs
	rm -f $HOUSE/resize2fs_required
	sudo filetool.sh -b
	sudo reboot
	exit
fi

echo "Resize.sh skipped..."