#!/bin/sh

# Version: 3.21 2017-05-20
#	Changed to allow booting from USB on RPI3. PH.

# Version: 3.20 2017-03-08
#	Fixed pcp-xxx-functions issues. GE.

# Version: 3.10 2016-12-22
#	Added lirc[0-9] and hidraw[0-9]. GE.
#	Added LIRC gpio out for IR transmitter. GE.
#	Sourceforge repo updates. PH

# Version: 3.01 2016-08-27
#	Changed default lirc GPIO to 25. GE.

# Version: 3.00 2016-08-09
#	Changed to pcp-load to fetch the packages. SBP.
#	Added PCremote support. GE.

# Version: 0.01 2016-03-15 GE
#	Original.

. pcp-functions
. pcp-lms-functions
#. $CONFIGCFG

ORIG_IR_LIRC=$IR_LIRC			# <=== GE not implemented yet
ORIG_IR_DEVICE=$IR_DEVICE		# <=== GE not implemented yet

unset BACKUP_REQUIRED REBOOT_REQUIRED SDA1_MOUNTED CONFIG_FOUND

pcp_html_head "LIRC" "GE"

pcp_banner
pcp_navigation
pcp_running_script
pcp_httpd_query_string

FAIL_MSG="ok"
KERNEL=$(uname -r)
DEFAULT_IR_GPIO_IN="25"
DEFAULT_IR_GPIO_OUT=""

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
# Do a backup if required
#----------------------------------------------------------------------------------------
pcp_backup_if_required() {
	if [ $BACKUP_REQUIRED ]; then
		echo '<table class="bggrey">'
		echo '  <tr>'
		echo '    <td>'
		echo '      <div class="row">'
		echo '        <fieldset>'
		echo '          <legend>Backup required</legend>'
		echo '          <table class="bggrey percent100">'
		pcp_start_row_shade
		echo '            <tr class="'$ROWSHADE'">'
		echo '              <td>'
		echo '                <textarea class="inform" style="height:40px">'
		                        pcp_backup_nohtml
		                        [ $? -eq 0 ] || FAIL_MSG="Backup failed."
		echo '                </textarea>'
		echo '              </td>'
		echo '            </tr>'
		echo '          </table>'
		echo '        </fieldset>'
		echo '      </div>'
		echo '    </td>'
		echo '  </tr>'
		echo '</table>'
	fi
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

	pcp_footer
	pcp_copyright
	pcp_remove_query_string

	echo '</body>'
	echo '</html>'
	[ "$REBOOT_REQUIRED" ] && pcp_reboot_required
	exit
}

#========================================================================================
# Delete a file from the local repository
#----------------------------------------------------------------------------------------
pcp_delete_file() {
	echo -n '[ INFO ] Deleting '$1'... '
	rm -f $TCEMNT/tce/optional/${1}
	[ $? -eq 0 ] || FAIL_MSG="Cannot delete ${1}."
	[ "$FAIL_MSG" = "ok" ] && echo "OK" || echo "FAILED"
}

#========================================================================================
# LIRC install
#----------------------------------------------------------------------------------------
pcp_lirc_install() {

	echo '[ INFO ] Installing packages for IR remote control.'
	echo '[ INFO ] This can take a couple of minutes. Please wait...'
	sudo -u tc pcp-load -r $PCP_REPO -wi lirc.tcz

	echo '[ INFO ] Updating configuration files... '

	touch /home/tc/.lircrc
	sudo chown tc:staff /home/tc/.lircrc

	# Add lirc-rpi dtoverlay to config.txt
	pcp_mount_mmcblk0p1_nohtml
	echo '[ INFO ] Adding lirc-rpi overlay to config.txt... '
	sed -i '/dtoverlay=lirc-rpi/d' $CONFIGTXT
	if [ "$IR_GPIO_OUT" = "" ]; then
		sudo echo "dtoverlay=lirc-rpi,gpio_in_pin=$IR_GPIO_IN" >> $CONFIGTXT
	else
		sudo echo "dtoverlay=lirc-rpi,gpio_in_pin=$IR_GPIO_IN,gpio_out_pin=$IR_GPIO_OUT" >> $CONFIGTXT
	fi
	pcp_umount_mmcblk0p1_nohtml

	# Add lirc conf to the .filetool.lst
	[ $DEBUG -eq 1 ] && echo '[ DEBUG ] lirc configuration is added to .filetool.lst'
	sudo sed -i '/lircd.conf/d' /opt/.filetool.lst
	sudo echo 'usr/local/etc/lirc/lircd.conf' >> /opt/.filetool.lst
	sudo sed -i '/.lircrc/d' /opt/.filetool.lst
	sudo echo 'home/tc/.lircrc' >> /opt/.filetool.lst

	if [ "$JIVELITE" = "yes" ]; then
		sudo cp -f /usr/local/share/lirc/files/lircd-jivelite /usr/local/etc/lirc/lircd.conf
	else
		sudo cp -f /usr/local/share/lirc/files/lircd.conf /usr/local/etc/lirc/lircd.conf
	fi

	[ "$FAIL_MSG" = "ok" ] && IR_LIRC="yes" && pcp_save_to_config
}

