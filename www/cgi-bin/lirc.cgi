#!/bin/sh

# Version: 7.0.0 2020-06-03

. pcp-functions
. pcp-lms-functions

ORIG_IR_LIRC=$IR_LIRC			# <=== GE not implemented yet
ORIG_IR_DEVICE=$IR_DEVICE		# <=== GE not implemented yet

unset BACKUP_REQUIRED REBOOT_REQUIRED SDA1_MOUNTED CONFIG_FOUND

pcp_html_head "LIRC" "GE"

pcp_navbar
pcp_httpd_query_string

FAIL_MSG="ok"
KERNEL=$(uname -r)
DEFAULT_IR_GPIO_IN="25"
DEFAULT_IR_GPIO_OUT=""

COLUMN2_1="col-sm-2"
COLUMN2_2="col-10"

COLUMN3_1="col-sm-2"
COLUMN3_2="col-sm-4"
COLUMN3_3="col-sm-6"

#========================================================================================
#  225280 pcp-lirc.tcz
#   57344 media-rc-KERNEL.tcz
#  376832 libasound.tcz
#    8192 libcofi.tcz
# --------
#  667648
#----------------------------------------------------------------------------------------
SPACE_REQUIRED=700

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
		pcp_heading5 "Backup required"
		pcp_infobox_begin
		pcp_backup "text"
		[ $? -eq 0 ] || FAIL_MSG="Backup failed."
		pcp_infobox_end
	fi
}

#========================================================================================
# Generate status message and finish html page
#----------------------------------------------------------------------------------------
pcp_html_end() {
	pcp_border_begin
	pcp_heading5 "Status"
	echo '    <div class="row mx-1">'
	echo '      <div class="col-12">'
	echo '        <p>'$FAIL_MSG'</p>'
	echo '      </div>'
	echo '    </div>'
	pcp_border_end

	pcp_footer
	pcp_copyright
	pcp_remove_query_string

	echo '</body>'
	echo '</html>'
	[ "$REBOOT_REQUIRED" ] && pcp_reboot_required
	exit
}

#========================================================================================
# LIRC install
#----------------------------------------------------------------------------------------
pcp_lirc_upd_dtoverlay() {
	# Add gpio-ir dtoverlay to config.txt
	pcp_mount_bootpart
	pcp_message INFO "Adding gpio-ir overlay to config.txt..." "text"
	# lirc-rpi is obsolete, make sure there are no remnants
	sed -i '/dtoverlay=lirc-rpi/d' $CONFIGTXT
	sed -i '/dtoverlay=gpio-ir/d' $CONFIGTXT
	sudo echo "dtoverlay=gpio-ir,gpio_pin=$IR_GPIO_IN" >> $CONFIGTXT
	if [ "$IR_GPIO_OUT" != "" ]; then
		# might need testing, some recommend dtoverlay=pwm-ir-tx 
		sudo echo "dtoverlay=gpio-ir-tx,gpio_pin=$IR_GPIO_OUT" >> $CONFIGTXT
	fi
	pcp_umount_bootpart
}

pcp_ir_install() {
	pcp_message INFO "Installing packages for IR remote control." "text"
	pcp_message INFO "This can take a couple of minutes. Please wait..." "text"
	case $1 in
		lirc) EXTN="pcp-lirc.tcz";;
		irtools) EXTN="pcp-irtools.tcz";;
		*) FAIL_MSG="Bad Package";;
	esac
	[ "$FAIL_MSG" = "ok" ] && sudo -u tc pcp-load -r $PCP_REPO -wi $EXTN

	pcp_message INFO "Updating configuration files..." "text"

	case $1 in
		lirc)
			touch /home/tc/.lircrc
			sudo chown tc:staff /home/tc/.lircrc

			# Add lirc conf to the .filetool.lst
			[ $DEBUG -eq 1 ] && pcp_message DEBUG "lirc configuration is added to .filetool.lst" "text"
			sudo sed -i '/lircd.conf/d' /opt/.filetool.lst
			sudo echo 'usr/local/etc/lirc/lircd.conf' >> /opt/.filetool.lst
			sudo sed -i '/.lircrc/d' /opt/.filetool.lst
			sudo echo 'home/tc/.lircrc' >> /opt/.filetool.lst
			sudo cp -f /usr/local/share/lirc/files/lircd.conf /usr/local/etc/lirc/lircd.conf
			[ "$FAIL_MSG" = "ok" ] && IR_LIRC="yes" && IR_CONFIG="/home/tc/.lircrc"
		;;
		irtools)
			[ "$FAIL_MSG" = "ok" ] && IR_KEYTABLES="yes"
		;;
	esac
	pcp_save_to_config
	pcp_lirc_upd_dtoverlay
}

