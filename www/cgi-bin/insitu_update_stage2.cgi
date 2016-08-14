#!/bin/sh

# Version 3.00 2016-08-09 PH
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
M<BDN>"\D0E5)3$0O=&-Z(@I;("UZ("1215!/7T%"4R!=('Q\($U)4E)/4CTD
M4D503U]!0E,*?0H*86)O<G1?=&]?<V%V961?9&ER*"E["@EE8VAO("(Q(B`^
M("]T;7`O87!P<V5R<@H):68@6R`B)$)/3U1)3D<B(%T[('1H96X*"0E32TE0
M/512544*"65L<V4*"0DC8V0@(B13059%1%]$25(B"@D)97AI="`Q"@EF:0I]
M"@IW:&EL92!G971O<'1S('=I;&-B;W-F<CIT.G4Z($]05$E/3@ID;PH)8V%S
M92`D>T]05$E/3GT@:6X*"0EW*2!71T54/512544@.SL*"0EI*2!)3E-404Q,
M/512544@.SL*"0EL*2!,3T%$7T].3%D]5%)512`[.PH)"6,I($-/4%E)3E-4
M04Q,/512544@.SL*"0EB*2!"3T]424Y'/512544@.SL*"0EO*2!/3D1%34%.
M1#U44E5%(#L["@D)<RD@4U504%)%4U,]5%)512`[.PH)"68I($9/4D-%/2)Y
M(B`[.PH)"7(I(%)%4$\](B1/4%1!4D<B(#L["@D)="D@5$-%1$E2/2(D3U!4
M05)'(B`[.PH)"74I(%)%4$]?04)3/2(D3U!405)'(B`[.PH)"2HI(&%B;W)T
M(#L["@EE<V%C"F1O;F4*<VAI9G0@8&5X<'(@)$]05$E.1"`M(#%@"EL@+7H@
M(B0Q(B!=('Q\("@@6R`M>B`B)%='150B(%T@)B8@6R`M>B`B)$E.4U1!3$PB
M(%T@*2`F)B!A8F]R=`H*87!P7V5X:7-T<R@I('L*"6EF(%L@(B1&3U)#12(@
M/2`B>2(@73L@=&AE;@H)"7)M("UF("(D,B\D,2(*"0ER;2`M9B`B)#(O)#$B
M+FUD-2YT>'0*"0ER;2`M9B`B)#(O)#$B+F1E<`H)"7)E='5R;B`Q"@EE;'-E
M"@D)6R`M9B`B)#(O)#$B(%T@)B8@6R`M9B`B)#(O)#$B+FUD-2YT>'0@72`F
M)B`H8V0@(B0R(B`F)B!M9#5S=6T@+6-S("(D,2(N;60U+G1X="D*"69I"GT*
M"F9E=&-H7V%P<"@I('L*"65C:&\@(CQP/EL@24Y&3R!=($1O=VYL;V%D:6YG
M.B`D,3PO<#XB"@EW9V5T("UC<2`B)$U)4E)/4B(O(B0Q(BYM9#4N='AT(#(^
M+V1E=B]N=6QL"@EE8VAO("UN("(\<#XB"@EW9V5T("UC("(D34E24D]2(B\B
M)#$B(#$^)C(*"65C:&\@+6X@(CPO<#XB"@EE8VAO("(\<#Y;($E.1D\@72!#
M:&5C:VEN9R!-1#4@;V8Z("1[,7TN+BXN+B(*"6UD-7-U;2`M8W,@(B0Q(BYM
M9#4N='AT"@EI9B!;("(D/R(@(3T@,"!=.R!T:&5N"@D)96-H;R`B/"]P/EL@
M15)23U(@72!%<G)O<B!O;B`D,3PO<#XB"@D)<FT@+68@)#$J"@D)96-H;R`B
M,2(@/B`O=&UP+V%P<'-E<G(*"65L<V4*"0EE8VAO("(D,2!/2SPO<#XB"@EF
M:0I]"@IC;W!Y26YS=&%L;"@I('L*"5L@+60@+VUN="]T97-T(%T@?'P@<W5D
M;R`O8FEN+VUK9&ER("UP("]M;G0O=&5S=`H)<W5D;R`O8FEN+V)U<WEB;W@N
M<W5I9"!M;W5N="`D,2`O;6YT+W1E<W0@+70@<W%U87-H9G,@+6\@;&]O<"QR
M;RQB<STT,#DV"@EI9B!;("(D/R(@/3T@,"!=.R!T:&5N"@D):68@6R`B)"AL
M<R`M02`O;6YT+W1E<W0I(B!=.R!T:&5N"@D)"7EE<R`B)$9/4D-%(B!\('-U
M9&\@+V)I;B]C<"`M86D@+VUN="]T97-T+RX@+R`R/B]D978O;G5L;`H)"0E;
M("UN(")@9FEN9"`O;6YT+W1E<W0O("UT>7!E(&0@+6YA;64@;6]D=6QE<V`B
M(%T@)B8@34]$54Q%4SU44E5%"@D)9FD*"0ES=61O("]B:6XO=6UO=6YT("UD
M("]M;G0O=&5S=`H)9FD*?0H*=7!D871E7W-Y<W1E;2@I('L*"6EF(%L@(B1"
M3T]424Y'(B!=.R!T:&5N"@D)6R`B)$U/1%5,15,B(%T@)B8@<W5D;R`O8FEN
M+W1O=6-H("]E=&,O<WES8V]N9FEG+VYE=VUO9'5L97,*"65L<V4*"0E;("(D
M5$A)4T%04"(@(3T@(B1%6%1%3E-)3TXB(%T@?'P@6R`B)$1/5TY,3T%$7T].
M3%DB(%T@?'P@6R`B)$Q/041?3TY,62(@72!\?"!E8VAO("(D5$A)4T%04"(@
M/CX@+BXO)$].0D]/5$Y!344*"0EI9B!;("(D34]$54Q%4R(@73L@=&AE;@H)
M"0ES=61O("]S8FEN+V1E<&UO9"`M82`R/B]D978O;G5L;`H)"0ES=61O("]S
M8FEN+W5D979A9&T@=')I9V=E<@H)"69I"@D)<W5D;R`O<V)I;B]L9&-O;F9I
M9R`R/B]D978O;G5L;`H)9FD*"6EF(%L@+7@@(B140T5)3E-404Q,140B+R0R
M(%T[('1H96X*"0EI9B!;("(D0D]/5$E.1R(@72`[('1H96X*"0D)96-H;R`B
M)%1#14E.4U1!3$Q%1"(O)#(@/CX@+W1M<"]S971U<"YL<W0*"0EE;'-E"@D)
M"7-U9&\@(B140T5)3E-404Q,140B+R0R"@D)9FD*"65L<V4*"0ET;W5C:"`B
M)%1#14E.4U1!3$Q%1"(O)#(*"69I"GT*"FEN<W1A;&PH*7L*"75N<V5T($U/
M1%5,15,@14U05%E%6%0*"@EI9B!;("(D3$%.1R(@(3T@(D,B(%T[('1H96X*
M"0E,3T-!3$5%6%0](B1[,24N=&-Z?2UL;V-A;&4N=&-Z(@H)"5L@+68@(B1,
M3T-!3$5%6%0B(%T@)B8@:6YS=&%L;"`B)$Q/0T%,14585"(*"69I"@H)5$A)
M4T%04#TB)#$B"@E!4%!.04U%/2(D>U1(25-!4%`E+BI](@H*"6EF(%L@(B1)
M3E-404Q,(B!=.R!T:&5N"@D):68@6R`B)$-/4%E)3E-404Q,(B!=('Q\(%L@
M+64@(B1[1E)/35=(15)%)2\J?2(O8V]P>3)F<RYF;&<@72!\?"!G<F5P("UQ
M=R`D05!03D%-12`B)'M&4D]-5TA%4D4E+RI](B]C;W!Y,F9S+FQS="`R/B]D
M978O;G5L;#L@=&AE;@H)"0EC;W!Y26YS=&%L;"`B)%1(25-!4%`B"@D)"75P
M9&%T95]S>7-T96T@(B142$E305!0(B`B)$%04$Y!344B"@D)"6EF(%L@(2`B
M)$)/3U1)3D<B(%T[('1H96X*"0D)"5L@+7,@+V5T8R]S>7-C;VYF:6<O9&5S
M:W1O<"!=("8F(&1E<VMT;W`N<V@@(B1!4%!.04U%(@H)"0EF:0H)"65L<V4*
M"0D)6R`M9"`O=&UP+W1C;&]O<"\B)$%04$Y!344B(%T@?'P@<W5D;R`O8FEN
M+VUK9&ER("UP("]T;7`O=&-L;V]P+R(D05!03D%-12(*"0D)87=K("UV(&%P
M<&YA;64](B]T;7`O=&-L;V]P+R1!4%!.04U%(B`G('L@:68@*"`D,B`]/2!A
M<'!N86UE("D@(&5X:70@,2!])R`O971C+VUT86(*"0D)6R`B)#\B(#T](#$@
M72!\?"!S=61O("]B:6XO8G5S>6)O>"YS=6ED(&UO=6YT("(D5$A)4T%04"(@
M+W1M<"]T8VQO;W`O(B1!4%!.04U%(B`M="!S<75A<VAF<R`M;R!L;V]P+')O
M+&)S/30P.38@,CXF,0H)"0E;("(D/R(@/3T@,"!=('Q\(&%B;W)T7W1O7W-A
M=F5D7V1I<@H)"0E;(")@9FEN9"`O=&UP+W1C;&]O<"\D>T%04$Y!345]("UM
M:6YD97!T:"`Q("UM87AD97!T:"`R('P@=V,@+6Q@(B`M;&4@,2!=("8F($5-
M4%1915A4/3$*"@D)"6EF(%L@+7H@(B1%35!464585"(@73L@=&AE;@H)"0D)
M>65S("(D1D]20T4B('P@<W5D;R`O8FEN+V-P("UA:7,@+W1M<"]T8VQO;W`O
M(B1!4%!.04U%(B\J("\@,CXO9&5V+VYU;&P*"0D)"5L@+6X@(F!F:6YD("]T
M;7`O=&-L;V]P+R1!4%!.04U%("UT>7!E(&0@+6YA;64@;6]D=6QE<V`B(%T@
M)B8@34]$54Q%4SU44E5%"@D)"0EU<&1A=&5?<WES=&5M("(D5$A)4T%04"(@
M(B1!4%!.04U%(@H)"0D):68@6R`A("(D0D]/5$E.1R(@73L@=&AE;@H)"0D)
M"5L@+7,@+V5T8R]S>7-C;VYF:6<O9&5S:W1O<"!=("8F(&1E<VMT;W`N<V@@
M(B1!4%!.04U%(@H)"0D)9FD*"0D)96QS90H)"0D)<W5D;R`O8FEN+W5M;W5N
M="`M9"`O=&UP+W1C;&]O<"\B)$%04$Y!344B"@D)"0EU<&1A=&5?<WES=&5M
M("(D5$A)4T%04"(@(B1!4%!.04U%(@H)"0EF:0H)"69I"@D)6R`B)$)/3U1)
M3D<B(%T@)B8@6R`B)%-(3U=!4%!3(B!=("8F(&5C:&\@+6X@(B1[645,3$]7
M?21!4%!.04U%("1[3D]234%,?2(*"69I"@H)<F5T=7)N(#`*?0H*<F5C=7)S
M:79E7W-C86Y?9&5P*"D@>PH)96-H;R`M92`B)$`B?&%W:R`G"@EF=6YC=&EO
M;B!R96-U<G-I=F5?<V-A;BAN86UE+"!O<'1I;VYA;"P@;6ER<F]R+"!?+"!D
M97!F:6QE+"!L:6YE+"!I*2!["@D)9W-U8B@O6UQT(%TK+RP@(B(L(&YA;64I
M"@D):68@*&YA;64I('L*"0D)<W5B*"]<+4M%4DY%3%PN=&-Z+RP@(BTB2T52
M3D5,5D52(BYT8WHB+"!N86UE*0H)"0EI9B`H;F%M92!I;B!-05)+*2!["@D)
M"0EI9B`H34%22UMN86UE72`]/2`R*2!["@D)"0D):68@*"$@4U504%)%4U,I
M"@D)"0D)"7-Y<W1E;2@B96-H;R`\<#Y;(%=!4DX@72!787)N:6YG(&QO;W`@
M9&5P96YD96YC>3H@(FYA;64B/"]P/B`Q/B8R(BD*"0D)"7T@96QS92!["@D)
M"0D)4D5354Q46RLK241873TB0",B;F%M90H)"0D)?0H)"0E](&5L<V4@>PH)
M"0D)2418*STQ"@D)"0E215-53%1;241873UN86UE"@D)"0E)4D%.1T5;;F%M
M92(C,2)=/4E$6`H)"0D)9&5P9FEL93UO<'1I;VYA;"(O(FYA;64B+F1E<"(*
M"0D)"6EF("AM:7)R;W(@)B8@*'-Y<W1E;2@B=&5S="`A("UF(")D97!F:6QE
M*2`]/2`P('Q\('-Y<W1E;2@B=&5S="`A("UF(")O<'1I;VYA;"(O(FYA;64I
M(#T](#`I*0H)"0D)"6EF("AS>7-T96TH(G)M("UF(")D97!F:6QE(CL@=V=E
M="`M8R`M4"`B;W!T:6]N86PB(")M:7)R;W(B+R)N86UE(BYD97`@,CXO9&5V
M+VYU;&PB*2`]/2`P("8F("$@4U504%)%4U,I"@D)"0D)"7-Y<W1E;2@B96-H
M;R`M;B!<(CQP/EL@24Y&3R!=(")N86UE(BYD97`@1&]W;FQO861E9"XN+BXN
M7"(@,3XF,B(I"@D)"0E-05)+6VYA;65=/3(*"0D)"49)4E-46VYA;65=/3`*
M"0D)"6EF("AM:7)R;W(@?'P@<WES=&5M*")T97-T("UF(")O<'1I;VYA;"(O
M(FYA;64I(#T](#`I('L*"0D)"0EW:&EL92`H9V5T;&EN92!L:6YE(#P@9&5P
M9FEL92`^(#`I>PH)"0D)"0EI9B`H($9)4E-46VYA;65=(#T](#`@*7L*"0D)
M"0D)"6EF("@@;&EN92`A?B`O6V$M>D$M6C`M.5\K72YT8WHD+R`I>PH)"0D)
M"0D)"7-Y<W1E;2@B96-H;R!<(CPO<#X\<#Y;($524D]2(%T@(FYA;64B($9A
M:6QE9"!#:&5C:W,\+W`^7"(@,3XF,B(I"@D)"0D)"0D)8VQO<V4H9&5P9FEL
M92D*"0D)"0D)"0ES>7-T96T@*")E8VAO(%PB,5PB(#X@+W1M<"]A<'!S97)R
M(BD*"0D)"0D)"0ES>7-T96T@*")R;2`M9B`B(&1E<&9I;&4I"@D)"0D)"0D)
M97AI="`Q"@D)"0D)"0E]"@D)"0D)"0EI9B`H(&QE;F=T:"AN86UE*2`^(#`@
M*7L*"0D)"0D)"0ES>7-T96TH(F5C:&\@7"(B;F%M92(@1$50(%1E<W0@3VL\
M+W`^7"(@,3XF,B(I"@D)"0D)"0E]"@D)"0D)"0E&25)35%MN86UE73TQ"@D)
M"0D)"7T*"0D)"0D)<F5C=7)S:79E7W-C86XH;&EN92P@;W!T:6]N86PL(&UI
M<G)O<BD*"0D)"0E]"@D)"0D)8VQO<V4H9&5P9FEL92D*"0D)"7T*"0D)"4U!
M4DM;;F%M95T],0H)"0D)25)!3D=%6VYA;64B(S(B73U)1%@*"0D)?0H)"7T*
M"7T*"69U;F-T:6]N(&]U='!U="AI9'@Q+"!I9'@R+"!?+"!N86UE+"!I+"!R
M969N86UE*2!["@D)9F]R("AI/6ED>#([(&D^/6ED>#$[(&DM+2D@>PH)"0EN
M86UE/5)%4U5,5%MI70H)"0EI9B`H(2`H;F%M92!I;B!04DE.5$5$*2D@>PH)
M"0D)4%))3E1%1%MN86UE73TQ"@D)"0EI9B`H<W5B<W1R*&YA;64L(#$L(#(I
M(#T](")`(R(I('L*"0D)"0ER969N86UE(#T@<W5B<W1R*&YA;64L(#,I"@D)
M"0D);W5T<'5T*$E204Y'15MR969N86UE(B,Q(ETK,"P@25)!3D=%6W)E9FYA
M;64B(S(B72D*"0D)"7T@96QS92!["@D)"0D)<')I;G0@;F%M90H)"0D)?0H)
M"0E]"@D)?0H)?0H)0D5'24X@>TM%4DY%3%9%4CTB)R(D2T523D5,5D52(B<B
M.R!355!04D534STB)R(D4U504%)%4U,B)R([($E$6#TP.WT*"7MP:3U)1%@[
M(')E8W5R<VEV95]S8V%N*"0Q+"`D,B`_("0R(#H@(BXB+"`D,RD[('!R:6YT
M(")`("(D,3L@;W5T<'5T*'!I*S$L($E$6"D[(&1E;&5T92!04DE.5$5$.WT*
M"2<*?0H*(R!-86EN"F5C:&\@(C`B(#X@+W1M<"]A<'!S97)R"EL@+60@(B14
M0T5$25(B(%T@?'P@97AI="`Q"EL@+6X@(B0Q(B!=('Q\(&5X:70@,0I;("UF
M("]E=&,O<WES8V]N9FEG+W-H;W=A<'!S(%T@)B8@4TA/5T%04%,]5%)512`F
M)B!355!04D534SU44E5%"B,@($-H96-K(&9O<B!D;W=N;&]A9"!O;FQY"EL@
M+7H@(B1)3E-404Q,(B!=("8F($1/5TY,3T%$7T].3%D],0I;("UZ("(D5T=%
M5"(@72`F)B!;("(D24Y35$%,3"(@72`F)B!,3T%$7T].3%D],0H*3U!424].
M04P](F!R96%L<&%T:"`D5$-%1$E28"]O<'1I;VYA;"(*5$%21T544TQ/0T%,
M/2(B"E1!4D=%5%-&151#2#TB(@I&4D]-5TA%4D4](B(*"F9O<B!405)'151!
M4%`@:6X@)$`[(&1O"@I405)'151!4%`](B1[5$%21T5405!0)2YT8WI]+G1C
M>B(*5$%21T5405!0/2(D>U1!4D=%5$%04"\M2T523D5,+G1C>B\M)'M+15).
M14Q615)]+G1C>GTB"D585$5.4TE/3CTB)'M405)'151!4%`C(RHO?2(*05!0
M3D%-13TB)'M%6%1%3E-)3TXE+BI](@H*:68@6R`M>B`B)$923TU72$5212(@
M73L@=&AE;@H):68@6R`B)%1!4D=%5$%04"(@/2`B)$585$5.4TE/3B(@72`F
M)B!;("$@+68@(B1%6%1%3E-)3TXB(%T[('1H96X*"0E&4D]-5TA%4D4](B1/
M4%1)3TY!3"(*"65L<V4*"0E&4D]-5TA%4D4]8&1I<FYA;64@(B1405)'151!
M4%`B8`H)9FD*9FD*"B,@268@;&]A9"!L;V-A;"!O<B!I;G-T86QL('1H96X@
M86QS;R!C:&5C:R!I9B!A;')E861Y(&EN<W1A;&QE9"X*:68@6R`B)$E.4U1!
M3$PB(%T@)B8@6R`A("(D0D]/5$E.1R(@73L@=&AE;@H):68@6R`M9B`B)%1#
M14E.4U1!3$Q%1"\D05!03D%-12(@73L@=&AE;@H)"65C:&\@(CQP/EL@24Y&
M3R!=("1!4%!.04U%(&ES(&%L<F5A9'D@:6YS=&%L;&5D(3PO<#XB"@D)8V]N
M=&EN=64*"69I"F9I"@II9B!;("(D5T=%5"(@73L@=&AE;@H):68@87!P7V5X
M:7-T<R`B)$585$5.4TE/3B(@(B1&4D]-5TA%4D4B.R!T:&5N"@D)96-H;R`B
M/'`^6R!)3D9/(%T@)$%04$Y!344@:7,@86QR96%D>2!D;W=N;&]A9&5D+CPO
M<#XB"@EE;'-E"@D);6MD:7(@+7`@(B1&4D]-5TA%4D4B"@D)5$%21T544T9%
M5$-(/2(D5$%21T544T9%5$-(7&XD15A414Y324].(@H)"5L@(B1$3U=.3$]!
M1%]/3DQ9(B!=("8F(%L@(B1/3D1%34%.1"(@72`F)B!O;F1E;6%N9"`B)$58
M5$5.4TE/3B(*"69I"F5L<V4*"51!4D=%5%-,3T-!3#TB)%1!4D=%5%-,3T-!
M3%QN)$585$5.4TE/3B(*9FD*"F1O;F4@(R!&:6YI<V@@=&AE(&9O<BUL;V]P
M(&9O<B!M=6QT:7!L92!E>'1E;G-I;VYS"@IC9"`B)$923TU72$5212(@?'P@
M97AI="`Q"@I2151263TP"DU!6%]215122453/34*"G=H:6QE(%L@)%)%5%)9
M("UL="`D34%87U)%5%))15,@70ID;PH)96-H;R`B,"(@/B`O=&UP+V%P<'-E
M<G(*"@EI9B!;("(D5$%21T544T9%5$-((B!=.R!T:&5N"@D)9V5T36ER<F]R
M"@D)5$%21T544T9%5$-(/2)@96-H;R`M92`D5$%21T544T9%5$-(('P@87=K
M("<O7'<O('MP<FEN="`D,2(@+B`G(B1-25)23U(B)R)])V`B"@D)<F5C=7)S
M:79E7W-C86Y?9&5P("(D5$%21T544T9%5$-((B!\('=H:6QE(')E860@1CL@
M9&\*"0D)>R!T97-T("(D>T8E)2`J?2(@/2`B0"(@)B8@15A414Y324]./2(D
M>T8C0"!](B`F)B!32TE0/2(B('Q\('1E<W0@(B132TE0(CL@?2`F)B!C;VYT
M:6YU90H)"0E&/2(D>T8C(RHO?2(*"0D)87!P7V5X:7-T<R`B)$8B("(N(B!\
M?"!F971C:%]A<'`@(B1&(@H)"0E;("0H8V%T("]T;7`O87!P<V5R<BD@/2`B
M,2(@72`F)B!B<F5A:PH)"0E;("UF("(D5$-%24Y35$%,3$5$+R1[1B4N*GTB
M(%T@?'P@:6YS=&%L;"`B)$8B"B,)"61O;F4@?'P@97AI="`Q(",@<W5B<VAE
M;&P@8V%N;F]T(&5X:70@9&ER96-T;'D*"0ED;VYE('Q\(&5C:&\@(C$B(#X@
M+W1M<"]A<'!S97)R(`H)9FD*"6EF(%L@)"AC870@+W1M<"]A<'!S97)R*2`]
M("(Q(B!=.R!T:&5N"@D)96-H;R`B/'`^6R!%4E)/4ET@5&AE<F4@=V%S(&$@
M97)R;W(@9&]W;FQO861I;F<@)'M%6%1%3E-)3TY]/"]P/B(*(PD)<FT@+68@
M)$585$5.4TE/3BH@("!.;W0@;F5E9&5D(&AE<F4N+BXN22!T:&EN:PH)"5)%
M5%)9/20H*%)%5%)9*S$I*0H)"6EF(%L@)%)%5%)9("UL="`D34%87U)%5%))
M15,@73L@=&AE;@H)"0EE8VAO("(\<#Y;($E.1D\@72!2971R>6EN9R!E>'1E
M;G-I;VX@)'M%6%1%3E-)3TY]+BXN+BXN+BYI;B`U('-E8V]N9',N/"]P/B(*
M"0D)<VQE97`@-0H)"65L<V4*"0D)96-H;R`B/'`^6R!%4E)/4B!=36%X(')E
M=')I97,@<F5A8VAE9#PO<#XB"@D)9FD*"65L<V4*"0EE8VAO("(\<#Y;($E.
M1D\@72!!;&P@1FEL97,@5&5S=&5D($=O;V0\+W`^(@H)"6)R96%K"@EF:0ID
M;VYE"@H*:68@6R`B)%1!4D=%5%-,3T-!3"(@73L@=&AE;@H)5$%21T544TQ/
M0T%,/2)@96-H;R`M92`D5$%21T544TQ/0T%,('P@87=K("<O7'<O('MP<FEN
M="`D,7TG8"(*"7)E8W5R<VEV95]S8V%N7V1E<"`B)%1!4D=%5%-,3T-!3"(@
M?"!W:&EL92!R96%D($8[(&1O"@D)>R!T97-T("(D>T8E)2`J?2(@/2`B0"(@
M)B8@15A414Y324]./2(D>T8C0"!](B`F)B!32TE0/2(B('Q\('1E<W0@(B13
M2TE0(CL@?2`F)B!C;VYT:6YU90H)"48](B1[1B,C*B]](@H)"6EF(%L@(2`M
M9B`B)%1#14E.4U1!3$Q%1"\D>T8E+BI](B!=.R!T:&5N"@D)"6EF(%L@+68@
M(B1&(B!=.R!T:&5N"@D)"0EI;G-T86QL("(D1B(*"0D)"5L@(B1355!04D53
M4R(@72!\?"!E8VAO("(D1CH@3TLB"@D)"65L<V4*"0D)"65C:&\@(B1&(&YO
M="!F;W5N9"$B"@D)"0EA8F]R=%]T;U]S879E9%]D:7(*"0D)9FD*"0EF:0H)
M9&]N92!\?"!E>&ET(#$@(R!S=6)S:&5L;"!C86YN;W0@97AI="!D:7)E8W1L
M>0IF:0H*6R`B)$)/3U1)3D<B(%T@)B8@97AI="`P"EL@)"AW:&EC:"`B)$1%
M4TM43U`B7W)E<W1A<G0I(%T@)B8@(B1$15-+5$]0(E]R97-T87)T(#(^+V1E
M=B]N=6QL"@II9B!;("0H8V%T("]T;7`O87!P<V5R<BD@/2`B,2(@73L@=&AE
:;@H)97AI="`Q"F5L<V4*"65X:70@,`IF:0H`
`
end
