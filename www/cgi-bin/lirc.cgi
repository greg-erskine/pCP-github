#!/bin/sh

# Version pCP3.00 2016-06-12 SBP
#	Changed to pcp-load to fetch the packages

# Version: 0.01 2016-03-15 GE
#	Original.

. pcp-lms-functions
. pcp-functions
pcp_variables
. $CONFIGCFG

ORIG_IR_LIRC=$IR_LIRC


pcp_html_head "LIRC" "GE"

pcp_banner
pcp_navigation
pcp_running_script
pcp_httpd_query_string


need_backup=no



#WGET="/bin/busybox wget"
#LIRC_REPOSITORY="https://raw.github.com/ralph-irving/tcz-lirc/master"
#PICO_REPOSITORY="http://ralph_irving.users.sourceforge.net/pico"
#IR_DOWNLOAD="/tmp/LIRC"
FAIL_MSG="ok"
#RESULT=0
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
#Copy the correct LIRC config files dependent upon Jivelite is in use or not
#----------------------------------------------------------------------------------------
pcp_lirc_configfiles() {
[ "$JIVELITE" = "yes" ] && sudo cp -f /usr/local/share/lirc/files/lircd-jivelite  /usr/local/etc/lirc/lircd.conf
[ "$JIVELITE" = "no" ] && sudo cp -f /usr/local/share/lirc/files/lircd.conf /usr/local/etc/lirc/lircd.conf
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
	[ "$need_backup" = "yes" ] && pcp_backup_nohtml
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
	echo '[ INFO ] Installing packages for IR remote control...'
	sudo -u tc pcp-load -r $PCP_REPO -wfi lirc.tcz
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
	echo '[ INFO ] Updating configuration files... '
	
	touch /home/tc/.lircrc
	sudo chown tc:staff /home/tc/.lircrc

	#add lirc-dtoverlay to config.txt
	pcp_mount_mmcblk0p1_nohtml
	echo '<p class="info">[ INFO ] Adding lirc overlay to config.txt...</p>'
	sed -i '/dtoverlay=lirc-rpi/d' $CONFIGTXT
	sudo echo "dtoverlay=lirc-rpi,gpio_in_pin=$IR_GPIO" >> $CONFIGTXT
	pcp_umount_mmcblk0p1_nohtml


	#add lirc conf to the filetool.lst
	[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] lirc configuration is added to .filetool.lst</p>'
	sudo sed -i '/lircd.conf/d' /opt/.filetool.lst
	sudo echo 'usr/local/etc/lirc/lircd.conf' >> /opt/.filetool.lst
	sudo sed -i '/.lircrc/d' /opt/.filetool.lst
	sudo echo 'home/tc/.lircrc' >> /opt/.filetool.lst

	pcp_lirc_configfiles

	# download lirc.dep file until the pcp-load script can handle this.
	[ ! -f /mnt/mmcblk0p2/tce/optional/lirc.tcz.dep ] && echo "[INFO] Downloading missing lirc.tcz.dep file"
	[ ! -f /mnt/mmcblk0p2/tce/optional/lirc.tcz.dep ] &&  sudo wget https://sourceforge.net/projects/picoreplayer/files/repo/8.x/armv7/tcz/lirc.tcz.dep/download -O /mnt/mmcblk0p2/tce/optional/lirc.tcz.dep

	[ "$FAIL_MSG" = "ok" ] && IR_LIRC="yes" && pcp_save_to_config
	[ "$FAIL_MSG" = "ok" ] && echo "OK" || echo "FAILED"
	need_backup=yes
}

#========================================================================================
# LIRC uninstall
#----------------------------------------------------------------------------------------
pcp_lirc_uninstall() {
	[ "$FAIL_MSG" = "ok" ] && pcp_delete_file irda-${KERNEL}.tcz
	[ "$FAIL_MSG" = "ok" ] && pcp_delete_file irda-${KERNEL}.tcz.md5.txt
	[ "$FAIL_MSG" = "ok" ] && pcp_delete_file lirc.tcz
#	[ "$FAIL_MSG" = "ok" ] && pcp_delete_file lirc.tcz.dep         <----- this file is not downloaded by pcp-load so for now we supply it with the image
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
	sudo sed -i '/lircd.conf/d' /opt/.filetool.lst
	sudo sed -i '/.lircrc/d' /opt/.filetool.lst

	[ "$FAIL_MSG" = "ok" ] && IR_LIRC="no" && pcp_save_to_config
	[ "$FAIL_MSG" = "ok" ] && echo "OK" || echo "FAILED"
}

