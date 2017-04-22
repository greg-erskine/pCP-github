#!/bin/sh

# Version 3.20 2017-04-22
#	Updates for new Repo and Newer kernels

# Version 3.10 2016-12-26
#	Changes for shairport-sync.  Incomplete PH
#	Sourceforge repo changes. PH

# Version 3.02 2016-09-04 PH
#	Updated Kernel Information for 3.02 piCore8.0 Release
#	Removed pcp-load, as 3.00 and on had the updated file.  Not needed for pcp 2.xx

# Version 3.00 2016-08-09 PH
#	Add Download new Kernel modules, for all current existing Modules

# Version 2.06 2016-06-17 PH
#	Added Copy entire update /sbin directory to location (pcp-load), Bootfix, and changed bootlocal.sh processing.
#	Added oldpiversion.cfg to allow bootfix to know what the old version was.

# Version 2.05 2016-04-17 SBP
#	Currently a copy of the old insitu_update.cgi.

. /etc/init.d/tc-functions
. pcp-functions

pcp_html_head "Update pCP" "GE"

pcp_banner
pcp_navigation
pcp_running_script
pcp_httpd_query_string

WGET="/bin/busybox wget -T 30"
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
#INSITU_DOWNLOAD="http://picoreplayer.sourceforge.net/insitu"  #<----- defined in pcp-functions otherwise the beta testing does not work

#========================================================================================
#      382 - insitu.cfg
# 21044878 - piCorePlayer2.00_boot.tar.gz
# 14932349 - piCorePlayer2.00_tce.tar.gz
# --------
# 35977609 bytes
#----------------------------------------------------------------------------------------
#SPACE_REQUIRED=$((35977609 * 2 / 1000))
case "${VERSION}" in
	piCorePlayer3.20*)
		SPACE_REQUIRED=12000
		BOOT_SIZE_REQUIRED=25500
	;;
	*)
		SPACE_REQUIRED=15000
		BOOT_SIZE_REQUIRED=27000
	;;
esac

