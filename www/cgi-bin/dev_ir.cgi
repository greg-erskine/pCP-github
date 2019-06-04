#!/bin/sh

# Version: 5.0.0 2019-05-28

. pcp-functions
. pcp-lms-functions

unset BACKUP_REQUIRED REBOOT_REQUIRED SDA1_MOUNTED CONFIG_FOUND

pcp_html_head "IR" "GE"

pcp_banner
pcp_navigation
pcp_running_script
pcp_httpd_query_string

FAIL_MSG="ok"
KERNEL=$(uname -r)
DEFAULT_IR_GPIO_IN="25"
DEFAULT_IR_GPIO_OUT=""

DEBUG=1

#========================================================================================
#  225280 -----pcp-lirc.tcz
#   57344      |-----media-rc-KERNEL.tcz
#  ******      |-----libasound.tcz
#  ******      |     |-----alsa-modules-KERNEL.tcz
#    8192      |-----libcofi.tcz
# --------
#  290816
#----------------------------------------------------------------------------------------
SPACE_REQUIRED=300

#========================================================================================
# Debug variables
#----------------------------------------------------------------------------------------
if [ $DEBUG -eq 1 ]; then
	pcp_table_top "Debug"
	echo '<!-- Start of debug info -->'
	pcp_debug_variables "html" JIVELITE IR_LIRC IR_GPIO_IN IR_GPIO_OUT IR_DEVICE IR_CONFIG
	echo '<!-- End of debug info -->'
	pcp_table_end