#========================================================================================
# Main
#----------------------------------------------------------------------------------------
case "$ACTION" in
	Install)
		ACTION=$ACTION
		pcp_sufficient_free_space "$SPACE_REQUIRED"
	;;
	Uninstall)
		ACTION=$ACTION
	;;
	Custom)
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
	echo '                  <p>Set LIRC GPIO number&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Set GPIO to the connected IR Receiver.</p>'
	echo '                    <p>Default is using GPIO number 27, but change to match the GPIO you use for IR Receiver.</p>'
	echo '                    </ul>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	#----------------------------------------------------------------------------------------

	#------------------------------------------Custom LIRC Config-----------------------------------
if [ -f /usr/local/etc/lirc/lircd.conf ]; then
DISABLED=""
else
DISABLED="disabled"
fi

	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
		echo '                <td class="column150 center">'
		echo '                  <input type="submit" name="ACTION" value="Custom" '$DISABLED' />'
		echo '                </td>'
		echo '                <td>'
		echo '                  <p>Provide your own LIRC configuration file&nbsp;&nbsp;'
		echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
		echo '                  </p>'
		echo '                  <div id="'$ID'" class="less">'
		echo '                    <p>Default installation only supports Logitech Squeezebox remote, If you are using another remote controller you need to supply your own configuration files</p>'
		echo '                    <p>To use your own configuration file please either: </p>'
		echo '                  <ul>'
		echo '                    <li>1. Copy the file(s) via shh to the /tmp directory.</li>'
		echo '                  </ul>'
		echo '                    <p>or</p>'
		echo '                  <ul>'
		echo '                    <li>2. Copy the file(s) to an attached USB stick.</li>'
		echo '                  </ul>'
		echo '                    <p>Then press the button "Custom" and your configuration file will be copied and used by pCP.</p>'
		echo '                    <p>If you use <b>LIRC with Jivelite</b> the configuratio file should be named <b>"lircd.conf</b>".</p>'
		echo '                    <p>If you use <b>LIRC on a headless system (no Jivelite)</b> you will need to provide both <b>"lircd.conf" and "lircrc"</b> configuration files.</p>'
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
		echo '                  <p>Change LIRC GPIO number&nbsp;&nbsp;'
		echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
		echo '                  </p>'
		echo '                  <div id="'$ID'" class="less">'
		echo '                    <ul>'
		echo '                      <li>Change LIRC GPIO to a new value.</li>'
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
#		echo '                  <textarea class="inform" style="height:240px">'
		pcp_internet_indicator
		[ "$FAIL_MSG" = "ok" ] || pcp_html_end
		echo '[ INFO ] '$INTERNET_STATUS'<br>'
		pcp_sourceforge_indicator
		[ "$FAIL_MSG" = "ok" ] || pcp_html_end
		echo '[ INFO ] '$SOURCEFORGE_STATUS'<br>'
		pcp_sufficient_free_space $SPACE_REQUIRED
		pcp_get_file
		pcp_lirc_install
		need_backup=yes
	fi
	#---------------------------------------Uninstall----------------------------------------
	if [ "$ACTION" = "Uninstall" ]; then
		echo '                  <textarea class="inform" style="height:200px">'
		[ "$FAIL_MSG" = "ok" ] && pcp_lirc_uninstall
		need_backup=yes
	fi
	#---------------------------------------Custom-------------------------------------------
	if [ "$ACTION" = "Custom" ]; then
		echo '                  <textarea class="inform" style="height:100px">'
		#Copy from tmp to correct location
		[ -f /tmp/lircd.conf ] && sudo cp -f /tmp/lircd.conf /usr/local/etc/lirc/lircd.conf && sudo rm -f /tmp/lircd.conf
		[ -f /tmp/lircrc ] && sudo cp -f /tmp/lircrc /home/tc/.lircrc && sudo rm -f /tmp/lircrc

		#Copy from USB to correct location		
		# Check if sda1 is mounted, otherwise mount it.
		MNTUSB=/mnt/sda1
		if mount | grep $MNTUSB; then
		echo "/dev/sda1 already mounted."
		else
				# Check if sda1 is inserted before trying to mount it.
				if [ -e /dev/sda1 ]; then
				[ -d /mnt/sda1 ] || mkdir -p /mnt/sda1
				echo "Trying to mount /dev/sda1."
				sudo mount /dev/sda1 >/dev/null 2>&1
				else
				echo "No USB Device detected in /dev/sda1"
				fi
		fi

	[ -f $MNTUSB/lircd.conf ] && sudo cp -f $MNTUSB/lircd.conf /home/tc/.lircrc && sudo mv $MNTUSB/lircd.conf $MNTUSB/used_lircd.conf
	[ -f $MNTUSB/lircrc ] && sudo cp -f $MNTUSB/lircrc /home/tc/.lircrc && sudo mv $MNTUSB/lircrc $MNTUSB/used_lircrc

	need_backup=yes
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
		need_backup=yes
	fi
	#----------------------------------------------------------------------------------------
	
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
