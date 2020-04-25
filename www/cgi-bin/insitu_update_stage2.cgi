#!/bin/sh

# Version: 6.0.0

. /etc/init.d/tc-functions
. pcp-functions

pcp_html_head "Update pCP" "GE"

pcp_banner
pcp_navigation
pcp_running_script
pcp_httpd_query_string

WGET_IUS2="/bin/busybox wget -T 30"
FAIL_MSG="ok"

if [ -n $CORE ]; then
	case $CORE in
		#AUDIOTAR is used to download correct package
		*pcpAudioCore*) AUDIOTAR="-Audio";;
		*) AUDIOTAR="";;
	esac
fi

# As all the insitu update is done in one file, it may be better to define this here
UPD_PCP="/tmp/pcp_insitu_update"
#INSITU_DOWNLOAD=<----- defined in pcp-functions otherwise the beta testing does not work

# VERSION format = x.y.z  (Does not include beta tags)
CURRENT_VERSION=$(echo "$(pcp_picoreplayer_version)" | cut -d'-' -f1)
NEW_VERSION=$(echo "$VERSION" | awk -F'piCorePlayer' '{ print $2 }' | cut -d '-' -f1)

# Version format is the full name with beta  piCorePlayerx.y.z-b
NEW_PCP_VERSION="$VERSION"

# This function returns a version number to use in a > < comparison
function version_number { echo "$@" | awk -F. '{ printf("%d%03d%03d%03d\n", $1,$2,$3,$4); }'; }

# Parse out numerical versions of upgrade version (comes from query string)...
# Currently not using these.
# MAJOR_VERSION=$(echo "$NEW_VERSION" | cut -d '.' -f1)
# vtmp=$(echo "$NEW_VERSION" | cut -d '.' -f2)
# MINOR_VERSION=${vtmp:0:2}
# vtmp=$(echo "$NEW_VERSION" | cut -d '.' -f3)
# PATCH_VERSION=$(echo "$vtmp" | cut -d '-' -f1)

#========================================================================================
#      382 - insitu.cfg
# 21044878 - piCorePlayer2.00_boot.tar.gz
# 14932349 - piCorePlayer2.00_tce.tar.gz
# --------
# 35977609 bytes
#----------------------------------------------------------------------------------------
#SPACE_REQUIRED=$((35977609 * 2 / 1000))
BUILD=$(getBuild)
case "${NEW_PCP_VERSION}" in
	piCorePlayer6.0.*)
		SPACE_REQUIRED=12000
		BOOT_SIZE_REQUIRED=47000
		############################
		KERNEL_REVISION="4.19.105"
		RT_REVISION="rt42"
		############################
		#These are used for sed modification of config.txt
		CNF_INITRDBASE="initrd_pcp_10.3.gz"
		CNF_INITRDMODULES="initrd-${KERNEL_REVISION}"
		CNF_KERNEL="kernel$(echo ${KERNEL_REVISION} | tr -d '.')"
		# Set the below for downloading new kernel modules
		KUPDATE=1
		case $CORE in
			*pcpAudioCore*) NEWKERNELVER="${KERNEL_REVISION}-${RT_REVISION}";;
			*) NEWKERNELVER="${KERNEL_REVISION}";;
		esac
		PICOREVERSION="10.x"
		NEWKERNELVERCORE="${NEWKERNELVER}-${CORE%+}"
	;;
	*)
		SPACE_REQUIRED=15000
		BOOT_SIZE_REQUIRED=62000
		KUPDATE=0
	;;
esac

# We are only going to do the 64 bit kernel on PI4's
case $(uname -r | cut -d '_' -f2) in
	v8)	NEWKERNEL="${NEWKERNELVERCORE}_v8"
		PIARCH="v8"
	;;
	v7l)NEWKERNEL="${NEWKERNELVERCORE}_v8"
		BUILD="armv8"
		PIARCH="v8"
	;;
	v7)	NEWKERNEL="${NEWKERNELVERCORE}_v7"
		PIARCH="v7"
	;;
	*)	NEWKERNEL="${NEWKERNELVERCORE}"
		PIARCH=""
	;;
esac

#========================================================================================
# DEBUG info showing variables
#----------------------------------------------------------------------------------------
pcp_debug_info() {
	pcp_debug_variables "html" QUERY_STRING ACTION NEW_PCP_VERSION CURRENT_VERSION NEW_VERSION UPD_PCP INSITU_DOWNLOAD SPACE_REQUIRED BOOT_SIZE_REQUIRED BOOT_SIZE
}

#========================================================================================
# Check we have internet access - set FAIL_MSG if not accessible
#----------------------------------------------------------------------------------------
pcp_internet_indicator() {
	if [ $(pcp_internet_accessible) -eq 0 ]; then
		INTERNET_STATUS="Internet accessible."
	else
		INTERNET_STATUS="Internet not accessible!!"
		FAIL_MSG="Internet not accessible!!"
	fi
}

