#!/bin/sh

# Version: 5.0.0 2019-05-21

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

function version { echo "$@" | awk -F. '{ printf("%d%03d%03d%03d\n", $1,$2,$3,$4); }'; }

# Parse out numerical versions of upgrade version (comes from query string)...
VERS=$(echo "$VERSION" | awk -F'piCorePlayer' '{ print $2 }' | cut -d '-' -f1)
MAJOR_VERSION=$(echo "$VERS" | cut -d '.' -f1)
vtmp=$(echo "$VERS" | cut -d '.' -f2)
MINOR_VERSION=${vtmp:0:2}
vtmp=$(echo "$VERS" | cut -d '.' -f3)
PATCH_VERSION=$(echo "$vtmp" | cut -d '-' -f1)

#========================================================================================
#      382 - insitu.cfg
# 21044878 - piCorePlayer2.00_boot.tar.gz
# 14932349 - piCorePlayer2.00_tce.tar.gz
# --------
# 35977609 bytes
#----------------------------------------------------------------------------------------
#SPACE_REQUIRED=$((35977609 * 2 / 1000))
BUILD=$(getBuild)
case "${VERSION}" in
	piCorePlayer5.0.*)
		SPACE_REQUIRED=12000
		BOOT_SIZE_REQUIRED=27700
		#These are used for sed modification of config.txt
		CNF_INITRD="pcp_10.1"
		CNF_KERNEL="kernel41940"
		# Set the below for downloading new kernel modules
		KUPDATE=1
		case $CORE in
			*pcpAudioCore*) NEWKERNELVER="4.19.40-rt19";;
			*) NEWKERNELVER="4.19.40";;
		esac
		PICOREVERSION="10.x"
		NEWKERNELVERCORE="${NEWKERNELVER}-${CORE%+}"
	;;
	*)
		SPACE_REQUIRED=15000
		BOOT_SIZE_REQUIRED=27800
		KUPDATE=0
	;;
esac
case $BUILD in
	armv7) NEWKERNEL="${NEWKERNELVERCORE}_v7";;
	armv6) NEWKERNEL="${NEWKERNELVERCORE}";;
esac



#========================================================================================
# DEBUG info showing variables
#----------------------------------------------------------------------------------------
pcp_debug_info() {
	pcp_debug_variables "html" QUERY_STRING ACTION VERSION UPD_PCP INSITU_DOWNLOAD SPACE_REQUIRED BOOT_SIZE_REQUIRED BOOT_SIZE
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
		PCP_REPO="https://repo.picoreplayer.org/repo"
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

			if [ $(version $OLDPCPVERSION) -lt $(version "5.0.0") ]; then
					#irda changes to media-rc in >4.2.0
					sed -i 's/irda/media-rc/' /tmp/current
			fi

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
	echo '[ INFO ] Step 3C. - Downloading '${VERSION}${AUDIOTAR}'_boot.tar.gz'
	echo '[ INFO ] Download Location link: '${INSITU_DOWNLOAD}'/'${VERSION}'/'${VERSION}${AUDIOTAR}'_boot.tar.gz'
	echo '[ INFO ] This will take a few minutes. Please wait...'
	$WGET_IUS2 ${INSITU_DOWNLOAD}/${VERSION}/${VERSION}${AUDIOTAR}_boot.tar.gz -O ${UPD_PCP}/boot/${VERSION}${AUDIOTAR}_boot.tar.gz 2>&1
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
		find ${BOOTMNT} | grep -E "(kernel|pcp_|\.dtb)" | xargs rm -f
		[ $? -eq 0 ] || FAIL_MSG="Error deleting files from ${BOOTMNT}"

		pcp_save_configuration
	fi
	if [ "$FAIL_MSG" = "ok" ]; then
		# Untar the boot files
		echo '[ INFO ] Untarring '${VERSION}${AUDIOTAR}'_boot.tar.gz...'
		#config.txt and cmdline.txt should not be in insitu archive, but just incase, exlude them.
		tar --exclude config.txt --exclude cmdline.txt -xvf ${UPD_PCP}/boot/${VERSION}${AUDIOTAR}_boot.tar.gz -C ${BOOTMNT}/ 2>&1
		TST=$?
		if [ $TST -eq 0 ]; then
			echo '[  OK  ] Successfully untarred boot tar.'
		else
			echo '[ ERROR ] Error untarring boot tar. Result: '$TST
			FAIL_MSG="Error untarring boot tar."
		fi
	fi

	#We are not replacing the current config.txt and cmdline.txt, so make appropriate updates.
	if [ "$FAIL_MSG" = "ok" ]; then
		sed -i -r "s/^initramfs pcp_[0-9]{1,2}\.[0-9]/initramfs ${CNF_INITRD}/g" ${BOOTMNT}/config.txt
		[ $? -eq 0 ] || FAIL_MSG="Error updating config.txt"
		sed -i -r "s/^kernel kernel[0-9]{4,7}/kernel ${CNF_KERNEL}/g" ${BOOTMNT}/config.txt
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
	local V
	echo '[ INFO ] Saving configuration files.'
	[ -r /usr/local/etc/pcp/pcp.cfg ] && sudo cp -f /usr/local/etc/pcp/pcp.cfg ${BOOTMNT}/newpcp.cfg
	sudo dos2unix -u ${BOOTMNT}/newpcp.cfg
	[ $? -eq 0 ] || FAIL_MSG="Error saving piCorePlayer configuration file."
	#save the current pcpversion to determine potential bootfix(es) later  
	[ -r $PCPVERSIONCFG ] && . $PCPVERSIONCFG
	[ -e ${BOOTMNT}/oldpcpversion.cfg ] && rm -f ${BOOTMNT}/oldpcpversion.cfg
	echo "OLDPCPVERS=\"$V\"" > ${BOOTMNT}/oldpcpversion.cfg;
	[ "$FAIL_MSG" = "ok" ] && echo '[  OK  ] Your configuration files have been saved to the boot partition.'
}

