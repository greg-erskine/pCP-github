#!/bin/sh

# Version: 0.01 2016-03-15 GE
#	Original.

. pcp-lms-functions
. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "LIRC" "GE"

pcp_banner
pcp_navigation
pcp_running_script
pcp_httpd_query_string

WGET="/bin/busybox wget"
LIRC_REPOSITORY="https://raw.github.com/ralph-irving/tcz-lirc/master"
PICO_REPOSITORY="http://ralph_irving.users.sourceforge.net/pico"
IR_DOWNLOAD="/tmp/LIRC"
FAIL_MSG="ok"
RESULT=0
KERNEL=$(uname -r)

#========================================================================================
#  335872 irda-4.1.13-piCore+.tcz
#  221184 lirc.tczlirc.tcz
#    8192 libcofi.tcz
# --------
#  565248
#----------------------------------------------------------------------------------------
SPACE_REQUIRED=600

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
# Check for free space - set FAIL_MSG if insufficient space is available
#----------------------------------------------------------------------------------------
pcp_enough_free_space() {
	REQUIRED_SPACE=$1
	FREE_SPACE=$(pcp_free_space k)
	if [ $FREE_SPACE -gt $REQUIRED_SPACE ]; then
		echo '[  OK  ] Free space: '$FREE_SPACE'k - Required space: '$REQUIRED_SPACE'k'
	else
		echo '[ ERROR ] Free space: '$FREE_SPACE'k - Required space: '$REQUIRED_SPACE'k'
		echo '[ ERROR ] Not enough free space - try expanding your partition.'
		FAIL_MSG="Not enough free space - try expanding your partition."
	fi
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

	pcp_footer
	pcp_copyright

	echo '</body>'
	echo '</html>'
	[ "$ACTION" != "Initial" ] && pcp_reboot_required
	exit
}

#========================================================================================
# Get a file from a remote repository
#----------------------------------------------------------------------------------------
pcp_get_file() {
	[ "$1" = "lirc" ] && REPOSITORY=${LIRC_REPOSITORY}
	[ "$1" = "pico" ] && REPOSITORY=${PICO_REPOSITORY}
	echo -n '[ INFO ] Downloading '$2'... '
	$WGET --no-check-certificate ${REPOSITORY}/$2 -O ${IR_DOWNLOAD}/$2
	if [ $? -eq 0 ]; then
		echo "OK"
	else
		echo "FAILED"
		FAIL_MSG="Failed to download $1"
	fi
}

#========================================================================================
# Delete a file from the local repository
#----------------------------------------------------------------------------------------
pcp_delete_file() {
	echo -n '[ INFO ] Deleting '$1'... '
	rm -f /mnt/mmcblk0p2/tce/optional/${1}
	[ $? -eq 0 ] || FAIL_MSG="Cannot delete ${1}."
	[ "$FAIL_MSG" = "ok" ] && echo "OK" || echo "FAILED"
}