#========================================================================================
# Check we have repo access - set FAIL_MSG if not accessible
#----------------------------------------------------------------------------------------
pcp_repo_indicator() {
	if [ $(pcp_pcp_repo_accessible) -eq 0 ]; then
		REPO_STATUS="pCP repository accessible."
	else
		REPO_STATUS="pCP repository not accessible!!"
		FAIL_MSG="pCP repo not accessible!!"
	fi
}

#========================================================================================
# Check for free space - set FAIL_MSG if insufficient space is available
#----------------------------------------------------------------------------------------
pcp_enough_free_space() {
	INITSPACE=0
	REQUIRED_SPACE=$1
	FREE_SPACE=$(pcp_free_space k)
	if [ $FREE_SPACE -gt $REQUIRED_SPACE ]; then
		echo '[  OK  ] Free space: '$FREE_SPACE'k - Required space: '$REQUIRED_SPACE'k'
	else
		echo '[ ERROR ] Free space: '$FREE_SPACE'k - Required space: '$REQUIRED_SPACE'k'
		echo '[ ERROR ] Not enough free space - try expanding your partition.'
		FAIL_MSG="Not enough free space - try expanding your partition."
		INITSPACE=1
	fi
}

#=========================================================================================
# Reboot popups - need to be self contained
#-----------------------------------------------------------------------------------------
pcp_reboot_required() {
	echo '<script language="javascript">'
	echo '  pcp_confirm('\''Reboot '$NAME'?\n\nPress [OK] to reboot now or [Cancel] to manually reboot later.'\'','\''main.cgi?ACTION=reboot'\'')'
	echo '</script>'
}

#========================================================================================
# update onboot.lst
#----------------------------------------------------------------------------------------
pcp_update_onbootlst() {
	# $1 - add|remove
	local EXTENSION=$2
	local ERROR=0

	sudo sed -i '/'$EXTENSION'/d' $ONBOOTLST
	[ $? -eq 0 ] || ERROR=$((ERROR+1))
	if [ "$1" = "add" ]; then
		sudo echo $EXTENSION >> $ONBOOTLST
		[ $? -eq 0 ] || ERROR=$((ERROR+1))
	fi

	return $ERROR
}

#========================================================================================
# Prepare download directories - Do we really need boot and tce directory???
#----------------------------------------------------------------------------------------
pcp_create_download_directory() {
	if [ -d $UPD_PCP ]; then
		sudo rm -rf $UPD_PCP
		[ $? -ne 0 ] && FAIL_MSG="Can not remove directory $UPD_PCP"
	fi
	sudo mkdir -m 755 $UPD_PCP
	[ $? -ne 0 ] && FAIL_MSG="Can not make directory $UPD_PCP"
	sudo mkdir ${UPD_PCP}/boot
	[ $? -ne 0 ] && FAIL_MSG="Can not make directory ${UPD_PCP}/boot"
	sudo mkdir ${UPD_PCP}/tce
	[ $? -ne 0 ] && FAIL_MSG="Can not make directory ${UPD_PCP}/tce"
	sudo mkdir ${UPD_PCP}/mydata
	[ $? -ne 0 ] && FAIL_MSG="Can not make directory ${UPD_PCP}/mydata"
}

#========================================================================================
# Download kernel modules for new kernel
#----------------------------------------------------------------------------------------

