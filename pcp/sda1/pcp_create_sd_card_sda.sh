#!/bin/sh

# Version: 0.01 2015-09-07 GE
#	Original.

#========================================================================================
# This script creates a files system on sda suitable for piCorePlayer.
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

# Check that you are running the script as root
if [ "$(id -u)" != "0" ]; then
	echo "${RED}[ ERROR ] Script must be run as root.${NORMAL}"
	exit 1
else
	echo "${GREEN}[ INFO ] Script is running as root.${NORMAL}"
fi

echo "${RED}[ WARNING ] This script will overwrite sda!${NORMAL}"
echo "${RED}[ WARNING ] IN DEVELOPMENT - sort of works${NORMAL}"
while true; do
	read -p "${RED}Do you wish to continue? ${NORMAL}" yn
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

NOOFPART=$(fdisk -l /dev/sda | grep "sda" | wc -l)
NOOFPART=$(($NOOFPART - 1))
echo "${YELLOW}"
mount /mnt/sda1
if [ $? = 0 ]; then
	echo "${GREEN}[ INFO ] sda found.${NORMAL}"
else
	echo "${RED}[ ERROR ] sda not found.${NORMAL}"
	#exit
fi
echo "${YELLOW}"
umount /mnt/sda1
umount /mnt/mmcblk0p2

echo "${GREEN}[ INFO ] Found $NOOFPART partitions on sda.${YELLOW}"
case $NOOFPART in
	1)
		echo "${GREEN}[ INFO ] Deleteing $NOOFPART partition on sda...${YELLOW}"
		fdisk /dev/sda <<EOF
p
d
p
w
EOF
		;;
	2)
		echo "${GREEN}[ INFO ] Deleteing $NOOFPART partition on sda...${YELLOW}"
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

echo "${YELLOW}"
mkfs.vfat -n PCP /dev/sda1
mkfs.ext4 /dev/sda2

pcp_backup

fdisk -l /dev/sda

mount /mnt/mmcblk0p1
mount /mnt/mmcblk0p2
mount /mnt/sda1
mount /mnt/sda2

cd /mnt/sda1
cp -Rvp /mnt/mmcblk0p1/* .
cd /mnt/sda2
mkdir tce
cd tce
cp -Rvp /mnt/mmcblk0p2/tce/* .

while true; do
	read -p "${RED}Do you wish to reboot? ${NORMAL}" yn
	case $yn in
		[Yy]* ) break;;
		[Nn]* ) exit;;
		* ) echo "${RED}[ ERROR ] Please answer yes or no.${NORMAL}";;
	esac
done
"${GREEN}[ INFO ] Rebooting ${NORMAL}"
sudo reboot
exit