#========================================================================================
# Download the tce files from Repo
#----------------------------------------------------------------------------------------
pcp_get_tce_files() {
	echo '[ INFO ] Step 3B. - Downloading '${VERSION}${AUDIOTAR}'_tce.tar.gz'
	echo '[ INFO ] Download Location link: '${INSITU_DOWNLOAD}'/'${VERSION}'/'${VERSION}${AUDIOTAR}'_tce.tar.gz'
	echo '[ INFO ] This will take a few minutes. Please wait...'
	$WGET_IUS2 ${INSITU_DOWNLOAD}/${VERSION}/${VERSION}${AUDIOTAR}_tce.tar.gz -O ${UPD_PCP}/tce/${VERSION}${AUDIOTAR}_tce.tar.gz 2>&1
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
	echo '[ INFO ] Untarring '${VERSION}${AUDIOTAR}'_tce.tar.gz...'
	[ "$FAIL_MSG" = "ok" ] && sudo tar -zxvf ${UPD_PCP}/tce/${VERSION}${AUDIOTAR}_tce.tar.gz ./optional -C /etc/sysconfig/tcedir
	if [ $? -eq 0 ]; then
		[ $DEBUG -eq 1 ] && echo '[ DEBUG ] tce tar result: '$?
		echo '[  OK  ] Successfully untarred tce tar.'
	else
		echo '[ ERROR ] Error untarring tce tar. Result: '$?
		FAIL_MSG="Error untarring tce tar."
	fi
}