#========================================================================================
# LIRC uninstall
#----------------------------------------------------------------------------------------
pcp_lirc_uninstall() {
	#Should we move this to tce-audit delete ?
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
	[ $? -eq 0 ] && echo "[ INFO ] dtoverlay=lirc-rpi removed." || FAIL_MSG="Can not remove dtoverlay=lirc-rpi."
	pcp_umount_mmcblk0p1_nohtml

	sudo sed -i '/lirc.tcz/d' $ONBOOTLST
	sudo sed -i '/lircd.conf/d' /opt/.filetool.lst
	sudo sed -i '/.lircrc/d' /opt/.filetool.lst

	if [ "$FAIL_MSG" = "ok" ]; then
		IR_LIRC="no"
		IR_GPIO_IN=$DEFAULT_IR_GPIO_IN
		IR_GPIO_OUT=$DEFAULT_IR_GPIO_OUT
		IR_DEVICE="lirc0"
		IR_CONFIG=""
		pcp_save_to_config
	fi
}

#========================================================================================
# Main				<==== GE. This section is a little weird.
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
	Save)
		ACTION=$ACTION
		[ "$IR_GPIO_IN" = "" ] && IR_GPIO_IN=$DEFAULT_IR_GPIO_IN
	;;
	*)
		ACTION="Initial"
	;;
esac

#========================================================================================
# Linux Infrared Remote Control (LIRC) table
#----------------------------------------------------------------------------------------
if [ "$ACTION" = "Initial" ] || [ "$ACTION" = "Save" ]; then
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Linux Infrared Remote Control (LIRC)</legend>'
	echo '          <table class="bggrey percent100">'
	echo '            <form name="main" action="'$0'" method="get">'

	#------------------------------------------Install/Unintall LIRC-------------------------
	pcp_incr_id
	pcp_start_row_shade
	echo '              <tr class="'$ROWSHADE'">'

	if [ "$IR_LIRC" = "yes" ]; then
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
	else
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
	fi

	echo '              </tr>'
	#----------------------------------------------------------------------------------------

	#------------------------------------------Custom LIRC Config----------------------------
	[ -f /usr/local/etc/lirc/lircd.conf ] && DISABLED="" || DISABLED="disabled"

	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="ACTION" value="Custom" '$DISABLED' />'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Install your own LIRC configuration file(s)&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Default installation only supports Logitech Squeezebox remote. If you are using another'
	echo '                       remote controller you need to supply your own configuration file(s).</p>'
	echo '                    <p>To use your own configuration file(s): </p>'
	echo '                    <ol>'
	echo '                      <li>Copy the file(s) either:</li>'
	echo '                        <ul>'
	echo '                          <li>via ssh to the /tmp directory, <b>or</b></li>'
	echo '                          <li>to an attached USB flash drive.</li>'
	echo '                        </ul>'
	echo '                      <li>Press the [Custom] button and your configuration file(s) will be copied and used by pCP.</li>'
	echo '                    </ol>'
	echo '                    <p><b>Note:</b></p>'
	echo '                    <ul>'
	echo '                      <li>If you use <b>LIRC with Jivelite</b> the configuration file should be named <b>"lircd.conf</b>".</li>'
	echo '                      <li>If you use <b>LIRC on a headless system (no Jivelite)</b> you will need to provide'
	echo '                       both <b>"lircd.conf" and "lircrc"</b> configuration files.</li>'
	echo '                    </ul>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	#----------------------------------------------------------------------------------------

	#----------------------------------------------------------------------------------------
	echo '            </form>'
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
	#----------------------------------------------------------------------------------------

	#========================================================================================
	# LIRC Settings table
	#----------------------------------------------------------------------------------------
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>LIRC Settings</legend>'
	echo '          <table class="bggrey percent100">'
	echo '            <form name="settings" action="'$0'" method="get">'
	#----------------------------------------------------------------------------------------

	#------------------------------------------LIRC GPIO IN-----------------------------------
	# gpio_in_pin    GPIO for input (default "18")
	#-----------------------------------------------------------------------------------------
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                  <input class="input"'
	echo '                         type="number"'