#========================================================================================
# IR/LIRC uninstall
#----------------------------------------------------------------------------------------
pcp_ir_uninstall() {

	case $1 in
		lirc) EXTN="pcp-lirc.tcz";;
		irtools) EXTN="pcp-irtools.tcz";;
	esac

	pcp_message INFO "Uninstalling packages for $1 remote control." "text"
	sudo -u tc tce-audit builddb
	echo
	pcp_message INFO "After a reboot the following extensions will be permanently deleted:" "text"
	sudo -u tc tce-audit delete $EXTN

	pcp_message INFO "Removing configuration files..." "text"
	case $1 in
		lirc)
			rm -f /home/tc/.lircrc

			sudo sed -i '/pcp-lirc.tcz/d' $ONBOOTLST
			sudo sed -i '/lircd.conf/d' /opt/.filetool.lst
			sudo sed -i '/.lircrc/d' /opt/.filetool.lst
			IR_LIRC="no"
			pcp_save_to_config
		;;
		irtools)
			sudo sed -i '/pcp-irtools.tcz/d' $ONBOOTLST
			IR_KEYTABLES="no"
			pcp_save_to_config
		;;
	esac

	if [ "$IR_LIRC" = "no" -a "$IR_KEYTABLES" = "no" ]; then
		pcp_mount_bootpart
		sed -i '/dtoverlay=lirc-rpi/d' $CONFIGTXT
		sed -i '/dtoverlay=gpio-ir/d' $CONFIGTXT
		[ $? -eq 0 ] && echo "[ INFO ] dtoverlay=gpio-ir removed." || FAIL_MSG="Can not remove dtoverlay=gpio-ir."
		pcp_umount_bootpart

		if [ "$FAIL_MSG" = "ok" ]; then
			IR_GPIO_IN=$DEFAULT_IR_GPIO_IN
			IR_GPIO_OUT=$DEFAULT_IR_GPIO_OUT
			IR_DEVICE="lirc0"
			IR_CONFIG=""
			pcp_save_to_config
		fi
	fi
}