#========================================================================================
# Finish the install process
#----------------------------------------------------------------------------------------
pcp_finish_install() {
	OLDPCPVERSION=$(pcp_picoreplayer_version)
	# Unpack the tce.tar and the new mydata.tgz and then copy the content from the new version to the correct locations
	sudo mkdir -p ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce
	sudo tar zxvf ${UPD_PCP}/tce/${VERSION}${AUDIOTAR}_tce.tar.gz -C ${UPD_PCP}/mydata
	sudo tar zxvf ${UPD_PCP}/mydata/mydata.tgz -C ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce

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

	if [ $(version $OLDPCPVERSION) -lt $(version "5.0.0") ]; then
		sed -i 's/firmware-rpi3-wireless/firmware-rpi-wifi/' $ONBOOTLST
		rm -f ${PACKAGEDIR}/firmware-rpi3-wireless.*
	fi

	echo "[ INFO ] content of mnt onboot.lst after:"; cat $ONBOOTLST

	# Track and include user made changes to .filetool.lst It is important as user might have modified filetool.lst.
	# So check that the final .filetool.lst contains all from the new version and add eventual extra from the old
	sudo chown root:staff /opt/.filetool.lst
	sudo cat /opt/.filetool.lst >> ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce/opt/.filetool.lst
	sort -u ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce/opt/.filetool.lst > /opt/.filetool.lst
	sudo chown root:staff /opt/.filetool.lst
	sudo chmod u=rw,g=rw,o=r /opt/.filetool.lst
	# if [ $MAJOR_VERSION -ge 5 ]; then
		# if [ $MINOR_VERSION -ge 0 ]; then
			# echo "[ INFO ] Updating .filetool.lst :"
		# fi
	# fi

	# Track and include user made changes to .xfiletool.lst It is important as user might have modified filetool.lst.
	# So check that the final .filetool.lst contains all from the new version and add eventual extra from the old
	sudo chown root:staff /opt/.xfiletool.lst
	sudo cat /opt/.xfiletool.lst >> ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce/opt/.xfiletool.lst
	sort -u ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce/opt/.xfiletool.lst > /opt/.xfiletool.lst
	sudo chown root:staff /opt/.xfiletool.lst
	sudo chmod u=rw,g=rw,o=r /opt/.xfiletool.lst

	# Track and include user made changes to bootlocal.sh. It is important as user might have modified bootlocal.sh.
	# We don't make changes to bootlocal.sh that much, so make changes here if needed
	# Do not change indentation.
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
            outfile.write("/home/tc/www/cgi-bin/pcp_startup.sh 2>&1 | tee -a /var/log/pcp_boot.log\n")
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

	# Update pCP by copying the content from the new version to the correct location followed by a backup
	[ -f pcp-powerbutton.sh ] || sudo cp -af ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce/home/pcp-powerbutton.sh /home/tc/pcp-powerbutton.sh
	sudo cp -Rf ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce/home/tc/www/ /home/tc/
	sudo cp -Rf ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce/home/tc/.ashrc /home/tc/.ashrc
	sudo cp -af ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce/home/tc/.local/bin/.pbtemp /home/tc/.local/bin/.pbtemp
	sudo cp -af ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce/home/tc/.local/bin/copywww.sh /home/tc/.local/bin/copywww.sh
	sudo cp -af ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce/usr/local/etc/pointercal /usr/local/etc/pointercal
	sudo cp -Rf ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce/usr/local/etc/pcp/ /usr/local/etc/
	sudo cp -Rf ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce/usr/local/sbin/ /usr/local/

	sudo chown tc:staff /home/tc/pcp-powerbutton.sh
	sudo chown -R tc:staff /home/tc/www
	sudo chmod u=rwx,g=rx,o= /home/tc/www/cgi-bin/*
	sudo chmod u=rw,g=r,o= /home/tc/www/css/*
	sudo chmod u=rw,g=r,o= /home/tc/www/images/*
	sudo chmod u=rw,g=r,o= /home/tc/www/js/*
	sudo chmod u=rw,g=r,o= /home/tc/www/index.html
	sudo chown tc.staff /usr/local/etc/pcp/cards/*
	sudo chmod u=rw,g=rw,o=r /usr/local/etc/pcp/cards/*

	[ ! -f /etc/httpd.conf ] && sudo cp -Rf ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce/etc/httpd.conf /etc/httpd.conf
	
	# Add pcm.pcpinput section to asound.conf
	cat $ASOUNDCONF | grep -q "pcm.pcpinput"
	if [ $? -ne 0 ]; then
		sed -i '/^#---ALSA EQ/i pcm.pcpinput {\n\ttype plug\n\tslave.pcm \"hw:0.0\"\n}\n' $ASOUNDCONF
	fi

	# Backup changes to make a new mydata.tgz containing an updated version
	pcp_backup_nohtml

	if [ $(version $OLDPCPVERSION) -lt $(version "5.0.0") ]; then
		echo '[ INFO ] Updating installed/required extensions.'
		echo "https://repo.picoreplayer.org/repo" > /opt/tcemirror
		echo "10.1pCP" > /usr/share/doc/tc/release.txt

		UPGRADE_LIST="alsaequal.tcz nano.tcz slimserver.tcz pcp-jivelite.tcz pcp-lirc.tcz"
		for UPG in $UPGRADE_LIST; do
			if [ -f ${PACKAGEDIR}/$UPG ]; then
				echo '[ INFO ] '$UPG' found, updating....'
				sudo -u tc pcp-update kernel $NEWKERNEL $UPG
			fi
		done
		for METER in $(PACKAGEDIR/VU_Meter*.tcz); do
			echo '[ INFO ] '$METER' found, updating....'
			sudo -u tc pcp-update $METER
		done
		if [ "$JIVELITE" = "yes" -a "$IR_LIRC" = "yes" ]; then
			sudo -u tc pcp-load -wi pcp-irtools.tcz
		fi
		rm -f /home/tc/.alsaequal.bin
	fi
}

#========================================================================================
# Generate warning message
#----------------------------------------------------------------------------------------
pcp_warning_message() {
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <table class="bggrey percent100">'
	echo '            <tr class="warning">'
	echo '              <td>'
	echo '                <p style="color:white"><b>Warning:</b></p>'
	echo '                <ul>'
	echo '                  <li style="color:white">Assume an insitu update will overwrite ALL the data on your SD card.</li>'
	echo '                  <li style="color:white">Any user modified or added files may be lost or overwritten.</li>'
	echo '                  <li style="color:white">An insitu update requires about 50% free space.</li>'
	echo '                  <li style="color:white">You may need to manually update your plugins, extensions, static IP etc.</li>'
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

	#$(pcp_picoreplayer_version) returns current version
	#${VERS} returns version selected for upgrade.

	if [ $(version $(pcp_picoreplayer_version)) -lt $(version "5.0.0") ]; then
		echo '[ INFO ] Updating extensions with known requirements. This will increase free space required for upgrade.'

		#For 5.0.0, these extensions are upgraded automatically, make sure there is free space.
		if [ -f ${PACKAGEDIR}/alsaequal.tcz ]; then
			echo '[ INFO ] alsaequal found, will be automatically updated.'
			SPACE_REQUIRED=`expr $SPACE_REQUIRED + 300`
		fi
		if [ -f ${PACKAGEDIR}/nano.tcz ]; then
			echo '[ INFO ] nano found, will be automatically updated.'
			SPACE_REQUIRED=`expr $SPACE_REQUIRED + 800`
		fi
		if [ -f ${PACKAGEDIR}/slimserver.tcz ]; then
			echo '[ INFO ] slimserver found, will be automatically updated.'
			SPACE_REQUIRED=`expr $SPACE_REQUIRED + 44000`
		fi
		if [ -f ${PACKAGEDIR}/pcp-jivelite.tcz ]; then
			echo '[ INFO ] pcp-jivelite found, will be automatically updated.'
			VU_SIZE=`expr $(ls -1 ${PACKAGEDIR}/VU_Meter*.tcz | wc -l) \* 475`
			SPACE_REQUIRED=`expr $SPACE_REQUIRED + 10200 + $VU_SIZE`
		fi
		if [ -f ${PACKAGEDIR}/pcp-lirc.tcz ]; then
			echo '[ INFO ] pcp-lirc found, will be automatically updated.'
			SPACE_REQUIRED=`expr $SPACE_REQUIRED + 235`
		fi
	fi

	if [ $(version $(pcp_picoreplayer_version)) -ge $(version "5.0.0") ]; then
		[ $(version $(pcp_picoreplayer_version)) -ge $(version "4.1.2") ] || FAIL_MSG="You must be using 4.1.2 or higher to update. Run Hotfix."
		[ $(version ${VERS}) -lt $(version "5.0.0") ] && FAIL_MSG="Downgrading version is not permitted."
	fi

	BOOT_SIZE=$(/bin/busybox fdisk -l | grep ${BOOTDEV} | sed "s/*//" | tr -s " " | cut -d " " -f6 | tr -d +)
	echo '[ INFO ] Boot partition size required: '${BOOT_SIZE_REQUIRED}'. Boot partition size is: '${BOOT_SIZE}
	if [ "$FAIL_MSG" = "ok" -a $BOOT_SIZE -lt $BOOT_SIZE_REQUIRED ]; then
		FAIL_MSG="BOOT disk is not large enough, upgrade not possible"
	fi
	echo '[ INFO ] Space required for update and extensions: '$SPACE_REQUIRED'k'
	[ "$FAIL_MSG" = "ok" ] && pcp_enough_free_space $SPACE_REQUIRED
	echo '[ INFO ] You are downloading '${VERSION}
	[ "$FAIL_MSG" = "ok" ] && pcp_get_kernel_modules
	[ "$FAIL_MSG" = "ok" ] && pcp_enough_free_space $SPACE_REQUIRED

	[ "$FAIL_MSG" = "ok" ] && pcp_get_boot_files
	[ "$FAIL_MSG" = "ok" ] && pcp_get_tce_files
	[ "$FAIL_MSG" = "ok" ] && pcp_enough_free_space $SPACE_REQUIRED
fi
#----------------------------------------------------------------------------------------
if [ "$ACTION" = "install" ]; then
	echo '[ INFO ] You are installing '$VERSION
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
	echo                      '[ INFO ] Installing tce files...'
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
	echo                      '[ INFO ] Installing tce files...'
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
