#!/bin/sh

# Version: 0.02 2015-11-05 GE
#	Original.

# Version: 0.01 2015-09-07 GE
#	Original.

#========================================================================================
# This script duplicates and prepares a piCore SD card ready for piCorePlayer.
# piCore uses 3 heads, 8 sectors. This script generates 4 heads, 16 sectors.
#
#   1. Insert piCore SD card into mmcblk0p
#   2. Insert second SD card into sda
#
# NOTE: sda will be completely overwritten, ALL data will be lost.
#
# Disk /dev/sda: 7948 MB, 7948206080 bytes
# 4 heads, 16 sectors/track, 242560 cylinders
# Units = cylinders of 64 * 512 = 32768 bytes
#
#    Device Boot      Start         End      Blocks  Id System
# /dev/sda1              33         832       30720   c Win95 FAT32 (LBA)
# /dev/sda2             833        2519       48864  83 Linux
#========================================================================================
# TO DO:
#  - mount routine
#  - umount routine
#  - yes/no continue routine
#  - more error checking
#  - redirection of error messages
#  - cyclinder x units calculation routine for image size.
#----------------------------------------------------------------------------------------

clear
. /etc/init.d/tc-functions

echo "${GREEN}[ INFO ] This script duplicates and prepares a piCore SD card ready for piCorePlayer.${NORMAL}"
echo "${GREEN}[ INFO ] 1. piCore SD card should be in mmcblk0p.${NORMAL}"
echo "${GREEN}[ INFO ] 2. piCorePlyaer SD card should be in sda.${NORMAL}"
echo

# Check that you are running the script as root
if [ "$(id -u)" != "0" ]; then
	echo "${RED}[ ERROR ] Script must be run as root.${NORMAL}"
	exit 1
else
	echo "${GREEN}[ INFO ] Script is running as root.${NORMAL}"
	echo
fi

echo "${RED}[ WARNING ] This script will overwrite ALL data on sda!${NORMAL}"
echo "${RED}[ WARNING ] IN DEVELOPMENT - sort of works${NORMAL}"
echo
while true; do
	read -p "${YELLOW}Do you wish to continue? ${NORMAL}" yn
	case $yn in
		[Yy]* ) break;;
		[Nn]* ) exit;;
		* ) echo "${RED}[ ERROR ] Please answer yes or no.${NORMAL}";;
	esac
done

#========================================================================================
# Check for dosfstools.tcz and download and install
#-----------------------------------------------------------------------------------------
pcp_check_dosfsck() {
	echo "${GREEN}"
	mount /mnt/mmcblk0p2
	echo "${GREEN}[ INFO ] Note: Requires dosfstools.tcz${NORMAL}"
	which dosfsck
	if [ $? = 0 ]; then
		echo "${GREEN}[ INFO ] dosfstools.tcz already installed.${NORMAL}"
	else
		if [ ! -f /mnt/mmcblk0p2/tce/optional/dosfstools.tcz ]; then
			echo "${GREEN}[ INFO ] dosfstools.tcz downloading... ${NORMAL}"
			sudo -u tc tce-load -w dosfstools.tcz
			[ $? = 0 ] && echo 'Done.' || echo 'Error.'
		else
			echo "${GREEN}[ INFO ] dosfstools.tcz downloaded.${NORMAL}"
		fi
		echo "${GREEN}[ INFO ] dosfstools.tcz installing... ${NORMAL}"
		sudo -u tc tce-load -i dosfstools.tcz
		[ $? = 0 ] && echo "${GREEN}[ INFO ] Done." || echo "${RED}[ ERROR ] Error."
	fi
	echo "${GREEN}"
	umount /mnt/mmcblk0p2
}

#=========================================================================================
# Backup routine with error check and report
#-----------------------------------------------------------------------------------------
pcp_backup() {
	# Delete any previous backup_done file
	[ -e /tmp/backup_done ] && sudo rm -f /tmp/backup_done

	# Do a backup - filetool.sh backs up files in .filetool.lst
	echo "${YELLOW}[ INFO ] "
	sudo filetool.sh -b
	sync
	echo "${NORMAL}"

	# If backup_status file exists and is non-zero in size then an error has occurred
	if [ -s /tmp/backup_status ]; then
		echo "${RED}[ ERROR ] Backup status.${YELLOW}"
		cat /tmp/backup_status
	fi

	# If backup_done exists then the backup was successful
	if [ -f /tmp/backup_done ]; then
		echo "${GREEN}[ OK ] Backup successful.${NORMAL}"
	else
		echo "${RED}[ ERROR ] Backup failed.${NORMAL}"
	fi
}