#========================================================================================
# Main				<==== GE. This section is a little weird.
#----------------------------------------------------------------------------------------
case "$ACTION" in
	Install*)
		EXTENSION="$ACTION"
		ACTION="Install"
		pcp_sufficient_free_space "$SPACE_REQUIRED"
	;;
	Uninstall*)
		EXTENSION=$ACTION
		ACTION="Uninstall"
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
if [ "$ACTION" = "Initial" ] || [ "$ACTION" = "Save" ]; then

	#====================================================================================
	# Kernel Keytables (IR)
	#------------------------------------------------------------------------------------
	if [ "$JIVELITE" = "yes" ]; then
		#------------------------------------------Install/Unintall IRTOOLS--------------
		pcp_border_begin
		pcp_heading5 "Kernel Keytables (IR)"
		echo '  <form name="main" action="'$0'" method="get">'
		#--------------------------------------------------------------------------------
		if [ "$IR_KEYTABLES" = "yes" ]; then
			UPLKEYDIS=""
			echo '    <div class="row mx-1">'
			echo '      <div class="'$COLUMN2_1'">'
			echo '        <button class="'$BUTTON'" "type="submit" name="ACTION" value="Uninstall-irtools">Uninstall</button>'
			echo '      </div>'
			pcp_incr_id
			echo '      <div class="'$COLUMN2_2'">'
			echo '        <p>Uninstall IR-Tools&nbsp;&nbsp;'
			pcp_helpbadge
			echo '        </p>'
			echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
			echo '          <p>Uninstall IR-Tools from '$NAME'.</p>'
			echo '        </div>'
			echo '      </div>'
			echo '    </div>'
		else
			UPLKEYDIS="disabled"
			echo '    <div class="row mx-1">'
			echo '      <div class="'$COLUMN2_1'">'
			echo '        <button class="'$BUTTON'" type="submit" name="ACTION" value="Install-irtools">Install</button>'
			echo '      </div>'
			pcp_incr_id
			echo '      <div class="'$COLUMN2_2'">'
			echo '        <p>Install IR tools for use with jivelite&nbsp;&nbsp;'
			pcp_helpbadge
			echo '        </p>'
			echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
			echo '          <p>Install IR packages from repository.</p>'
			echo '        </div>'
			echo '      </div>'
			echo '    </div>'
		fi
		echo '  </form>'
		#--------------------------------------------------------------------------------
		pcp_incr_id
		echo '  <form name="Customkeytable" action="uploadconffile.cgi" enctype="multipart/form-data" method="post">'
		echo '    <div class="row mx-1">'
		echo '      <div class="'$COLUMN3_1'">'
		echo '        <button class="'$BUTTON'" id="UP3" type="submit" name="ACTION" value="Custom" disabled>Upload</button>'
		echo '      </div>'
		echo '      <div class="'$COLUMN3_2'">'
		echo '        <input class="input" type="file" id="file1" name="KEYTABLE" onclick="document.getElementById('\''UP3'\'').disabled = false" '$UPLKEYDIS'>'
		echo '      </div>'
		echo '      <div class="'$COLUMN3_3'">'
		echo '        <p>Upload custom <b>jivelite keytables</b> to pCP&nbsp;&nbsp;'
		pcp_helpbadge
		echo '        </p>'
		echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
		echo '          <p>Used to define IR remote functions for jivelite.</p>'
		echo '        </div>'
		echo '      </div>'
		echo '    </div>'
		echo '  </form>'
		pcp_border_end
	fi

	#====================================================================================
	# Linux Infrared Remote Control (LIRC)
	#------------------------------------------------------------------------------------
	pcp_border_begin
	pcp_heading5 "Linux Infrared Remote Control (LIRC)"
	echo '  <form name="main" action="'$0'" method="get">'
	#-------------------------------------Install/Uninstall LIRC-------------------------
	if [ "$IR_LIRC" = "yes" ]; then
		echo '    <div class="row mx-1">'
		echo '      <div class="'$COLUMN2_1'">'
		echo '        <button class="'$BUTTON'" type="submit" name="ACTION" value="Uninstall-lirc">Uninstall</button>'
		echo '      </div>'
		pcp_incr_id
		echo '      <div class="'$COLUMN2_2'">'
		echo '        <p>Uninstall LIRC&nbsp;&nbsp;'
		pcp_helpbadge
		echo '        </p>'
		echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
		echo '          <p>Uninstall LIRC from '$NAME'.</p>'
		echo '        </div>'
		echo '      </div>'
		echo '    </div>'
	else
		echo '    <div class="row mx-1">'
		echo '      <div class="'$COLUMN2_1'">'
		echo '        <button class="'$BUTTON'" type="submit" name="ACTION" value="Install-lirc">Install</button>'
		echo '      </div>'
		pcp_incr_id
		echo '      <div class="'$COLUMN2_2'">'
		echo '        <p>Install LIRC for Squeezelite&nbsp;&nbsp;'
		pcp_helpbadge
		echo '        </p>'
		echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
		echo '          <p>Install packages from repository.</p>'
		echo '        </div>'
		echo '      </div>'
		echo '    </div>'
	fi
	#--------------------------------------Custom LIRC Config----------------------------
	[ -f /usr/local/etc/lirc/lircd.conf ] && DISABLED="" || DISABLED="disabled"

	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN2_1'">'
	echo '        <input class="'$BUTTON'" type="submit" name="ACTION" value="Custom" '$DISABLED'>'
	echo '      </div>'
	pcp_incr_id
	echo '      <div class="'$COLUMN2_2'">'
	echo '        <p>Install your own LIRC configuration file(s)&nbsp;&nbsp;'
	pcp_helpbadge
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>Default installation only supports Logitech Squeezebox remote. If you are using another'
	echo '             remote controller you need to supply your own configuration file(s).</p>'
	echo '          <p>To use your own configuration file(s): </p>'
	echo '          <ol>'
	echo '            <li>Copy the file(s) either:</li>'
	echo '              <ul>'
	echo '                <li>via ssh to the /tmp directory, <b>or</b></li>'
	echo '                <li>to an attached USB flash drive.</li>'
	echo '              </ul>'
	echo '            <li>Press the [Custom] button and your configuration file(s) will be copied and used by pCP.</li>'
	echo '          </ol>'
	echo '          <p><b>Note:</b></p>'
	echo '          <ul>'
	echo '            <li>To use <b>LIRC on a headless system (no Jivelite)</b> you will need to provide'
	echo '             both <b>"lircd.conf" and "lircrc"</b> configuration files.</li>'
	echo '          </ul>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
	#----------------------------------------------------------------------------------------
	echo '  </form>'
	#----------------------------------------------------------------------------------------

	#----------------------------------------------------------------------------------------
	echo '  <form name="Customlirc" action="uploadconffile.cgi" enctype="multipart/form-data" method="post">'
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <button class="'$BUTTON'" id="UP1" type="submit" name="ACTION" value="Custom" disabled>Upload</button>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <input class="large22" type="file" id="file2" name="LIRCCONF" onclick="document.getElementById('\''UP1'\'').disabled = false">'
	echo '      </div>'
	pcp_incr_id
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <p>Upload custom <b>lirc.conf</b> to pCP&nbsp;&nbsp;'
	pcp_helpbadge
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>Used to define ir remote functions.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
	echo '  </form>'
	#----------------------------------------------------------------------------------------

	#----------------------------------------------------------------------------------------
	echo '  <form name="Customlircrc" action="uploadconffile.cgi" enctype="multipart/form-data" method="post">'
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <button class="'$BUTTON'" id="UP2" type="submit" name="ACTION" value="Custom" disabled>Upload</button>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <input class="large22" type="file" id="file3" name="LIRCRC" onclick="document.getElementById('\''UP2'\'').disabled = false">'
	echo '      </div>'
	pcp_incr_id
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <p>Upload custom <b>lircrc</b> to pCP&nbsp;&nbsp;'
	pcp_helpbadge
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>Used to define ir remote functions.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
	echo '  </form>'
	#------------------------------------------------------------------------------------
	pcp_border_end
	#------------------------------------------------------------------------------------

	#====================================================================================
	# IR device Settings
	#------------------------------------------------------------------------------------
	pcp_border_begin
	pcp_heading5 "IR device Settings"
	echo '  <form name="settings" action="'$0'" method="get">'
	#------------------------------------------LIRC GPIO IN------------------------------
	# gpio_in_pin    GPIO for input
	#------------------------------------------------------------------------------------
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN2_1'">'
	echo '        <input class="form-control form-control-sm"'
	echo '               type="number"'
	echo '               name="IR_GPIO_IN"'
	echo '               value="'$IR_GPIO_IN'"'
	echo '               title="( 0 - 31 )"'
	echo '               min="0"'
	echo '               max="31"'
	echo '        >'
	echo '      </div>'
	pcp_incr_id
	echo '      <div class="'$COLUMN2_2'">'
	echo '        <p>Set IR GPIO in number (IR receiver)&nbsp;&nbsp;'
	pcp_helpbadge
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>&lt;0 - 31&gt;</p>'
	echo '          <p><b>Default:</b> '$DEFAULT_IR_GPIO_IN'</p>'
	echo '          <p>Set GPIO in number to match the GPIO used to connect the IR Receiver.</p>'
	echo '          <p><b>Warning:</b> Be careful not to set the GPIO to one being used for another purpose.</p>'
	echo '          <p><b>Note:</b> Not used for USB PCRemote.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
	#--------------------------------------LIRC GPIO OUT---------------------------------
	# gpio_out_pin    GPIO for output
	#------------------------------------------------------------------------------------
	if [ $MODE -ge $MODE_PLAYER ]; then
		echo '    <div class="row mx-1">'
		echo '      <div class="'$COLUMN2_1'">'
		echo '        <input class="form-control form-control-sm"'
		echo '               type="number"'
		echo '               name="IR_GPIO_OUT"'
		echo '               value="'$IR_GPIO_OUT'"'
		echo '               title="( 0 - 31 )"'
		echo '               min="0"'
		echo '               max="31"'
		echo '        >'
		echo '      </div>'
		pcp_incr_id
		echo '      <div class="'$COLUMN2_2'">'
		echo '        <p>Set LIRC GPIO out number (IR transmitter)&nbsp;&nbsp;'
		pcp_helpbadge
		echo '        </p>'
		echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
		echo '          <p>&lt;0 - 31&gt;</p>'
		echo '          <p><b>Default:</b> '$DEFAULT_IR_GPIO_OUT'</p>'
		echo '          <p>Set GPIO out number to match the GPIO used to connect the IR Transmitter.</p>'
		echo '          <p><b>Warning:</b> Be careful not to set the GPIO to one being used for another purpose.</p>'
		echo '        </div>'
		echo '      </div>'
		echo '    </div>'
	fi
	#------------------------------------------IR Device---------------------------------
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN2_1'">'
	echo '        <input id="input'$ID'"'
	echo '               class="form-control form-control-sm"'
	echo '               type="text"'
	echo '               name="IR_DEVICE"'
	echo '               value="'$IR_DEVICE'"'
	echo '               title="( lirc[0-9] | hidraw[0-9] )"'
	echo '               pattern="(lirc[0-9]|hidraw[0-9])"'
	echo '        >'
	echo '      </div>'
	pcp_incr_id
	echo '      <div class="'$COLUMN2_2'">'
	echo '        <p>Set IR Device to GPIO or USB&nbsp;&nbsp;'
	pcp_helpbadge
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>&lt;lirc[0-9]|hidraw[0-9]&gt;</p>'
	echo '          <p><b>Default:</b> lirc0</p>'
	echo '          <ul>'
	echo '            <li class="pointer" title="Click to use lirc0" onclick="pcp_copy_click_to_input('\'input${ID}\',\'option1\'')">'
	echo '              <span id="option1">lirc0</span> - GPIO IR Receiver.</li>'
	echo '            <li class="pointer" title="Click to use hidraw1" onclick="pcp_copy_click_to_input('\'input${ID}\',\'option2\'')">'
	echo '              <span id="option2">hidraw1</span> - USB Remote control.</li>'
	echo '          </ul>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------Save Button-------------------------------------
	if [ "$IR_LIRC" = "yes" -o "$IR_KEYTABLES" = "yes" ]; then
		pcp_incr_id
		echo '    <div class="row mx-1">'
		echo '      <div class="'$COLUMN3_1'">'
		echo '        <input class="'$BUTTON'"'
		echo '               type="submit"'
		echo '               name="ACTION"'
		echo '               value="Save"'
		echo '               title="Save LIRC settings"'
		echo '        >'
		echo '      </div>'
		echo '    </div>'
	fi
	#------------------------------------------------------------------------------------
	echo '  </form>'
	#------------------------------------------------------------------------------------
	pcp_border_end