#	echo '                         type="text"'
	echo '                         name="IR_GPIO_IN"'
	echo '                         value="'$IR_GPIO_IN'"'
	echo '                         title="( 0 - 31 )"'
#	echo '                         title="( 4,5,6,12,13,16,17,20,22,23,24,25,26,27 )"'
	echo '                         min="0"'
	echo '                         max="31"'
#	echo '                         pattern="(4|5|6|12|13|16|17|20|22|23|24|25|26|27)"'
	echo '                  >'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Set LIRC GPIO in number (IR receiver)&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>&lt;0 - 31&gt;</p>'
#	echo '                    <p>&lt;4,5,6,12,13,16,17,20,22,23,24,25,26,27&gt;</p>'
	echo '                    <p><b>Default:</b> '$DEFAULT_IR_GPIO_IN'</p>'
	echo '                    <p>Set GPIO in number to match the GPIO used to connect the IR Receiver.</p>'
	echo '                    <p><b>Warning:</b> Be careful not to set the GPIO to one being used for another purpose.</p>'
	echo '                    <p><b>Note:</b> Not used for USB PCRemote.</p>'
	echo '                    </ul>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	#----------------------------------------------------------------------------------------

	if [ $MODE -ge $MODE_BETA ]; then
		#------------------------------------------LIRC GPIO OUT---------------------------------
		# gpio_out_pin    GPIO for output (default "17")
		#----------------------------------------------------------------------------------------
		pcp_incr_id
		pcp_toggle_row_shade
		echo '              <tr class="'$ROWSHADE'">'
		echo '                <td class="column150 center">'
		echo '                  <input class="input"'
		echo '                         type="number"'
		echo '                         name="IR_GPIO_OUT"'
		echo '                         value="'$IR_GPIO_OUT'"'
		echo '                         title="( 0 - 31 )"'
		echo '                         min="0"'
		echo '                         max="31"'
		echo '                  >'
		echo '                </td>'
		echo '                <td>'
		echo '                  <p>Set LIRC GPIO out number (IR transmitter)&nbsp;&nbsp;'
		echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
		echo '                  </p>'
		echo '                  <div id="'$ID'" class="less">'
		echo '                    <p>&lt;0 - 31&gt;</p>'
		echo '                    <p><b>Default:</b> '$DEFAULT_IR_GPIO_OUT'</p>'
		echo '                    <p>Set GPIO out number to match the GPIO used to connect the IR Transmitter.</p>'
		echo '                    <p><b>Warning:</b> Be careful not to set the GPIO to one being used for another purpose.</p>'
		echo '                    </ul>'
		echo '                  </div>'
		echo '                </td>'
		echo '              </tr>'
		#----------------------------------------------------------------------------------------
	fi

	#------------------------------------------IR Device-------------------------------------
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                  <input id="input'$ID'"'
	echo '                         class="input"'
	echo '                         type="text"'
	echo '                         name="IR_DEVICE"'
	echo '                         value="'$IR_DEVICE'"'
	echo '                         title="( lirc[0-9] | hidraw[0-9] )"'
	echo '                         pattern="(lirc[0-9]|hidraw[0-9])"'
	echo '                  >'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Set IR Device to GPIO or USB&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>&lt;lirc[0-9]|hidraw[0-9]&gt;</p>'
	echo '                    <p><b>Default:</b> lirc0</p>'
	echo '                    <ul>'
	echo '                      <li class="pointer" title="Click to use lirc0" onclick="pcp_copy_click_to_input('\'input${ID}\',\'option1\'')">'
	echo '                        <span id="option1">lirc0</span> - GPIO IR Receiver.</li>'
	echo '                      <li class="pointer" title="Click to use hidraw1" onclick="pcp_copy_click_to_input('\'input${ID}\',\'option2\'')">'
	echo '                        <span id="option2">hidraw1</span> - USB Remote control.</li>'
	echo '                    </ul>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	#----------------------------------------------------------------------------------------

	#------------------------------------------Save------------------------------------------
	if [ "$IR_LIRC" = "yes" ]; then
		pcp_incr_id
		pcp_toggle_row_shade
		echo '              <tr class="'$ROWSHADE'">'
		echo '                <td class="column150 center" colspan="3">'
		echo '                  <input type="submit"'
		echo '                         name="ACTION"'
		echo '                         value="Save"'
		echo '                         title="Save LIRC settings"'
		echo '                  />'
		echo '                </td>'
		echo '              </tr>'
	fi
	#----------------------------------------------------------------------------------------

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
	#----------------------------------------------------------------------------------------

	#---------------------------------------Install------------------------------------------
	if [ "$ACTION" = "Install" ]; then
		echo '                  <textarea class="inform" style="height:240px">'
		pcp_internet_indicator
		[ "$FAIL_MSG" = "ok" ] || pcp_html_end
		echo '[ INFO ] '$INTERNET_STATUS
		pcp_sourceforge_indicator
		[ "$FAIL_MSG" = "ok" ] || pcp_html_end
		echo '[ INFO ] '$SOURCEFORGE_STATUS
		pcp_sufficient_free_space "nohtml" $SPACE_REQUIRED
		pcp_lirc_install
		BACKUP_REQUIRED=TRUE
		REBOOT_REQUIRED=TRUE
	fi
	#----------------------------------------------------------------------------------------

	#---------------------------------------Uninstall----------------------------------------
	if [ "$ACTION" = "Uninstall" ]; then
		echo '                  <textarea class="inform" style="height:200px">'
		[ "$FAIL_MSG" = "ok" ] && pcp_lirc_uninstall
		BACKUP_REQUIRED=TRUE
		REBOOT_REQUIRED=TRUE
	fi

	#----------------------------------------------------------------------------------------

	#---------------------------------------Custom-------------------------------------------
	if [ "$ACTION" = "Custom" ]; then
		echo '                  <textarea class="inform" style="height:100px">'
		# Copy from tmp to correct location
		echo "[ INFO ] Looking for configuration file(s) in /tmp..."
		if [ -f /tmp/lircd.conf ]; then
			echo "[ INFO ] Copying /tmp/lircd.conf..."
			sudo cp -f /tmp/lircd.conf /usr/local/etc/lirc/lircd.conf
			sudo rm -f /tmp/lircd.conf
			BACKUP_REQUIRED=TRUE
			REBOOT_REQUIRED=TRUE
			CONFIG_FOUND=TRUE
		else
			echo "[ INFO ] /tmp/lircd.conf not found."
		fi
		if [ -f /tmp/lircrc ]; then
			echo "[ INFO ] Copying /tmp/lircrc..."
			sudo cp -f /tmp/lircrc /home/tc/.lircrc
			sudo rm -f /tmp/lircrc
			BACKUP_REQUIRED=TRUE
			REBOOT_REQUIRED=TRUE
			CONFIG_FOUND=TRUE
		else
			echo "[ INFO ] /tmp/lircrc not found."
		fi

		if [ ! $CONFIG_FOUND ]; then
			# Copy from USB to correct location
			# Check if sda1 is mounted, otherwise mount it.
			MNTUSB=/mnt/sda1
			if mount >/dev/null | grep $MNTUSB; then
				echo "[ WARN ] /dev/sda1 already mounted."
				SDA1_MOUNTED=TRUE
			else
				# Check if sda1 is inserted before trying to mount it.
				if [ -e /dev/sda1 ]; then
					[ -d /mnt/sda1 ] || mkdir -p /mnt/sda1
					sudo mount /dev/sda1 >/dev/null 2>&1
					[ $? -eq 0 ] && echo "[ INFO ] Mounted /dev/sda1."
					SDA1_MOUNTED=TRUE
				else
					echo "[ WARN ] No USB Device detected in /dev/sda1"
				fi
			fi

			if [ "$SDA1_MOUNTED" ]; then
				echo "[ INFO ] Looking for configuration file(s) on /mnt/sda1..."
				if [ -f $MNTUSB/lircd.conf ]; then
					echo "[ INFO ] Copying /tmp/lircd.conf..."
					sudo cp -f $MNTUSB/lircd.conf /home/tc/.lircrc
					sudo mv $MNTUSB/lircd.conf $MNTUSB/used_lircd.conf
					BACKUP_REQUIRED=TRUE
					REBOOT_REQUIRED=TRUE
					CONFIG_FOUND=TRUE
				else
					echo "[ INFO ] /mnt/sda1/lircd.conf not found."
				fi
				if [ -f $MNTUSB/lircrc ]; then
					echo "[ INFO ] Copying /mnt/sda1/lircrc..."
					sudo cp -f $MNTUSB/lircrc /home/tc/.lircrc
					sudo mv $MNTUSB/lircrc $MNTUSB/used_lircrc
					BACKUP_REQUIRED=TRUE
					REBOOT_REQUIRED=TRUE
					CONFIG_FOUND=TRUE
				else
					echo "[ INFO ] /mnt/sda1/lircrc not found."
				fi
			fi
		fi
		[ $CONFIG_FOUND ] && echo "[ INFO ] Configuration file(s) found." || echo "[ WARN ] Configuration file(s) not found."
	fi
	#----------------------------------------------------------------------------------------

	#---------------------------------------Save---------------------------------------------
	if [ "$ACTION" = "Save" ]; then
		echo '                  <textarea class="inform" style="height:50px">'
		[ "$FAIL_MSG" = "ok" ] && pcp_save_to_config
		pcp_mount_mmcblk0p1_nohtml
		echo '[ INFO ] Changing '$CONFIGTXT'... '
		sed -i '/dtoverlay=lirc-rpi/d' $CONFIGTXT
		if [ "$IR_GPIO_OUT" = "" ]; then
			sudo echo "dtoverlay=lirc-rpi,gpio_in_pin=$IR_GPIO_IN" >> $CONFIGTXT
		else
			sudo echo "dtoverlay=lirc-rpi,gpio_in_pin=$IR_GPIO_IN,gpio_out_pin=$IR_GPIO_OUT" >> $CONFIGTXT
		fi
		pcp_umount_mmcblk0p1_nohtml
		BACKUP_REQUIRED=TRUE
		REBOOT_REQUIRED=TRUE
	fi
	#----------------------------------------------------------------------------------------

	#----------------------------------------------------------------------------------------
	echo '                  </textarea>'
	echo '                </td>'
	echo '              </tr>'
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
fi

if [ $DEBUG -eq 1 ]; then
	pcp_table_top "Debug"
	echo '<p class="debug">[ DEBUG ] $IR_LIRC: '$IR_LIRC'<br />'
	echo '                 [ DEBUG ] $IR_GPIO_IN: '$IR_GPIO_IN'<br />'
	echo '                 [ DEBUG ] $IR_GPIO_OUT: '$IR_GPIO_OUT'<br />'
	echo '                 [ DEBUG ] $IR_DEVICE: '$IR_DEVICE'</p>'
	pcp_mount_mmcblk0p1
	echo '<p class="info">[ INFO ] Last few lines of config.txt</p>'
	pcp_textarea_inform "none" "tail -2 $CONFIGTXT" "30"
	pcp_umount_mmcblk0p1
	pcp_table_end
fi

pcp_backup_if_required
pcp_html_end
