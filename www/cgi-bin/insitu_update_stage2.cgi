#!/bin/sh

# Version 2.05 2016-04-17 SBP
#	Currently a copy of the old insitu_update.cgi.  

# Version: 0.03 2016-02-19 SBP
#	Added code to allow existing add-ons to remain functioning.
#	Fixed sourceforge redirection issue.

# Version: 0.02 2016-02-10 GE
#	Added warning on each page.
#	Added warnings for alsaequal and slimserver.

# version: 0.01 2016-02-03 GE
#	Original - Combined upd_picoreplayer.cgi, insitu.cgi and do_updatepicoreplayer.cgi

. pcp-functions
pcp_variables

pcp_html_head "Update pCP" "GE"

pcp_banner
pcp_navigation
pcp_running_script
pcp_httpd_query_string

WGET="/bin/busybox wget -T 30"
FAIL_MSG="ok"

# As all the insitu upgrade is done in one file, it may be better to define this here
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
	echo '[ INFO ] Step 1. - Downloading insitu.cfg...'
	$WGET ${INSITU_DOWNLOAD}/insitu.cfg/download -O ${UPD_PCP}/insitu.cfg
	if [ $? -eq 0 ]; then
		echo '[  OK  ] Successfully downloaded insitu.cfg'
	else
		echo '[ ERROR ] Error downloading insitu.cfg'
		FAIL_MSG="Error downloading insitu.cfg"
	fi
}

#========================================================================================
# Download the boot files from Sourceforge
#----------------------------------------------------------------------------------------
pcp_get_boot_files() {
	echo '[ INFO ] Step 2A. - Downloading '$VERSION'_boot.tar.gz'
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

	[ "$FAIL_MSG" = "ok" ] && echo '[  OK  ] Your configuration files have been saved to the boot partition.'
}

#========================================================================================
# Download the tce files from Sourceforge
#----------------------------------------------------------------------------------------
pcp_get_tce_files() {
	echo '[ INFO ] Step 2B. - Downloading '$VERSION'_tce.tar.gz'
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
	# Unpack the tce.tar and the new mydata.tgz and then copy the content from the new version to the correct loactions
	sudo mkdir ${UPD_PCP}/mydata
	sudo tar zxvf ${UPD_PCP}/tce/${VERSION}_tce.tar.gz -C ${UPD_PCP}/mydata
	sudo tar zxvf ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce/mydata.tgz -C ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce

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
	# So check that the final bootlocal.sh contains all from the new version and add eventual extra from the old
	sudo chown root:staff /opt/bootlocal.sh
	grep -Fxv -f /opt/bootlocal.sh ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce/opt/bootlocal.sh >> /opt/bootlocal.sh

#	sudo cat /opt/bootlocal.sh >> ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce/opt/bootlocal.sh
#	sort -u ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce/opt/bootlocal.sh > /opt/bootlocal.sh
	sudo chown root:staff /opt/bootlocal.sh
	sudo chmod u=rwx,g=rwx,o=rx /opt/bootlocal.sh

	#update of the config.cfg file is done via newconfig and do_rebootstuff after next reboot as it always have been done

	# Update pCP by copying the content from the new version to the correct loaction followed by a backup 
	sudo cp -af ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce/etc/motd /etc/motd
	sudo cp -Rf ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce/home/tc/www/ /home/tc/

	sudo cp -af ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce/home/tc/.local/bin/.pbtemp /home/tc/.local/bin/.pbtemp
	sudo cp -af ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce/home/tc/.local/bin/copywww.sh /home/tc/.local/bin/copywww.sh
	sudo cp -af ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce/usr/local/etc/pointercal /usr/local/etc/pointercal
	sudo cp -Rf ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce/usr/local/etc/init.d/ /usr/local/etc/init.d/
	sudo cp -af ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce/usr/local/sbin/pcp /usr/local/sbin/pcp
	sudo cp -af ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce/usr/local/sbin/piversion.cfg /usr/local/sbin/piversion.cfg
	sudo cp -af ${UPD_PCP}/mydata/mnt/mmcblk0p2/tce/usr/local/sbin/setup /usr/local/sbin/setup

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
	echo '                <p style="color:white"><b>Warning:</b> An insitu upgrade will overwrite ALL data on your SD card.</p>'
	echo '                <ul>'
	echo '                  <li style="color:white">Any addtional extensions will need to be reinstalled i.e. jivelite, shairport-sync, alsaequal.</li>'
	echo '                  <li style="color:white">Any modified or additional files will be lost.</li>'
	echo '                  <li style="color:white">An insitu upgrade requires about 50% free space.</li>'
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
		STEP="Step 1 - Downloading available versions"
		pcp_warning_message
		pcp_internet_indicator
		[ "$FAIL_MSG" = "ok" ] || pcp_html_end
		pcp_sourceforge_indicator
		[ "$FAIL_MSG" = "ok" ] || pcp_html_end
		pcp_create_download_directory
		[ "$FAIL_MSG" = "ok" ] || pcp_html_end
		;;
	download)
		STEP="Step 2 - Downloading files"
		pcp_warning_message
		;;
	install)
		STEP="Step 3 - Installing files"
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
	echo '          <legend>piCorePlayer insitu upgrade</legend>'
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
	echo '                  <p>Select the upgrade version of piCorePlayer required.</p>'
	echo '                </td>'
	echo '              </tr>'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="large18 center">'
	echo '                  <input class="large12" type="submit" value="Next >">'
	echo '                  <input type="hidden" name="ACTION" value="download">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Press the [ Next ] button to download upgrade files.</p>'
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
	echo '          <legend>piCorePlayer insitu upgrade</legend>'
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
	echo '                  <p>Press the [ Next ] button to install the upgrade files.</p>'
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
	echo '          <legend>piCorePlayer insitu upgrade</legend>'
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