fi
#----------------------------------------------------------------------------------------

#========================================================================================
# Actions
#----------------------------------------------------------------------------------------
if [ "$ACTION" != "Initial" ]; then
	pcp_incr_id
	pcp_heading5 "$ACTION"

	#---------------------------------------Install--------------------------------------
	if [ "$ACTION" = "Install" ]; then
		pcp_infobox_begin
		pcp_internet_indicator
		[ "$FAIL_MSG" = "ok" ] || pcp_html_end
		pcp_message INFO "$INTERNET_STATUS" "text"
		pcp_repo_indicator
		[ "$FAIL_MSG" = "ok" ] || pcp_html_end
		pcp_message INFO "$REPO_STATUS" "text"
		pcp_sufficient_free_space "text" $SPACE_REQUIRED
		[ "$EXTENSION" = "Install-lirc" ] && pcp_ir_install lirc
		[ "$EXTENSION" = "Install-irtools" ] && pcp_ir_install irtools
		BACKUP_REQUIRED=TRUE
		REBOOT_REQUIRED=TRUE
		pcp_infobox_end
	fi
	#----------------------------------------------------------------------------------------

	#---------------------------------------Uninstall----------------------------------------
	if [ "$ACTION" = "Uninstall" ]; then
		pcp_infobox_begin
		if [ "$FAIL_MSG" = "ok" ]; then
			[ "$EXTENSION" = "Uninstall-lirc" ] && pcp_ir_uninstall lirc
			[ "$EXTENSION" = "Uninstall-irtools" ] && pcp_ir_uninstall irtools
		fi
		BACKUP_REQUIRED=TRUE
		REBOOT_REQUIRED=TRUE
		pcp_infobox_end
	fi
	#----------------------------------------------------------------------------------------

	#---------------------------------------Custom-------------------------------------------
	if [ "$ACTION" = "Custom" ]; then
		pcp_infobox_begin
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
	pcp_infobox_end
	#----------------------------------------------------------------------------------------

	#---------------------------------------Save---------------------------------------------
	if [ "$ACTION" = "Save" ]; then
		pcp_infobox_begin
		[ "$FAIL_MSG" = "ok" ] && pcp_save_to_config
		pcp_lirc_upd_dtoverlay
		BACKUP_REQUIRED=TRUE
		REBOOT_REQUIRED=TRUE
		pcp_infobox_end
	fi
	#----------------------------------------------------------------------------------------
fi

if [ $DEBUG -eq 1 ]; then
	pcp_debug_variables "html" IR_LIRC IR_KEYTABLES IR_GPIO_IN IR_GPIO_OUT IR_DEVICE IR_CONFIG EXTENSION
	pcp_mount_bootpart
	pcp_message INFO "Last few lines of config.txt" "text"
	pcp_textarea "none" "tail -4 $CONFIGTXT" 3
	pcp_umount_bootpart
fi

pcp_backup_if_required
pcp_html_end
