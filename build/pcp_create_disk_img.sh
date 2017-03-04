#!/bin/bash

# Version: 0.01 2016-11-06 PH
#	Original.

#========================================================================================
# This script builds a image in /tmp, based on git, web repos and local kernel
#
#   1. Make sure picoreplayer git is checked out to correct branch
#   2. Run script as root
#
# Image/Partition 1 is 25MB
# Image/Partition 2 is 48MB
# Total image size is Automatically built on the above sizes
#
#	Image is built with 4 Heads and 16 Sectors
#
#    Device          Boot Start    End   Blocks  Id System
# /tmp/pCPImage.img1       2048  53247   51200  25M  c W95 FAT32 (LBA)
# /tmp/pCPImage.img2      53248 151551   98304  48M 83 Linux
#========================================================================================
#
# - PIVERSION is checked for similarity (i.e. 3.03 will match 3.03a, but not 3.02)
#
# TO DO:
# - Image name and loops usage on commandline.  Not done yet for recovery (ref next TODO)
# - usage function.  m mounts image, u unmounts image.
# - Make it work on any piCore or pCP based system
# - Download git from sourceforge or use local repo
# - dosfstools.tcz is not in piCore 8.x repo
# - Logging
# - More error traps and recovery.  Mainly around loop devices and errors
# - Make the insitu update packages.
# - Kake config.txt with both pcpCore and pcpAudioCore so kernel and initrd names are different.
# - Pull kernel build into this directory and put image and kernel scripts into the pcp git.
#----------------------------------------------------------------------------------------

DEBUG=0

#Have to set this before you run the script
PCP="piCorePlayer3.20alpha2"

BUILDROOT="/home/paul"

LOOP1="/dev/loop100"
LOOP2="/dev/loop101"

PART1="/tmp/part1"
PART2="/tmp/part2"

# ANSI COLORS
CRE="$(echo -e '\r\033[K')"
RED="$(echo -e '\033[1;31m')"
GREEN="$(echo -e '\033[1;32m')"
YELLOW="$(echo -e '\033[1;33m')"
BLUE="$(echo -e '\033[1;34m')"
MAGENTA="$(echo -e '\033[1;35m')"
CYAN="$(echo -e '\033[1;36m')"
WHITE="$(echo -e '\033[1;37m')"
NORMAL="$(echo -e '\033[0;39m')"

echo "${GREEN}[ INFO ] This creates a new image file in /tmp ready to burn to SD card for piCorePlayer.${NORMAL}"
echo "${GREEN}[ INFO ] 1. pCP git is local.${NORMAL}"
echo "${GREEN}[ INFO ] 2. update the extensions in the build/tcz-for-image before building image.${NORMAL}"
echo "${GREEN}[ INFO ] 3. Kernel and rpi Firmware need to be local. Currently in ${BUILDROOT}/pcp ${NORMAL}"
echo

# Check that you are running the script as root
if [ "$(id -u)" != "0" ]; then
	echo "${RED}[ ERROR ] Script must be run as root.${NORMAL}"
	exit 1
else
	echo "${GREEN}[ INFO ] Script is running as root.${NORMAL}"
	echo
fi