fi

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
# Check we have pCP repo access - set FAIL_MSG if not accessible
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
pcp_ir_html_end() {
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
# IR install
#----------------------------------------------------------------------------------------
#  Name:   gpio-ir
#  Info:   Use GPIO pin as rc-core style infrared receiver input. The rc-core-
#          based gpio_ir_recv driver maps received keys directly to a
#          /dev/input/event* device, all decoding is done by the kernel - LIRC is
#          not required! The key mapping and other decoding parameters can be
#          configured by "ir-keytable" tool.
#  Load:   dtoverlay=gpio-ir,<param>=<val>
#  Params: gpio_pin                Input pin number. Default is 18.
#  
#          gpio_pull               Desired pull-up/down state (off, down, up)
#                                  Default is "up".
#  
#          rc-map-name             Default rc keymap (can also be changed by
#                                  ir-keytable), defaults to "rc-rc6-mce"
#----------------------------------------------------------------------------------------


pcp_ir_upd_dtoverlay() {
	# Add gpio-ir dtoverlay to config.txt
	pcp_mount_bootpart_nohtml
	echo '[ INFO ] Adding gpio-ir overlay to config.txt...'

	#### lirc-rpi is obsolete, make sure there are no remnants
	sed -i '/dtoverlay=lirc-rpi/d' $CONFIGTXT

	sed -i '/dtoverlay=gpio-ir/d' $CONFIGTXT
	sudo echo "dtoverlay=gpio-ir,gpio_pin=$IR_GPIO_IN" >> $CONFIGTXT
	if [ x"$IR_GPIO_OUT" != x"" ]; then
		# Might need testing, some recommend dtoverlay=pwm-ir-tx
		sudo echo "dtoverlay=gpio-ir-tx,gpio_pin=$IR_GPIO_OUT" >> $CONFIGTXT
	fi
	pcp_umount_bootpart_nohtml
}

pcp_ir_install() {
	echo '[ INFO ] Installing packages for IR remote control.'
	echo '[ INFO ] This can take a couple of minutes. Please wait...'

	if [ "$JIVELITE" = "no" ]; then
		sudo -u tc pcp-load -r $PCP_REPO -wi pcp-lirc.tcz
	else
		sudo -u tc pcp-load -r $PCP_REPO -wi pcp-irtools.tcz
	fi

	echo '[ INFO ] Updating configuration files... '

	if [ "$JIVELITE" = "no" ]; then
		touch /home/tc/.lircrc
		sudo chown tc:staff /home/tc/.lircrc

		# Add lirc conf to the .filetool.lst
		[ $DEBUG -eq 1 ] && echo '[ DEBUG ] lirc configuration is added to .filetool.lst'
		sudo sed -i '/lircd.conf/d' /opt/.filetool.lst
		sudo echo 'usr/local/etc/lirc/lircd.conf' >> /opt/.filetool.lst
		sudo sed -i '/.lircrc/d' /opt/.filetool.lst
		sudo echo 'home/tc/.lircrc' >> /opt/.filetool.lst
		sudo cp -f /usr/local/share/lirc/files/lircd.conf /usr/local/etc/lirc/lircd.conf
	else
		sudo cp -f /usr/local/share/pcp-irtools/files/slimdevices /usr/local/etc/keytables/jivelite
		sudo echo 'usr/local/etc/keytables/jivelite' >> /opt/.filetool.lst
	fi

	pcp_ir_upd_dtoverlay

	[ "$FAIL_MSG" = "ok" ] && IR_LIRC="yes" && IR_CONFIG="/home/tc/.lircrc" && pcp_save_to_config
}

#========================================================================================
# LIRC uninstall
#----------------------------------------------------------------------------------------
pcp_ir_uninstall() {
	sudo -u tc tce-audit builddb
	if [ "$JIVELITE" = "no" ]; then
		[ "$FAIL_MSG" = "ok" ] && sudo -u tc tce-audit delete pcp-lirc.tcz
	else
		[ "$FAIL_MSG" = "ok" ] && sudo -u tc tce-audit delete pcp-irtools.tcz
	fi

	echo '[ INFO ] Removing configuration files... '

	pcp_mount_bootpart_nohtml
	sed -i '/dtoverlay=lirc-rpi/d' $CONFIGTXT
	sed -i '/dtoverlay=gpio-ir/d' $CONFIGTXT
	[ $? -eq 0 ] && echo "[ INFO ] dtoverlay=gpio-ir removed." || FAIL_MSG="Can not remove dtoverlay=gpio-ir."
	pcp_umount_bootpart_nohtml

	if [ "$JIVELITE" = "no" ]; then
		rm -f /home/tc/.lircrc

		sudo sed -i '/pcp-lirc.tcz/d' $ONBOOTLST
		sudo sed -i '/lircd.conf/d' /opt/.filetool.lst
		sudo sed -i '/.lircrc/d' /opt/.filetool.lst
	else
		sudo sed -i '/pcp-irtools.tcz/d' $ONBOOTLST
		sudo rm /usr/local/etc/keytables/jivelite
		sudo sed -i '/usr\/local\/etc\/keytables\/jivelite/d' /opt/.filetool.lst
	fi

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
# Linux kernel Infrared Remote Control table
#----------------------------------------------------------------------------------------
if [ "$ACTION" = "Initial" ] || [ "$ACTION" = "Save" ]; then
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Linux kernel Infrared Remote Control</legend>'
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
	echo '                      <li>To use <b>LIRC on a headless system (no Jivelite)</b> you will need to provide'
	echo '                       both <b>"lircd.conf" and "lircrc"</b> configuration files.</li>'
	echo '                    </ul>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
	#------------------------------------------------------------------------------------
	pcp_incr_id
	pcp_toggle_row_shade
	echo '            <form name="Customlirc" action="uploadconffile.cgi" enctype="multipart/form-data" method="post">'
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                  <button id="UP1" type="submit" name="ACTION" value="Custom" disabled>Upload</button>'
	echo '                </td>'
	echo '                <td class="column280">'
	echo '                  <input class="large22" type="file" id="file" name="LIRCCONF" onclick="document.getElementById('\''UP1'\'').disabled = false">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Upload custom <b>lirc.conf</b> to pCP&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Used to define ir remote functions.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
	#------------------------------------------------------------------------------------
	pcp_incr_id
	pcp_toggle_row_shade
	echo '            <form name="Customlircrc" action="uploadconffile.cgi" enctype="multipart/form-data" method="post">'
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                  <button id="UP2" type="submit" name="ACTION" value="Custom" disabled>Upload</button>'
	echo '                </td>'
	echo '                <td class="column280">'
	echo '                  <input class="large22" type="file" id="file" name="LIRCRC" onclick="document.getElementById('\''UP2'\'').disabled = false">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Upload custom <b>lircrc</b> to pCP&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Used to define ir remote functions.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
	#------------------------------------------------------------------------------------
	pcp_incr_id
	pcp_toggle_row_shade
	echo '            <form name="Customkeytable" action="uploadconffile.cgi" enctype="multipart/form-data" method="post">'
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                  <button id="UP3" type="submit" name="ACTION" value="Custom" disabled>Upload</button>'
	echo '                </td>'
	echo '                <td class="column280">'
	echo '                  <input class="large22" type="file" id="file" name="KEYTABLE" onclick="document.getElementById('\''UP3'\'').disabled = false">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Upload custom <b>jivelite keytables</b> to pCP&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Used to define ir remote functions for jivelite.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
	#------------------------------------------------------------------------------------
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
	#------------------------------------------------------------------------------------

	#====================================================================================
	# gpio_ir settings table
	#------------------------------------------------------------------------------------
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>LIRC Settings</legend>'
	echo '          <form name="settings" action="'$0'" method="get">'
	echo '            <table class="bggrey percent100">'
	#----------------------------------------------------------------------------------------

	#------------------------------------------LIRC GPIO IN-----------------------------------
	# gpio_in_pin    GPIO for input
	#-----------------------------------------------------------------------------------------
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                  <input class="input"'
	echo '                         type="number"'
	echo '                         name="IR_GPIO_IN"'
	echo '                         value="'$IR_GPIO_IN'"'
	echo '                         title="( 0 - 31 )"'
	echo '                         min="0"'
	echo '                         max="31"'
	echo '                  >'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Set LIRC GPIO in number (IR receiver)&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>&lt;0 - 31&gt;</p>'
	echo '                    <p><b>Default:</b> '$DEFAULT_IR_GPIO_IN'</p>'
	echo '                    <p>Set GPIO in number to match the GPIO used to connect the IR Receiver.</p>'
	echo '                    <p><b>Warning:</b> Be careful not to set the GPIO to one being used for another purpose.</p>'
	echo '                    <p><b>Note:</b> Not used for USB PCRemote.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	#----------------------------------------------------------------------------------------

	if [ $MODE -ge $MODE_BETA ]; then
		#------------------------------------------LIRC GPIO OUT---------------------------------
		# gpio_out_pin    GPIO for output
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
		echo '                  </div>'
		echo '                </td>'
		echo '              </tr>'
		#--------------------------------------------------------------------------------
	fi

	#------------------------------------------IR Device---------------------------------
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
	#------------------------------------------Save button-------------------------------
	if [ "$IR_LIRC" = "yes" ]; then
		pcp_incr_id
		pcp_toggle_row_shade
		echo '              <tr class="'$ROWSHADE'">'
		echo '                <td class="column150 center" colspan="2">'
		echo '                  <input type="submit"'
		echo '                         name="ACTION"'
		echo '                         value="Save"'
		echo '                         title="Save LIRC settings"'
		echo '                  />'
		echo '                </td>'
		echo '              </tr>'
	fi
	#----------------------------------------------------------------------------------------
	echo '            </table>'
	echo '          </form>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