#=========================================================================================
# Check if partition is mounted otherwise mount it
#-----------------------------------------------------------------------------------------
pcp_mount() {
	PARTITION=$1
	if mount | grep /mnt/$PARTITION >/dev/null 2>&1; then
		echo "${RED}[ ERROR ] /mnt/$PARTITION already mounted.${NORMAL}"
		RESULT=0
	else
		echo "${GREEN}[ INFO ] Mounting /mnt/$PARTITION...${NORMAL}"
		sudo mount /mnt/$PARTITION >/dev/null 2>&1
		RESULT=$?
	fi
	[ $RESULT = 0 ] || echo "${RED}[ ERROR ] Mounting /mnt/$PARTITION.${NORMAL}"
}

#=========================================================================================
# Check if partition is unmounted otherwise unmount it
#-----------------------------------------------------------------------------------------
pcp_umount() {
	PARTITION=$1
	if mount | grep /mnt/$PARTITION >/dev/null 2>&1; then
		echo "${GREEN}[ INFO ] Unmounting /mnt/$PARTITION...${NORMAL}"
		sudo umount /mnt/$PARTITION >/dev/null 2>&1
		RESULT=$?
	else
		echo "${RED}[ ERROR ] /mnt/$PARTITION already unmounted.${NORMAL}"
		RESULT=0
	fi
	[ $RESULT = 0 ] || echo "${RED}[ ERROR ] Unmounting /mnt/$PARTITION.${NORMAL}"
}

# Work out the number of partitions on sda. There should be 1 or 2 partitions.
NOOFPART=$(fdisk -l /dev/sda | grep "sda" | wc -l)
NOOFPART=$(($NOOFPART - 1))
echo "${YELLOW}"
pcp_mount sda1
if [ $? = 0 ]; then
	echo "${GREEN}[ INFO ] sda found.${NORMAL}"
else
	echo "${RED}[ ERROR ] sda not found.${NORMAL}"
	exit 1
fi
echo "${YELLOW}"
pcp_umount sda1
pcp_umount mmcblk0p2

echo "${GREEN}[ INFO ] Found $NOOFPART partitions on sda.${YELLOW}"
case $NOOFPART in
	1)
		echo "${GREEN}[ INFO ] Deleting $NOOFPART partition on sda...${YELLOW}"
		fdisk /dev/sda <<EOF
p
d
p
w
EOF
		;;
	2)
		echo "${GREEN}[ INFO ] Deleting $NOOFPART partition on sda...${YELLOW}"
		fdisk /dev/sda <<EOF
p
d
1
d
p
w
EOF
		;;
	*)
		echo "${RED}[ ERROR ] Incorrect number of partitions.${NORMAL}"
		exit 1
		;;
esac

echo "${GREEN}[ INFO ] Creating new partitions on sda...${YELLOW}"

fdisk -H 4 -S 16 /dev/sda <<EOF
p
n
p
1
33
832
t
c
n
p
2
833
+50M
p
w
EOF

pcp_check_dosfsck

pcp_umount sda1
pcp_umount sda2

echo "${YELLOW}"
mkfs.vfat -n PCP /dev/sda1
mkfs.ext4 /dev/sda2

while true; do
	read -p "${BLUE}Do you wish to continue? ${NORMAL}" yn
	case $yn in
		[Yy]* ) break;;
		[Nn]* ) exit;;
		* ) echo "${RED}[ ERROR ] Please answer yes or no.${NORMAL}";;
	esac
done

fdisk -l /dev/sda

pcp_mount mmcblk0p1
pcp_mount mmcblk0p2
pcp_mount sda1
pcp_mount sda2

while true; do
	read -p "${BLUE}Do you wish to continue? ${NORMAL}" yn
	case $yn in
		[Yy]* ) break;;
		[Nn]* ) exit;;
		* ) echo "${RED}[ ERROR ] Please answer yes or no.${NORMAL}";;
	esac
done

cd /mnt/sda1
cp -Rvp /mnt/mmcblk0p1/* .
cd /mnt/sda2
mkdir tce
cd tce
cp -Rvp /mnt/mmcblk0p2/tce/* .

while true; do
	read -p "${YELLOW}Do you wish to shutdown? ${NORMAL}" yn
	case $yn in
		[Yy]* ) break;;
		[Nn]* ) exit;;
		* ) echo "${RED}[ ERROR ] Please answer yes or no.${NORMAL}";;
	esac
done
echo "${GREEN}[ INFO ] Shutting down... ${NORMAL}"
exitcheck.sh
exit