#========================================================================================
# DEBUG info showing variables
#----------------------------------------------------------------------------------------
pcp_debug_info() {
	echo '<p class="debug">[ DEBUG ] QUERY_STRING: '$QUERY_STRING'<br />'
	echo '                 [ DEBUG ] ACTION: '$ACTION'<br />'
	echo '                 [ DEBUG ] VERSION: '$VERSION'<br />'
	echo '                 [ DEBUG ] UPD_PCP: '$UPD_PCP'<br />'
	echo '                 [ DEBUG ] INSITU_DOWNLOAD: '$INSITU_DOWNLOAD'<br />'
	echo '                 [ DEBUG ] SPACE_REQUIRED: '$SPACE_REQUIRED'<br />'
	echo '                 [ DEBUG ] BOOT_SPACE_REQUIRED: '$BOOT_SIZE_REQUIRED'<br />'
	echo '                 [ DEBUG ] BOOT_SIZE: '$BOOT_SIZE'</p>'
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
# Check we have sourceforge access - set FAIL_MSG if not accessible
#----------------------------------------------------------------------------------------
pcp_sourceforge_indicator() {
	if [ $(pcp_sourceforge_accessible) -eq 0 ]; then
		SOURCEFORGE_STATUS="Sourceforge repository accessible."
	else
		SOURCEFORGE_STATUS="Sourceforge repository not accessible!!"
		FAIL_MSG="Sourceforge not accessible!!"
	fi
}

#========================================================================================
# Check for extension - display reload extension warning message
#----------------------------------------------------------------------------------------
pcp_check_for_extension() {
	EXTENSION=$1
	if [ -f "/usr/local/tce.installed/${EXTENSION}" ]; then
		echo '[ WARN ] *** You may need to REINSTALL '$EXTENSION' ***'
	fi
}

pcp_check_for_all_extensions() {
	pcp_check_for_extension jivelite
	pcp_check_for_extension shairport-sync
	pcp_check_for_extension alsaequal
	pcp_check_for_extension slimserver
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
# Download a list of piCorePlayer versions that are available on Sourceforge - insitu.cfg
#----------------------------------------------------------------------------------------
pcp_get_insitu_cfg() {
	echo '[ INFO ] Step 3. - Downloading insitu.cfg...'
	$WGET ${INSITU_DOWNLOAD}/insitu.cfg -O ${UPD_PCP}/insitu.cfg
	if [ $? -eq 0 ]; then
		echo '[  OK  ] Successfully downloaded insitu.cfg'
	else
		echo '[ ERROR ] Error downloading insitu.cfg'
		FAIL_MSG="Error downloading insitu.cfg"
	fi
}

pcp_uudecode (){
# uudecode in GNU awk (and some others, like OpenBSD) decodes stdin to stdout
#
# Copyright (c) 2014, Rafael Kitover <rkitover@gmail.com>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDER ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

awk=awk

if command -v gawk >/dev/null; then
	awk=gawk
fi

$awk '
BEGIN {
    charset=" !\"#$%&'\''()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_";
}
function charval(char) {
    return index(charset, char) + 32 - 1;
}
/^begin / { next }
/^end$/   { exit }
{
    cnt = substr($0, 1, 1);
    if (cnt == "`") next;
    cnt = charval(cnt) - 32;
    enc = substr($0, 2, length($0) - 1);
    chars = 0;
    pos   = 1;
    while (chars < cnt) {
        grp = substr(enc, pos, 4);
        gsub(/`/, " ", grp); # zero bytes
        c1 = charval(substr(grp, 1, 1)) - 32;
        c2 = charval(substr(grp, 2, 1)) - 32;
        c3 = charval(substr(grp, 3, 1)) - 32;
        c4 = charval(substr(grp, 4, 1)) - 32;
        chars_bits = or(c4, or(or(lshift(c3, 6), lshift(c2, 12)), lshift(c1, 18)));
        char[1] = sprintf("%c", rshift(and(chars_bits, 16711680), 16));
        char[2] = sprintf("%c", rshift(and(chars_bits, 65280),     8));
        char[3] = sprintf("%c", and(chars_bits, 255));
        for (i = 1; i <= 3 && chars < cnt; i++) {
            printf("%s", char[i]);
            chars++;
        }
        pos += 4;
    }
}
'
}

#========================================================================================
# Download kernel modules for new kernel
#----------------------------------------------------------------------------------------
pcp_get_kernel_modules() {
#	Update pcp-load if needed  (This is not needed right now, but left this in for reference
#	grep -q "Version 3.00" /usr/local/sbin/pcp-load
#	if [ $? -ne 0 ]; then
#		# Need to Update pcp-load
#		MATCH=$(grep -n '^PAYLOAD:$' $0 | cut -d ':' -f 1)
#		PAYLOAD_START=$((MATCH+1))
#		tail -n +$PAYLOAD_START $0 | pcp_uudecode > /tmp/new-pcp-load
#		chmod 755 /tmp/new-pcp-load
#		cp -f /tmp/new-pcp-load /usr/local/sbin/pcp-load
#	fi
	case "${VERSION}" in
		piCorePlayer2.06)
			# Set the below for the new kernel
			KUPDATE=1
			NEWKERNELVER=4.1.20
			PICOREVERSION=7.x
		;;
		piCorePlayer3.00*)
			# Set the below for the new kernel
			KUPDATE=1
			NEWKERNELVER=4.4.15
			PICOREVERSION=8.x
		;;
		piCorePlayer3.02*)
			# Set the below for the new kernel
			KUPDATE=1
			NEWKERNELVER=4.4.20
			PICOREVERSION=8.x
		;;
		piCorePlayer3.20*)
			# Set the below for the new kernel
			KUPDATE=1
			NEWKERNELVER=4.9.21
			PICOREVERSION=8.x
			NEWKERNELVERCORE="${NEWKERNELVER}-${CORE%+}"
		;;
		*)  KUPDATE=0
		;;
	esac
	if [ $KUPDATE -eq 1 ]; then
		PCP_REPO="http://picoreplayer.sourceforge.net/tcz_repo"
#		[ -f /opt/tcemirror ] && read -r TCE_REPO < /opt/tcemirror || TCE_REPO="http://repo.tinycorelinux.net/"
		CURRENTKERNEL=$(uname -r)
		CURRENTKERNELCORE=$(uname -r | cut -d '-' -f2)
		BUILD=$(getBuild)
		case $BUILD in
			armv7) NEWKERNEL="${NEWKERNELVERCORE}_v7";;
			armv6) NEWKERNEL="${NEWKERNELVERCORE}";;
		esac
		PCP_DL="${PCP_REPO%/}/${PICOREVERSION}/${BUILD}/tcz"
		echo '[ INFO ] PCP_DL='$PCP_DL
		# Do a space check based on current kernel modules installed, then doubled for safety
		MODSIZE=0
		for I in $(ls /mnt/mmcblk0p2/tce/optional/*${CURRENTKERNELCORE}*.tcz | grep $CURRENTKERNEL); do
			MODSIZE=$((MODSIZE+$(du -k $I | awk '{print $1}')))
		done
		pcp_enough_free_space $((MODSIZE * 2))
		if [ "$FAIL_MSG" = "ok" ]; then
			# Get list of kernel modules matching current kernel
			ls /mnt/mmcblk0p2/tce/optional/*${CURRENTKERNELCORE}*.tcz | grep $CURRENTKERNEL | sed -e 's|[-][0-9].[0-9].*||' | sed 's/.*\///' > /tmp/current
			# Get list of kernel modules not matching current kernel
			ls /mnt/mmcblk0p2/tce/optional/*${CURRENTKERNELCORE}*.tcz | grep $NEWKERNEL | sed -e 's|[-][0-9].[0-9].*||' | sed 's/.*\///' > /tmp/newk
			#Remove Backlight from Modules list, it does not exist anymore
			sed -i '/backlight/d' /tmp/current
			# Show the old modules that do not have a current kernel version.
			MODULES=$(comm -1 -3 /tmp/newk /tmp/current)
			echo '[ INFO ] Downloading new kernel modules: '$MODULES
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
# Download the boot files from Sourceforge
#----------------------------------------------------------------------------------------
pcp_get_boot_files() {
	echo '[ INFO ] Step 4A. - Downloading '${VERSION}${AUDIOTAR}'_boot.tar.gz'
	echo '[ INFO ] Download Location link: '${INSITU_DOWNLOAD}'/'${VERSION}'/'${VERSION}${AUDIOTAR}'_boot.tar.gz'
	echo '[ INFO ] This will take a few minutes. Please wait...'
	$WGET ${INSITU_DOWNLOAD}/${VERSION}/${VERSION}${AUDIOTAR}_boot.tar.gz -O ${UPD_PCP}/boot/${VERSION}${AUDIOTAR}_boot.tar.gz 2>&1
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
	pcp_mount_mmcblk0p1_nohtml

	# Delete all files from the boot partition
	sudo rm -rf /mnt/mmcblk0p1/*
	[ $? -eq 0 ] || FAIL_MSG="Error deleting files /mnt/mmcblk0p1/*"

	pcp_save_configuration

	# Untar the boot files
	echo '[ INFO ] Untarring '${VERSION}${AUDIOTAR}'_boot.tar.gz...'
	[ "$FAIL_MSG" = "ok" ] && sudo tar -zxvf ${UPD_PCP}/boot/${VERSION}${AUDIOTAR}_boot.tar.gz -C /mnt/mmcblk0p1/
	if [ $? -eq 0 ]; then
		echo '[  OK  ] Successfully untarred boot tar.'
	else
		echo '[ ERROR ] Error untarring boot tar. Result: '$?
		FAIL_MSG="Error untarring boot tar."
	fi

	pcp_umount_mmcblk0p1_nohtml
}

#=========================================================================================
# Save configuration files to the boot partiton
#-----------------------------------------------------------------------------------------
pcp_save_configuration() {
	echo '[ INFO ] Saving configuration files.'
	sudo cp -f /usr/local/sbin/config.cfg /mnt/mmcblk0p1/newconfig.cfg
	[ $? -eq 0 ] || FAIL_MSG="Error saving piCorePlayer configuration file."
	sudo dos2unix -u /mnt/mmcblk0p1/newconfig.cfg
	[ $? -eq 0 ] || FAIL_MSG="Error saving piCorePlayer configuration file."
	#save the current piversion to determine potential bootfix(es) later
	. /usr/local/sbin/piversion.cfg
	[ -e /mnt/mmcblk0p1/oldpiversion.cfg ] && rm -f /mnt/mmcblk0p1/oldpiversion.cfg
	echo "OLDPIVERS=\"$PIVERS\"" > /mnt/mmcblk0p1/oldpiversion.cfg
	[ $? -eq 0 ] || FAIL_MSG="Error saving current piCorePlayer version."

	[ "$FAIL_MSG" = "ok" ] && echo '[  OK  ] Your configuration files have been saved to the boot partition.'
}

#========================================================================================
# Download the tce files from Sourceforge
#----------------------------------------------------------------------------------------
pcp_get_tce_files() {
	echo '[ INFO ] Step 4B. - Downloading '${VERSION}${AUDIOTAR}'_tce.tar.gz'
	echo '[ INFO ] Download Location link: '${INSITU_DOWNLOAD}'/'${VERSION}'/'${VERSION}${AUDIOTAR}'_tce.tar.gz'
	echo '[ INFO ] This will take a few minutes. Please wait...'
	$WGET ${INSITU_DOWNLOAD}/${VERSION}/${VERSION}${AUDIOTAR}_tce.tar.gz -O ${UPD_PCP}/tce/${VERSION}${AUDIOTAR}_tce.tar.gz 2>&1
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
#	[ "$FAIL_MSG" = "ok" ] && sudo tar -zxvf ${UPD_PCP}/tce/${VERSION}${AUDIOTAR}_tce.tar.gz mnt/mmcblk0p2/tce/optional -C /
	[ "$FAIL_MSG" = "ok" ] && sudo tar -zxvf ${UPD_PCP}/tce/${VERSION}${AUDIOTAR}_tce.tar.gz ./optional -C /mnt/mmcblk0p2/tce
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
	# Unpack the tce.tar and the new mydata.tgz and then copy the content from the new version to the correct locations
	sudo mkdir -p ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce
	sudo tar zxvf ${UPD_PCP}/tce/${VERSION}${AUDIOTAR}_tce.tar.gz -C ${UPD_PCP}/mydata
	sudo tar zxvf ${UPD_PCP}/mydata/mydata.tgz -C ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce

	# Move Bootfix into location if it is present
	if [ -f "${UPD_PCP}/mydata/bootfix/bootfix.sh" ]; then
		sudo cp -Rf ${UPD_PCP}/mydata/bootfix/ /mnt/mmcblk0p2/tce/
		chmod 755 /mnt/mmcblk0p2/tce/bootfix/*
	fi

	# Track and include user made changes to onboot.lst. It is also needed as different versions of piCorePlayer may have different needs.
	# So check that the final onboot contains all from the new version and add eventual extra from the old
	sudo chown tc:staff /mnt/mmcblk0p2/tce/onboot.lst
	echo "content of mnt onboot.lst before:"; cat /mnt/mmcblk0p2/tce/onboot.lst
	sudo cat /mnt/mmcblk0p2/tce/onboot.lst >> ${UPD_PCP}/mydata/onboot.lst
	sort -u ${UPD_PCP}/mydata/onboot.lst > /mnt/mmcblk0p2/tce/onboot.lst
	echo "content of tmp onboot.lst:"; cat ${UPD_PCP}/mydata/onboot.lst
	sudo chown tc:staff /mnt/mmcblk0p2/tce/onboot.lst
	sudo chmod u=rwx,g=rwx,o=rx /mnt/mmcblk0p2/tce/onboot.lst
	case "${VERSION}" in
		piCorePlayer3.20*)
			#pcp3.20 pcp.tcz handles all pcp dependencies (non-wifi)
			echo "Removing old boot extensions from onboot.lst:"
			sed -i '/busybox-httpd.tcz/d' /mnt/mmcblk0p2/tce/onboot.lst
			sed -i '/alsa.tcz/d' /mnt/mmcblk0p2/tce/onboot.lst
			sed -i '/openssh.tcz/d' /mnt/mmcblk0p2/tce/onboot.lst
			sed -i '/dialog.tcz/d' /mnt/mmcblk0p2/tce/onboot.lst
			sed -i '/alsa-utils.tcz/d' /mnt/mmcblk0p2/tce/onboot.lst
			sed -i '/pcp-squeezelite.tcz/d' /mnt/mmcblk0p2/tce/onboot.lst
		;;
	esac
	echo "content of mnt onboot.lst after:"; cat /mnt/mmcblk0p2/tce/onboot.lst

	# Track and include user made changes to .filetool.lst It is important as user might have modified filetool.lst.
	# So check that the final .filetool.lst contains all from the new version and add eventual extra from the old
	sudo chown root:staff /opt/.filetool.lst
	sudo cat /opt/.filetool.lst >> ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce/opt/.filetool.lst
	sort -u ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce/opt/.filetool.lst > /opt/.filetool.lst
	sudo chown root:staff /opt/.filetool.lst
	sudo chmod u=rw,g=rw,o=r /opt/.filetool.lst
	case "${VERSION}" in
		piCorePlayer3.20*)
			#pcp3.20 moved pcp-load, setup and pcp to pcp-base.tcz
			sed -i 'usr\/local\/sbin\/setup/d' /opt/.filetool.lst
			sed -i 'usr\/local\/sbin\/pcp/d' /opt/.filetool.lst
			sed -i 'usr\/local\/sbin\/pcp-load/d' /opt/.filetool.lst
		;;
	esac
	
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
            outfile.write("/home/tc/www/cgi-bin/do_rebootstuff.sh 2>&1 | tee -a /var/log/pcp_boot.log\n")
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

	case "${VERSION}" in
		piCorePlayer3.20*)
			#pcp3.20 made a change in card configs to shini, remove all old card conf files
			rm -f /usr/local/etc/pcp/cards/*
		;;
	esac

	# Update pCP by copying the content from the new version to the correct location followed by a backup
	sudo cp -af ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce/etc/motd /etc/motd
	sudo cp -af ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce/etc/modprobe.conf /etc/modprobe.conf
	sudo cp -af ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce/etc/sysconfig/wifi-wpadrv /etc/sysconfig/wifi-wpadrv
	sudo cp -Rf ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce/home/tc/www/ /home/tc/

	sudo cp -af ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce/home/tc/.local/bin/.pbtemp /home/tc/.local/bin/.pbtemp
	sudo cp -af ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce/home/tc/.local/bin/copywww.sh /home/tc/.local/bin/copywww.sh
	sudo cp -af ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce/usr/local/etc/pointercal /usr/local/etc/pointercal
	sudo cp -Rf ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce/usr/local/etc/init.d/ /usr/local/etc/
	sudo cp -Rf ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce/usr/local/etc/pcp/ /usr/local/etc/
	sudo cp -Rf ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce/usr/local/sbin/ /usr/local/

	sudo chown -R tc:staff /home/tc/www
	sudo chmod u=rwx,g=rx,o= /home/tc/www/cgi-bin/*
	sudo chmod u=rw,g=r,o= /home/tc/www/css/*
	sudo chmod u=rw,g=r,o= /home/tc/www/images/*
	sudo chmod u=rw,g=r,o= /home/tc/www/js/*
	sudo chmod u=rw,g=r,o= /home/tc/www/index.html
	sudo chown tc.staff /usr/local/etc/pcp/cards/*
	sudo chmod u=rw,g=rw,o=r /usr/local/etc/pcp/cards/*

	# Backup changes to make a new mydata.tgz containing an updated version
	pcp_backup_nohtml
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
	echo '          <legend>Warning</legend>'
	echo '          <table class="bggrey percent100">'
	echo '            <tr class="warning">'
	echo '              <td>'
	echo '                <p style="color:white"><b>Warning:</b> Assume an insitu update will overwrite ALL the data on your SD card.</p>'
	echo '                <ul>'
	echo '                  <li style="color:white">Any additional extensions may need to be reinstalled i.e. LMS, jivelite, shairport-sync, alsaequal.</li>'
	echo '                  <li style="color:white">Any user modified or added files may be lost.</li>'
	echo '                  <li style="color:white">An insitu update requires about 50% free space.</li>'
	echo '                  <li style="color:white">Boot files config.txt and cmdline.txt will be overwritten.</li>'
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
# Generate staus message and finish html page
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
		STRING1='Not enough space. Press OK to start expanding your partition or Cancel to abort'
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
		STEP="Step 3 - Downloading available versions"
		pcp_warning_message
		pcp_internet_indicator
		[ "$FAIL_MSG" = "ok" ] || pcp_html_end
		pcp_sourceforge_indicator
		[ "$FAIL_MSG" = "ok" ] || pcp_html_end
		pcp_create_download_directory
		[ "$FAIL_MSG" = "ok" ] || pcp_html_end
	;;
	download)
		STEP="Step 4 - Downloading files"
		pcp_warning_message
	;;
	install)
		STEP="Step 5 - Installing files"
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
if [ "$ACTION" = "initial" ]; then
	echo '[ INFO ] '$INTERNET_STATUS
	echo '[ INFO ] '$SOURCEFORGE_STATUS
	[ "$FAIL_MSG" = "ok" ] && pcp_get_insitu_cfg
fi
#----------------------------------------------------------------------------------------
if [ "$ACTION" = "download" ]; then
	echo '[ INFO ] You are downloading '${VERSION}
	echo '[ INFO ] You are currently using piCorePlayer'$(pcp_picoreplayer_version)

	case "${VERSION}" in
		piCorePlayer3.*)  # For a 3.x insitu update to be permitted must be at least pcp 3.00
			VVV=$(pcp_picoreplayer_version)
			[ $(printf  "%.0f" ${VVV:0:4}) -lt 3 ] && FAIL_MSG="You must be using 3.00 or higher to update"
		;;
	esac
	BOOT_SIZE=$(/bin/busybox fdisk -l | grep mmcblk0p1 | tr -s " " | cut -d " " -f4 | tr -d +)
	echo '[ INFO ] Boot partition size required: '${BOOT_SIZE_REQUIRED}'. Boot partition size is: '${BOOT_SIZE}
	if [ "$FAIL_MSG" = "ok" -a $BOOT_SIZE -lt $BOOT_SIZE_REQUIRED ]; then
		FAIL_MSG="BOOT disk is not large enough, upgrade not possible"
	fi
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
# Initial
#----------------------------------------------------------------------------------------
case $(uname -r) in
	*pcpAudioCore*) PCPAUDIOCOREyes="checked";PCPCOREyes="";;
	*) PCPCOREyes="checked";PCPAUDIOCORE="";;
esac
COL1=75
COL2=200
if [ "$ACTION" = "initial" ] && [ "$FAIL_MSG" = "ok" ] ; then
	pcp_incr_id
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>piCorePlayer insitu update: Select Kernel Type and Version</legend>'
	echo '          <table class="bggrey percent100">'
	echo '            <form name="initial" action= "'$0'" method="get">'
	pcp_start_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column'$COL1' center">'
	echo '                  <input class="small1" type="radio" name="CORE" value="pcpCore" '$PCPCOREyes'>'
	echo '                </td>'
	echo '                <td class="column'$COL2'">'
	echo '                  <p>Standard version:</p>'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>pcpCore Kernel&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>This version uses the kernel code and config from <a href="https://github.com/raspberrypi/linux">Raspberry Pi</a>.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column'$COL1' center">'
	echo '                  <input class="small1" type="radio" name="CORE" value="pcpAudioCore" '$PCPAUDIOCOREyes'>'
	echo '                </td>'
	echo '                <td class="column'$COL2'">'
	echo '                  <p>Audio enthusiast version:</p>'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>pcpAudioCore Kernel&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>This version starts with the same kernel code from <a href="https://github.com/raspberrypi/linux">Raspberry Pi</a>.</p>'
	echo '                    <p>The kernel is then patched with extra drivers and modifications to support additional custom DACs and higher sample rates.</p>'
	echo '                    <p>This version should not be used with WIFI.  Some wifi chips are known to not work with this version</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="large18 center">'
	echo '                  <select name="VERSION">'
	                          awk '{ print "<option value=\""$1"\">" $1"</option>" }' ${UPD_PCP}/insitu.cfg
	echo '                  </select>'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Select the update version of piCorePlayer required.</p>'
	echo '                </td>'
	echo '              </tr>'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="large18 center">'
	echo '                  <input class="large12" type="submit" value="Next >">'
	echo '                  <input type="hidden" name="ACTION" value="download">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Press the [ Next ] button to download update files.</p>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
fi

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
	echo '          <table class="bggrey percent100">'
	echo '            <form name="download" action= "'$0'" method="get">'
	pcp_start_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="large18 center">'
	echo '                  <input class="large12" type="submit" value="Next >">'
	echo '                  <input type="hidden" name="ACTION" value="install">'
	echo '                  <input type="hidden" name="VERSION" value="'$VERSION'">'
	echo '                  <input type="hidden" name="CORE" value="'$CORE'">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Press the [ Next ] button to install the update files.</p>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
	echo '          </table>'
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
	echo '          <table class="bggrey percent100">'
	echo '            <form name="install" action= "'$0'" method="get">'
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
	echo '            </form>'
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
fi

pcp_html_end

exit 0
