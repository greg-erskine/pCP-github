#!/bin/sh

# Version 3.00 2016-07-29 PH
#	Add Download new Kernel modules, for all current existing Modules

# Version 2.06 2016-06-17 PH
#	Added Copy entire update /sbin directory to location (pcp-load), Bootfix, and changed bootlocal.sh processing.
#	Added oldpiversion.cfg to allow bootfix to know what the old version was.

# Version 2.05 2016-04-17 SBP
#	Currently a copy of the old insitu_update.cgi.  

. /etc/init.d/tc-functions
. pcp-functions
pcp_variables

pcp_html_head "Update pCP" "GE"

pcp_banner
pcp_navigation
pcp_running_script
pcp_httpd_query_string

WGET="/bin/busybox wget -T 30"
FAIL_MSG="ok"

# As all the insitu update is done in one file, it may be better to define this here
UPD_PCP="/tmp/pcp_insitu_update"
#INSITU_DOWNLOAD="https://sourceforge.net/projects/picoreplayer/files/insitu"  #<----- defined in pcp-functions otherwise the beta testing does not work

#========================================================================================
#      382 - insitu.cfg
# 21044878 - piCorePlayer2.00_boot.tar.gz
# 14932349 - piCorePlayer2.00_tce.tar.gz
# --------
# 35977609 bytes
#----------------------------------------------------------------------------------------
#SPACE_REQUIRED=$((35977609 * 2 / 1000))
SPACE_REQUIRED=21044