find ./tcz-for-img/* -not -type d | grep -q .tcz
if [ $? -ne 0 ]; then
	echo "${RED}[ ERROR ] No extensions found in directory \"tcz-for-img\"."
	echo "Use download script to download needed extensions before running this script.${NORMAL}"
	exit 1
fi

#========================================================================================
# Check for dosfstools.tcz and download and install
#-----------------------------------------------------------------------------------------
pcp_check_dosfsck() {
	echo "${GREEN}"

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
}

pcp_check_losetup() {
	echo "${GREEN}"
	which losetup
	if [ $? = 0 ]; then
		echo "${GREEN}[ INFO ] util-linux.tcz already installed.${NORMAL}"
	else
		if [ ! -f /mnt/mmcblk0p2/tce/optional/util-linux.tcz ]; then
			echo "${GREEN}[ INFO ] util-linux.tcz downloading... ${NORMAL}"
			sudo -u tc tce-load -w util-linux.tcz
			[ $? = 0 ] && echo 'Done.' || echo 'Error.'
		else
			echo "${GREEN}[ INFO ] util-linux.tcz downloaded.${NORMAL}"
		fi
		echo "${GREEN}[ INFO ] util-linux.tcz installing... ${NORMAL}"
		sudo -u tc tce-load -i util-linux.tcz
		[ $? = 0 ] && echo "${GREEN}[ INFO ] Done." || echo "${RED}[ ERROR ] Error."
	fi
	echo "${GREEN}"
}

pcp_set_image_sizes(){
	P1SIZE=32     #to be Mulitplied by 2048 for partition alignment to SDCard
	P2SIZE=48
	DDBS="1M"
	DDCOUNT=$(expr 4 + $P1SIZE + $P2SIZE )

	P1ST=8192    #Start of image for 1MB Card alignment
	P1BLKS=$(expr $P1SIZE \* 2048 )  #orig 51200
	P1END=$(expr $P1ST + $P1BLKS - 1 ) #orig 53247

	P2ST=$(expr $P1ST + $P1BLKS)   #orig 53248
	P2BLKS=$(expr $P2SIZE \* 2048 )  #orig 98304
	P2END=$(expr $P2ST + $P2BLKS - 1 )     #orig 151511(Short of the SDcard Alignment )


	if [ $DEBUG -eq 1 ]; then
		echo "P1SIZE=$P1SIZE"
		echo "P2SIZE=$P2SIZE"
		echo "DDBS=$DDBS"
		echo "DDCOUNT=$DDCOUNT"
		echo
		echo "P1ST=$P1ST"
		echo "P1BLKS=$P1BLKS"
		echo "P1END=$P1END"
		echo
		echo "P2ST=$P2ST"
		echo "P2BLKS=$P2BLKS"
		echo "P2END=$P2END"
	fi
}

#=========================================================================================
# Setup the image file/partitions and mount them
#-----------------------------------------------------------------------------------------
pcp_setup_image() {
	pcp_check_dosfsck
	pcp_check_losetup

	#CLEANUP
	umount $PART1
	umount $PART2
	[ -e ${LOOP1} ] && losetup -d ${LOOP1}
	[ -e ${LOOP2} ] && losetup -d ${LOOP2}

	echo "${GREEN}[ INFO ] Creating new partitions on /tmp/${PCP}.img...${YELLOW}"

	pcp_set_image_sizes

	if [ -e /tmp/${PCP}.img ]; then
		echo "${YELLOW}[ WARN ]${PCP}.img exists, will be deleted${NORMAL}"
		while true; do
			read -p "${YELLOW}Do you wish to continue? ${NORMAL}" yn
			case $yn in
				[Yy]* ) break;;
				[Nn]* ) exit;;
				* ) echo "${RED}[ ERROR ] Please answer yes or no.${NORMAL}";;
			esac
		done
	fi

	dd if=/dev/zero of=/tmp/${PCP}.img bs=${DDBS} count=${DDCOUNT}

	fdisk -u -H 4 -S 16 /tmp/${PCP}.img <<EOF
p
n
p
1
$P1ST
$P1END
t
c
n
p
2
$P2ST
$P2END
p
w
EOF

	#Create Loops   Use 101 and 102.....should be safe, but change to find free loops
	losetup -o `expr $P1ST \* 512` --sizelimit `expr $P1BLKS \* 512` ${LOOP1} /tmp/${PCP}.img
	losetup -o `expr $P2ST \* 512` --sizelimit `expr $P2BLKS \* 512` ${LOOP2} /tmp/${PCP}.img

	echo "${YELLOW}"
	mkfs.vfat -n PCP -s 4 -f 2 -F 16 ${LOOP1}
	mkfs.ext4 ${LOOP2}

	while true; do
		read -p "${BLUE}Do you wish to continue? ${NORMAL}" yn
		case $yn in
			[Yy]* ) break;;
			[Nn]* ) losetup -d ${LOOP1}; losetup -d ${LOOP2}; exit;;
			* ) echo "${RED}[ ERROR ] Please answer yes or no.${NORMAL}";;
		esac
	done

	echo "${GREEN}[ INFO ]Image Partition info"	${YELLOW}
	fdisk -l /tmp/${PCP}.img

	mount_loops
}

copy_boot_part1(){
	rm -rf ${PART1}/*

	#Contents and location of files on mmcblk0p1 (PART1)
	#rpi firmware:
	#Location   ${BUILDROOT}/pcp/firmware/boot
	FILELIST=/tmp/files.lst
	cat << EOF > ${FILELIST}
COPYING.linux
LICENCE.broadcom
bootcode.bin
fixup.dat
fixup_cd.dat
fixup_x.dat
start.elf
start_cd.elf
start_x.elf
EOF

	rsync --files-from=${FILELIST} ${BUILDROOT}/pcp/firmware/boot $PART1

	#Location   ${BUILDROOT}/pcp/pcpCore/armv6/kernel/<selected kernel>
	cat << EOF > ${FILELIST}
bcm2708-rpi-0-w.dtb
bcm2708-rpi-b-plus.dtb
bcm2708-rpi-b.dtb
bcm2708-rpi-cm.dtb
EOF
	rsync --files-from=${FILELIST}  ~/pcp/pcpCore/armv6/kernel/${KERNELV6} $PART1

	#Location   ${BUILDROOT}/pcp/pcpCore/armv7/kernel/<selected kernel>
	cat << EOF > ${FILELIST}
bcm2709-rpi-2-b.dtb
bcm2710-rpi-3-b.dtb
bcm2710-rpi-cm3.dtb
EOF
	rsync --files-from=${FILELIST} ${BUILDROOT}/pcp/pcpCore/armv7/kernel/${KERNELV7} $PART1

	#Copy overlays, doesn't matter which arch we copy from
	[ ! -d $PART1/overlays ] && mkdir $PART1/overlays
	rsync ${BUILDROOT}/pcp/pcpCore/armv7/kernel/${KERNELV7}/overlays/* $PART1/overlays

	#Copy Both Kernels
	cp ${BUILDROOT}/pcp/pcpCore/armv6/kernel/${KERNELV6}/kernel*.img $PART1
	cp ${BUILDROOT}/pcp/pcpCore/armv7/kernel/${KERNELV7}/kernel*v7.img $PART1

	#Copy the initrds
	cp ${BUILDROOT}/pcp/pcpCore/armv6/initrd/${KERNELV6}/*.gz $PART1
	cp ${BUILDROOT}/pcp/pcpCore/armv7/initrd/${KERNELV7}/*v7.gz $PART1

	#copy the files from pcp git
	#location ${BUILDROOT}/git/picoreplayer-picoreplayer/pcp/mmcblk0p1
	cat << EOF > ${FILELIST}
cmdline.txt
config.txt
LICENCE.piCorePlayer
README
RELEASE
EOF

	rsync --files-from=${FILELIST} ${BUILDROOT}/git/picoreplayer-picoreplayer/pcp/mmcblk0p1 $PART1

	chmod -R 777 $PART1
	dos2unix ${PART1}/config.txt
	dos2unix ${PART1}/cmdline.txt

}

pcp_txt_cp() {
	#SRC=$1
	#DEST=$2  (Make sure to use the file name as dest)
	#OWNER=$3
	#FILEMOD=$4

	cp -f $1 $2
	dos2unix $2
	chown $3 $2
	chmod $4 $2
}

pcp_tcz_cp() {
	#SRC=$1
	#DEST=$2  (Make sure to use the file name as dest)
	#OWNER=$3
	#FILEMOD=$4

	echo "${BLUE}[ INFO ] Copying Extension ${1%%//.*}"
	for FILE_EXT in $(echo "tcz tcz.dep tcz.md5.txt"); do
		if [ -e ${1%//.*}.${FILE_EXT} ]; then
			cp -f ${1%//.*}.${FILE_EXT} ${2%//.*}.${FILE_EXT}
			chown $3 ${2%//.*}.${FILE_EXT}
			chmod $4 ${2%//.*}.${FILE_EXT}
		else
			[ $DEBUG -eq 1 ] && echo "${YELLOW}[ WARN ] ${1%//.*}.${FILE_EXT} not Found.${BLUE}"
		fi
	done
}

copy_part2(){
	rm -rf ${PART2}/*

	echo "${BLUE}[ INFO ] Setting up Partition mmcblk0p2"
	[ ! -d ${PART2}/tce/optional ] && mkdir -p ${PART2}/tce/optional
	[ ! -d ${PART2}/tce/ondemand ] && mkdir -p ${PART2}/tce/ondemand

	find $PART2/* -type d | grep -v lost | xargs chown 1001.50 
	find $PART2/* -type d | grep -v lost | xargs chmod 775

	pcp_txt_cp ${BUILDROOT}/git/picoreplayer-picoreplayer/pcp/mmcblk0p2/tce/onboot.lst $PART2/tce/onboot.lst 1001.50 664
	pcp_txt_cp ${BUILDROOT}/git/picoreplayer-picoreplayer/pcp/mmcblk0p2/tce/piCorePlayer.dep $PART2/tce/piCorePlayer.dep 1001.50 664

	EXT=$(ls -1 ${BUILDROOT}/git/picoreplayer-picoreplayer/build/tcz-for-img/*.tcz)

	for I in $EXT; do
		J=$(basename ${I%%.*})
		pcp_tcz_cp ${BUILDROOT}/git/picoreplayer-picoreplayer/build/tcz-for-img/$J ${PART2}/tce/optional/$J 1001.50 664	
	done

	pcp_tcz_cp ${BUILDROOT}/git/picoreplayer-picoreplayer/tcz/firmware-brcmwifi/repo/firmware-brcmwifi ${PART2}/tce/optional/firmware-brcmwifi 1001.50 664
	pcp_tcz_cp ${BUILDROOT}/git/picoreplayer-picoreplayer/tcz/RTL_firmware/firmware-rtlwifi ${PART2}/tce/optional/firmware-rtlwifi 1001.50 664
	pcp_tcz_cp ${BUILDROOT}/git/picoreplayer-picoreplayer/tcz/libts-tcz/libts ${PART2}/tce/optional/libts 1001.50 664

	MOD_TCZ="alsa-modules backlight irda net-usb touchscreen wireless"
	for I in $MOD_TCZ; do
		pcp_tcz_cp ${BUILDROOT}/pcp/pcpCore/armv6/extensions/${KERNELV6}/${I}-${KERNELV6%^*} ${PART2}/tce/optional/${I}-${KERNELV6%^*} 1001.50 664
		pcp_tcz_cp ${BUILDROOT}/pcp/pcpCore/armv7/extensions/${KERNELV7}/${I}-${KERNELV7%^*} ${PART2}/tce/optional/${I}-${KERNELV7%^*} 1001.50 664
	done
}

build_mydata(){
	MYDATA="/tmp/mydata"
	rm -rf ${MYDATA}

	mkdir -p ${MYDATA}/home/tc/.X.d
	mkdir -p ${MYDATA}/home/tc/.local/bin
	mkdir -p ${MYDATA}/home/tc/www/cgi-bin
	mkdir -p ${MYDATA}/home/tc/www/js
	mkdir -p ${MYDATA}/home/tc/www/images
	mkdir -p ${MYDATA}/home/tc/www/css
	mkdir -p ${MYDATA}/opt
	mkdir -p ${MYDATA}/usr/local/bin
	mkdir -p ${MYDATA}/usr/local/sbin
	mkdir -p ${MYDATA}/usr/local/etc/ssh
	mkdir -p ${MYDATA}/usr/local/etc/init.d
	mkdir -p ${MYDATA}/var/spool/cron/crontabs
	mkdir -p ${MYDATA}/var/lib/alsa

	cp -dR --preserve=all ${BUILDROOT}/git/picoreplayer-picoreplayer/pcp/mydata/* ${MYDATA}/

	chown 0.50 ${MYDATA}/etc
	chown -R 0.0 ${MYDATA}/usr
	chown 0.50 ${MYDATA}/usr/local/bin
	chown -R 0.50 ${MYDATA}/var
	chown 0.0 ${MYDATA}/etc/*
	find ${MYDATA}/etc -not -type d | xargs -r chmod 644
	chown 0.50 ${MYDATA}/opt/*
	chmod 775 ${MYDATA}/opt/bootsync.sh
	chmod 664 ${MYDATA}/opt/tcemirror
	chmod 775 ${MYDATA}/opt/.xfiletool.lst
	chown 0.50 ${MYDATA}/etc/sysconfig/*
	chmod 664 ${MYDATA}/etc/sysconfig/*

	find ${MYDATA}/etc -not -type d | xargs -r dos2unix

	find ${MYDATA}/usr/local/etc/pcp -type d | xargs -r chown 0.50

	find ${MYDATA}/usr/local/etc/pcp -not -type d | xargs -r dos2unix
	find ${MYDATA}/usr/local/etc/pcp -not -type d | xargs -r chown 0.50
	find ${MYDATA}/usr/local/etc/pcp -not -type d | xargs -r chmod 664

	# These files have already been copied, but this is setting ownership,type and dos2unix.
	pcp_txt_cp ${BUILDROOT}/git/picoreplayer-picoreplayer/pcp/mydata/etc/asound.conf ${MYDATA}/etc/asound.conf root.staff 664
	pcp_txt_cp ${BUILDROOT}/git/picoreplayer-picoreplayer/pcp/mydata/etc/motd ${MYDATA}/etc/motd root.staff 664
	pcp_txt_cp ${BUILDROOT}/git/picoreplayer-picoreplayer/pcp/mydata/etc/modprobe.conf ${MYDATA}/etc/modprobe.conf root.staff 664

	pcp_txt_cp ${BUILDROOT}/git/picoreplayer-picoreplayer/pcp/mydata/home/tc/.local/bin/copywww.sh ${MYDATA}/home/tc/.local/bin/copywww.sh 1001.50 755
	pcp_txt_cp ${BUILDROOT}/git/picoreplayer-picoreplayer/pcp/mydata/home/tc/.local/bin/.pbtemp ${MYDATA}/home/tc/.local/bin/.pbtemp 1001.50 644
	pcp_txt_cp ${BUILDROOT}/git/picoreplayer-picoreplayer/pcp/mydata/home/tc/.alsaequal.presets ${MYDATA}/home/tc/.alsaequal.presets 1001.50 644
	pcp_txt_cp ${BUILDROOT}/git/picoreplayer-picoreplayer/pcp/mydata/home/tc/.ashrc ${MYDATA}/home/tc/.ashrc 1001.50 644
	pcp_txt_cp ${BUILDROOT}/git/picoreplayer-picoreplayer/pcp/mydata/home/tc/wifi.db ${MYDATA}/home/tc/wifi.db root.root 600
	pcp_txt_cp ${BUILDROOT}/git/picoreplayer-picoreplayer/pcp/mydata/home/tc/powerscript.sh ${MYDATA}/home/tc/powerscript.sh 1001.50 755

	#Copy the www folder
	cp -dR --preserve=all ${BUILDROOT}/git/picoreplayer-picoreplayer/www/* ${MYDATA}/home/tc/www
	find ${MYDATA}/home/tc/www/* -not -type d | xargs dos2unix
	find ${MYDATA}/home/tc/www/* -not -type d | xargs chown 1001.50
	find ${MYDATA}/home/tc/www/* -not -type d | xargs chmod 644
	find ${MYDATA}/home/tc/www/cgi-bin/* -not -type d | xargs chmod 755


	pcp_txt_cp ${BUILDROOT}/git/picoreplayer-picoreplayer/pcp/mydata/opt/bootlocal.sh ${MYDATA}/opt/bootlocal.sh 0.50 775
	pcp_txt_cp ${BUILDROOT}/git/picoreplayer-picoreplayer/pcp/mydata/opt/bootsync.sh ${MYDATA}/opt/bootsync.sh 0.50 775
	pcp_txt_cp ${BUILDROOT}/git/picoreplayer-picoreplayer/pcp/mydata/opt/.filetool.lst ${MYDATA}/opt/.filetool.lst 0.50 664

	pcp_txt_cp ${BUILDROOT}/git/picoreplayer-picoreplayer/pcp/mydata/usr/local/sbin/config.cfg ${MYDATA}/usr/local/sbin/config.cfg 1001.50 664
	pcp_txt_cp ${BUILDROOT}/git/picoreplayer-picoreplayer/pcp/mydata/usr/local/sbin/piversion.cfg ${MYDATA}/usr/local/sbin/piversion.cfg 1001.50 664

	pcp_txt_cp ${BUILDROOT}/git/picoreplayer-picoreplayer/pcp/mydata/usr/local/sbin/pcp ${MYDATA}/usr/local/sbin/pcp root.root 755
	pcp_txt_cp ${BUILDROOT}/git/picoreplayer-picoreplayer/pcp/mydata/usr/local/sbin/pcp-load ${MYDATA}/usr/local/sbin/pcp-load root.root 755
	pcp_txt_cp ${BUILDROOT}/git/picoreplayer-picoreplayer/pcp/mydata/usr/local/sbin/setup ${MYDATA}/usr/local/sbin/setup root.root 755

	pcp_txt_cp ${BUILDROOT}/git/picoreplayer-picoreplayer/pcp/mydata/usr/local/etc/pointercal ${MYDATA}/usr/local/etc/pointercal root.root 644

	pcp_txt_cp ${BUILDROOT}/git/picoreplayer-picoreplayer/pcp/mydata/usr/local/etc/init.d/httpd ${MYDATA}/usr/local/etc/init.d/httpd root.root 755

	touch ${MYDATA}/var/lib/alsa/asound.state
	touch ${MYDATA}/var/spool/cron/crontabs/root
	chown 0.0 ${MYDATA}/var/spool/cron/crontabs/root

	chown 0.50 ${MYDATA}/home
	chmod 775 ${MYDATA}/home
	chown -R 1001.50 ${MYDATA}/home/tc
	chmod 750 ${MYDATA}/home/tc
	chmod g+s ${MYDATA}/home/tc

	chmod 750 ${MYDATA}/home/tc/.local
	chmod 750 ${MYDATA}/home/tc/.local/bin
	chmod g+s ${MYDATA}/home/tc/.local
	chmod g+s ${MYDATA}/home/tc/.local/bin

	chown -R 0.50 ${MYDATA}/opt
	chmod 755 ${MYDATA}/opt
	chmod g+s ${MYDATA}/opt

	echo "${GREEN}Ready to compress mydata. Evaluate mounted image if needed. Press enter to continue."
	read key

	PWD=`pwd`
	cd ${MYDATA}
	rm -f ${PART2}/tce/mydata.tgz
	tar zcf ${PART2}/tce/mydata.tgz *
	cd $PWD

	chown 1001.50 ${PART2}/tce/mydata.tgz

}

mount_loops() {
	losetup -l | grep -q $LOOP1
	if [ $? -eq 1 ]; then 
		pcp_set_image_sizes
		losetup -o `expr $P1ST \* 512` --sizelimit `expr $P1BLKS \* 512` ${LOOP1} /tmp/${PCP}.img
		if [ $? -ne 0 ]; then
			echo "${RED}[ ERROR ] Error setting up ${LOOP1}"
			exit 1
		fi
	fi
	losetup -l | grep -q $LOOP2
	if [ $? -eq 1 ]; then
		pcp_set_image_sizes
		losetup -o `expr $P2ST \* 512` --sizelimit `expr $P2BLKS \* 512` ${LOOP2} /tmp/${PCP}.img
		if [ $? -ne 0 ]; then
			echo "${RED}[ ERROR ] Error setting up ${LOOP2}"
			exit 1
		fi
	fi

	mount | grep -q ${PART1}
	if [ $? -eq 1 ]; then 
		[ ! -d ${PART1} ] && mkdir ${PART1}
		mount ${LOOP1} ${PART1}
		if [ $? -ne 0 ]; then
			echo "${RED}[ ERROR ] Error mounting ${LOOP1}"
			exit 1
		fi
	fi
	mount | grep -q ${PART2}
	if [ $? -eq 1 ]; then 
		[ ! -d ${PART2} ] && mkdir ${PART2}
		mount ${LOOP2} ${PART2}
		if [ $? -ne 0 ]; then
			echo "${RED}[ ERROR ] Error mounting ${LOOP2}"
			exit 1
		fi
	fi
}

unmount_loops(){
	umount ${PART1}
	umount ${PART2}
	losetup -d ${LOOP1}
	losetup -d ${LOOP2}
	rmdir ${PART1}
	rmdir ${PART2}
}

abort(){
	unmount_loops
	exit 1
}

#Check to be sure the config.txt matches the kernel, 
#For now pcpCore and pcpAudioCore use the same file names for initrd and kernel names
check_config_txt(){
	CFG=${BUILDROOT}/git/picoreplayer-picoreplayer/pcp/mmcblk0p1/config.txt
	#Copy Both Kernels
	ARMV6KERNEL=$(basename ${BUILDROOT}/pcp/pcpCore/armv6/kernel/${KERNELV6}/kernel*.img)
	ARMV7KERNEL=$(basename ${BUILDROOT}/pcp/pcpCore/armv7/kernel/${KERNELV7}/kernel*v7.img)
	ARMV6INITRD=$(basename ${BUILDROOT}/pcp/pcpCore/armv6/initrd/${KERNELV6}/*.gz)
	ARMV7INITRD=$(basename ${BUILDROOT}/pcp/pcpCore/armv7/initrd/${KERNELV7}/*.gz)
	RPI0=1
	RPI1=1
	RPI2=1
	RPI3=1

	while read -r line
	do
    	case $line in
			\[PI0\]) ARM=6; RPI0=0; read -r INITRD; read -r KERNEL;;
			\[PI1\]) ARM=6; RPI1=0; read -r INITRD; read -r KERNEL;;
			\[PI2\]) ARM=7; RPI2=0; read -r INITRD; read -r KERNEL;;
			\[PI3\]) ARM=7; RPI3=0; read -r INITRD; read -r KERNEL;;
			*) ARM=0;;
		esac
		if [ $ARM -eq 6 ]; then
			[ $DEBUG -eq 1 ] && echo "${ARMV6INITRD} - $INITRD - ${ARMV6KERNEL} - $KERNEL"
			if [[ "$INITRD" =~ "${ARMV6INITRD}" ]] && [[ "$KERNEL" =~ "${ARMV6KERNEL}" ]]; then
				FAIL=0
			else
				echo "${RED}[ ERROR ] ${ARMV6INITRD} - $INITRD - ${ARMV6KERNEL} - $KERNEL"
				FAIL=1
			fi
		fi
		if [ $ARM -eq 7 ]; then
			[ $DEBUG -eq 1 ] && echo "${ARMV7INITRD} - $INITRD - ${ARMV7KERNEL} - $KERNEL"
			if [[ "$INITRD" =~ "${ARMV7INITRD}" ]] && [[ "$KERNEL" =~ "${ARMV7KERNEL}" ]]; then
				FAIL=0
			else
				echo "${RED}[ ERROR ] ${ARMV7INITRD} - $INITRD - ${ARMV7KERNEL} - $KERNEL"
				FAIL=1
			fi
		fi
		if [ $ARM -ne 0 ]; then
			if [ $FAIL -eq 1 ]; then
				echo "${RED}[ ERROR ] config.txt does not match selected kernel. RPI = ${line}"
				echo "Fix config.txt in git, then start process again.${NORMAL}"
				break
			fi
		fi
		[ $DEBUG -eq 1 ] && echo "${RPI0} - ${RPI1} - ${RPI2} - ${RPI3}"
		if [ ${RPI0} -eq 0 -a ${RPI1} -eq 0 -a ${RPI2} -eq 0 -a ${RPI3} -eq 0 ]; then
			break
		fi
	done < "${CFG}"
	return ${FAIL}
}

check_deps(){
	cd ${PART2}/tce/optional
	echo "${BLUE} [ INFO ] Checking Dependancies."
	for I in `ls -1 *.dep`; do
		echo -n "${BLUE}    [ INFO ] Checking $I."
		FAIL=0
		while read -r LINE; do
			#check for a malformed dep file
			# regex [a-zA-Z0-9_+].tcz$
			if [[ $LINE = *[![:space:]]* ]]; then
				# echo "String contains non-whitespace"
				echo $LINE | grep -q ".tcz"
				[ $? -eq 1 ] && FAIL=1
				echo $LINE | grep -q "KERNEL"
				if [ $? -eq 0 ]; then
					#Need to Check both Kernels
					FILEv6=$(echo $LINE | sed "s/KERNEL/${KERNELV6%^*}/")
					FILEv7=$(echo $LINE | sed "s/KERNEL/${KERNELV7%^*}/")
					[ -e "$FILEv6" ] || ( FAIL=1; echo -n "${RED} ERROR on $LINE." )
					[ -e "$FILEv7" ] || ( FAIL=1; echo -n "${RED} ERROR on $LINE." )
				else
					[ -e "$LINE" ] || ( FAIL=1; echo -n "${RED} ERROR on $LINE." )
				fi
			fi
		done < $I
		[ $FAIL -eq 0 ] && echo "${GREEN} OK." || echo "${RED} ERROR"
	done
	cd $BUILDROOT
}



#*******************************************************************************************
#******************************************START********************************************
#*******************************************************************************************

if [ "$1" == "m" ]; then 
	pcp_set_image_sizes
	mount_loops
	exit 0
fi
if [ "$1" == "u" ]; then 
	unmount_loops
	exit 0
fi

#*******************************************************************************************
# Check piversion.cfg and PCP image name.  They should match.
. ${BUILDROOT}/git/picoreplayer-picoreplayer/pcp/mydata/usr/local/sbin/piversion.cfg

VERSION=$(echo $PIVERS | cut -d ' ' -f2)
case $PCP in
	*${VERSION}*) ;;
	*) echo "${RED}[ ERROR ] piversion does not match image name."
		echo "From piversion.cfg, PIVERS=${PIVERS}"
		echo "PCP image name=${PCP}.${NORMAL}"
		exit 1;;
esac
#*******************************************************************************************

echo "${GREEN}[ INFO ] Starting ${YELLOW}${PCP} ${GREEN}image build for ${YELLOW}${PIVERS}.${NORMAL}"
echo
while true; do
	read -p "${GREEN}[ INFO ] Do you need to setup the image file at ${YELLOW}/tmp/${PCP}.img? ${NORMAL}" yn
	case $yn in
		[Yy]* ) pcp_setup_image; break;;
		[Nn]* ) break;;
		* ) echo "${RED}[ ERROR ] Please answer yes or no.${NORMAL}";;
	esac
done

mount_loops

echo
echo "${GREEN}[ INFO ] Ready to Populate the Image."
while true; do
	read -p "${BLUE}Do you wish to continue? ${NORMAL}" yn
	case $yn in
		[Yy]* ) break;;
		[Nn]* ) abort;;
		* ) echo "${RED}[ ERROR ] Please answer yes or no.${NORMAL}";;
	esac
done
echo 
echo "${GREEN}[ INFO ] Preparing to populate the boot partition of /tmp/${PCP}.img...${NORMAL}"

echo
echo "${GREEN}[ INFO ] Please Select the ${YELLOW}armv6 KERNEL${GREEN} version to use for starting module file listings"
select KERNELV6 in $(ls -r --sort=time ${BUILDROOT}/pcp/pcpCore/armv6/kernel/);
do
	if [ "$KERNELV6" != "" ]; then
		echo "${YELLOW}You picked ${KERNELV6}${NORMAL}"
		read -p "Do you wish to continue? (y)es, (n)o, e(x)it " yn
		case $yn in
			[Yy]* ) break;;
			[Nn]* ) ;;
			[Xx]* ) abort;;
			* ) echo "Please answer (y)es, (n)o or e(x)it.";;
		esac
		echo "Press Enter to reselect${GREEN}"
	fi
done
echo
echo "${GREEN}[ INFO ] Please Select the ${YELLOW}armv7 KERNEL${GREEN} version to use for starting module file listings"
select KERNELV7 in $(ls -r --sort=time ${BUILDROOT}/pcp/pcpCore/armv7/kernel/);
do
	if [ "$KERNELV7" != "" ]; then
		echo "${YELLOW}You picked ${KERNELV7}${NORMAL}"
		read -p "Do you wish to continue? (y)es, (n)o, e(x)it " yn
		case $yn in
			[Yy]* ) break;;
			[Nn]* ) ;;
			[Xx]* ) abort;;
			* ) echo "Please answer (y)es, (n)o or e(x)it.";;
		esac
		echo "Press Enter to reselect${GREEN}"
	fi
done

#Check to be sure the config.txt matches the kernel, 
#For now pcpCore and pcpAudioCore use the same file names for initrd and kernels
check_config_txt
[ $? -ne 0 ] && exit 1

copy_boot_part1 
copy_part2
build_mydata
check_deps

echo "${GREEN}Done building image. Evaluate mounted image if needed. Press enter to continue."
read key
unmount_loops


cd /tmp
[ -f ${PCP}.zip ] && rm ${PCP}.zip
md5sum ${PCP}.img > ${PCP}.img.md5.txt
zip -9 ${PCP}.zip ${PCP}.img*

exit 0