pcp_get_kernel_modules() {
	if [ $KUPDATE -eq 1 ]; then
		[ $PCP_CUR_REPO -eq 1 ] && PCP_REPO="$PCP_REPO_1" || PCP_REPO="$PCP_REPO_2"
		#For early beta versions of pCP6.0.0
		[ "$PCP_REPO" = "" ] && PCP_REPO="https://repo.picoreplayer.org/repo"
		CURRENTKERNEL=$(uname -r)
		CURRENTKERNELCORE=$(uname -r | cut -d '-' -f2)
		PCP_DL="${PCP_REPO%/}/${PICOREVERSION}/${BUILD}/tcz"
		echo '[ INFO ] PCP_DL='$PCP_DL
		# Do a space check based on current kernel modules installed, then doubled for safety
		MODSIZE=0
		for I in $(ls ${PACKAGEDIR}/*${CURRENTKERNELCORE}*.tcz | grep $CURRENTKERNEL); do
			MODSIZE=$((MODSIZE+$(du -k $I | awk '{print $1}')))
		done
		pcp_enough_free_space $((MODSIZE * 2))
		if [ "$FAIL_MSG" = "ok" ]; then
			# Get list of kernel modules matching current kernel
			ls ${PACKAGEDIR}/*${CURRENTKERNELCORE}*.tcz | grep $CURRENTKERNEL | sed -e 's|[-][0-9].[0-9].*||' | sed 's/.*\///' > /tmp/current
			# Get list of kernel modules not matching new kernel
			ls ${PACKAGEDIR}/*${CURRENTKERNELCORE}*.tcz | grep $NEWKERNEL | sed -e 's|[-][0-9].[0-9].*||' | sed 's/.*\///' > /tmp/newk

			# Show the old modules that do not have a current kernel version.
			MODULES=$(comm -1 -3 /tmp/newk /tmp/current)
			echo '[ INFO ] Step 3A. Downloading new kernel modules: '$MODULES
			if [ -z "${MODULES}" ]; then
				echo '[ INFO ] All new Kernel modules for '${NEWKERNEL}' already present.'
			else
				for EXT in ${MODULES}; do
					# All kernel modules distributed from PCP_REPO
					sudo -u tc pcp-load -w -u ${PCP_DL} ${EXT}-${NEWKERNEL}.tcz
					[ $? -ne 0 ] && FAIL_MSG="Error downloading new Kernel Modules"
				done
			fi
		fi
	fi
}

#========================================================================================
# Download the boot files from Repo
#----------------------------------------------------------------------------------------
pcp_get_boot_files() {
	echo '[ INFO ] Step 3C. - Downloading '${NEW_PCP_VERSION}${AUDIOTAR}'_boot.tar.gz'
	echo '[ INFO ] Download Location link: '${INSITU_DOWNLOAD}'/'${NEW_PCP_VERSION}'/'${NEW_PCP_VERSION}${AUDIOTAR}'_boot.tar.gz'
	echo '[ INFO ] This will take a few minutes. Please wait...'
	$WGET_IUS2 ${INSITU_DOWNLOAD}/${NEW_PCP_VERSION}/${NEW_PCP_VERSION}${AUDIOTAR}_boot.tar.gz -O ${UPD_PCP}/boot/${NEW_PCP_VERSION}${AUDIOTAR}_boot.tar.gz 2>&1
	if [ $? -eq 0 ]; then
		echo '[  OK  ] Successfully downloaded boot files.'
	else
		echo '[ ERROR ] Error downloading boot files.'
		FAIL_MSG="Error downloading boot files."
	fi
}

#========================================================================================
# Install the boot files
#----------------------------------------------------------------------------------------
pcp_install_boot_files() {
	echo '[ INFO ] Installing boot files...'
	pcp_mount_bootpart_nohtml
	cd $BOOTMNT
	[ -f /tmp/osbackup.tar ] && rm -f /tmp/osbackup.tar
	echo '[ INFO ] Backing up old OS...'
	tar -cf /tmp/osbackup.tar *
	cd

	if [ "$FAIL_MSG" = "ok" ]; then
		# Delete version specific files from the boot partition
		find ${BOOTMNT} | grep -E "(kernel|initrd|pcp_)" | xargs rm -f
		[ $? -eq 0 ] || FAIL_MSG="Error deleting files from ${BOOTMNT}"

		pcp_save_configuration
	fi
	if [ "$FAIL_MSG" = "ok" ]; then
		# Untar the boot files
		echo '[ INFO ] Extracting '${NEW_PCP_VERSION}${AUDIOTAR}'_boot.tar.gz...'
		#config.txt and cmdline.txt should not be in insitu archive, but just incase, exlude them.
		#exclude extracting the kernel and initrds right now.
		tar --exclude config.txt --exclude cmdline.txt --exclude './kernel*' --exclude './initrd*' -xvf ${UPD_PCP}/boot/${NEW_PCP_VERSION}${AUDIOTAR}_boot.tar.gz -C ${BOOTMNT}/ 2>&1
		TST=$?
		if [ $TST -eq 0 ]; then
			echo '[  OK  ] Successfully extracted boot configuration files.'
		else
			echo '[ ERROR ] Error extracting boot tar. Result: '$TST
			FAIL_MSG="Error extracting boot tar."
			return
		fi
		#extract the kernel and initrd needed
		tar -xvf ${UPD_PCP}/boot/${NEW_PCP_VERSION}${AUDIOTAR}_boot.tar.gz -C ${BOOTMNT}/ ./${CNF_KERNEL}${PIARCH}.img ./${CNF_INITRDBASE} ./${CNF_INITRDMODULES}${PIARCH}.gz
		TST=$?
		if [ $TST -eq 0 ]; then
			echo '[  OK  ] Successfully extracted kernel and initramfs files.'
		else
			echo '[ ERROR ] Error extracting kernel and initramfs files. Result: '$TST
			FAIL_MSG="Error extracting boot tar."
			return
		fi

	fi

	#We are not replacing the current config.txt and cmdline.txt, so make appropriate updates.
	if [ "$FAIL_MSG" = "ok" ]; then
		# Remove everything in [PI4] section, Then insert the 64 bit codes.  The versions are xxx, will get updated later.
		sed -i '/\[PI4\]/,/\[ALL\]/ {/\[PI4\]/n /\[ALL\]/ !{d}}' ${BOOTMNT}/config.txt
		sed -i '/\[PI4\]/a arm_64bit=1\ninitramfs xxx.gz followkernel\nkernel kernel12345v8.img' ${BOOTMNT}/config.txt

		#Erase the initramfs lines
		sed -i '/^initramfs/d' ${BOOTMNT}/config.txt
		sed -i "/^\[PI0\]/a initramfs ${CNF_INITRDBASE},${CNF_INITRDMODULES}.gz followkernel" ${BOOTMNT}/config.txt
		sed -i "/^\[PI1\]/a initramfs ${CNF_INITRDBASE},${CNF_INITRDMODULES}.gz followkernel" ${BOOTMNT}/config.txt
		sed -i "/^\[PI2\]/a initramfs ${CNF_INITRDBASE},${CNF_INITRDMODULES}v7.gz followkernel" ${BOOTMNT}/config.txt
		sed -i "/^\[PI3\]/a initramfs ${CNF_INITRDBASE},${CNF_INITRDMODULES}v7.gz followkernel" ${BOOTMNT}/config.txt
		sed -i "/^\[PI4\]/a initramfs ${CNF_INITRDBASE},${CNF_INITRDMODULES}v8.gz followkernel" ${BOOTMNT}/config.txt
#		sed -i -r "s/^initramfs pcp_[0-9]{1,2}\.[0-9]/initramfs ${CNF_INITRD}/g" ${BOOTMNT}/config.txt

		sed -i -r "s/^kernel kernel[0-9]{4,7}/kernel ${CNF_KERNEL}/g" ${BOOTMNT}/config.txt
		[ $? -eq 0 ] || FAIL_MSG="Error updating config.txt"
		sed -i "s/pi3-disable-bt/disable-bt/" ${BOOTMNT}/config.txt
		[ $? -eq 0 ] || FAIL_MSG="Error updating config.txt"
		sed -i "s/pi3-disable-wifi/disable-wifi/" ${BOOTMNT}/config.txt
		[ $? -eq 0 ] || FAIL_MSG="Error updating config.txt"
	fi

	if [ "$FAIL_MSG" != "ok" ]; then
		echo '[ INFO ] Restoring old OS...'
		rm -rf ${BOOTMNT}/*
		tar -xf /tmp/osbackup.tar -C ${BOOTMNT}/
	fi

	pcp_umount_bootpart_nohtml
}

#=========================================================================================
# Save configuration files to the boot partiton
#-----------------------------------------------------------------------------------------
pcp_save_configuration() {
	echo '[ INFO ] Saving configuration files.'
	[ -r /usr/local/etc/pcp/pcp.cfg ] && sudo cp -f /usr/local/etc/pcp/pcp.cfg ${BOOTMNT}/newpcp.cfg
	#Turn off t3 mode automatically
	sudo sed -i "s/\(TEST=\).*/\1\"0\"/" ${BOOTMNT}/newpcp.cfg
	sudo dos2unix -u ${BOOTMNT}/newpcp.cfg
	[ $? -eq 0 ] || FAIL_MSG="Error saving piCorePlayer configuration file."

	[ "$FAIL_MSG" = "ok" ] && echo '[  OK  ] Your configuration files have been saved to the boot partition.'
}

#========================================================================================
# Download the tce files from Repo
#----------------------------------------------------------------------------------------
pcp_get_tce_files() {
	echo '[ INFO ] Step 3B. - Downloading '${NEW_PCP_VERSION}${AUDIOTAR}'_tce.tar.gz'
	echo '[ INFO ] Download Location link: '${INSITU_DOWNLOAD}'/'${NEW_PCP_VERSION}'/'${NEW_PCP_VERSION}${AUDIOTAR}'_tce.tar.gz'
	echo '[ INFO ] This will take a few minutes. Please wait...'
	$WGET_IUS2 ${INSITU_DOWNLOAD}/${NEW_PCP_VERSION}/${NEW_PCP_VERSION}${AUDIOTAR}_tce.tar.gz -O ${UPD_PCP}/tce/${NEW_PCP_VERSION}${AUDIOTAR}_tce.tar.gz 2>&1
	if [ $? -eq 0 ]; then
		echo '[  OK  ] Successfully downloaded tce files.'
	else
		echo '[ ERROR ] Error downloading tce files.'
		FAIL_MSG="Error downloading boot files."
	fi
}

#========================================================================================  <------------------------------------Started with the new version from here
# Install the tce files
#----------------------------------------------------------------------------------------
pcp_install_tce_files() {
	# Untar and update the tzc packages files to optional
	echo '[ INFO ] Untarring new extensions from '${NEW_PCP_VERSION}${AUDIOTAR}'_tce.tar.gz...'
	[ "$FAIL_MSG" = "ok" ] && sudo tar -zxvf ${UPD_PCP}/tce/${NEW_PCP_VERSION}${AUDIOTAR}_tce.tar.gz ./optional -C /etc/sysconfig/tcedir
	if [ $? -eq 0 ]; then
		[ $DEBUG -eq 1 ] && echo '[ DEBUG ] tce tar result: '$?
		echo '[  OK  ] Successfully untarred tce tar.'
		echo ''
	else
		echo '[ ERROR ] Error untarring tce tar. Result: '$?
		FAIL_MSG="Error untarring tce tar."
	fi
}

#========================================================================================
# Finish the install process
#----------------------------------------------------------------------------------------
pcp_finish_install() {
	#save the current pcpversion to determine potential bootfix(es) later  
	echo '[ INFO ] Saving old pcpversion.cfg for bootfix(es)...'
	cp -f /usr/local/etc/pcp/pcpversion.cfg /usr/local/etc/pcp/oldpcpversion.cfg
	sed -i 's/PCPVERS/OLDPCPVERS/' /usr/local/etc/pcp/oldpcpversion.cfg

	OLDPCPVERSION=$(pcp_picoreplayer_version)
	# Unpack the tce.tar and the new mydata.tgz and then copy the content from the new version to the correct locations
	echo '[ INFO ] Untarring new mydata from '${NEW_PCP_VERSION}${AUDIOTAR}'_tce.tar.gz...'
	sudo mkdir -p ${UPD_PCP}/mydata/sysroot
	sudo tar zxvf ${UPD_PCP}/tce/${NEW_PCP_VERSION}${AUDIOTAR}_tce.tar.gz --exclude ./optional* -C ${UPD_PCP}/mydata
	sudo tar zxvf ${UPD_PCP}/mydata/mydata.tgz -C ${UPD_PCP}/mydata/sysroot

	# Move Bootfix into location if it is present
	if [ -f "${UPD_PCP}/mydata/bootfix/bootfix.sh" ]; then
		sudo cp -Rf ${UPD_PCP}/mydata/bootfix/ ${TCEMNT}/tce/
		chmod 755 ${TCEMNT}/tce/bootfix/*
	fi

	# Track and include user made changes to onboot.lst. It is also needed as different versions of piCorePlayer may have different needs.
	# So check that the final onboot contains all from the new version and add eventual extra from the old
	sudo chown tc:staff $ONBOOTLST
	echo "[ INFO ] content of mnt onboot.lst before:"; cat $ONBOOTLST
	sudo cat $ONBOOTLST >> ${UPD_PCP}/mydata/onboot.lst
	sort -u ${UPD_PCP}/mydata/onboot.lst > $ONBOOTLST
	echo "[INFO] content of tmp onboot.lst:"; cat ${UPD_PCP}/mydata/onboot.lst
	sudo chown tc:staff $ONBOOTLST
	sudo chmod u=rwx,g=rwx,o=rx $ONBOOTLST

	# if [ $(version_number $OLDPCPVERSION) -lt $(version_number "5.0.0") ]; then
		# sed -i 's/firmware-rpi3-wireless/firmware-rpi-wifi/' $ONBOOTLST
		# rm -f ${PACKAGEDIR}/firmware-rpi3-wireless.*
	# fi

	#Make sure onboot has the latest www extension.
	sed -i '/pcp-.*-www.tcz/d' $ONBOOTLST
	echo pcp-${NEW_VERSION}-www.tcz >> $ONBOOTLST

	echo "[ INFO ] content of mnt onboot.lst after:"; cat $ONBOOTLST

	# Track and include user made changes to .filetool.lst It is important as user might have modified filetool.lst.
	# So check that the final .filetool.lst contains all from the new version and add eventual extra from the old
	sudo chown root:staff /opt/.filetool.lst
	sudo cat /opt/.filetool.lst >> ${UPD_PCP}/mydata/sysroot/opt/.filetool.lst
	sort -u ${UPD_PCP}/mydata/sysroot/opt/.filetool.lst > /opt/.filetool.lst
	sudo chown root:staff /opt/.filetool.lst
	sudo chmod u=rw,g=rw,o=r /opt/.filetool.lst

	echo "usr/local/etc/init.d/pcp_startup.sh" >> /opt/.filetool.lst

	# Track and include user made changes to .xfiletool.lst It is important as user might have modified filetool.lst.
	# So check that the final .filetool.lst contains all from the new version and add eventual extra from the old
	sudo chown root:staff /opt/.xfiletool.lst
	sudo cat /opt/.xfiletool.lst >> ${UPD_PCP}/mydata/sysroot/opt/.xfiletool.lst
	sort -u ${UPD_PCP}/mydata/sysroot/opt/.xfiletool.lst > /opt/.xfiletool.lst
	sudo chown root:staff /opt/.xfiletool.lst
	sudo chmod u=rw,g=rw,o=r /opt/.xfiletool.lst

	# Track and include user made changes to bootlocal.sh. It is important as user might have modified bootlocal.sh.
	# We don't make changes to bootlocal.sh that much, so make changes here if needed
	# Do not change indentation, this is a python script.
/usr/bin/micropython -c '
import os
import sys
infile = open("/opt/bootlocal.sh", "r")
outfile = open ("/tmp/bootlocal.sh", "w")
CUT=0
while True:
    ln = infile.readline()
    if ln == "":
        break
    if CUT == 0:
        if "#pCPstart------" in ln:
            CUT=1
            outfile.write("#pCPstart------\n")
            outfile.write("/usr/local/etc/init.d/pcp_startup.sh 2>&1 | tee -a /var/log/pcp_boot.log\n")
            outfile.write("#pCPstop------\n")
        else:
            if not "#pCPstop------" in ln:
                outfile.write(ln)
    else:
        if "#pCPstop------" in ln:
            CUT=0
infile.close
outfile.close
'
	mv -f /tmp/bootlocal.sh /opt/bootlocal.sh
	sudo chown root:staff /opt/bootlocal.sh
	chmod 775 /opt/bootlocal.sh

	sudo chown root:staff /opt/bootlocal.sh
	sudo chmod u=rwx,g=rwx,o=rx /opt/bootlocal.sh

	sudo cp -af ${UPD_PCP}/mydata/sysroot/opt/bootsync.sh /opt/bootsync.sh 
	sudo chown root:staff /opt/bootsync.sh
	sudo chmod u=rwx,g=rwx,o=rx /opt/bootsync.sh

	# Update pCP by copying the content from the new version to the correct location followed by a backup
	sudo cp -af ${UPD_PCP}/mydata/sysroot/home/tc/pcp-powerbutton.sh /home/tc/pcp-powerbutton.sh.sample

	#/home/tc/www directory should not be there anymore. But it will be removed in boofix.
	# Just remove the boot script, as it gets loaded from new location.
	[ -f /home/tc/www/cgi-bin/pcp_startup.sh ] && rm -f /home/tc/www/cgi-bin/pcp_startup.sh

	sudo cp -Rf ${UPD_PCP}/mydata/sysroot/home/tc/.ashrc /home/tc/.ashrc
	sudo cp -af ${UPD_PCP}/mydata/sysroot/home/tc/.local/bin/.pbtemp /home/tc/.local/bin/.pbtemp
	sudo cp -af ${UPD_PCP}/mydata/sysroot/home/tc/.local/bin/copywww.sh /home/tc/.local/bin/copywww.sh
#	sudo cp -af ${UPD_PCP}/mydata/sysroot/usr/local/etc/pointercal /usr/local/etc/pointercal
	sudo cp -Rf ${UPD_PCP}/mydata/sysroot/usr/local/sbin/ /usr/local/
	sudo cp -Rf ${UPD_PCP}/mydata/sysroot/usr/local/etc/pcp/ /usr/local/etc/
	sudo cp -af ${UPD_PCP}/mydata/sysroot/usr/local/etc/init.d/pcp_startup.sh /usr/local/etc/init.d/pcp_startup.sh

	sudo chmod 755 /usr/local/etc/init.d/pcp_startup.sh
	sudo chown tc:staff /home/tc/pcp-powerbutton.sh*
	sudo chown -R tc.staff /usr/local/etc/pcp/cards
	sudo chmod u=rw,g=rw,o=r /usr/local/etc/pcp/cards/*

	[ ! -f /etc/httpd.conf ] && sudo cp -af ${UPD_PCP}/mydata/sysroot/etc/httpd.conf /etc/httpd.conf

	# asound.conf needs to be fully updated for 6.0.0
	sudo cp -af ${UPD_PCP}/mydata/sysroot/etc/asound.conf /etc/asound.conf
	rm -f /home/tc/.alsaequal.bin*

	#Because it's annoying, set the theme in the new config file.
	sudo sed -i "s/\(THEME=\).*/\1\"$THEME\"/" $PCPCFG

	# Backup changes to make a new mydata.tgz containing an updated version
	pcp_backup text

	# if [ $(version_number $OLDPCPVERSION) -lt $(version_number "5.0.0") ]; then
		# echo '[ INFO ] Updating installed/required extensions.'
		# echo "https://repo.picoreplayer.org/repo" > /opt/tcemirror
		# echo "10.1pCP" > /usr/share/doc/tc/release.txt

		# UPGRADE_LIST="alsaequal.tcz nano.tcz slimserver.tcz pcp-jivelite.tcz pcp-lirc.tcz samba4.tcz"
		# for UPG in $UPGRADE_LIST; do
			# if [ -f ${PACKAGEDIR}/$UPG ]; then
				# echo '[ INFO ] '$UPG' found, updating....'
				# sudo -u tc pcp-update kernel $NEWKERNEL $UPG
				# [ $? -ne 0 ] && FAIL_MSG="Error Upgrading Package $UPG. You will need to manually upgrade after upgrade. Please Reboot Now"
			# fi
		# done
		# for METER in $(PACKAGEDIR/VU_Meter*.tcz); do
			# echo '[ INFO ] '$METER' found, updating....'
			# sudo -u tc pcp-update $METER
			# [ $? -ne 0 ] && FAIL_MSG="Error Upgrading Package $METER. You will need to manually upgrade after upgrade. Please Reboot Now"
		# done
		# if [ "$JIVELITE" = "yes" -a "$IR_LIRC" = "yes" ]; then
			# sudo -u tc pcp-load -wi pcp-irtools.tcz
			# IR_KEYTABLES="yes"
		# fi

	# fi
}

#========================================================================================
# Generate warning message
#----------------------------------------------------------------------------------------
pcp_warning_message() {
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset class="warning">'
	echo '          <table class="bggrey percent100">'
	echo '            <tr>'
	echo '              <td>'
	echo '                <p><b>Warning:</b></p>'
	echo '                <ul>'
	echo '                  <li>Assume an insitu update will overwrite ALL the data on your SD card.</li>'
	echo '                  <li>Any user modified or added files may be lost or overwritten.</li>'
	echo '                  <li>An insitu update requires about 50% free space.</li>'
	echo '                  <li>You may need to manually update your plugins, extensions, static IP etc.</li>'
	echo '                </ul>'
	echo '              </td>'
	echo '            </tr>'
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
}

#========================================================================================
# Generate status message and finish html page
#----------------------------------------------------------------------------------------
pcp_html_end() {
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Status</legend>'
	echo '          <table class="bggrey percent100">'
	pcp_start_row_shade
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td>'
	echo '                <p>'$FAIL_MSG'</p>'
	echo '              </td>'
	echo '            </tr>'
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
	if [ $INITSPACE -eq 1 ]; then
		STRING1='Not enough space. Press [OK] to start expanding your partition or [Cancel] to abort'
		SCRIPT1=xtras_resize.cgi
		pcp_confirmation_required
	fi
	pcp_footer
	pcp_copyright

	if [ "$ACTION" = "install" ] && [ "$FAIL_MSG" = "ok" ] ; then
		pcp_reboot_required
	fi
	echo '</body>'
	echo '</html>'
	exit
}

#========================================================================================
# Main routine - this is done before any tables are generated
#----------------------------------------------------------------------------------------
case "$ACTION" in
	initial)
		FAIL_MSG="Reached initial in error."
		[ "$FAIL_MSG" = "ok" ] || pcp_html_end
	;;
	download)
		STEP="Step 3 - Downloading files"
		pcp_warning_message
		pcp_create_download_directory
		[ "$FAIL_MSG" = "ok" ] || pcp_html_end
	;;
	install)
		STEP="Step 4 - Installing files"
		pcp_warning_message
	;;
	*)
		STEP="Invalid ACTION"
		FAIL_MSG="Invalid ACTION: $ACTION"
	;;