#========================================================================================
# LIRC install
#----------------------------------------------------------------------------------------
pcp_lirc_install() {
	echo '[ INFO ] Preparing download directory...'
	if [ -d $IR_DOWNLOAD ]; then
		sudo rm -rf $IR_DOWNLOAD
		[ $? -ne 0 ] && FAIL_MSG="Can not remove directory $IR_DOWNLOAD"
	fi
	sudo mkdir -m 755 $IR_DOWNLOAD
	[ $? -ne 0 ] && FAIL_MSG="Can not make directory $IR_DOWNLOAD"

	[ "$FAIL_MSG" = "ok" ] && pcp_get_file lirc irda-${KERNEL}.tcz
	[ "$FAIL_MSG" = "ok" ] && pcp_get_file lirc irda-${KERNEL}.tcz.md5.txt
	[ "$FAIL_MSG" = "ok" ] && pcp_get_file lirc lirc.tcz
 	[ "$FAIL_MSG" = "ok" ] && pcp_get_file lirc lirc.tcz.dep
 	[ "$FAIL_MSG" = "ok" ] && pcp_get_file lirc lirc.tcz.md5.txt

	if [ ! -f /mnt/mmcblk0p2/tce/optional/libcofi.tcz ]; then
		[ "$FAIL_MSG" = "ok" ] && pcp_get_file pico libcofi.tcz
		[ "$FAIL_MSG" = "ok" ] && pcp_get_file pico libcofi.tcz.md5.txt
	fi

	echo -n '[ INFO ] Installing files... '
	[ "$FAIL_MSG" = "ok" ] && sudo chown tc:staff $IR_DOWNLOAD/*
	[ $? -eq 0 ] || FAIL_MSG="Can not change ownership."
	[ "$FAIL_MSG" = "ok" ] && sudo chmod u=rw,g=rw,o=r $IR_DOWNLOAD/*
	[ $? -eq 0 ] || FAIL_MSG="Can not change permissions."
	[ "$FAIL_MSG" = "ok" ] && sudo cp -af $IR_DOWNLOAD/* /mnt/mmcblk0p2/tce/optional/
	[ $? -eq 0 ] || FAIL_MSG="Can not copy to tce/optional."
	[ "$FAIL_MSG" = "ok" ] && echo "OK" || echo "FAILED"

	echo '[ INFO ] Updating configuration files... '

	touch /home/tc/.lircrc
	sudo chown tc:staff /home/tc/.lircrc

	pcp_mount_mmcblk0p1_nohtml
	sed -i '/dtoverlay=lirc-rpi/d' $CONFIGTXT
	sudo echo "dtoverlay=lirc-rpi,gpio_in_pin=$IR_GPIO" >> $CONFIGTXT
	pcp_umount_mmcblk0p1_nohtml

	sudo sed -i '/lirc.tcz/d' $ONBOOTLST
	sudo echo "lirc.tcz" >> $ONBOOTLST

	[ "$FAIL_MSG" = "ok" ] && IR_LIRC="yes" && pcp_save_to_config
	[ "$FAIL_MSG" = "ok" ] && echo "OK" || echo "FAILED"
}

#========================================================================================
# LIRC uninstall
#----------------------------------------------------------------------------------------
pcp_lirc_uninstall() {
	[ "$FAIL_MSG" = "ok" ] && pcp_delete_file irda-${KERNEL}.tcz
	[ "$FAIL_MSG" = "ok" ] && pcp_delete_file irda-${KERNEL}.tcz.md5.txt
	[ "$FAIL_MSG" = "ok" ] && pcp_delete_file lirc.tcz
	[ "$FAIL_MSG" = "ok" ] && pcp_delete_file lirc.tcz.dep
	[ "$FAIL_MSG" = "ok" ] && pcp_delete_file lirc.tcz.md5.txt

	if [ $SHAIRPORT = "no" ]; then
		[ "$FAIL_MSG" = "ok" ] && pcp_delete_file libcofi.tcz
		[ "$FAIL_MSG" = "ok" ] && pcp_delete_file libcofi.tcz.md5.txt
	fi

	echo '[ INFO ] Removing configuration files... '

	rm -f /home/tc/.lircrc

	pcp_mount_mmcblk0p1_nohtml
	sed -i '/dtoverlay=lirc-rpi/d' $CONFIGTXT
	pcp_umount_mmcblk0p1_nohtml

	sudo sed -i '/lirc.tcz/d' $ONBOOTLST

	[ "$FAIL_MSG" = "ok" ] && IR_LIRC="no" && pcp_save_to_config
	[ "$FAIL_MSG" = "ok" ] && echo "OK" || echo "FAILED"
}

#========================================================================================
# Main
#----------------------------------------------------------------------------------------
case "$ACTION" in
	Install)
		ACTION=$ACTION
	;;
	Uninstall)
		ACTION=$ACTION
	;;
	Change)
		ACTION=$ACTION
	;;
	*)
		ACTION=Initial
	;;
esac

#========================================================================================
# Start Initial table
#----------------------------------------------------------------------------------------
if [ "$ACTION" = "Initial" ] || [ "$ACTION" = "Change" ]; then
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Linux Infrared Remote Control (LIRC)</legend>'
	echo '          <table class="bggrey percent100">'
	echo '            <form name="LIRC" action="'$0'" method="get">'

	#------------------------------------------Install/Unintall LIRC-------------------------
	pcp_incr_id
	pcp_start_row_shade
	echo '              <tr class="'$ROWSHADE'">'

	if [ "$IR_LIRC" = "no" ]; then
		echo '                <td class="column150 center">'
		echo '                  <input type="submit" name="ACTION" value="Install" />'
		echo '                </td>'
		echo '                <td>'
		echo '                  <p>Install LIRC&nbsp;&nbsp;'
		echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
		echo '                  </p>'
		echo '                  <div id="'$ID'" class="less">'
		echo '                    <p>Install LIRC from repository.</p>'
		echo '                  </div>'
		echo '                </td>'
	else
		echo '                <td class="column150 center">'
		echo '                  <input type="submit" name="ACTION" value="Uninstall" />'
		echo '                </td>'
		echo '                <td>'
		echo '                  <p>Uninstall LIRC&nbsp;&nbsp;'
		echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
		echo '                  </p>'
		echo '                  <div id="'$ID'" class="less">'
		echo '                    <p>Uninstall LIRC from '$NAME'.</p>'
		echo '                  </div>'
		echo '                </td>'
	fi

	echo '              </tr>'
	#----------------------------------------------------------------------------------------

	#------------------------------------------LIRC GPIO-------------------------------------
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                  <input class="input" type="number" name="IR_GPIO" value="'$IR_GPIO'">'  
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Set LIRC GPIO&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Set GPIO to the connected IR Receiver.</p>'
	echo '                    </ul>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	#----------------------------------------------------------------------------------------

	#------------------------------------------LIRC Config-----------------------------------
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                  <input class="input" type="text" name="IR_CONFIG" value="'$IR_CONFIG'">'  
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Set alternative LIRC configuration file&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Default:</b> ~/.licrc</p>'
	echo '                    </ul>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	#----------------------------------------------------------------------------------------

	#------------------------------------------Change----------------------------------------
	if [ "$IR_LIRC" = "yes" ]; then
		pcp_incr_id
		pcp_toggle_row_shade
		echo '              <tr class="'$ROWSHADE'">'
		echo '                <td class="column150 center">'
		echo '                  <input type="submit" name="ACTION" value="Change" />'
		echo '                </td>'
		echo '                <td>'
		echo '                  <p>Change LIRC GPIO and/or configuration file&nbsp;&nbsp;'
		echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
		echo '                  </p>'
		echo '                  <div id="'$ID'" class="less">'
		echo '                    <ul>'
		echo '                      <li>Change LIRC GPIO to a new value.</li>'
		echo '                      <li>Change LIRC configuration file.</li>'
		echo '                    </ul>'
		echo '                  </div>'
		echo '                </td>'
		echo '              </tr>'
	fi
	#----------------------------------------------------------------------------------------

	echo '            </form>'
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
fi
#----------------------------------------------------------------------------------------

#========================================================================================
# Installing table
#----------------------------------------------------------------------------------------
if [ "$ACTION" != "Initial" ]; then
	pcp_incr_id
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>'$ACTION'</legend>'
	echo '          <table class="bggrey percent100">'
	pcp_start_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td>'
	#---------------------------------------Install------------------------------------------
	if [ "$ACTION" = "Install" ]; then
		echo '                  <textarea class="inform" style="height:240px">'
		pcp_internet_indicator
		[ "$FAIL_MSG" = "ok" ] || pcp_html_end
		echo '[ INFO ] '$INTERNET_STATUS
		pcp_sourceforge_indicator
		[ "$FAIL_MSG" = "ok" ] || pcp_html_end
		echo '[ INFO ] '$SOURCEFORGE_STATUS
		pcp_enough_free_space $SPACE_REQUIRED
		[ "$FAIL_MSG" = "ok" ] && pcp_lirc_install
	fi
	#---------------------------------------Uninstall----------------------------------------
	if [ "$ACTION" = "Uninstall" ]; then
		echo '                  <textarea class="inform" style="height:200px">'
		[ "$FAIL_MSG" = "ok" ] && pcp_lirc_uninstall
	fi
	#---------------------------------------Change-------------------------------------------
	if [ "$ACTION" = "Change" ]; then
		echo '                  <textarea class="inform" style="height:100px">'
		[ "$FAIL_MSG" = "ok" ] && pcp_save_to_config
		pcp_mount_mmcblk0p1_nohtml
		echo '[ INFO ] Changing '$CONFIGTXT'... '
		sed -i '/dtoverlay=lirc-rpi/d' $CONFIGTXT
		sudo echo "dtoverlay=lirc-rpi,gpio_in_pin=$IR_GPIO" >> $CONFIGTXT
		pcp_umount_mmcblk0p1_nohtml
	fi
	#----------------------------------------------------------------------------------------
	pcp_backup_nohtml

	echo '                  </textarea>'
	echo '                </td>'
	echo '              </tr>'
	#----------------------------------------------------------------------------------------
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
fi

pcp_html_end