#========================================================================================
# DEBUG info showing variables
#----------------------------------------------------------------------------------------
pcp_debug_info() {
	echo '<p class="debug">[ DEBUG ] QUERY_STRING: '$QUERY_STRING'<br />'
	echo '                 [ DEBUG ] ACTION: '$ACTION'<br />'
	echo '                 [ DEBUG ] VERSION: '$VERSION'<br />'
	echo '                 [ DEBUG ] UPD_PCP: '$UPD_PCP'<br />'
	echo '                 [ DEBUG ] INSITU_DOWNLOAD: '$INSITU_DOWNLOAD'<br />'
	echo '                 [ DEBUG ] SPACE_REQUIRED: '$SPACE_REQUIRED'</p>'
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
	$WGET ${INSITU_DOWNLOAD}/insitu.cfg/download -O ${UPD_PCP}/insitu.cfg
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
	#Update pcp-load if needed
	grep -q "Version 3.00" /usr/local/sbin/pcp-load
	if [ $? -ne 0 ]; then
		# Need to Update pcp-load
		MATCH=$(grep -n '^PAYLOAD:$' $0 | cut -d ':' -f 1)
		PAYLOAD_START=$((MATCH+1))
		tail -n +$PAYLOAD_START $0 | pcp_uudecode > /tmp/new-pcp-load
		chmod 755 /tmp/new-pcp-load
		cp -f /tmp/new-pcp-load /usr/local/sbin/pcp-load
	fi	
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
		*)  KUPDATE=0
			;;
	esac
	if [ $KUPDATE -eq 1 ]; then
		PCP_REPO="https://sourceforge.net/projects/picoreplayer/files/repo"
		TCE_REPO="http://repo.tinycorelinux.net/"
		CURRENTKERNEL=$(uname -r)
		BUILD=$(getBuild)
		case $BUILD in
			armv6) KERNEL="${NEWKERNELVER}-piCore+" ;;
			armv7) KERNEL="${NEWKERNELVER}-piCore_v7+" ;;
			*) FAIL_MSG="Kernel Version Error"
			;;
		esac
		TCE_DL="${TCE_REPO%/}/${PICOREVERSION}/${BUILD}/tcz"
		PCP_DL="${PCP_REPO%/}/${PICOREVERSION}/${BUILD}/tcz"
		echo 'TCE_DL='$TCE_DL
		echo 'PCP_DL='$PCP_DL
		# Get list of kernel modules matching current kernel
		ls /mnt/mmcblk0p2/tce/optional/*piCore*.tcz | grep $CURRENTKERNEL | sed -e 's|[-][0-9].[0-9].*||' | sed 's/.*\///' > /tmp/current
		# Get list of kernel modules not matching current kernel
		ls /mnt/mmcblk0p2/tce/optional/*piCore*.tcz | grep $KERNEL | sed -e 's|[-][0-9].[0-9].*||' | sed 's/.*\///' > /tmp/newk
		# Show the old modules that do not have a current kernel version.
		MODULES=$(comm -1 -3 /tmp/newk /tmp/current)
		echo '[ INFO ] Downloading new kernel modules: '$MODULES
		if [ -z "${MODULES}" ]; then
			echo '[ INFO ] All new Kernel modules for ${KERNEL} already present.'
		else
			for EXT in ${MODULES}; do
				case $EXT in
					irda|backlight|touchscreen) #These are the current PCP extra modules
						sudo -u tc pcp-load -w -u ${PCP_DL} ${EXT}-${KERNEL}.tcz | sed -e 's/<[^>]*>//g'
						[ $? -ne 0 ] && FAIL_MSG="Error downloading new Kernel Modules"
					;;
					*) #Get file from the TC repo
						sudo -u tc pcp-load -w -u ${TCE_DL} ${EXT}-${KERNEL}.tcz | sed -e 's/<[^>]*>//g'
						[ $? -ne 0 ] && FAIL_MSG="Error downloading new Kernel Modules"
					;;
				esac
			done
		fi
	fi
}

#========================================================================================
# Download the boot files from Sourceforge
#----------------------------------------------------------------------------------------
pcp_get_boot_files() {
	echo '[ INFO ] Step 4A. - Downloading '$VERSION'_boot.tar.gz'
	echo '[ INFO ] This will take a few minutes. Please wait...'
	$WGET ${INSITU_DOWNLOAD}/${VERSION}/${VERSION}_boot.tar.gz/download -O ${UPD_PCP}/boot/${VERSION}_boot.tar.gz
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
	echo '[ INFO ] Untarring '${VERSION}'_boot.tar.gz...'
	[ "$FAIL_MSG" = "ok" ] && sudo tar -zxvf ${UPD_PCP}/boot/${VERSION}_boot.tar.gz -C /
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
	echo '[ INFO ] Step 4B. - Downloading '$VERSION'_tce.tar.gz'
	echo '[ INFO ] This will take a few minutes. Please wait...'
	$WGET ${INSITU_DOWNLOAD}/${VERSION}/${VERSION}_tce.tar.gz/download -O ${UPD_PCP}/tce/${VERSION}_tce.tar.gz
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
	# Delete all the kernel specific files in the optional directory - so no stray files are left    <------------Now we need to add a check which kernel-specific files we can delete during the first boot. When the new kernel is in use.
	#sudo rm -rf /mnt/mmcblk0p2/tce/optional/*piCore*.*
	#[ $? -eq 0 ] || FAIL_MSG="Error removing kernel specific files."

	# Untar and update the tzc packages files to optional
	echo '[ INFO ] Untarring '${VERSION}'_tce.tar.gz...'
	[ "$FAIL_MSG" = "ok" ] && sudo tar -zxvf ${UPD_PCP}/tce/${VERSION}_tce.tar.gz mnt/mmcblk0p2/tce/optional -C /

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
	sudo mkdir ${UPD_PCP}/mydata
	sudo tar zxvf ${UPD_PCP}/tce/${VERSION}_tce.tar.gz -C ${UPD_PCP}/mydata
	sudo tar zxvf ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce/mydata.tgz -C ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce
	
	# Move Bootfix into location if it is present
	if [ -f "${UPD_PCP}/mydata/mnt/mmcblk0p2/tce/bootfix/bootfix.sh" ]; then
		sudo cp -Rf ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce/bootfix/ /mnt/mmcblk0p2/tce/
		chmod 755 /mnt/mmcblk0p2/tce/bootfix/*
	fi

	# Track and include user made changes to onboot.lst. It is also needed as different versions of piCorePlayer may have different needs.
	# So check that the final onboot contains all from the new version and add eventual extra from the old
	sudo chown tc:staff /mnt/mmcblk0p2/tce/onboot.lst
	echo "content of mnt onboot.lst before:"; cat /mnt/mmcblk0p2/tce/onboot.lst
	sudo cat /mnt/mmcblk0p2/tce/onboot.lst >> ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce/onboot.lst
	sort -u ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce/onboot.lst > /mnt/mmcblk0p2/tce/onboot.lst
	echo "content of tmp onboot.lst:"; cat ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce/onboot.lst
	echo "content of mnt onboot.lst after:"; cat /mnt/mmcblk0p2/tce/onboot.lst
	sudo chown tc:staff /mnt/mmcblk0p2/tce/onboot.lst
	sudo chmod u=rwx,g=rwx,o=rx /mnt/mmcblk0p2/tce/onboot.lst

	# Track and include user made changes to .filetool.lst It is important as user might have modified filetool.lst.
	# So check that the final .filetool.lst contains all from the new version and add eventual extra from the old
	sudo chown root:staff /opt/.filetool.lst 
	sudo cat /opt/.filetool.lst >> ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce/opt/.filetool.lst
	sort -u ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce/opt/.filetool.lst > /opt/.filetool.lst
	sudo chown root:staff /opt/.filetool.lst
	sudo chmod u=rw,g=rw,o=r /opt/.filetool.lst

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
            outfile.write("/home/tc/www/cgi-bin/do_rebootstuff.sh | tee -a /var/log/pcp_boot.log\n")
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

#	sudo cat /opt/bootlocal.sh >> ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce/opt/bootlocal.sh
#	sort -u ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce/opt/bootlocal.sh > /opt/bootlocal.sh
	sudo chown root:staff /opt/bootlocal.sh
	sudo chmod u=rwx,g=rwx,o=rx /opt/bootlocal.sh

	#update of the config.cfg file is done via newconfig and do_rebootstuff after next reboot as it always have been done

	# Update pCP by copying the content from the new version to the correct location followed by a backup 
	sudo cp -af ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce/etc/motd /etc/motd
	sudo cp -Rf ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce/home/tc/www/ /home/tc/

	sudo cp -af ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce/home/tc/.local/bin/.pbtemp /home/tc/.local/bin/.pbtemp
	sudo cp -af ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce/home/tc/.local/bin/copywww.sh /home/tc/.local/bin/copywww.sh
	sudo cp -af ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce/usr/local/etc/pointercal /usr/local/etc/pointercal
	sudo cp -Rf ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce/usr/local/etc/init.d/ /usr/local/etc/
	sudo cp -Rf ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce/usr/local/sbin/ /usr/local/

	# Copy possible new content from the new untarred tce directory except directories.
	# sudo cp /${UPD_PCP}/mydata/mnt/mmcblk0p2/tce/* /mnt/mmcblk0p2/tce
	# sudo cp -f /home/tc/www/cgi-bin/insitu_update_new.cgi /home/tc/www/cgi-bin/insitu_update.cgi     # This is because otherwise the old version will be used

	sudo chown -R tc:staff /home/tc/www
	sudo chmod u=rwx,g=rx,o= /home/tc/www/cgi-bin/*
	sudo chmod u=rw,g=r,o= /home/tc/www/css/*
	sudo chmod u=rw,g=r,o= /home/tc/www/images/*
	sudo chmod u=rw,g=r,o= /home/tc/www/js/*
	sudo chmod u=rw,g=r,o= /home/tc/www/index.html

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
		#pcp_finish_install
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
	echo '[ INFO ] You are currently using piCorePlayer'$(pcp_picoreplayer_version)
	pcp_enough_free_space $SPACE_REQUIRED
	pcp_check_for_all_extensions
	[ "$FAIL_MSG" = "ok" ] && pcp_get_insitu_cfg
fi
#----------------------------------------------------------------------------------------
if [ "$ACTION" = "download" ]; then
	echo '[ INFO ] You are downloading '$VERSION
	echo '[ INFO ] You are currently using piCorePlayer'$(pcp_picoreplayer_version)
	pcp_enough_free_space $SPACE_REQUIRED
	[ "$FAIL_MSG" = "ok" ] && pcp_get_kernel_modules
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
if [ "$ACTION" = "initial" ] && [ "$FAIL_MSG" = "ok" ] ; then
	pcp_incr_id
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>piCorePlayer insitu update</legend>'
	echo '          <table class="bggrey percent100">'
	echo '            <form name="initial" action= "'$0'" method="get">'
	pcp_start_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="large18">'
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
PAYLOAD:
begin 755 pcp-load
M(R$O8FEN+V)U<WEB;W@@87-H"B,@*&,I(%)O8F5R="!3:&EN9VQE9&5C:V5R
M(#(P,#0M,C`Q,`HC('1C>B!C;VYC97!T(&%N9"!C;V1E(&9R;VT@2F%S;VX@
M5VEL;&EA;7,*(PHC(%9E<G-I;VX@,RXP,"`R,#$V+3`W+3(Y(%!("B,@"7!C
M<"UL;V%D(&UO9&EF:65D('9E<G-I;VX@9F]R('!I0V]R95!L87EE<@HC"4]P
M=&EO;G,@=&\@<W!E8VEF>2!215!/(&%N9"!&=6QL(%!A=&@@;VX@8V]M;6%N
M9"!L:6YE"B,*+B`O971C+VEN:70N9"]T8RUF=6YC=&EO;G,*=7-E0G5S>6)O
M>`IC:&5C:VYO=')O;W0*4%)/1U].04U%/20H8F%S96YA;64@)#`I"DM%4DY%
M3%9%4CTD*'5N86UE("UR*0IU;G-E="!71T54($E.4U1!3$P@0T]064E.4U1!
M3$P@0D]/5$E.1R!/3D1%34%.1"!$3U=.3$]!1%]/3DQ9($Q/041?3TY,62!3
M55!04D534R!215!/"D9/4D-%/2)N(B`@(R!/=F5R=W)I=&4@<WES=&5M(&9I
M;&5S(&1E9F%U;'0@=&\@;F\N(%5S92`M9B!T;R!F;W)C92!O=F5R=W)I=&4N
M"E-!5D5$7T1)4CU@<'=D8`H*3TY"3T]43D%-13TB)"AG971B;V]T<&%R86T@
M;'-T(#(^+V1E=B]N=6QL*2(*6R`M;B`B)$].0D]/5$Y!344B(%T@?'P@3TY"
M3T]43D%-13TB;VYB;V]T+FQS="(*5$-%24Y35$%,3$5$/2]U<W(O;&]C86PO
M=&-E+FEN<W1A;&QE9`I40T5$25(]+V5T8R]S>7-C;VYF:6<O=&-E9&ER"@IA
M8F]R="@I>PH)96-H;R`B5F5R<VEO;B!@=F5R<VEO;F`B.PH)96-H;R`B57-A
M9V4Z("1[4%)/1U].04U%?2!;("UI("UW("UW:2`M=V\@+7=I;"`M:6,@+7=I
M8R`M=VEC;%U[<WT@97AT96YS:6]N<R(*"65C:&\@(B`@+6D@("!,;V%D<R!L
M;V-A;"!E>'1E;G-I;VXB"@EE8VAO("(@("UW("`@1&]W;FQO860@97AT96YS
M:6]N(&]N;'DB"@EE8VAO("(@("UW:2`@1&]W;FQO860@86YD(&EN<W1A;&P@
M97AT96YS:6]N(@H)96-H;R`B("`M=V\@($1O=VYL;V%D(&%N9"!C<F5A=&4@
M86X@;VYD96UA;F0@:71E;2(*"65C:&\@(B`@061D:6YG("UF('1O("UW('=I
M;&P@<F5M;W9E(&-U<G)E;G0@97AT96YS:6]N(&%N9"!F;W)C92!R961O=VYL
M;V%D(@H)96-H;R`B("`M<B![<V5R=F5R(&%D9')E<W,@;V8@<F5P;WTB"@EE
M8VAO("(@($%D9&EN9R`M8R!T;R!A;GD@+6D@;W!T:6]N('=I;&P@9F]R8V4@
M82!O;F4@=&EM92!C;W!Y('1O(&9I;&4@<WES=&5M(@H)96-H;R`B("!!9&1I
M;F<@+6P@=&\@86YY("UI(&]P=&EO;B!I;F1I8V%T97,@;&]A9"!O;FQY("T@
M9&\@;F]T('5P9&%T92!O;F)O;W0@;W(@;VYD96UA;F0B"@EE8VAO("(@($%D
M9&EN9R`M<R!T;R!A;GD@;W!T:6]N('=I;&P@<W5P<')E<W,@3TL@;65S<V%G
M92!U<V5D(&)Y(&%P<',@1U5)(@H)96-H;R`M92`@(EQN17AA;7!L92!U<V%G
M93HB"@EE8VAO("(@3&]A9"!L;V-A;"!E>'1E;G-I;VXZ(@H)96-H;R`B("`@
M)'M04D]'7TY!345]("UI("]M;G0O:&1A,2]T8V4O;W!T:6]N86PO;F%N;RYT
M8WHB"@EE8VAO("(@1&]W;FQO860@:6YT;R!T8V4O;W!T:6]N86P@9&ER96-T
M;W)Y+"!U<&1A=&5S($]N0F]O="!A;F0@:6YS=&%L;',Z(@H)96-H;R`B("`@
M)'M04D]'7TY!345]("UW("UI(&YA;F\N=&-Z(@H)96-H;R`B($1O=VYL;V%D
M(&]N;'D@:6YT;R!T8V4O;W!T:6]N86P@9&ER96-T;W)Y.B(*"65C:&\@(B`@
M("1[4%)/1U].04U%?2`M=R!N86YO+G1C>B(*"65C:&\@(B!5<V4@86QT97)N
M871I=F4@<F5P;W-I=&]R>2P@<F]O="!L979E;"(*"65C:&\@(B`@("1[4%)/
M1U].04U%?2`M<B!H='1P<SHO+W-O=7)C969O<F=E+FYE="]P<F]J96-T<R]P
M:6-O<F5P;&%Y97(O9FEL97,O<F5P;R(*"65C:&\@(B!5<V4@86QT97)N871I
M=F4@<F5P;W-I=&]R>2P@;W9E<G)I9&4@86)S;VQU=&4@<&%T:"XB"@EE8VAO
M("(@("`D>U!23T=?3D%-17T@+74@:'1T<',Z+R]S;W5R8V5F;W)G92YN970O
M<')O:F5C=',O<&EC;W)E<&QA>65R+V9I;&5S+W)E<&\O."YX+V%R;78V+W1C
M>B(*"65X:70@,@I]"@HC<F5P;&%C92!T:&4@9V5T36ER<F]R(&9R;VT@=&,M
M9G5N8W1I;VYS"F=E=$UI<G)O<B@I('L*0E5)3$0])"AG971"=6EL9"D*6R`M
M>B`D4D503R!=("8F(')E860@34E24D]2(#P@+V]P="]T8V5M:7)R;W(@?'P@
M34E24D]2/21215!/"DU)4E)/4CTB)'M-25)23U(E+WTO)"AG971-86IO<E9E
M<BDN>"\D0E5)3$0O=&-Z(@I;("UZ("1215!/7T%"4R!=("8F(')E860@34E2
M4D]2(#P@+V]P="]T8V5M:7)R;W(@?'P@34E24D]2/21215!/7T%"4PI]"@IA
M8F]R=%]T;U]S879E9%]D:7(H*7L*"65C:&\@(C$B(#X@+W1M<"]A<'!S97)R
M"@EI9B!;("(D0D]/5$E.1R(@73L@=&AE;@H)"5-+25`]5%)510H)96QS90H)
M"2-C9"`B)%-!5D5$7T1)4B(*"0EE>&ET(#$*"69I"GT*"G=H:6QE(&=E=&]P
M=',@=VEL8V)O<V9R.G0Z=3H@3U!424]."F1O"@EC87-E("1[3U!424].?2!I
M;@H)"7<I(%='150]5%)512`[.PH)"6DI($E.4U1!3$P]5%)512`[.PH)"6PI
M($Q/041?3TY,63U44E5%(#L["@D)8RD@0T]064E.4U1!3$P]5%)512`[.PH)
M"6(I($)/3U1)3D<]5%)512`[.PH)"6\I($].1$5-04Y$/512544@.SL*"0ES
M*2!355!04D534SU44E5%(#L["@D)9BD@1D]20T4](GDB(#L["@D)<BD@4D50
M3STB)$]05$%21R(@.SL*"0ET*2!40T5$25(](B1/4%1!4D<B(#L["@D)=2D@
M4D503U]!0E,](B1/4%1!4D<B(#L["@D)*BD@86)O<G0@.SL*"65S86,*9&]N
M90IS:&EF="!@97AP<B`D3U!424Y$("T@,6`*6R`M>B`B)#$B(%T@?'P@*"!;
M("UZ("(D5T=%5"(@72`F)B!;("UZ("(D24Y35$%,3"(@72`I("8F(&%B;W)T
M"@IA<'!?97AI<W1S*"D@>PH):68@6R`B)$9/4D-%(B`](")Y(B!=.R!T:&5N
M"@D)<FT@+68@(B0R+R0Q(@H)"7)M("UF("(D,B\D,2(N;60U+G1X=`H)"7)M
M("UF("(D,B\D,2(N9&5P"@D)<F5T=7)N(#$*"65L<V4*"0E;("UF("(D,B\D
M,2(@72`F)B!;("UF("(D,B\D,2(N;60U+G1X="!=("8F("AC9"`B)#(B("8F
M(&UD-7-U;2`M8W,@(B0Q(BYM9#4N='AT*0H)9FD*?0H*9F5T8VA?87!P*"D@
M>PH)96-H;R`B/'`^6R!)3D9/(%T@1&]W;FQO861I;F<Z("0Q/"]P/B(*"7=G
M970@+6-Q("(D34E24D]2(B\B)#$B+FUD-2YT>'0@,CXO9&5V+VYU;&P*"65C
M:&\@+6X@(CQP/B(*"7=G970@+6,@(B1-25)23U(B+R(D,2(@,3XF,@H)96-H
M;R`M;B`B/"]P/B(*"65C:&\@(CQP/EL@24Y&3R!=($-H96-K:6YG($U$-2!O
M9CH@)'LQ?2XN+BXN(@H);60U<W5M("UC<R`B)#$B+FUD-2YT>'0*"6EF(%L@
M(B0_(B`A/2`P(%T[('1H96X*"0EE8VAO("(\+W`^6R!%4E)/4B!=($5R<F]R
M(&]N("0Q/"]P/B(*"0ER;2`M9B`D,2H*"0EE8VAO("(Q(B`^("]T;7`O87!P
M<V5R<@H)96QS90H)"65C:&\@(B0Q($]+/"]P/B(*"69I"GT*"F-O<'E);G-T
M86QL*"D@>PH)6R`M9"`O;6YT+W1E<W0@72!\?"!S=61O("]B:6XO;6MD:7(@
M+7`@+VUN="]T97-T"@ES=61O("]B:6XO8G5S>6)O>"YS=6ED(&UO=6YT("0Q
M("]M;G0O=&5S="`M="!S<75A<VAF<R`M;R!L;V]P+')O+&)S/30P.38*"6EF
M(%L@(B0_(B`]/2`P(%T[('1H96X*"0EI9B!;("(D*&QS("U!("]M;G0O=&5S
M="DB(%T[('1H96X*"0D)>65S("(D1D]20T4B('P@<W5D;R`O8FEN+V-P("UA
M:2`O;6YT+W1E<W0O+B`O(#(^+V1E=B]N=6QL"@D)"5L@+6X@(F!F:6YD("]M
M;G0O=&5S="\@+71Y<&4@9"`M;F%M92!M;V1U;&5S8"(@72`F)B!-3T153$53
M/512544*"0EF:0H)"7-U9&\@+V)I;B]U;6]U;G0@+60@+VUN="]T97-T"@EF
M:0I]"@IU<&1A=&5?<WES=&5M*"D@>PH):68@6R`B)$)/3U1)3D<B(%T[('1H
M96X*"0E;("(D34]$54Q%4R(@72`F)B!S=61O("]B:6XO=&]U8V@@+V5T8R]S
M>7-C;VYF:6<O;F5W;6]D=6QE<PH)96QS90H)"5L@(B142$E305!0(B`A/2`B
M)$585$5.4TE/3B(@72!\?"!;("(D1$]73DQ/041?3TY,62(@72!\?"!;("(D
M3$]!1%]/3DQ9(B!=('Q\(&5C:&\@(B142$E305!0(B`^/B`N+B\D3TY"3T]4
M3D%-10H)"6EF(%L@(B1-3T153$53(B!=.R!T:&5N"@D)"7-U9&\@+W-B:6XO
M9&5P;6]D("UA(#(^+V1E=B]N=6QL"@D)"7-U9&\@+W-B:6XO=61E=F%D;2!T
M<FEG9V5R"@D)9FD*"0ES=61O("]S8FEN+VQD8V]N9FEG(#(^+V1E=B]N=6QL
M"@EF:0H):68@6R`M>"`B)%1#14E.4U1!3$Q%1"(O)#(@73L@=&AE;@H)"6EF
M(%L@(B1"3T]424Y'(B!=(#L@=&AE;@H)"0EE8VAO("(D5$-%24Y35$%,3$5$
M(B\D,B`^/B`O=&UP+W-E='5P+FQS=`H)"65L<V4*"0D)<W5D;R`B)%1#14E.
M4U1!3$Q%1"(O)#(*"0EF:0H)96QS90H)"71O=6-H("(D5$-%24Y35$%,3$5$
M(B\D,@H)9FD*?0H*:6YS=&%L;"@I>PH)=6YS970@34]$54Q%4R!%35!46458
M5`H*"6EF(%L@(B1,04Y'(B`A/2`B0R(@73L@=&AE;@H)"4Q/0T%,14585#TB
M)'LQ)2YT8WI]+6QO8V%L92YT8WHB"@D)6R`M9B`B)$Q/0T%,14585"(@72`F
M)B!I;G-T86QL("(D3$]#04Q%15A4(@H)9FD*"@E42$E305!0/2(D,2(*"4%0
M4$Y!344](B1[5$A)4T%04"4N*GTB"@H):68@6R`B)$E.4U1!3$PB(%T[('1H
M96X*"0EI9B!;("(D0T]064E.4U1!3$PB(%T@?'P@6R`M92`B)'M&4D]-5TA%
M4D4E+RI](B]C;W!Y,F9S+F9L9R!=('Q\(&=R97`@+7%W("1!4%!.04U%("(D
M>T923TU72$52124O*GTB+V-O<'DR9G,N;'-T(#(^+V1E=B]N=6QL.R!T:&5N
M"@D)"6-O<'E);G-T86QL("(D5$A)4T%04"(*"0D)=7!D871E7W-Y<W1E;2`B
M)%1(25-!4%`B("(D05!03D%-12(*"0D):68@6R`A("(D0D]/5$E.1R(@73L@
M=&AE;@H)"0D)6R`M<R`O971C+W-Y<V-O;F9I9R]D97-K=&]P(%T@)B8@9&5S
M:W1O<"YS:"`B)$%04$Y!344B"@D)"69I"@D)96QS90H)"0E;("UD("]T;7`O
M=&-L;V]P+R(D05!03D%-12(@72!\?"!S=61O("]B:6XO;6MD:7(@+7`@+W1M
M<"]T8VQO;W`O(B1!4%!.04U%(@H)"0EA=VL@+78@87!P;F%M93TB+W1M<"]T
M8VQO;W`O)$%04$Y!344B("<@>R!I9B`H("0R(#T](&%P<&YA;64@*2`@97AI
M="`Q('TG("]E=&,O;71A8@H)"0E;("(D/R(@/3T@,2!=('Q\('-U9&\@+V)I
M;B]B=7-Y8F]X+G-U:60@;6]U;G0@(B142$E305!0(B`O=&UP+W1C;&]O<"\B
M)$%04$Y!344B("UT('-Q=6%S:&9S("UO(&QO;W`L<F\L8G,]-#`Y-B`R/B8Q
M"@D)"5L@(B0_(B`]/2`P(%T@?'P@86)O<G1?=&]?<V%V961?9&ER"@D)"5L@
M(F!F:6YD("]T;7`O=&-L;V]P+R1[05!03D%-17T@+6UI;F1E<'1H(#$@+6UA
M>&1E<'1H(#(@?"!W8R`M;&`B("UL92`Q(%T@)B8@14U05%E%6%0],0H*"0D)
M:68@6R`M>B`B)$5-4%1915A4(B!=.R!T:&5N"@D)"0EY97,@(B1&3U)#12(@
M?"!S=61O("]B:6XO8W`@+6%I<R`O=&UP+W1C;&]O<"\B)$%04$Y!344B+RH@
M+R`R/B]D978O;G5L;`H)"0D)6R`M;B`B8&9I;F0@+W1M<"]T8VQO;W`O)$%0
M4$Y!344@+71Y<&4@9"`M;F%M92!M;V1U;&5S8"(@72`F)B!-3T153$53/512
M544*"0D)"75P9&%T95]S>7-T96T@(B142$E305!0(B`B)$%04$Y!344B"@D)
M"0EI9B!;("$@(B1"3T]424Y'(B!=.R!T:&5N"@D)"0D)6R`M<R`O971C+W-Y
M<V-O;F9I9R]D97-K=&]P(%T@)B8@9&5S:W1O<"YS:"`B)$%04$Y!344B"@D)
M"0EF:0H)"0EE;'-E"@D)"0ES=61O("]B:6XO=6UO=6YT("UD("]T;7`O=&-L
M;V]P+R(D05!03D%-12(*"0D)"75P9&%T95]S>7-T96T@(B142$E305!0(B`B
M)$%04$Y!344B"@D)"69I"@D)9FD*"0E;("(D0D]/5$E.1R(@72`F)B!;("(D
M4TA/5T%04%,B(%T@)B8@96-H;R`M;B`B)'M914Q,3U=])$%04$Y!344@)'M.
M3U)-04Q](@H)9FD*"@ER971U<FX@,`I]"@IR96-U<G-I=F5?<V-A;E]D97`H
M*2!["@EE8VAO("UE("(D0")\87=K("<*"69U;F-T:6]N(')E8W5R<VEV95]S
M8V%N*&YA;64L(&]P=&EO;F%L+"!M:7)R;W(L(%\L(&1E<&9I;&4L(&QI;F4L
M(&DI('L*"0EG<W5B*"];7'0@72LO+"`B(BP@;F%M92D*"0EI9B`H;F%M92D@
M>PH)"0ES=6(H+UPM2T523D5,7"YT8WHO+"`B+2)+15).14Q615(B+G1C>B(L
M(&YA;64I"@D)"6EF("AN86UE(&EN($U!4DLI('L*"0D)"6EF("A-05)+6VYA
M;65=(#T](#(I('L*"0D)"0EI9B`H(2!355!04D534RD*"0D)"0D)<WES=&5M
M*")E8VAO(#QP/EL@5T%23B!=(%=A<FYI;F<@;&]O<"!D97!E;F1E;F-Y.B`B
M;F%M92(\+W`^(#$^)C(B*0H)"0D)?2!E;'-E('L*"0D)"0E215-53%1;*RM)
M1%A=/2)`(R)N86UE"@D)"0E]"@D)"7T@96QS92!["@D)"0E)1%@K/3$*"0D)
M"5)%4U5,5%M)1%A=/6YA;64*"0D)"4E204Y'15MN86UE(B,Q(ET]2418"@D)
M"0ED97!F:6QE/6]P=&EO;F%L(B\B;F%M92(N9&5P(@H)"0D):68@*&UI<G)O
M<B`F)B`H<WES=&5M*")T97-T("$@+68@(F1E<&9I;&4I(#T](#`@?'P@<WES
M=&5M*")T97-T("$@+68@(F]P=&EO;F%L(B\B;F%M92D@/3T@,"DI"@D)"0D)
M:68@*'-Y<W1E;2@B<FT@+68@(F1E<&9I;&4B.R!W9V5T("UC("U0(")O<'1I
M;VYA;"(@(FUI<G)O<B(O(FYA;64B+F1E<"`R/B]D978O;G5L;"(I(#T](#`@
M)B8@(2!355!04D534RD*"0D)"0D)<WES=&5M*")E8VAO("UN(%PB/'`^6R!)
M3D9/(%T@(FYA;64B+F1E<"!$;W=N;&]A9&5D+BXN+BY<(B`Q/B8R(BD*"0D)
M"4U!4DM;;F%M95T],@H)"0D)1DE24U1;;F%M95T],`H)"0D):68@*&UI<G)O
M<B!\?"!S>7-T96TH(G1E<W0@+68@(F]P=&EO;F%L(B\B;F%M92D@/3T@,"D@
M>PH)"0D)"7=H:6QE("AG971L:6YE(&QI;F4@/"!D97!F:6QE(#X@,"E["@D)
M"0D)"6EF("@@1DE24U1;;F%M95T@/3T@,"`I>PH)"0D)"0D):68@*"!L:6YE
M("%^("];82UZ02U:,"TY7RM=+G1C>B0O("E["@D)"0D)"0D)<WES=&5M*")E
M8VAO(%PB/"]P/CQP/EL@15)23U(@72`B;F%M92(@1F%I;&5D($-H96-K<SPO
M<#Y<(B`Q/B8R(BD*"0D)"0D)"0EC;&]S92AD97!F:6QE*0H)"0D)"0D)"7-Y
M<W1E;2`H(F5C:&\@7"(Q7"(@/B`O=&UP+V%P<'-E<G(B*0H)"0D)"0D)"7-Y
M<W1E;2`H(G)M("UF("(@9&5P9FEL92D*"0D)"0D)"0EE>&ET(#$*"0D)"0D)
M"7T*"0D)"0D)"6EF("@@;&5N9W1H*&YA;64I(#X@,"`I>PH)"0D)"0D)"7-Y
M<W1E;2@B96-H;R!<(B)N86UE(B!$15`@5&5S="!/:SPO<#Y<(B`Q/B8R(BD*
M"0D)"0D)"7T*"0D)"0D)"49)4E-46VYA;65=/3$*"0D)"0D)?0H)"0D)"0ER
M96-U<G-I=F5?<V-A;BAL:6YE+"!O<'1I;VYA;"P@;6ER<F]R*0H)"0D)"7T*
M"0D)"0EC;&]S92AD97!F:6QE*0H)"0D)?0H)"0D)34%22UMN86UE73TQ"@D)
M"0E)4D%.1T5;;F%M92(C,B)=/4E$6`H)"0E]"@D)?0H)?0H)9G5N8W1I;VX@
M;W5T<'5T*&ED>#$L(&ED>#(L(%\L(&YA;64L(&DL(')E9FYA;64I('L*"0EF
M;W(@*&D]:61X,CL@:3X]:61X,3L@:2TM*2!["@D)"6YA;64]4D5354Q46VE=
M"@D)"6EF("@A("AN86UE(&EN(%!224Y4140I*2!["@D)"0E04DE.5$5$6VYA
M;65=/3$*"0D)"6EF("AS=6)S='(H;F%M92P@,2P@,BD@/3T@(D`C(BD@>PH)
M"0D)"7)E9FYA;64@/2!S=6)S='(H;F%M92P@,RD*"0D)"0EO=71P=70H25)!
M3D=%6W)E9FYA;64B(S$B72LP+"!)4D%.1T5;<F5F;F%M92(C,B)=*0H)"0D)
M?2!E;'-E('L*"0D)"0EP<FEN="!N86UE"@D)"0E]"@D)"7T*"0E]"@E]"@E"
M14=)3B![2T523D5,5D52/2(G(B1+15).14Q615(B)R([(%-54%!215-3/2(G
M(B1355!04D534R(G(CL@2418/3`[?0H)>W!I/4E$6#L@<F5C=7)S:79E7W-C
M86XH)#$L("0R(#\@)#(@.B`B+B(L("0S*3L@<')I;G0@(D`@(B0Q.R!O=71P
M=70H<&DK,2P@2418*3L@9&5L971E(%!224Y4140[?0H))PI]"@HC($UA:6X*
M96-H;R`B,"(@/B`O=&UP+V%P<'-E<G(*6R`M9"`B)%1#141)4B(@72!\?"!E
M>&ET(#$*6R`M;B`B)#$B(%T@?'P@97AI="`Q"EL@+68@+V5T8R]S>7-C;VYF
M:6<O<VAO=V%P<',@72`F)B!32$]705!04SU44E5%("8F(%-54%!215-3/512
M544*(R`@0VAE8VL@9F]R(&1O=VYL;V%D(&]N;'D*6R`M>B`B)$E.4U1!3$PB
M(%T@)B8@1$]73DQ/041?3TY,63TQ"EL@+7H@(B171T54(B!=("8F(%L@(B1)
M3E-404Q,(B!=("8F($Q/041?3TY,63TQ"@I/4%1)3TY!3#TB8')E86QP871H
M("140T5$25)@+V]P=&EO;F%L(@I405)'15133$]#04P](B(*5$%21T544T9%
M5$-(/2(B"D923TU72$5213TB(@H*9F]R(%1!4D=%5$%04"!I;B`D0#L@9&\*
M"E1!4D=%5$%04#TB)'M405)'151!4%`E+G1C>GTN=&-Z(@I405)'151!4%`]
M(B1[5$%21T5405!0+RU+15).14PN=&-Z+RTD>TM%4DY%3%9%4GTN=&-Z?2(*
M15A414Y324]./2(D>U1!4D=%5$%04",C*B]](@I!4%!.04U%/2(D>T585$5.
M4TE/3B4N*GTB"@II9B!;("UZ("(D1E)/35=(15)%(B!=.R!T:&5N"@EI9B!;
M("(D5$%21T5405!0(B`]("(D15A414Y324].(B!=("8F(%L@(2`M9B`B)$58
M5$5.4TE/3B(@73L@=&AE;@H)"4923TU72$5213TB)$]05$E/3D%,(@H)96QS
M90H)"4923TU72$5213U@9&ER;F%M92`B)%1!4D=%5$%04")@"@EF:0IF:0H*
M(R!)9B!L;V%D(&QO8V%L(&]R(&EN<W1A;&P@=&AE;B!A;'-O(&-H96-K(&EF
M(&%L<F5A9'D@:6YS=&%L;&5D+@II9B!;("(D24Y35$%,3"(@72`F)B!;("$@
M(B1"3T]424Y'(B!=.R!T:&5N"@EI9B!;("UF("(D5$-%24Y35$%,3$5$+R1!
M4%!.04U%(B!=.R!T:&5N"@D)96-H;R`B/'`^6R!)3D9/(%T@)$%04$Y!344@
M:7,@86QR96%D>2!I;G-T86QL960A/"]P/B(*"0EC;VYT:6YU90H)9FD*9FD*
M"FEF(%L@(B171T54(B!=.R!T:&5N"@EI9B!A<'!?97AI<W1S("(D15A414Y3
M24].(B`B)$923TU72$5212([('1H96X*"0EE8VAO("(\<#Y;($E.1D\@72`D
M05!03D%-12!I<R!A;')E861Y(&1O=VYL;V%D960N/"]P/B(*"65L<V4*"0EM
M:V1I<B`M<"`B)$923TU72$5212(*"0E405)'15131D540T@](B1405)'1513
M1D540TA<;B1%6%1%3E-)3TXB"@D)6R`B)$1/5TY,3T%$7T].3%DB(%T@)B8@
M6R`B)$].1$5-04Y$(B!=("8F(&]N9&5M86YD("(D15A414Y324].(@H)9FD*
M96QS90H)5$%21T544TQ/0T%,/2(D5$%21T544TQ/0T%,7&XD15A414Y324].
M(@IF:0H*9&]N92`C($9I;FES:"!T:&4@9F]R+6QO;W`@9F]R(&UU;'1I<&QE
M(&5X=&5N<VEO;G,*"F-D("(D1E)/35=(15)%(B!\?"!E>&ET(#$*"E)%5%)9
M/3`*34%87U)%5%))15,]-0H*=VAI;&4@6R`D4D544ED@+6QT("1-05A?4D54
M4DE%4R!="F1O"@EE8VAO("(P(B`^("]T;7`O87!P<V5R<@H*"6EF(%L@(B14
M05)'15131D540T@B(%T[('1H96X*"0EG971-:7)R;W(*"0E405)'15131D54
M0T@](F!E8VAO("UE("1405)'15131D540T@@?"!A=VL@)R]<=R\@>W!R:6YT
M("0Q(B`N("<B)$U)4E)/4B(G(GTG8"(*"0ER96-U<G-I=F5?<V-A;E]D97`@
M(B1405)'15131D540T@B('P@=VAI;&4@<F5A9"!&.R!D;PH)"0E[('1E<W0@
M(B1[1B4E("I](B`](")`(B`F)B!%6%1%3E-)3TX](B1[1B-`('TB("8F(%-+
M25`](B(@?'P@=&5S="`B)%-+25`B.R!]("8F(&-O;G1I;G5E"@D)"48](B1[
M1B,C*B]](@H)"0EA<'!?97AI<W1S("(D1B(@(BXB('Q\(&9E=&-H7V%P<"`B
M)$8B"@D)"5L@)"AC870@+W1M<"]A<'!S97)R*2`]("(Q(B!=("8F(&)R96%K
M"@D)"5L@+68@(B140T5)3E-404Q,140O)'M&)2XJ?2(@72!\?"!I;G-T86QL
M("(D1B(*(PD)9&]N92!\?"!E>&ET(#$@(R!S=6)S:&5L;"!C86YN;W0@97AI
M="!D:7)E8W1L>0H)"61O;F4@?'P@96-H;R`B,2(@/B`O=&UP+V%P<'-E<G(@
M"@EF:0H):68@6R`D*&-A="`O=&UP+V%P<'-E<G(I(#T@(C$B(%T[('1H96X*
M"0EE8VAO("(\<#Y;($524D]272!4:&5R92!W87,@82!E<G)O<B!D;W=N;&]A
M9&EN9R`D>T585$5.4TE/3GT\+W`^(@HC"0ER;2`M9B`D15A414Y324].*B`@
M($YO="!N965D960@:&5R92XN+BY)('1H:6YK"@D)4D544ED])"@H4D544EDK
M,2DI"@D):68@6R`D4D544ED@+6QT("1-05A?4D544DE%4R!=.R!T:&5N"@D)
M"65C:&\@(CQP/EL@24Y&3R!=(%)E=')Y:6YG(&5X=&5N<VEO;B`D>T585$5.
M4TE/3GTN+BXN+BXN+FEN(#4@<V5C;VYD<RX\+W`^(@H)"0ES;&5E<"`U"@D)
M96QS90H)"0EE8VAO("(\<#Y;($524D]2(%U-87@@<F5T<FEE<R!R96%C:&5D
M/"]P/B(*"0EF:0H)96QS90H)"65C:&\@(CQP/EL@24Y&3R!=($%L;"!&:6QE
M<R!497-T960@1V]O9#PO<#XB"@D)8G)E86L*"69I"F1O;F4*"@II9B!;("(D
M5$%21T544TQ/0T%,(B!=.R!T:&5N"@E405)'15133$]#04P](F!E8VAO("UE
M("1405)'15133$]#04P@?"!A=VL@)R]<=R\@>W!R:6YT("0Q?2=@(@H)<F5C
M=7)S:79E7W-C86Y?9&5P("(D5$%21T544TQ/0T%,(B!\('=H:6QE(')E860@
M1CL@9&\*"0E[('1E<W0@(B1[1B4E("I](B`](")`(B`F)B!%6%1%3E-)3TX]
M(B1[1B-`('TB("8F(%-+25`](B(@?'P@=&5S="`B)%-+25`B.R!]("8F(&-O
M;G1I;G5E"@D)1CTB)'M&(R,J+WTB"@D):68@6R`A("UF("(D5$-%24Y35$%,
M3$5$+R1[1B4N*GTB(%T[('1H96X*"0D):68@6R`M9B`B)$8B(%T[('1H96X*
M"0D)"6EN<W1A;&P@(B1&(@H)"0D)6R`B)%-54%!215-3(B!=('Q\(&5C:&\@
M(B1&.B!/2R(*"0D)96QS90H)"0D)96-H;R`B)$8@;F]T(&9O=6YD(2(*"0D)
M"6%B;W)T7W1O7W-A=F5D7V1I<@H)"0EF:0H)"69I"@ED;VYE('Q\(&5X:70@
M,2`C('-U8G-H96QL(&-A;FYO="!E>&ET(&1I<F5C=&QY"F9I"@I;("(D0D]/
M5$E.1R(@72`F)B!E>&ET(#`*6R`D*'=H:6-H("(D1$532U1/4")?<F5S=&%R
M="D@72`F)B`B)$1%4TM43U`B7W)E<W1A<G0@,CXO9&5V+VYU;&P*"FEF(%L@
M)"AC870@+W1M<"]A<'!S97)R*2`]("(Q(B!=.R!T:&5N"@EE>&ET(#$*96QS
-90H)97AI="`P"F9I"@``
`
end