esac

#========================================================================================
# First fieldset table
#----------------------------------------------------------------------------------------
pcp_incr_id
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>'$STEP'</legend>'
echo '          <table class="bggrey percent100">'
pcp_start_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td>'
echo '                  <textarea class="inform" style="height:130px">'
#----------------------------------------------------------------------------------------
if [ "$ACTION" = "download" ]; then
	echo '[ INFO ] You are currently using piCorePlayer'$(pcp_picoreplayer_version)

	#if we are in 64 bit mode, we are not going to allow using audiocore image
	# if [ $CORE = "pcpAudioCore" -a $(uname -r | cut -d '_' -f2) = "v8" ]; then
		# FAIL_MSG="pCP is currently using a 64bit Kernel! pCPAudioCore does not support 64bit kernels"
	# fi

	CV=$(version_number ${CURRENT_VERSION})
	NV=$(version_number ${NEW_VERSION})

	if [ $CV -lt $(version_number "5.0.0") ]; then
		FAIL_MSG="Insitu upgrade to ${NEW_VERSION} is not available for version ${CURRENT_VERSION}"
	fi

	if [ $CV -lt $(version_number "6.0.0") -a $NV -ge $(version_number "6.0.0") ]; then
		# For 5 to 6 upgrade, need to check a couple of things
		echo "************ Please Read ****************"
		echo ""
		echo "6.0.0 has significant package changes, you will likely need to update all extensions."
		echo ""
		if [ -f $PACKAGEDIR/pcp-bt.tcz ]; then
			echo "Bluetooth will need to be removed before proceeding."
			FAIL_MSG="You must remove the bluetooth extensions before continuing."
		fi
	fi

	if [ $NV -lt $(version_number "6.0.0") ]; then
		FAIL_MSG="Downgrading version is not permitted."
	fi

	if [ "$FAIL_MSG" = "ok" ]; then
		BOOT_SIZE=$(/bin/busybox fdisk -l | grep ${BOOTDEV} | sed "s/*//" | tr -s " " | cut -d " " -f6 | tr -d +)
		echo '[ INFO ] Boot partition size required: '${BOOT_SIZE_REQUIRED}'. Boot partition size is: '${BOOT_SIZE}
		if [ "$FAIL_MSG" = "ok" -a $BOOT_SIZE -lt $BOOT_SIZE_REQUIRED ]; then
			FAIL_MSG="BOOT disk is not large enough, upgrade not possible"
		fi
		echo '[ INFO ] Space required for update and extensions: '$SPACE_REQUIRED'k'
		[ "$FAIL_MSG" = "ok" ] && pcp_enough_free_space $SPACE_REQUIRED
		echo '[ INFO ] You are downloading '${NEW_PCP_VERSION}
		[ "$FAIL_MSG" = "ok" ] && pcp_get_kernel_modules
		[ "$FAIL_MSG" = "ok" ] && pcp_enough_free_space $SPACE_REQUIRED

		[ "$FAIL_MSG" = "ok" ] && pcp_get_boot_files
		[ "$FAIL_MSG" = "ok" ] && pcp_get_tce_files
		[ "$FAIL_MSG" = "ok" ] && pcp_enough_free_space $SPACE_REQUIRED
	fi