fi
#----------------------------------------------------------------------------------------

if [ $DEBUG -eq 1 ]; then
	pcp_table_top "Last few lines of config.txt"
	echo '<!-- Start of debug info -->'
	pcp_mount_bootpart >/dev/null 2>&1
	pcp_textarea_inform "none" "tail -2 $CONFIGTXT" "30"
	pcp_umount_bootpart >/dev/null 2>&1
	echo '<!-- End of debug info -->'
	pcp_table_end

	pcp_table_top "lsmod"
	echo '<!-- Start of debug info -->'
	pcp_textarea_inform "none" "lsmod | grep ir" "50"
	echo '<!-- End of debug info -->'
	pcp_table_end

	pcp_table_top "ir-keytable"
	echo '<!-- Start of debug info -->'
	pcp_textarea_inform "none" "ir-keytable 2>&1" "110"
	echo '<!-- End of debug info -->'
	pcp_table_end

	pcp_table_top "/dev/input"
	echo '<!-- Start of debug info -->'
	pcp_textarea_inform "none" "ls -Rl /dev/input" "90"
	echo '<!-- End of debug info -->'
	pcp_table_end

	pcp_table_top "/sys/class/rc"
	echo '<!-- Start of debug info -->'
	pcp_textarea_inform "none" "ls /sys/class/rc" "40"
	echo '<!-- End of debug info -->'
	pcp_table_end

	pcp_table_top "/usr/local/etc/keytables/"
	echo '<!-- Start of debug info -->'
	pcp_textarea_inform "none" "ls /usr/local/etc/keytables/" "40"
	echo '<!-- End of debug info -->'
	pcp_table_end

	pcp_table_top "ir-keytable -r"
	echo '<!-- Start of debug info -->'
	pcp_textarea_inform "none" "ir-keytable -r 2>&1" "110"
	echo '<!-- End of debug info -->'
	pcp_table_end

fi

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
		pcp_repo_indicator
		[ "$FAIL_MSG" = "ok" ] || pcp_html_end
		echo '[ INFO ] '$REPO_STATUS
		pcp_sufficient_free_space "nohtml" $SPACE_REQUIRED
		pcp_ir_install
		BACKUP_REQUIRED=TRUE
		REBOOT_REQUIRED=TRUE
	fi
	#---------------------------------------Uninstall----------------------------------------
	if [ "$ACTION" = "Uninstall" ]; then
		echo '                  <textarea class="inform" style="height:200px">'
		[ "$FAIL_MSG" = "ok" ] && pcp_ir_uninstall
		BACKUP_REQUIRED=TRUE
		REBOOT_REQUIRED=TRUE
	fi
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

			if [ $SDA1_MOUNTED ]; then
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
	#---------------------------------------Save---------------------------------------------
	if [ "$ACTION" = "Save" ]; then
		echo '                  <textarea class="inform" style="height:50px">'
		[ "$FAIL_MSG" = "ok" ] && pcp_save_to_config
		pcp_ir_upd_dtoverlay
		BACKUP_REQUIRED=TRUE
		REBOOT_REQUIRED=TRUE
	fi
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

pcp_backup_if_required
pcp_ir_html_end