fi
#----------------------------------------------------------------------------------------
if [ "$ACTION" = "install" ]; then
	echo '[ INFO ] You are installing '$NEW_PCP_VERSION
	pcp_enough_free_space $SPACE_REQUIRED
fi
#----------------------------------------------------------------------------------------
echo '                  </textarea>'
echo '                </td>'
echo '              </tr>'
#----------------------------------------------------------------------------------------
if [ $DEBUG -eq 1 ]; then
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td>'
	                        pcp_debug_info
	echo '                </td>'
	echo '              </tr>'
fi
#----------------------------------------------------------------------------------------
echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'

#========================================================================================
# Download
#----------------------------------------------------------------------------------------
if [ "$ACTION" = "download" ] && [ "$FAIL_MSG" = "ok" ] ; then
	pcp_incr_id
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>piCorePlayer insitu update</legend>'
	echo '          <form name="download" action= "'$0'" method="get">'
	echo '            <table class="bggrey percent100">'
	pcp_start_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="large18 center">'
	echo '                  <input class="large12" type="submit" value="Next >">'
	echo '                  <input type="hidden" name="ACTION" value="install">'
	echo '                  <input type="hidden" name="VERSION" value="'$VERSION'">'
	echo '                  <input type="hidden" name="CORE" value="'$CORE'">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Press the [ Next > ] button to install the update files.</p>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </table>'
	echo '          </form>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
fi

#========================================================================================
# Install
#----------------------------------------------------------------------------------------
if [ "$ACTION" = "install" ] && [ "$FAIL_MSG" = "ok" ] ; then
	pcp_incr_id
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>piCorePlayer insitu update</legend>'
	echo '          <form name="install" action= "'$0'" method="get">'
	echo '            <table class="bggrey percent100">'
	pcp_start_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td>'
	echo '                  <textarea class="inform" style="height:130px">'
	                          [ "$FAIL_MSG" = "ok" ] && pcp_install_boot_files
	echo '                  </textarea>'
	echo '                </td>'
	echo '              </tr>'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td>'
	echo '                  <p></p>'
	echo '                </td>'
	echo '              </tr>'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td>'
	echo '                  <textarea class="inform" style="height:130px">'
	echo                      '[ INFO ] Installing tce extensions...'
	                          [ "$FAIL_MSG" = "ok" ] && pcp_install_tce_files
	echo '                  </textarea>'
	echo '                </td>'
	echo '              </tr>'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td>'
	echo '                  <p></p>'
	echo '                </td>'
	echo '              </tr>'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td>'
	echo '                  <textarea class="inform" style="height:130px">'
	echo                      '[ INFO ] Installing mydata and backup files...'
	                          [ "$FAIL_MSG" = "ok" ] && pcp_finish_install
	echo '                  </textarea>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </table>'
	echo '          </form>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
fi

pcp_html_end

exit 0
