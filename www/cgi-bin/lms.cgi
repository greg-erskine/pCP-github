#!/bin/sh

# Version: 7.0.0 2020-06-12

. pcp-functions
. pcp-rpi-functions
. pcp-lms-functions

pcp_html_head "LMS Main Page" "SBP"

pcp_controls
pcp_navbar
pcp_remove_query_string
pcp_httpd_query_string

# Read from slimserver.cfg file
CFG_FILE="/home/tc/.slimserver.cfg"
TCEDIR=$(readlink "/etc/sysconfig/tcedir")

[ -f "$CFG_FILE" ] && . $CFG_FILE

# Set Default Settings if not defined in CFG_FILE
[ -n "$CACHE" ] || CACHE=${TCEDIR}/slimserver/Cache
[ -n "$LOGS" ] || LOGS=/var/log/slimserver
[ -n "$PREFS" ] || PREFS=${TCEDIR}/slimserver/prefs
[ -n "$LMSUSER" ] || LMSUSER=tc
[ -n "$LMSGROUP" ] || LMSGROUP=staff
[ -n "$OPTIONS" ] || OPTIONS=""

LMS_SERV_LOG="${LOGS}/server.log"
LMS_SCAN_LOG="${LOGS}/scanner.log"
LMS_UPDATE_LOG="${LOGS}/LMS_update.log"
LMS_CC_FILE="/usr/local/slimserver/custom-convert.conf"
WGET="/bin/busybox wget"

COLUMN1_1="col-12"

COLUMN2_1="col-sm-2"
COLUMN2_2="col-sm-10"

COLUMN3_1="col-sm-2"
COLUMN3_2="col-sm-2"
COLUMN3_3="col-sm-8"

COLUMN4_1="col-sm-2"
COLUMN4_2="col-sm-4"
COLUMN4_3="col-sm-2"
COLUMN4_4="col-sm-4"

#========================================================================================
# Local functions
#----------------------------------------------------------------------------------------
pcp_lms_warning() {
	echo '    <div class="alert alert-primary" role="alert">'
	echo '      <b>Warning:</b>'
	echo '      <p>Logitech Media Server (LMS) is a server database application'
	echo '      and needs to be shutdown properly:</p>'
	echo '      <ul>'
	echo '        <li>Do NOT just pull the power plug.</li>'
	echo '        <li>Use [Main Page] > [Shutdown].</li>'
	echo '      </ul>'
	echo '    </div>'
}

pcp_install_lms() {
	pcp_message INFO "Downloading LMS..." "text"
	sudo -u tc pcp-load -r $PCP_REPO -w slimserver.tcz
	if [ -f $TCEMNT/tce/optional/slimserver.tcz ]; then
		pcp_message INFO "Installing LMS..." "text"
		sudo -u tc pcp-load -i slimserver.tcz
		sudo sed -i '/slimserver.tcz/d' $ONBOOTLST
		sudo echo 'slimserver.tcz' >> $ONBOOTLST
		[ $DEBUG -eq 1 ] && pcp_message DEBUG "LMS is added to onboot.lst" "text"
		[ $DEBUG -eq 1 ] && cat $ONBOOTLST
	fi
}

pcp_remove_lms() {
	sudo /usr/local/etc/init.d/slimserver stop >/dev/null 2>&1
	pcp_message INFO "" "text" "-n"
	sudo -u tc tce-audit builddb
	echo
	pcp_message INFO "After a reboot these extensions will be permanently deleted:" "text"
	sudo -u tc tce-audit delete slimserver.tcz
	echo
	sudo sed -i '/slimserver.tcz/d' $ONBOOTLST
}

pcp_remove_lms_cache() {
	sudo rm -rf $TCEMNT/tce/slimserver/
	for I in $(find /mnt -maxdepth 1 | grep -Ev 'mmcblk0p[1-9]')
	do
		[ -d $I/slimserver ] && rm -rf $I/slimserver/
	done
	sync
}

pcp_remove_custom_convert() {
	sudo rm -rf $LMS_CC_FILE
	sed -i '/'$(echo ${LMS_CC_FILE##/} | sed 's|\/|\\\/|g')'/d' $FILETOOLLST
	pcp_backup "text"
}

pcp_install_fs() {
	RESULT=0
	pcp_message INFO "Downloading additional file systems support..." "text"
	sudo -u tc pcp-load -r $PCP_REPO -w ntfs-3g.tcz
	if [ -f $TCEMNT/tce/optional/ntfs-3g.tcz ]; then
		pcp_message INFO "Loading file systems extensions..." "text"
		sudo -u tc tce-load -i ntfs-3g.tcz
		[ $? -eq 0 ] || (echo $?; RESULT=1)
		if [ $RESULT -eq 0 ]; then
			echo "ntfs-3g.tcz" >> $ONBOOTLST
			pcp_message INFO "File systems support including NTFS loaded." "text"
		else
			pcp_message ERROR "Extensions not loaded, try again later!" "text"
		fi
	fi
}

pcp_remove_fs() {
	pcp_message INFO "Removing additional file systems extensions..." "text"
	pcp_message INFO "" "text" "-n"
	sudo -u tc tce-audit builddb
	echo
	pcp_message INFO "After a reboot these extensions will be permanently deleted:" "text"
	sudo -u tc tce-audit delete ntfs-3g.tcz
	echo
	sed -i '/ntfs-3g.tcz/d' $ONBOOTLST
}

pcp_install_exfat() {
	RESULT=0
	pcp_message INFO "Downloaded exFAT file system support..." "text"
	sudo -u tc pcp-load -r $PCP_REPO -w pcp-exfat-utils.tcz
	if [ -f $TCEMNT/tce/optional/pcp-exfat-utils.tcz ]; then
		pcp_message INFO "Loading exFAT extensions..." "text"
		sudo -u tc tce-load -i pcp-exfat-utils.tcz
		[ $? -eq 0 ] || (echo $?; RESULT=1)
		if [ $RESULT -eq 0 ]; then
			echo "pcp-exfat-utils.tcz" >> $ONBOOTLST
			pcp_message INFO "exFAT file system support loaded." "text"
		else
			pcp_message ERROR "Extensions not loaded, try again later!" "text"
		fi
	fi
}

pcp_remove_exfat() {
	pcp_message INFO "Removing exFAT file system extensions..." "text"
	pcp_message INFO "" "text" "-n"
	sudo -u tc tce-audit builddb
	echo
	pcp_message INFO "After a reboot these extensions will be permanently deleted:" "text"
	sudo -u tc tce-audit delete pcp-exfat-utils.tcz
	echo
	sed -i '/pcp-exfat-utils.tcz/d' $ONBOOTLST
}

pcp_install_samba4() {
	RESULT=0
	pcp_message INFO "Downloading Samba4..." "text"
	sudo -u tc pcp-load -r $PCP_REPO -w samba4.tcz
	[ $? -eq 0 ] || (echo $?; RESULT=1)
	if [ $RESULT -eq 0 ]; then
		sudo -u tc pcp-load -i samba4.tcz
		[ $? -eq 0 ] || (echo $?; RESULT=1)
	fi
	if [ $RESULT -eq 0 ]; then
		echo "samba4.tcz" >> $ONBOOTLST
		pcp_message INFO "Samba Support Loaded." "text"
		mkdir -p /usr/local/var/lib/samba
		mkdir -p /usr/local/etc/samba
		touch /usr/local/etc/samba/smb.conf
		echo "usr/local/var/lib/samba" >> /opt/.filetool.lst
		echo "usr/local/etc/samba/smb.conf" >> /opt/.filetool.lst
		SAMBA="yes"
		pcp_save_to_config
		pcp_backup "text"
	else
		pcp_message ERROR "Samba4.tcz not loaded, try again later!" "text"
	fi
}

pcp_remove_samba4() {
	pcp_message INFO "Removing Samba extensions..." "text"
	sed -i '/samba4.tcz/d' $ONBOOTLST
	pcp_message INFO "" "text" "-n"
	sudo -u tc tce-audit builddb
	echo
	pcp_message INFO "After a reboot these extensions will be permanently deleted:" "text"
	sudo -u tc tce-audit delete samba4.tcz
	echo
	# The init.d script is now part of the extension, but make sure it is not in backup
	sed -i '/usr\/local\/etc\/init.d\/samba/d' /opt/.filetool.lst
	sed -i '/usr\/local\/var\/lib\/samba/d' /opt/.filetool.lst
	sed -i '/usr\/local\/etc\/samba\/smb.conf/d' /opt/.filetool.lst
}

pcp_samba_status() {
	if [ -f /usr/local/etc/init.d/samba4 ]; then
		/usr/local/etc/init.d/samba4 status 1>/dev/null
		echo $?
	else
		echo 1
	fi
}
#----------------------------------------------------------------------------------------

REBOOT_REQUIRED=0
case "$ACTION" in
	Start)
		case "$LMSDATA" in
			usb:*|net:*) [ -f /home/tc/.slimserver.cfg ] && . /home/tc/.slimserver.cfg
				MNT=$(echo $CACHE | awk -F"/" '{$2="/"$2"/"; print $2$3}')
			;;
			default) MNT="$TCEMNT";;
		esac
		pcp_heading5 "Logitech Media Server (LMS)"
		pcp_infobox_begin
		mount | grep -qs $MNT
		if [ $? -eq 0 ]; then
			if [ ! -x /usr/local/etc/init.d/slimserver ]; then
				pcp_message INFO "Loading LMS extensions..." "text"
				sudo -u tc tce-load -i slimserver.tcz
			fi
			pcp_message INFO "Starting LMS..." "text"
			pcp_message INFO "" "text" "-n"
			sudo /usr/local/etc/init.d/slimserver start
		else
			pcp_message ERROR "LMS data disk not mounted at $MNT, LMS will not start." "text"
		fi
		pcp_infobox_end
	;;
	Stop)
		pcp_heading5 "Logitech Media Server (LMS)"
		pcp_infobox_begin
		pcp_message INFO "Stopping LMS..." "text"
		pcp_message INFO "" "text" "-n"
		sudo /usr/local/etc/init.d/slimserver stop
		sleep 2
		pcp_infobox_end
	;;
	Restart)
		pcp_heading5 "Logitech Media Server (LMS)"
		pcp_infobox_begin
		pcp_message INFO "Restarting LMS..." "text"
		pcp_message INFO "" "text" "-n"
		sudo /usr/local/etc/init.d/slimserver stop
		pcp_message INFO "" "text" "-n"
		sudo /usr/local/etc/init.d/slimserver start
		pcp_infobox_end
	;;
	Install)
		pcp_heading5 "Downloading Logitech Media Server (LMS)"
		pcp_infobox_begin
		pcp_sufficient_free_space 48000
		if [ $? -eq 0 ]; then
			pcp_install_lms
			if [ -f $TCEMNT/tce/optional/slimserver.tcz ]; then
				LMSERVER="yes"
				pcp_save_to_config
				pcp_backup "text"
			else
				pcp_message ERROR "Error Downloading LMS, please try again later." "text"
			fi
		fi
		pcp_infobox_end
	;;
	Remove)
		pcp_heading5 "Removing Logitech Media Server (LMS)"
		pcp_infobox_begin
		pcp_message INFO "Removing LMS Extensions..." "text"
		LMSERVER="no"
		pcp_save_to_config
		pcp_remove_lms
		pcp_backup "text"
		if [ x"$DISABLECACHE" = x"" ]; then
			STRING1='Press [OK] to remove LMS cache.....To keep the cache - Press [Cancel]'
			SCRIPT1='lms.cgi?ACTION=Remove_cache&REBOOT_REQUIRED=1'
			pcp_confirmation_required
		fi
		pcp_infobox_end
		REBOOT_REQUIRED=1
	;;
	Remove_cache)
		pcp_remove_lms_cache
	;;
	Remove_cconvert)
		pcp_heading5 "Removing custom_convert.conf"
		pcp_infobox_begin
		pcp_remove_custom_convert
		pcp_infobox_end
	;;
	Rescan*)
		( echo "$(pcp_controls_mac_address) $RESCAN"; echo exit ) | nc 127.0.0.1 9090 > /dev/null
	;;
	Install_FS)
		pcp_heading5 "Installing extra file system support"
		pcp_infobox_begin
		pcp_sufficient_free_space 4300
		if [ $? -eq 0 ]; then
			pcp_install_fs
		fi
		pcp_infobox_end
	;;
	Remove_FS)
		pcp_heading5 "Removing extra file system support"
		pcp_infobox_begin
		pcp_remove_fs
		pcp_infobox_end
		REBOOT_REQUIRED=1
	;;
	Install_EXFAT)
		pcp_heading5 "Installing exFAT file system support"
		pcp_infobox_begin
		pcp_sufficient_free_space 170
		if [ $? -eq 0 ]; then
			pcp_install_exfat
		fi
		pcp_infobox_end
	;;
	Remove_EXFAT)
		pcp_heading5 "Removing exFAT file system support"
		pcp_infobox_begin
		pcp_remove_exfat
		pcp_infobox_end
		REBOOT_REQUIRED=1
	;;
	Install_Samba)
		pcp_heading5 "Installing Samba4 Server"
		pcp_infobox_begin
		pcp_sufficient_free_space 25000 "text"
		if [ $? -eq 0 ]; then
			pcp_install_samba4
		fi
		pcp_infobox_end
	;;
	Remove_Samba)
		pcp_heading5 "Removing Samba4 Server"
		pcp_infobox_begin
		pcp_remove_samba4
		SAMBA="disabled"
		pcp_save_to_config
		pcp_backup "text"
		pcp_infobox_end
		REBOOT_REQUIRED=1
	;;
	SambaStart)
		pcp_heading5 "Starting Samba"
		pcp_textarea "none" "/usr/local/etc/init.d/samba4 start" 4
	;;
	SambaStop)
		pcp_heading5 "Stopping Samba"
		pcp_textarea "none" "/usr/local/etc/init.d/samba4 stop" 4
	;;
	SambaRestart)
		pcp_heading5 "Re-Starting Samba"
		pcp_textarea "none" "/usr/local/etc/init.d/samba4 restart" 4
	;;
	Mysb)
		pcp_heading5 "Setting LMS command line options"
		pcp_infobox_begin
		pcp_message INFO "Setting --nomysqueezebox commandline option..." "text"
		case $NOMYSB in
			yes) pcp_lms_set_slimconfig OPTS "--nomysqueezebox" ADD;;
			no)  pcp_lms_set_slimconfig OPTS "--nomysqueezebox" DEL;;
			*)   pcp_warning_message;;
		esac
		[ -f $CFG_FILE ] && . $CFG_FILE
		pcp_infobox_end
	;;
	*)
		pcp_warning_message
	;;
esac
[ $REBOOT_REQUIRED -eq 1 ] && pcp_reboot_required

#--------Set Variables that need to be checked after the above Case Statement -----------
# logic to activate/inactivate buttons depending upon whether LMS is installed or not
if [ -f $TCEMNT/tce/optional/slimserver.tcz ]; then
	DISABLE_LMS=""
else
	DISABLE_LMS="disabled"
fi

# logic to activate/inactivate buttons depending upon whether LMS cache is present or not
TMP=$(find /mnt -type d -maxdepth 3 | grep slimserver/Cache)
if [ -d $TCEMNT/tce/slimserver -o "$TMP" != "" ]; then
	DISABLECACHE=""
else
	DISABLECACHE="disabled"
fi

df | grep -qs ntfs
[ $? -eq 0 ] && EXTRAFSYS="yes" || EXTRAFSYS="no"

[ x"$ACTION" = x"" -a $MODE -ge $MODE_SERVER ] && pcp_lms_warning

#========================================================================================
# Warning message if using AudioCore
#----------------------------------------------------------------------------------------
pcp_lms_audiocore_warning() {
	echo '  <div class="alert alert-primary" role="alert">'
	echo '    <p><b>Warning:</b> Running LMS on the Realtime AudioCore is not recommended.</p>'
	echo '    <ul>'
	echo '      <li>Realtime kernels do not work well in a server environment.</li>'
	echo '      <li>If it does not work properly, you have been warned.</li>'
	echo '    </ul>'
	echo '  </div>'
}
[ $(pcp_audio_core) -eq 1 -a $MODE -ge $MODE_SERVER ] && pcp_lms_audiocore_warning

#========================================================================================
# Main table
#----------------------------------------------------------------------------------------
pcp_border_begin
echo '  <div class="row mt-3">'
#-----------------------------------LMS Indication---------------------------------------
if [ $(pcp_lms_status) -eq 0 ]; then
	pcp_green_tick "running"
else
	pcp_red_cross "not running"
fi

#echo '    <div class="col-1 col-lg-1 ml-1 text-right">'
#echo '      <p>'$INDICATOR'</p>'
#echo '    </div>'
pcp_incr_id
echo '    <div class="col-12 col-lg-4 mx-1">'
echo '      <p>'$INDICATOR'&nbsp;&nbsp;LMS is '$STATUS'&nbsp;&nbsp;'
pcp_helpbadge
echo '      </p>'
echo '      <div id="dt'$ID'" class="'$COLLAPSE' mr-2">'
echo '        <ul>'
echo '          <li>'$(pcp_bi_check)' = LMS running.</li>'
echo '          <li>'$(pcp_bi_x)' = LMS not running.</li>'
echo '        </ul>'
echo '        <p><b>Note:</b></p>'
echo '        <ul>'
echo '          <li>LMS must be running to stream music to players from this pCP.</li>'
echo '        </ul>'
echo '      </div>'
echo '    </div>'
#----------------------------------------------------------------------------------------

#------------------------------------Samba Indication------------------------------------
if [ $(pcp_samba_status) -eq 0 ]; then
	pcp_green_tick "running"
else
	pcp_red_cross "not running"
fi

#echo '      <div class="col-1 col-lg-1 ml-1 text-right">'
#echo '        <p>'$INDICATOR'</p>'
#echo '      </div>'
pcp_incr_id
echo '      <div class="col-12 col-lg-4 mx-1">'
echo '        <p>'$INDICATOR'&nbsp;&nbsp;Samba is '$STATUS'&nbsp;&nbsp;'
pcp_helpbadge
echo '        </p>'
echo '        <div id="dt'$ID'" class="'$COLLAPSE' mr-2">'
echo '          <ul>'
echo '          <li>'$(pcp_bi_check)' = LMS running.</li>'
echo '          <li>'$(pcp_bi_x)' = LMS not running.</li>'
echo '          </ul>'
echo '          <p><b>Note:</b></p>'
echo '          <ul>'
echo '            <li>Samba must be running to share files from this pCP.</li>'
echo '          </ul>'
echo '        </div>'
echo '      </div>'
#----------------------------------------------------------------------------------------
echo '  </div>'
pcp_border_end

pcp_border_begin
pcp_heading5 "Logitech Media Server (LMS) operations"
#----------------------------Enable/disable autostart of LMS-----------------------------
pcp_lms_enable_lms() {

	case "$LMSERVER" in
		yes) LMSERVERyes="checked" ;;
		no) LMSERVERno="checked" ;;
	esac

	echo '  <form name="Select" action="writetolms.cgi" method="get">'
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <button class="'$BUTTON'" type="submit" value="LMS autostart" '$DISABLE_LMS'>Set Autostart</button>'
	echo '      </div>'
	pcp_incr_id
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <div class="form-check form-check-inline">'
	echo '          <input class="form-check-input" id="rad1" type="radio" name="LMSERVER" value="yes" '$LMSERVERyes'>'
	echo '          <label class="form-check-label" for="rad1">Yes</label>'
	echo '          <input type="hidden" name="ACTION" value="Startup">'
	echo '        </div>'
	echo '        <div class="form-check form-check-inline">'
	echo '          <input class="form-check-input" id="rad2" type="radio" name="LMSERVER" value="no" '$LMSERVERno'>'
	echo '          <label class="form-check-label" for="rad2">No</label>'
	echo '        </div>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <p>Automatic start of LMS when pCP boots&nbsp;&nbsp;'
	pcp_helpbadge
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>Yes - will enable automatic start of LMS when pCP boots.</p>'
	echo '          <p>No - will disable automatic start of LMS when pCP boots.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
	echo '  </form>'
}
[ $MODE -ge $MODE_SERVER ] && pcp_lms_enable_lms
#----------------------------------------------------------------------------------------

#------------------------------------Configure LMS---------------------------------------
pcp_lms_server_interface() {

	[ x"" = x"$LMSWEBPORT" ] && LMSPORT=9000 || LMSPORT=$LMSWEBPORT
	[ x"" = x"$(pcp_eth0_ip)" ] && LMS_SERVER_WEB=$(pcp_wlan0_ip) || LMS_SERVER_WEB=$(pcp_eth0_ip)
	LMS_SERVER_WEB_URL="http://${LMS_SERVER_WEB}:${LMSPORT}"

	echo '  <form name="LMS_Interface" action="'$LMS_SERVER_WEB_URL'" target="_blank">'
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN2_1'">'
	echo '        <button class="'$BUTTON'" value="LMS_Web_Page" '$DISABLE_LMS'>LMS Web Page</button>'
	echo '      </div>'
	pcp_incr_id
	echo '      <div class="'$COLUMN2_2'">'
	echo '        <p>LMS Web Pages&nbsp;&nbsp;'
	pcp_helpbadge
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>Use the standard LMS web interface to play music.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
	echo '  </form>'
}
[ $MODE -ge $MODE_SERVER ] && pcp_lms_server_interface
#----------------------------------------------------------------------------------------

#------------------------------------Configure LMS---------------------------------------
pcp_lms_configure_lms() {

	[ x"" = x"$LMSWEBPORT" ] && LMSPORT=9000 || LMSPORT=$LMSWEBPORT
	[ x"" = x"$(pcp_eth0_ip)" ] && LMS_SERVER_WEB=$(pcp_wlan0_ip) || LMS_SERVER_WEB=$(pcp_eth0_ip)
	LMS_SERVER_WEB_URL="http://${LMS_SERVER_WEB}:${LMSPORT}/settings/index.html"

	echo '  <form name="Configure" action="'$LMS_SERVER_WEB_URL'" target="_blank">'
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN2_1'">'
	echo '        <button class="'$BUTTON'" value="Configure LMS" '$DISABLE_LMS'>Configure LMS</button>'
	echo '      </div>'
	pcp_incr_id
	echo '      <div class="'$COLUMN2_2'">'
	echo '        <p>Configure LMS&nbsp;&nbsp;'
	pcp_helpbadge
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>Use the standard LMS web interface to adjust the LMS settings.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
	echo '  </form>'
}
[ $MODE -ge $MODE_SERVER ] && pcp_lms_configure_lms
#----------------------------------------------------------------------------------------

#-----------------------------------LMS Function Form------------------------------------
echo '  <form name="LMS" action="'$0'">'
#--------------------------------------Rescan LMS----------------------------------------
pcp_rescan_lms() {
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <input class="'$BUTTON'" type="submit" name="ACTION" value="Rescan LMS">'
	echo '      </div>'
	pcp_incr_id
	echo '      <div class="form-group '$COLUMN3_2'">'
	echo '        <select class="form-control form-control-sm" name="RESCAN">'
	echo '          <option value="rescan">Look for new and changed media files</option>'
	echo '          <option value="wipecache">Clear library and rescan everything</option>'
	echo '        </select>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <p>Rescan LMS library&nbsp;&nbsp;'
	pcp_helpbadge
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>Rescan the local LMS library.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_rescan_lms
#----------------------------------------------------------------------------------------

#------------------------------------------Install/uninstall LMS-------------------------
pcp_lms_install_lms() {
	if [ ! -f $TCEMNT/tce/optional/slimserver.tcz ]; then
		echo '    <div class="row mx-1">'
		echo '      <div class="'$COLUMN2_1'">'
		echo '        <button class="'$BUTTON'" type="submit" name="ACTION" value="Install">Install LMS</button>'
		echo '      </div>'
		pcp_incr_id
		echo '      <div class="'$COLUMN2_2'">'
		echo '        <p>Install LMS on pCP&nbsp;&nbsp;'
		pcp_helpbadge
		echo '        </p>'
		echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
		echo '          <p>This will install LMS on pCP.</p>'
		echo '        </div>'
		echo '      </div>'
		echo '    </div>'
	else
		echo '    <div class="row mx-1">'
		echo '      <div class="'$COLUMN2_1'">'
		echo '        <input class="'$BUTTON'"'
		echo '               type="submit"'
		echo '               name="ACTION"'
		echo '               value="Remove"'
		echo '               onclick="return confirm('\''This will remove LMS from pCP.\n\nAre you sure?'\'')"'
		echo '        >'
		echo '      </div>'
		pcp_incr_id
		echo '      <div class="'$COLUMN2_2'">'
		echo '        <p>Remove LMS from pCP&nbsp;&nbsp;'
		pcp_helpbadge
		echo '        </p>'
		echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
		echo '          <p>This will remove LMS and all the extra packages that was added with LMS.</p>'
		echo '          <p>You will be promted in the process whether you want to remove or keep your LMS cache.</p>'
		echo '        </div>'
		echo '      </div>'
		echo '    </div>'
	fi
}
[ $MODE -ge $MODE_SERVER ] && pcp_lms_install_lms
#----------------------------------------------------------------------------------------

#------------------------------------------Remove LMS cache-------------------------
pcp_lms_remove_cache() {
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN2_1'">'
	echo '        <button class="'$BUTTON'" type="submit" name="ACTION" value="Remove_cache" onclick="return confirm('\''This will remove all LMS Cache,settings and plugins.\n\nAre you sure?'\'')" '$DISABLECACHE'>Remove cache</button>'
	echo '      </div>'
	pcp_incr_id
	echo '      <div class="'$COLUMN2_2'">'
	echo '        <p>Remove LMS Cache and Preferences from pCP&nbsp;&nbsp;'
	pcp_helpbadge
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>This will remove your the LMS cache and preferences from pCP.</p>'
	echo '          <p>This includes all installed plugins and settings.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_SERVER ] && pcp_lms_remove_cache
#----------------------------------------------------------------------------------------

#-------------------------------------| Start LMS |--------------------------------------
pcp_lms_start_lms() {
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN2_1'">'
	echo '        <button class="'$BUTTON'" type="submit" name="ACTION" value="Start" '$DISABLE_LMS'>Start LMS</button>'
	echo '      </div>'
	pcp_incr_id
	echo '      <div class="'$COLUMN2_2'">'
	echo '        <p>Start LMS&nbsp;&nbsp;'
	pcp_helpbadge
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>This will start LMS.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_SERVER ] && pcp_lms_start_lms
#----------------------------------------------------------------------------------------

#---------------------------------------Stop LMS-----------------------------------------
pcp_lms_stop_lms() {
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN2_1'">'
	echo '        <button class="'$BUTTON'" type="submit" name="ACTION" value="Stop" '$DISABLE_LMS'>Stop LMS</button>'
	echo '      </div>'
	pcp_incr_id
	echo '      <div class="'$COLUMN2_2'">'
	echo '        <p>Stop LMS&nbsp;&nbsp;'
	pcp_helpbadge
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>This will stop LMS.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_SERVER ] && pcp_lms_stop_lms
#----------------------------------------------------------------------------------------

#--------------------------------------Restart LMS---------------------------------------
pcp_lms_restart_lms() {
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN2_1'">'
	echo '        <button class="'$BUTTON'" type="submit" name="ACTION" value="Restart" '$DISABLE_LMS'>Restart LMS</button>'
	echo '      </div>'
	pcp_incr_id
	echo '      <div class="'$COLUMN2_2'">'
	echo '        <p>Restart LMS&nbsp;&nbsp;'
	pcp_helpbadge
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>This will stop LMS and then restart it.</p>'
	echo '          <p><b>Note:</b></p>'
	echo '          <ul>'
	echo '            <li>A restart of LMS is rarely needed.</li>'
	echo '            <li>LMS running indicator will turn green.</li>'
	echo '          </ul>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_SERVER ] && pcp_lms_restart_lms
#----------------------------------------------------------------------------------------

#------------------------------------nomysqueezebox--------------------------------------
pcp_lms_no_mysb() {

	case $OPTIONS in
		*--nomysqueezebox*) NOMYSByes="checked";;
		*) NOMYSBno="checked";;
	esac

	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <button class="'$BUTTON'" type="submit" name="ACTION" value="Mysb" '$DISABLE_LMS'>No MySB</button>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <div class="form-check form-check-inline">'
	echo '          <input class="form-check-input" id="1rad1" type="radio" name="NOMYSB" value="yes" '$NOMYSByes'>'
	echo '          <label class="form-check-label" for="1rad1">Yes</label>'
	echo '        </div>'
	echo '        <div class="form-check form-check-inline">'
	echo '          <input class="form-check-input" id="1rad2" type="radio" name="NOMYSB" value="no" '$NOMYSBno'>'
	echo '          <label class="form-check-label" for="1rad2">No</label>'
	echo '        </div>'
	echo '      </div>'
	pcp_incr_id
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <p>Set --nomysqueezebox command line option for LMS&nbsp;&nbsp;'
	pcp_helpbadge
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>If enabled, this tells LMS to not use any mysqueezebox integrations.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_SERVER ] && pcp_lms_no_mysb
#----------------------------------------------------------------------------------------

#-------------------------------------Show LMS logs--------------------------------------
pcp_lms_show_logs() {

	case "$LOGSHOW" in
		yes) LOGSHOWyes="checked" ;;
		*) LOGSHOWno="checked" ;;
	esac

	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <input class="'$BUTTON'" type="submit" value="Show Logs" '$DISABLE_LMS'>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <div class="form-check form-check-inline">'
	echo '          <input class="form-check-input" id="2rad1" type="radio" name="LOGSHOW" value="yes" '$LOGSHOWyes'>'
	echo '          <label class="form-check-label" for="2rad1">Yes</label>'
	echo '        </div>'
	echo '        <div class="form-check form-check-inline">'
	echo '          <input class="form-check-input" id="2rad2" type="radio" name="LOGSHOW" value="no" '$LOGSHOWno'>'
	echo '          <label class="form-check-label" for="2rad2">No</label>'
	echo '        </div>'
	echo '      </div>'
	pcp_incr_id
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <p>Show LMS logs&nbsp;&nbsp;'
	pcp_helpbadge
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>Show Server and Scanner log in text area below.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_SERVER ] && pcp_lms_show_logs
#----------------------------------------------------------------------------------------

#-------------------------------Show custom_convert.conf---------------------------------
pcp_lms_show_cconvert() {

	case "$CCSHOW" in
		yes) CCSHOWyes="checked" ;;
		*) CCSHOWno="checked" ;;
	esac

	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <input class="'$BUTTON'" type="submit" value="Show CConv" '$DISABLE_LMS'>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <div class="form-check form-check-inline">'
	echo '          <input class="form-check-input" id="3rad1" type="radio" name="CCSHOW" value="yes" '$CCSHOWyes'>'
	echo '          <label class="form-check-label" for="3rad1">Yes</label>'
	echo '        </div>'
	echo '        <div class="form-check form-check-inline">'
	echo '          <input class="form-check-input" id="3rad2" type="radio" name="CCSHOW" value="no" '$CCSHOWno'>'
	echo '          <label class="form-check-label" for="3rad2">No</label>'
	echo '        </div>'
	echo '      </div>'
	pcp_incr_id
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <p>Show LMS Custom Convert&nbsp;&nbsp;'
	pcp_helpbadge
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>Show the current custom-convert.conf file on the system.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN2_1'">'
	echo '        <button class="'$BUTTON'"'
	echo '                type="submit"'
	echp '                name="ACTION"'
	echo '                value="Remove_cconvert"'
	echo '                onclick="return confirm('\''This will remove your custom convert settings file.\n\nAre you sure?'\'')"'
	echo '                '$DISABLECACHE'>Remove CConv'
	echo '        </button>'
	echo '      </div>'
	pcp_incr_id
	echo '      <div class="'$COLUMN2_2'">'
	echo '        <p>Remove LMS custom_convert.conf from pCP&nbsp;&nbsp;'
	pcp_helpbadge
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>This will remove your the custom convert file for LMS  from pCP.</p>'
	echo '          <p>Custom convert is used to define custom trascoding options.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_SERVER -a -f $LMS_CC_FILE ] && pcp_lms_show_cconvert
#----------------------------------------------------------------------------------------
echo '  </form>'

#-------------------------------Upload custom convert------------------------------------
pcp_lms_customconvert() {
	echo '  <form name="Custom" action="uploadconffile.cgi" enctype="multipart/form-data" method="post">'
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <button class="'$BUTTON'" id="UP1" type="submit" name="ACTION" value="Custom" disabled>Upload</button>'
	echo '      </div>'
	echo '      <div class="col-4">'
	echo '        <input type="file" id="file" name="CUSTOMCONVERT" onclick="document.getElementById('\''UP1'\'').disabled = false">'
	echo '      </div>'
	pcp_incr_id
	echo '      <div class="col-6">'
	echo '        <p>Upload custom-convert to LMS&nbsp;'
	pcp_helpbadge
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>Custom convert is used to define custom trascoding options.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
	echo '  </form>'
}
[ $MODE -ge $MODE_SERVER -a "$DISABLE_LMS" = "" ] && pcp_lms_customconvert
#----------------------------------------------------------------------------------------

#--------------------------------------Update LMS----------------------------------------
pcp_update_lms() {
	echo '  <form name="Update" action="lms-update.cgi">'
	#---------------------------------Nightly update-------------------------------------
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN2_1'">'
	echo '        <button class="'$BUTTON'" type="submit" name="ACTION" value="Nightly" '$DISABLE_LMS'>Nightly Update</button>'
	echo '      </div>'
	pcp_incr_id
	echo '      <div class="'$COLUMN2_2'">'
	echo '        <p>Download and update LMS Nightly Server Package&nbsp;&nbsp;'
	pcp_helpbadge
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>The update process will take some minutes and finally LMS will restart.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
	#-----------------------------------Update libs--------------------------------------
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN2_1'">'
	echo '        <button class="'$BUTTON'" type="submit" name="ACTION" value="Binary" '$DISABLE_LMS'>Update Libs</button>'
	echo '      </div>'
	pcp_incr_id
	echo '      <div class="'$COLUMN2_2'">'
	echo '        <p>Download and update LMS Binaries and Libraries&nbsp;&nbsp;'
	pcp_helpbadge
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>These packages are specific to pCP.</p>'
	echo '          <p>A reboot will be required if there are updated packages.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	echo '  </form>'
}
[ $MODE -ge $MODE_SERVER ] && pcp_update_lms
#----------------------------------------------------------------------------------------
pcp_border_end

pcp_border_begin
#========================================================================================
# Slimserver Cache and Prefs to Mounted Drive
#----------------------------------------------------------------------------------------
pcp_slimserver_persistence() {

	COL1="col-1"
	COL2="col-2"
	COL3="col-4"
	COL4="col-5"

	pcp_heading5 "Save LMS Server Cache and Preferences to Mounted Drive"

	pcp_incr_id
	echo '  <form name="Mount" action="writetomount.cgi" method="get">'
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COL1'"><dt>Enabled</dt></div>'
	echo '      <div class="'$COL2'"><dt>Mount Type</dt></div>'
	echo '      <div class="'$COL3'"><dt>LMS Data Storage Location</dt></div>'
	echo '      <div class="'$COL4'">'
	echo '        <p>This is the Location where LMS will save Data&nbsp;&nbsp;'
	pcp_helpbadge
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>Including Music Database, Artwork Cache and System Preferences.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'

	USByes=""
	NETyes=""
	DEFyes=""
	case "$LMSDATA" in
		default) DEFyes="checked";;
		*);; #USB and NET checked will be set later.
	esac
	LMSMNTFOUND=0
	for I in $(mount | grep -E '/dev/(sd[a-z]|mmcblk0p[3-9])' | cut -d ' ' -f1); do
		if [ "$I" != "${BOOTDEV}" -a "$I" != "${TCEDEV}" ]; then
			USBMOUNT=$(mount | grep -w $I | cut -d ' ' -f3)
			USBUUID=$(blkid $I -s UUID| awk -F"UUID=" '{print $NF}' | tr -d "\"")
			USBmnt="usb:${USBUUID}"
			if [ "$LMSDATA" = "$USBmnt" ]; then
				USByes="checked"
				LMSMNTFOUND=1
			else
				USByes=""
			fi

			echo '    <div class="row mx-1">'
			echo '      <div class="'$COL1' text-sm-center">'
			echo '        <input id="'$I'" type="radio" name="LMSDATA" value="'$USBmnt'" '$USByes'>'
			echo '      </div>'
			echo '      <div class="'$COL2'">'

			case $I in
				/dev/sd*) echo '        <p>USB Disk</p>';;
				/dev/mmcblk0p*) echo '        <p>microSD Card</p>';;
			esac

			echo '      </div>'
			echo '      <div class="'$COL3'">'
			echo '        <p>'${USBMOUNT}'/slimserver</p>'
			echo '      </div>'
			if [ -d ${USBMOUNT}/slimserver/Cache ]; then
				echo '      <div class="'$COL4'">'
				echo '        <p>There is a Cache folder found on this drive.</p>'
				echo '      </div>'
			fi
			echo '      </div>'
		fi
	done

	for NETMOUNT in $(mount | grep -E 'cifs|nfs' | awk -F' on ' '{print $2}' | cut -d ' ' -f1); do
		NETmnt="net:${NETMOUNT}"
		if [ "$LMSDATA" = "$NETmnt" ]; then
			NETyes="checked"
			LMSMNTFOUND=1
		else
			Netyes=""
		fi

		echo '    <div class="row mx-1">'
		echo '      <div class="'$COL1' text-sm-center">'
		echo '          <input id="'$NETMOUNT'" type="radio" name="LMSDATA" value="'$NETmnt'" '$NETyes'>'
		echo '          <label for="'$NETMOUNT'">&nbsp;</label>'
		echo '      </div>'
		echo '      <div class="'$COL2'">'
		echo '        <p>Network Disk</p>'
		echo '      </div>'
		echo '      <div class="'$COL3'">'
		echo '        <p>'${NETMOUNT}'/slimserver</p>'
		echo '      </div>'
		if [ -d ${NETMOUNT}/slimserver/Cache ]; then
			echo '    <div class="'$COL4'">'
			echo '      <p>There is a Cache folder found on this drive.</p>'
			echo '    </div>'
		fi
		echo '    </div>'
	done

	case "${LMSDATA:0:4}" in
		usb:|net:)
			if [ $LMSMNTFOUND -eq 0 ]; then
				[ -f /home/tc/.slimserver.cfg ] && . /home/tc/.slimserver.cfg

				echo '    <div class="row mx-1">'
				echo '      <div class="'$COL1' text-sm-center">'
				echo '        <input id="radxx" type="radio" name="LMSDATA" value="'${LMSDATA}'" checked disabled>'
				echo '      </div>'
				echo '      <div class="'$COL2'">'
				echo '        <p>'$(echo ${LMSDATA:0:3} | tr [a-z] [A-Z])' Disk</p>'
				echo '      </div>'
				echo '      <div class="'$COL3'">'
				TMP=$(echo $CACHE | awk -F"/" '{$2="/"$2"/"; print $2$3}')
				echo '        <p>'$(echo ${LMSDATA:0:3} | tr [a-z] [A-Z])' Disk '${LMSDATA:4}' Not Mounted on '$TMP', LMS will not start.</p>'
				echo '      </div>'
				echo '    </div>'
			fi
		;;
		*);;
	esac
	#------------------------------------------------------------------------------------
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COL1' text-sm-center">'
	echo '        <input id="radboot" type="radio" name="LMSDATA" value="default" '$DEFyes'>'
	echo '      </div>'
	echo '      <div class="'$COL2'">'
	echo '        <p>pCP Boot Disk</p>'
	echo '      </div>'
	echo '      <div class="'$COL3'">'
	echo '        <p>'$TCEMNT'/tce/slimserver</p>'
	echo '      </div>'
	if [ -d $TCEMNT/tce/slimserver/Cache ]; then
		echo '      <div class="'$COL4'">'
		echo '        <p>There is a Cache folder found on this drive.</p>'
		echo '      </div>'
	fi
	echo '    </div>'
#--------------------------------------Submit button-------------------------------------
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <button class="'$BUTTON'" type="submit" name="ACTION" value="Set">Set LMS Data</button>'
	echo '        <input type="hidden" name="MOUNTTYPE" value="slimconfig">'
	echo '      </div>'
	echo '      <div class="col">'
	echo '        <p>Set the Data Location Only.</p>'
	echo '      </div>'
	echo '    </div>'
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <button class="'$BUTTON'" type="submit" name="ACTION" value="Move">Move LMS Data</button>'
	echo '      </div>'
	echo '      <div class="col">'
	echo '        <p>Set the Data Location and Move Cache to that location.</p>'
	echo '      </div>'
	echo '    </div>'
#----------------------------------------------------------------------------------------
	echo '  </form>'
}
[ $MODE -ge $MODE_SERVER ] && pcp_slimserver_persistence
pcp_border_end

pcp_border_begin
#========================================================================================
# Extra File System Support
#----------------------------------------------------------------------------------------
pcp_extra_filesys() {

	pcp_heading5 "Install and Enable additional File Systems"

	DISABLE_REMOVEFS=0
	DISABLE_REMOVEEXFAT=0
	for I in `mount | awk '{print $5}'`
	do
		case "$I" in
			fat*|vfat|*squash*|proc|tmpfs|sysfs|devpts|ext*);;
			exfat|fuseblk) DISABLE_REMOVEEXFAT=1;;
			*) DISABLE_REMOVEFS=1;;
		esac
	done
	#------------------------------------------------------------------------------------
	echo '  <form name="Start" action="'$0'" method="get">'

	pcp_incr_id
	echo '    <div class="row mx-1">'
	if [ "$EXTRAFSYS" = "no" ]; then
		echo '      <div class="'$COLUMN2_1'">'
		echo '        <button class="'$BUTTON'" type="submit" name="ACTION" value="Install_FS">Install</button>'
		echo '      </div>'
		echo '      <div class="'$COLUMN2_2'">'
		echo '        <p>Install additional file systems for pCP&nbsp;&nbsp;'
		pcp_helpbadge
		echo '        </p>'
		echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
		echo '          <p>This will install file system support for pCP.</p>'
		echo '          <p>FAT/vFAT/FAT32 ext2/3/4 are built-in to pCP by default.</p>'
		echo '          <p>These extra file systems include network and NTFS file systems.</p>'
		echo '        </div>'
		echo '      </div>'
	elif [ $DISABLE_REMOVEFS -eq 0 ]; then
		echo '      <div class="'$COLUMN2_1'">'
		echo '        <button class="'$BUTTON'" type="submit" name="ACTION" value="Remove_FS">Remove</button>'
		echo '      </div>'
		echo '      <div class="'$COLUMN2_2'">'
		echo '        <p>Remove additional file systems from pCP&nbsp;&nbsp;'
		pcp_helpbadge
		echo '        </p>'
		echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
		echo '          <p>This will remove all but the default file system support from pCP.</p>'
		echo '          <p>FAT/vFAT/FAT32 ext2/3/4 are built-in to pCP by default.</p>'
		echo '        </div>'
		echo '      </div>'
	else
		echo '      <div class="'$COLUMN2_1'">'
		echo '        <button class="'$BUTTON'" type="submit" name="ACTION" value="Remove_FS" Disabled>Remove</button>'
		echo '      </div>'
		echo '      <div class="'$COLUMN2_2'">'
		echo '        <p>Additional file systems are in use&nbsp;&nbsp;'
		pcp_helpbadge
		echo '        </p>'
		echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
		echo '          <p>Unable to remove additional file system support from pCP'
		echo '             as there are currently active drives mounted using this support.</p>'
		echo '        </div>'
		echo '      </div>'
	fi
	echo '    </div>'
	#------------------------------------------------------------------------------------
	pcp_incr_id
	echo '    <div class="row mx-1">'

	if [ "$EXTRAFSYS" = "yes" ]; then

		pcp_incr_id
		[ -x /usr/local/sbin/mount.exfat ] && EXFATFS="yes" || EXFATFS="no"
		if [ "$EXFATFS" = "no" ]; then
			echo '      <div class="'$COLUMN2_1'">'
			echo '        <button class="'$BUTTON'" type="submit" name="ACTION" value="Install_EXFAT">Install exFAT</button>'
			echo '      </div>'
			echo '      <div class="'$COLUMN2_2'">'
			echo '        <p>Install exFAT file system for pCP&nbsp;&nbsp;'
			pcp_helpbadge
			echo '        </p>'
			echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
			echo '          <p>This will install exFAT file system support for pCP.</p>'
			echo '          <p>FAT/vFAT/FAT32 ext2/3/4 are built-in to pCP by default.</p>'
			echo '          <p><b>Note:</b> This is only for exFAT file system support.</p>'
			echo '        </div>'
			echo '      </div>'
		elif [ $DISABLE_REMOVEEXFAT -eq 0 ]; then
			echo '      <div class="'$COLUMN2_1'">'
			echo '        <button class="'$BUTTON'" type="submit" name="ACTION" value="Remove_EXFAT">Remove exFAT</button>'
			echo '      </div>'
			echo '      <div class="'$COLUMN2_2'">'
			echo '        <p>Remove additional exFAT file system from pCP&nbsp;&nbsp;'
			pcp_helpbadge
			echo '        </p>'
			echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
			echo '          <p>This will remove exFAT file system support from pCP.</p>'
			echo '          <p>FAT/vFAT/FAT32 ext2/3/4 are built-in to pCP by default.</p>'
			echo '        </div>'
			echo '      </div>'
		else
			echo '      <div class="'$COLUMN2_1'">'
			echo '        <button class="'$BUTTON'" type="submit" name="ACTION" value="Remove_EXFAT" Disabled>Remove exFAT</button>'
			echo '      </div>'
			echo '      <div class="'$COLUMN2_2'">'
			echo '        <p>exFAT file systems are in use&nbsp;&nbsp;'
			pcp_helpbadge
			echo '        </p>'
			echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
			echo '          <p>Unable to remove exFAT file system support from pCP'
			echo '             as there are currently active drives mounted using this support.</p>'
			echo '        </div>'
			echo '      </div>'
		fi
	fi
	echo '    </div>'
	#------------------------------------------------------------------------------------
	echo '  </form>'
}
[ $MODE -ge $MODE_PLAYER ] && pcp_extra_filesys
#----------------------------------------------------------------------------------------
pcp_border_end

pcp_border_begin
#========================================================================================
# USB Disk Mounting Operations
#----------------------------------------------------------------------------------------
pcp_mount_usbdrives() {
	# Used to identify which fdisk, fdisk -V fails under busybox, but not util-linux.
	fdisk -V 2>&1 | grep -q -i busybox
	[ $? -eq 0 ] && BBFDISK=1 || BBFDISK=0
	# Read config file
	NUM_USB_CONF=0
	NUM_USB_CONF_ENABLED=0
	if [ -f  ${USBMOUNTCONF} ]; then
		while read LINE; do
			case $LINE in
				[*)
					NUM_USB_CONF=$((NUM_USB_CONF+1))
					# Assume disk is not plugged in, then enable in section below.
					eval DISKFOUND${NUM_USB_CONF}="no"
				;;
				*USBDISK*)
					eval USBDISK${NUM_USB_CONF}=$(pcp_trimval "${LINE}")
					[ $(eval echo \${USBDISK${NUM_USB_CONF}}) = "enabled" ] && $((NUM_USB_CONF_ENABLED+1))
				;;
				*POINT*) eval MOUNTPOINT${NUM_USB_CONF}=$(pcp_trimval "${LINE}");;
				*UUID*) eval MOUNTUUID${NUM_USB_CONF}=$(pcp_trimval "${LINE}");;
				*) ;;
			esac
		done < $USBMOUNTCONF
	fi
	#------------------------------------------------------------------------------------
	pcp_heading5 "Pick from the following detected USB disks to mount"
	echo '  <form name="Mount" action="writetomount.cgi" method="get">'
	#------------------------------------------------------------------------------------
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="col">'
	echo '        <p>Mount USB Disk&nbsp;&nbsp;'
	pcp_helpbadge
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>If Enabled checked, the USB disk will be mounted to the mount point and will be auto-mounted on startup.</p>'
	echo '          <p>&#60;Mount Point&#62; is the name of the mount point for the drive.</p>'
	echo '          <p>&nbsp;&nbsp;&nbsp;- Alpha-numeric pathnames required (up to 32 characters).</p>'
	echo '          <p>&nbsp;&nbsp;&nbsp;- Do not use hardware device names like sda1 or mmcblk0.</p>'
	echo '          <p>All other fields are for identification purposes.</p>'
	echo '          <br />'
	echo '          <p>GPT partitioned disks require the additional util-linux.tcz extension.</p>'
	echo '          <p>UTF-8 support for FAT32 requires the additional file systems extensions.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	COL1="col-1 text-center"
	COL2="col-2 mr-2"
	COL3="col-2"
	COL4="col-1 mr-3"
	COL5="col-1"
	COL6="col-3"
	COL7="col-1"
	#------------------------------------------------------------------------------------
	echo '    <div class="form-row mx-1">'
	echo '      <div class="'$COL1'"><dt>Enabled</dt></div>'
	echo '      <div class="'$COL2'"><dt>Mount Point</dt></div>'
	echo '      <div class="'$COL3'"><dt>Device</dt></div>'
	echo '      <div class="'$COL4'"><dt>Label</dt></div>'
	echo '      <div class="'$COL5'"><dt>FS Type</dt></div>'
	echo '      <div class="'$COL6'"><dt>UUID</dt></div>'
	echo '      <div class="'$COL7'"><dt>Size</dt></div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	# Find all USB devices currently attached to system
	ALLPARTS=$(fdisk -l | awk '$1 ~ /dev/{printf "%s\n",$1}')
	NUM_USB_ATTACHED=0
	for I in $ALLPARTS; do
		# Do not show the boot Drive
		if [ "$I" != "${BOOTDEV}" -a "$I" != "${TCEDEV}" ]; then
			NUM_USB_ATTACHED=$((NUM_USB_ATTACHED+1))
			PART=$I
			LBL=$(blkid $I -s LABEL| awk -F"LABEL=" '{print $NF}' | tr -d "\"")
			UUID=$(blkid $I -s UUID| awk -F"UUID=" '{print $NF}' | tr -d "\"")
			PTTYPE=$(blkid $I -s TYPE| awk -F"TYPE=" '{print $NF}' | tr -d "\"")
			if [ $BBFDISK -eq 1 ]; then
				SIZE=$(fdisk -l | grep $I | sed "s/*//" | tr -s " " | cut -d " " -f7 | tr -d +)
			else
				SIZE=$(fdisk -l | grep $I | sed "s/*//" | tr -s " " | cut -d " " -f5 | tr -d +)
			fi
			SIZExB="${SIZE}B"
			# Compare to previously configured drives from USBMOUNTCONF
			J=1
			while [ $J -le $NUM_USB_CONF ]
			do
				MNT=$(eval echo "\${MOUNTUUID${J}}")
				case "$MNT" in
					"$UUID")
						TST=$(eval echo "\${USBDISK${J}}")
						if [ "$TST" != "" ]; then
							USBDISKyes="checked"
							REQUIRED="required"
						fi
						eval DISKFOUND${J}="yes"
						PNT=$(eval echo "\${MOUNTPOINT${J}}")
						break
					;;
					*)
						USBDISKyes=""
						PNT=""
						REQUIRED=""
					;;
				esac
			J=$((J+1))
			done

			case "$PTTYPE" in
				fat*|vfat|ext*) DISABLE="";;
				exfat)
					if [ ! -x /usr/local/sbin/mount.exfat ]; then
						DISABLE="Disabled"
						UUID="Please install exfat-utils.tcz"
					else
						DISABLE=""
					fi
				;;
				*)
					if [ "$EXTRAFSYS" = "no" ]; then
						DISABLE="Disabled"
						UUID="Please install extra file systems"
					else
						DISABLE=""
					fi
				;;
			esac

			# Keepenabled is due to submitting a disabled checkbox does not submit current value
			if [ "${LMSDATA:4}" = "$UUID" ]; then
				DISABLE="disabled"
				KEEPENABLED="USBDISK${NUM_USB_ATTACHED}"
			fi
			# We must have a UUID defined.
			if [ "$UUID" = "" ]; then
				DISABLE="disabled"
				UUID="Invalid UUID, Please check/reformat disk"
			fi
			echo '    <div class="form-row mx-1">'
			echo '      <div class="'$COL1'">'
			echo '        <input type="checkbox" id="USB'${NUM_USB_ATTACHED}'" name="USBDISK'${NUM_USB_ATTACHED}'" value="enabled" onchange="setrequired('${NUM_USB_ATTACHED}')" '$USBDISKyes' '$DISABLE'>'
			echo '        <label for="USB'${NUM_USB_ATTACHED}'">&nbsp;</label>'
			echo '        <input type="hidden" name="MOUNTUUID'${NUM_USB_ATTACHED}'" value="'$UUID'">'
			echo '      </div>'
			echo '      <div class="'$COL2'">'
			echo '        <div class="input-group input-group-sm">'
			echo '          <div class="input-group-prepend">'
			echo '            <div class="input-group-text">/mnt/</div>'
			echo '          </div>'
			echo '          <input class="form-control form-control-sm" type="text" id="USBPOINT'${NUM_USB_ATTACHED}'" name="MOUNTPOINT'${NUM_USB_ATTACHED}'" value="'$PNT'" '$REQUIRED' pattern="(?!sd)(?!mmcblk)^[a-zA-Z0-9_]{1,32}$">'
			echo '        </div>'
			echo '      </div>'
			echo '      <div class="'$COL3'">'$PART'</div>'
			echo '      <div class="'$COL4'">'$LBL'</div>'
			echo '      <div class="'$COL5'">'$PTTYPE'</div>'
			echo '      <div class="'$COL6'">'$UUID'</div>'
			echo '      <div class="'$COL7'">'$SIZExB'</div>'
			echo '    </div>'
		fi
	done
	#------------------------------------------------------------------------------------
	fdisk -l | grep -q "Found valid GPT"
	if [ $? -eq 0 ]; then
		echo '    <div class="row mx-1">'
		echo '      <div class="'$COLUMN3_1'"></div>'
		echo '      <div class="'$COLUMN3_2'">'
		echo '        <p>Disk with GPT partition table Found! Install extension "util-linux.tcz" for compatability.</p>'
		echo '      </div>'
		echo '      <div class="'$COLUMN3_3'">'
		echo '        <button class="'$BUTTON'" type="submit" name="ACTION" value="gptfdisk">Install Support</button>'
		echo '      </div>'
		echo '    </div>'
	fi
	#------------------------------------------------------------------------------------
	J=1
	while [ $J -le $NUM_USB_CONF ]
	do
		if [ $(eval echo \${USBDISK${J}}) = "enabled" ]; then
			UUID=$(eval echo "\${MOUNTUUID${J}}")
			TST=$(eval echo "\${DISKFOUND${J}}")
			PNT=$(eval echo "\${MOUNTPOINT${J}}")
			if [ "$TST" = "no" ]; then
				# Drive is actually not attached, but we needed it to be.
				NUM_USB_ATTACHED=$((NUM_USB_ATTACHED+1))

				echo '    <div class="row mx-1">'
				echo '      <div class="col-1 text-sm-center">'
				echo '        <input type="checkbox" id="USB'${NUM_USB_ATTACHED}'" name="USBDISK'${NUM_USB_ATTACHED}'" value="enabled" checked>'
				echo '        <label for="USB'${NUM_USB_ATTACHED}'">&nbsp;</label>'
				echo '        <input type="hidden" name="MOUNTUUID'${NUM_USB_ATTACHED}'" value="'$UUID'">'
				echo '        <input type="hidden" name="MOUNTPOINT'${NUM_USB_ATTACHED}'" value="'$PNT'">'
				echo '      </div>'
				echo '      <div class="col-11">'
				echo '        <p>Previously selected disk '$UUID' not found. Please insert and reboot system, or uncheck to disable disk.</p>'
				echo '      </div>'
				echo '    </div>'
			fi
		fi
		J=$((J+1))
	done
	#--------------------------------------Submit button---------------------------------
	pcp_incr_id
	echo '    <div class="row mx-1 mb-2">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <button class="'$BUTTON'" type="submit" name="ACTION" value="Save">Set USB Mount</button>'
	echo '        <input type="hidden" name="MOUNTTYPE" value="localdisk">'
	echo '        <input type="hidden" name="NUMDRIVES" value="'$NUM_USB_ATTACHED'">'
	echo '      </div>'
	echo '    </div>'
	echo '    <div class="row mx-1 mb-2">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <button class="'$BUTTON'"'
	echo '                type="submit"'
	echo '                name="ACTION"'
	echo '                value="Permissions"'
	echo '                onclick="return confirm('\''This will set user ownership and write permissions to user tc on all mounted SD or USB disks.\n\nAre you sure?'\'')">Set Write Permissions</button>'
	echo '      </div>'
	echo '    </div>'
	case $LMSDATA in
		usb*)
			# Checkbox is disabled due to LMS using for cache storage, Keep the specific box enabled
			echo '    <div class="row mx-1 mb-2">'
			echo '      <div class="col">'
			echo '        <input type="hidden" name="'$KEEPENABLED'" value="enabled">'
			echo '        <p><b>Warning:</b> LMS is currently using disk '${LMSDATA:4}' for Data&nbsp;&nbsp;'
			pcp_helpbadge
			echo '        </p>'
			echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
			echo '          <p>Must Move LMS Data to another disk (SD card or Network Share)'
			echo '             in order to change this mount.</p>'
			echo '        </div>'
			echo '      </div>'
			echo '    </div>'
		;;
		*)
			if [ "$EXTRAFSYS" = "no" ]; then
				echo '    <div class="col">'
				echo '      <p>For UTF-8 support on FAT formatted drives, please install extra file systems above.</p>'
				echo '    </div>'
			fi
		;;
	esac
	echo '    </div>'
	#------------------------------------------------------------------------------------

	echo '  </form>'
	#------------------------------------------------------------------------------------
	echo '    <script>'
	echo '      function setrequired(id) {'
	echo '        var box = "USB";'
	echo '        var Box = box.concat(id);'
	echo '        var box1 = "USBPOINT";'
	echo '        var Box1 = box1.concat(id);'
	echo '        if (document.getElementById(Box).checked){'
	echo '          document.getElementById(Box1).setAttribute("required", "");'
	echo '        }'
	echo '        else {'
	echo '          document.getElementById(Box1).required = false;'
	echo '        }'
	echo '      }'
	echo '    </script>'
	#------------------------------------------------------------------------------------
}
[ $MODE -ge $MODE_PLAYER ] && pcp_mount_usbdrives
#----------------------------------------------------------------------------------------
pcp_border_end

pcp_border_begin
#========================================================================================
# Network Disk Mounting Operations
#----------------------------------------------------------------------------------------
pcp_mount_netdrives() {
	NUM_NET_CONF=0
	if [ -f  ${NETMOUNTCONF} ]; then
		while read LINE; do
			case $LINE in
				[*) NUM_NET_CONF=$((NUM_NET_CONF+1));;
				*NETENABLE*) eval NETENABLE${NUM_NET_CONF}=$(pcp_trimval "${LINE}");;
				*MOUNTPOINT*) eval NETMOUNTPOINT${NUM_NET_CONF}=$(pcp_trimval "${LINE}");;
				*MOUNTIP*) eval NETMOUNTIP${NUM_NET_CONF}=$(pcp_trimval "${LINE}");;
				*MOUNTSHARE*) eval NETMOUNTSHARE${NUM_NET_CONF}=$(pcp_trimval "${LINE}");;
				*FSTYPE*) eval NETMOUNTFSTYPE${NUM_NET_CONF}=$(pcp_trimval "${LINE}");;
				*PASS*) eval NETMOUNTPASS${NUM_NET_CONF}=$(pcp_trimval "${LINE}");;
				*USER*) eval NETMOUNTUSER${NUM_NET_CONF}=$(pcp_trimval "${LINE}");;
				*MOUNTOPTIONS*) eval NETMOUNTOPTIONS${NUM_NET_CONF}=$(echo "${LINE}" | awk -F= '{ st = index($0,"=");print substr($0,st+1)}');;
				*);;
			esac
		done < $NETMOUNTCONF
	fi

	if [ "$EXTRAFSYS" = "no" ]; then
		echo '        <div disabled="disabled"></div>'
	else
		echo '        <div></div>'
	fi

	pcp_heading5 "Setup Network Disk Mount"

	echo '  <form name="Mount" action="writetomount.cgi" method="get">'
	#------------------------------------------------------------------------------------
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="col-12">'
	echo '        <p>Mount Remote Network Share&nbsp;&nbsp;'
	pcp_helpbadge
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>Field usage.</p>'
	echo '          <ul>'
	echo '            <li>If Enabled is checked, the network share will be mounted by to the mount point and will be automounted on startup.</li>'
	echo '            <li>&#60;Mount Point&#62; the name of the mount point for the drive. Alpha-numeric pathnames required (up to 32 characters).'
	echo '              <ul>'
	echo '                <li>Do not use hardware device names like sda1 or mmcblk0.</li>'
	echo '              </ul>'
	echo '            </li>'
	echo '            <li>&#60;Server IP address&#62; is only the IP address.  Do not enter any / or :</li>'
	echo '            <li>&#60;Server Share&#62; for CIFS is the share name only (DO not use /).</li>'
	echo '            <li>&#60;Server Share&#62; for NFS is the complete volume i.e. /volume1/Media (DO not use :).</li>'
	echo '            <li>&#60;Username&#62; Username if needed for cifs mount.</li>'
	echo '            <li>&#60;Password&#62; Password if needed for cifs mount. Password must be re-entered for change in mount.</li>'
	echo '            <li>&#60;Options&#62; are a comma delimited list of mount options. Ref mount man pages.'
	echo '              <ul>'
	echo '                <li>CIFS'
	echo '                  <ul>'
	echo '                    <li>vers=2.0 - The linux kernel now defaults to SMB version 3.0, versions must be specified.</li>'
	echo '                    <li>uid=1001 - mounts the drive with user &quot;tc&quot;.  Useful if using ssh sessions to write data to share.</li>'
	echo '                    <li>gid=50 - mounts the drive with group &quot;staff&quot;.  Useful if using ssh sessions to write data to share.</li>'
	echo '                  </ul>'
	echo '                </li>'
	echo '                <li>NFS'
	echo '                  <ul>'
	echo '                    <li>vers=3 - The linux kernel now defaults to NFS version 3, versions must be specified.</li>'
	echo '                  </ul>'
	echo '                </li>'
	echo '              </ul>'
	echo '            </li>'
	echo '          </ul>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------

	#------------------------------------------------------------------------------------
	echo '    <script>'
	echo '      function setnetrequired(id) {'
	echo '        var box = "NET";'
	echo '        var Box = box.concat(id);'
	echo '        var box1 = "NETPOINT";'
	echo '        var Box1 = box1.concat(id);'
	echo '        var box2 = "NETIP";'
	echo '        var Box2 = box2.concat(id);'
	echo '        var box3 = "NETSHARE";'
	echo '        var Box3 = box3.concat(id);'
	echo '        if (document.getElementById(Box).checked){'
	echo '          document.getElementById(Box1).setAttribute("required", "");'
	echo '          document.getElementById(Box2).setAttribute("required", "");'
	echo '          document.getElementById(Box3).setAttribute("required", "");'
	echo '        }'
	echo '        else {'
	echo '          document.getElementById(Box1).required = false;'
	echo '          document.getElementById(Box2).required = false;'
	echo '          document.getElementById(Box3).required = false;'
	echo '        }'
	echo '        setfsopts(id);'
	echo '      }'
	echo '      function setfsopts(id) {'
	echo '        var box = "NET";'
	echo '        var Box = box.concat(id);'
	echo '        var box3 = "NETSHARE";'
	echo '        var Box3 = box3.concat(id);'
	echo '        var box4 = "NETOPTS";'
	echo '        var Box4 = box4.concat(id);'
	echo '        var box5 = "NETFS";'
	echo '        var Box5 = box5.concat(id);'
	echo '        if (document.getElementById(Box).checked && (document.getElementById(Box5).value == "cifs")){'
	echo '          var x = document.getElementById(Box4).value;'
	echo '          x = ( x.length > 0 ) ? x.concat(",") : x;'
	echo '          x = ( x.indexOf("uid=") != -1 ) ? x : x.concat("uid=1001");'
	echo '          x = ( x.indexOf("gid=") != -1 ) ? x : x.concat(",gid=50");'
	echo '          x = ( x.substr(x.length - 1) == ",") ? x.substring(0, x.length - 1) : x;'
	echo '          document.getElementById(Box4).value = x;'
	echo '        }'
	echo '        if (document.getElementById(Box5).value == "nfs"){'
	echo '          document.getElementById(Box3).pattern = "(^[\\/])[a-zA-Z0-9_\\- \\/]{1,32}";'
	echo '        } else {'
	echo '          document.getElementById(Box3).pattern = "[a-zA-Z0-9_\\- ]{1,32}";'
	echo '        }'
	echo '      }'
	echo '      function setfstype(id) {'
	echo '        var box = "NETFS";'
	echo '        var Box = box.concat(id);'
	echo '        var box1 = "NETUSER";'
	echo '        var Box1 = box1.concat(id);'
	echo '        var box2 = "NETPASS";'
	echo '        var Box2 = box2.concat(id);'
	echo '        if (document.getElementById(Box).value == "nfs" ){'
	echo '          document.getElementById(Box1).setAttribute("disabled", "");'
	echo '          document.getElementById(Box2).setAttribute("disabled", "");'
	echo '        }'
	echo '        else {'
	echo '          document.getElementById(Box1).disabled = false;'
	echo '          document.getElementById(Box2).disabled = false;'
	echo '        }'
	echo '        setfsopts(id);'
	echo '        setpwstyle(id);'
	echo '      }'
	echo '      function setpwstyle(id) {'
	echo '        var Box = "NETFS" + id;'
	echo '        var Box1 = "NETPASS" + id;'
	echo '        if ( (document.getElementById(Box).value == "cifs") && (document.getElementById(Box1).value == "" ))'
	echo '          document.getElementById(Box1).style.borderColor = "#ff9933";'
	echo '        else'
	echo '          document.getElementById(Box1).removeAttribute("style");'
	echo '      }'
	echo '    </script>'
	#------------------------------------------------------------------------------------
	COLUMN8_1="col-1"
	COLUMN8_2="col-1"
	COLUMN8_3="col-1"
	COLUMN8_4="col-1"
	COLUMN8_5="col-1"
	COLUMN8_6="col-1"
	COLUMN8_7="col-1"
	COLUMN8_8="col-1"
	#------------------------------------------------------------------------------------
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN8_1'"><dt>Enabled</dt></div>'
	echo '      <div class="'$COLUMN8_2'"><dt>Mount Point</dt></div>'
	echo '      <div class="'$COLUMN8_3'"><dt>IP Address</dt></div>'
	echo '      <div class="'$COLUMN8_4'"><dt>Share Name</dt></div>'
	echo '      <div class="'$COLUMN8_5'"><dt>Share Type</dt></div>'
	echo '      <div class="'$COLUMN8_6'"><dt>Username</dt></div>'
	echo '      <div class="'$COLUMN8_7'"><dt>Password</dt></div>'
	echo '      <div class="'$COLUMN8_8'"><dt>Options</dt></div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	I=1
	NUM_NET_CONF=$((NUM_NET_CONF+1))  # Adds a blank line to the form fields
	while [ $I -le $NUM_NET_CONF ]; do
		TST=$(eval echo \${NETENABLE${I}})
		case "$TST" in
			yes|no)
				[ "$TST" = "yes" ] && NETENABLEyes="checked" || NETENABLEyes=""
				[ "$TST" = "yes" ] && REQUIRED="required" || REQUIRED=""
				PNT=$(eval echo \${NETMOUNTPOINT${I}})
				IP=$(eval echo \${NETMOUNTIP${I}})
				SHARE=$(eval echo \${NETMOUNTSHARE${I}})
				FSTYPE=$(eval echo \${NETMOUNTFSTYPE${I}})
				USER=$(eval echo \${NETMOUNTUSER${I}})
#				PASS=$(eval echo \${NETMOUNTPASS${I}})
				PASS=""
				OPTIONS=$(eval echo \${NETMOUNTOPTIONS${I}})
				CIFS1yes=""
				NFS1yes=""
			;;
			*)
				NETENABLEyes=""
				REQUIRED=""
				PNT=""
				IP=""
				SHARE=""
				FSTYPE=""
				USER=""
				PASS=""
				OPTIONS=""
			;;
		esac
		if [ "${LMSDATA:4}" = "//${IP}/${SHARE}" ]; then
			DISABLE="disabled"
			KEEPENABLED="NETENABLE${I}"
		else
			DISABLE=""
		fi

		echo '    <div class="row mx-1">'
		echo '      <div class="'$COLUMN8_1'">'
		echo '          <input type="checkbox" id="NET'${I}'" name="NETENABLE'${I}'" value="yes" onchange="setnetrequired('${I}')" '$NETENABLEyes' '$DISABLE'>'
		echo '          <label for="NET'${I}'">&#8239;</label>'
		echo '      </div>'
		echo '      <div class="'$COLUMN8_2'">'
		echo '        <p>/mnt/&#8239;<input class="xxxx" type="text" id="NETPOINT'${I}'" name="NETMOUNTPOINT'${I}'" value="'$PNT'" '$REQUIRED' pattern="(?!sd)(?!mmcblk)^[a-zA-Z0-9_]{1,32}$"></p>'
		echo '      </div>'
		echo '      <div class="'$COLUMN8_3'">'
		echo '        <input class="xxxx" type="text" id="NETIP'${I}'" name="NETMOUNTIP'${I}'" value="'$IP'" title="Enter the IP Address of the Remote Server" '$REQUIRED' pattern="((^|\.)((25[0-5])|(2[0-4]\d)|(1\d\d)|([1-9]?\d))){4}$">'
		echo '      </div>'
		echo '      <div class="'$COLUMN8_4'">'
		echo '        <input class="xxxx" type="text" id="NETSHARE'${I}'" name="NETMOUNTSHARE'${I}'" value="'$SHARE'" title="Enter the Name of the Share. Expand the more> above for help" '$REQUIRED' pattern="" onclick="setfsopts('${I}')">'
		echo '      </div>'

		case "$FSTYPE" in
			cifs) CIFS1yes="selected"; USERdisable="";;
			nfs) NFS1yes="selected"; USERdisable="Disabled";;
		esac

		echo '      <div class="column'$COLUMN8_5'">'
		echo '        <select class="xxxx" id="NETFS'${I}'" name="NETMOUNTFSTYPE'${I}'" title="Only CIFS(Samba) and NFS shares are supported" onchange="setfstype('${I}')">'
		echo '          <option value="cifs" '$CIFS1yes'>CIFS</option>'
		echo '          <option value="nfs" '$NFS1yes'>NFS</option>'
		echo '        </select>'
		echo '      </div>'
		echo '      <div class="column'$COLUMN8_6'">'
		echo '        <input class="xxxx" type="text" id="NETUSER'${I}'" name="NETMOUNTUSER'${I}'" value="'$USER'" title="Enter the Username for the remote share.&#13;Not used with NFS" '$USERdisable'>'
		echo '      </div>'
		echo '      <div class="column'$COLUMN8_7'">'
		echo '        <input class="xxxx" type="password" id="NETPASS'${I}'" name="NETMOUNTPASS'${I}'" value="'$PASS'" title="Enter the Password for the remote share.&#13;Not used with NFS" onchange="setpwstyle('${I}')" '$USERdisable'>'
		echo '      </div>'
		echo '      <div class="column'$COLUMN8_8'">'
		echo '        <input class="xxxx" type="text" id="NETOPTS'${I}'" name="NETMOUNTOPTIONS'${I}'" value="'$OPTIONS'" title="Enter any comma delimeted mount option&#13;i.e. uid=1001,gid=50,vers=2.0">'
		echo '      </div>'
		echo '    </div>'
		#--------------------------------------------------------------------------------
		echo '    <script>'
		echo '      var share = "'${SHARE}'";'
		echo '      ShareBox = "NETSHARE'${I}'";'
		echo '      document.getElementById(ShareBox).value = decodeURIComponent(share.replace(/\+/g, "%20"));'
		echo '      setfsopts('${I}');'
		echo '      setpwstyle('${I}');'
		echo '    </script>'
		#--------------------------------------------------------------------------------
		I=$((I+1))
	done
	#------------------------------------------------------------------------------------
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <input id="netclear" type="checkbox" name="CLEARUNUSED" value="yes">'
	echo '        <label for="netclear">&nbsp;</label>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <p>Check this box to clear configuration data for unused shares.</p>'
	echo '      </div>'
	echo '    </div>'
	#--------------------------------------Submit button---------------------------------
	pcp_incr_id
	echo '    <div class="row mx-1">'
	if [ "$EXTRAFSYS" = "no" ]; then
		echo '      <div class="'$COLUMN3_1'">'
		echo '        <button class="'$BUTTON'" type="submit" name="ACTION" value="Save" Disabled>Set NET Mount</button>'
		echo '      </div>'
		echo '      <div class="'$COLUMN3_3'">'
		echo '        <p>Mounting network drives requires extra file system support&nbsp;&nbsp;'
		pcp_helpbadge
		echo '        </p>'
		echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
		echo '          <p>Please add additional file systems using the option above.</p>'
		echo '        </div>'
		echo '      </div>'
	elif [ "${LMSDATA:0:4}" = "net:" ]; then
		echo '      <div class="'$COLUMN3_1'">'
		echo '        <button class="'$BUTTON'" type="submit" name="ACTION" value="Save">Set NET Mount</button>'
		echo '        <input type="hidden" name="'$KEEPENABLED'" value="yes">'
		echo '        <input type="hidden" name="MOUNTTYPE" value="networkshare">'
		echo '        <input type="hidden" name="NUMNET" value="'$NUM_NET_CONF'">'
		echo '      </div>'
		echo '      <div class="'$COLUMN3_3'">'
		echo '        <p> LMS is currently using network drive '${LMSDATA:4}' for Data.&nbsp;&nbsp;'
		pcp_helpbadge
		echo '        </p>'
		echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
		echo '          <p>Must Move LMS Data to another disk (SDcard or USB Disk).</p>'
		echo '          <p>in order to change this mount.</p>'
		echo '        </div>'
		echo '      </div>'
	else
		echo '      <div class="'$COLUMN3_1'">'
		echo '        <button class="'$BUTTON'" type="submit" name="ACTION" value="Save">Set NET Mount</button>'
		echo '        <input type="hidden" name="MOUNTTYPE" value="networkshare">'
		echo '        <input type="hidden" name="NUMNET" value="'$NUM_NET_CONF'">'
		echo '      </div>'
	fi
	echo '    </div>'
#----------------------------------------------------------------------------------------
	echo '  </form>'
}
[ $MODE -ge $MODE_PLAYER ] && pcp_mount_netdrives
#----------------------------------------------------------------------------------------
pcp_border_end

pcp_border_begin
#========================================================================================
# Samba Share Drive Support
#----------------------------------------------------------------------------------------
pcp_samba() {
	pcp_heading5 "Setup Samba Share"
	echo '  <form name="Samba_Setup" action="'$0'" method="get">'
#----------------------------------------------------------------------------------------
	pcp_incr_id
	echo '    <div class="row mx-1">'
	if [ "$SAMBA" = "disabled" ]; then
		echo '      <div class="'$COLUMN3_1'">'
		echo '        <button class="'$BUTTON'" type="submit" name="ACTION" value="Install_Samba">Install</button>'
		echo '      </div>'
		echo '      <div class="col-10">'
		echo '        <p>Install Samba for pCP&nbsp;&nbsp;'
		pcp_helpbadge
		echo '        </p>'
		echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
		echo '          <p>This will install Samba Extension for SMB Share support for pCP.</p>'
		echo '        </div>'
		echo '      </div>'
	else
		echo '      <div class="'$COLUMN3_1'">'
		echo '        <button class="'$BUTTON'" type="submit" name="ACTION" value="Remove_Samba">Remove</button>'
		echo '      </div>'
		echo '      <div class="col-10">'
		echo '        <p>Remove Samba from pCP&nbsp;&nbsp;'
		pcp_helpbadge
		echo '        </p>'
		echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
		echo '          <p>This will remove Samba Extension for SMB Share support for pCP.</p>'
		echo '        </div>'
		echo '      </div>'
	fi
	echo '    </div>'
	#------------------------------------------------------------------------------------
	echo '  </form>'
	#------------------------------------------------------------------------------------
	if [ "$SAMBA" != "disabled" ]; then
		if [ -f $SAMBACONF ]; then
			# This will read the config file.
			GLOBAL=0
			SC=0

			trimshare() {
				echo $1 | tr -d '[]'
			}

			while read LINE; do
				case $LINE in
					*global*) GLOBAL=1;;
					netbios*) NETBIOS=$(pcp_trimval "${LINE}");;
					workgroup*) WGROUP=$(pcp_trimval "${LINE}");;
					[*) SC=$((SC+1)); eval SHARE${SC}=$(trimshare "${LINE}");;
					path*) eval SHAREPATH${SC}=$(pcp_trimval "${LINE}");;
					create\ mask*) eval SHAREMASK${SC}=$(pcp_trimval "${LINE}");;
					writeable*) eval SHARERO${SC}="no";;
					read\ only*) eval SHARERO${SC}="yes";;
					*);;
				esac
			done < $SAMBACONF
		fi

#----------------------------------------------------------------------------------------
		echo '  <form name="Samba_Write" action="writetosamba.cgi" method="get">'
#----------------------------------------------------------------------------------------

		case "$SAMBA" in
			yes) SAMBAyes="checked" ;;
			*) SAMBAno="checked" ;;
		esac

		pcp_incr_id
		echo '    <div class="row mx-1">'
		echo '      <div class="'$COLUMN3_1'">'
		echo '        <button class="'$BUTTON'" type="submit" name="COMMAND" value="autostart">SMB Autostart</button>'
		echo '      </div>'
		echo '      <div class="'$COLUMN3_2'">'
		echo '        <input type="hidden" name="ACTION" value="Startup">'
		echo '        <input id="radsmb1" type="radio" name="SAMBA" value="yes" '$SAMBAyes'>'
		echo '        <label for="radsmb1">Yes</label>'
		echo '        <input id="radsmb2" type="radio" name="SAMBA" value="no" '$SAMBAno'>'
		echo '        <label for="radsmb2">No</label>'
		echo '      </div>'
		echo '      <div class="'$COLUMN3_3'">'
		echo '        <p>Automatic start of Samba when pCP boots&nbsp;&nbsp;'
		pcp_helpbadge
		echo '        </p>'
		echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
		echo '          <p>Yes - will enable automatic start of Samba when pCP boots.</p>'
		echo '          <p>No - will disable automatic start of Samba when pCP boots.</p>'
		echo '        </div>'
		echo '      </div>'
		echo '    </div>'
		#--------------------------------------------------------------------------------
		echo '  </form>'
		#--------------------------------------------------------------------------------
		echo '  <form name="Samba_Run" action="'$0'">'
		#--------------------------------------------------------------------------------
		pcp_incr_id
		echo '    <div class="row mx-1">'
		echo '      <div class="'$COLUMN3_1'">'
		echo '        <button class="'$BUTTON'" type="submit" name="ACTION" value="SambaStart">Start Samba</button>'
		echo '      </div>'
		echo '      <div class="'$COLUMN3_2'">'
		echo '        <p>Start Samba&nbsp;&nbsp;'
		pcp_helpbadge
		echo '        </p>'
		echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
		echo '          <p>This will start Samba.</p>'
		echo '        </div>'
		echo '      </div>'
		echo '    </div>'
		#--------------------------------------------------------------------------------
		pcp_incr_id
		echo '    <div class="row mx-1">'
		echo '      <div class="'$COLUMN3_1'">'
		echo '        <button class="'$BUTTON'" type="submit" name="ACTION" value="SambaStop">Stop Samba</button>'
		echo '      </div>'
		echo '      <div class="'$COLUMN3_2'">'
		echo '        <p>Stop Samba&nbsp;&nbsp;'
		pcp_helpbadge
		echo '        </p>'
		echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
		echo '          <p>This will stop Samba.</p>'
		echo '        </div>'
		echo '      </div>'
		echo '    </div>'
		#--------------------------------------------------------------------------------
		pcp_incr_id
		echo '    <div class="row mx-1">'
		echo '      <div class="'$COLUMN3_1'">'
		echo '        <button class="'$BUTTON'" type="submit" name="ACTION" value="SambaRestart">Restart Samba</button>'
		echo '      </div>'
		echo '      <div class="'$COLUMN3_2'">'
		echo '        <p>Restart Samba&nbsp;&nbsp;'
		pcp_helpbadge
		echo '        </p>'
		echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
		echo '          <p>This will stop Samba and then restart it.</p>'
		echo '          <p><b>Note:</b></p>'
		echo '            <ul>'
		echo '              <li>A restart of Samba is rarely needed.</li>'
		echo '              <li>Samba running indicator will turn green.</li>'
		echo '            </ul>'
		echo '        </div>'
		echo '      </div>'
		echo '    </div>'
		#--------------------------------------------------------------------------------
		echo '  </form>'
		#--------------------------------------------------------------------------------
		echo '  <form name="Passwd" action="writetosamba.cgi" method="get">'
		#--------------------------------------------------------------------------------
		pcp_incr_id
		echo '    <div class="row mx-1">'

		if [ "$STATUS" = "running" ]; then
			PWDISABLE=""
		else
			PWDISABLE="disabled"
		fi

		echo '      <div class="'$COLUMN3_1'">'
		echo '        <button class="'$BUTTON'" type="submit" name="COMMAND" value="setpw" '$PWDISABLE'>Set Password</button>'
		echo '      </div>'
		echo '      <div class="'$COLUMN3_1' ">'
		echo '        <p>UserName: tc</p>'
		echo '      </div>'
		echo '      <div class="'$COLUMN3_1'">'
		echo '        <p>Password:</p>'
		echo '      </div>'
		echo '      <div class="'$COLUMN3_2'">'
		echo '        <input class="xxxx" type="password" name="SAMBAPASS" value="" '$PWDISABLE'>'
		echo '      </div>'
		if [ "$STATUS" = "running" ]; then
			echo '      <div class="'$COLUMN3_2'">'
			echo '        <p>Username and Password to be used to access share&nbsp;&nbsp;'
			pcp_helpbadge
			echo '        </p>'
			echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
			echo '          <p>Needs to be done first time.</p>'
			echo '          <p><b>Note:</b> This value is cached by alot of machines and may not change immediately in the browser.</p>'
			echo '        </div>'
			echo '      </div>'
		else
			echo '      <div class="'$COLUMN3_2'">'
			echo '        <p>Samba has to be running to set password.</p>'
			echo '      </div>'
		fi
		
		#--------------------------------------------------------------------------------
		echo '  </form>'
		#--------------------------------------------------------------------------------
		echo '  <form name="Select" action="writetosamba.cgi" method="get">'
		#--------------------------------------------------------------------------------
		pcp_incr_id
		echo '    <div class="row mx-1">'
		echo '      <div class="'$COLUMN3_1'">'
		echo '        <p>Server Name</p>'
		echo '      </div>'
		echo '      <div class="'$COLUMN3_2'">'
		echo '        <input class="xxxx" type="text" name="NETBIOS" value="'$NETBIOS'" required>'
		echo '      </div>'
		echo '      <div class="'$COLUMN3_3'">'
		echo '        <p>This is the Server name that will show up in your network browser&nbsp;&nbsp;'
		pcp_helpbadge
		echo '        </p>'
		echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
		echo '          <p><b>Note:</b> This value is cached by alot of machines and may not change immediately in the browser.</p>'
		echo '        </div>'
		echo '      </div>'
		echo '    </div>'
		#--------------------------------------------------------------------------------
		pcp_incr_id
		echo '     <div class="row mx-1">'
		echo '       <div class="'$COLUMN3_1'">'
		echo '         <p>Server WorkGroup</p>'
		echo '       </div>'
		echo '       <div class="'$COLUMN3_2'">'
		echo '         <input class="xxxx" type="text" name="WGROUP" value="'$WGROUP'" required>'
		echo '       </div>'
		echo '       <div class="'$COLUMN3_3'">'
		echo '         <p>This is the Server Work Group that will show up in your network browser&nbsp;&nbsp;'
		pcp_helpbadge
		echo '         </p>'
		echo '         <div id="dt'$ID'" class="'$COLLAPSE'">'
		echo '           <p><b>Note:</b> This value is cached by alot of machines and may not change immediately in the browser.</p>'
		echo '         </div>'
		echo '       </div>'
		echo '     </div>'
		#--------------------------------------------------------------------------------
		echo '     <div class="row mx-1">'
		echo '       <div class="'$COLUMN4_1'"><dt>Share Name</dt></div>'
		echo '       <div class="'$COLUMN4_2'"><dt>Share Path</dt></div>'
		echo '       <div class="'$COLUMN4_3'"><dt>Create File Mode</dt></div>'
		echo '       <div class="'$COLUMN4_4'"><dt>Read ONLY</dt></div>'
		echo '     </div>'
		I=1
		SC=$((SC+1))
		while [ $I -le $SC ]
		do
			TST=$(eval echo "\${SHARE${I}}")
			[ "$TST" != "" ] && REQ="required" || REQ=""

			echo '                <div class="row mx-1">'
			echo '                  <div class="'$COLUMN4_1'">'
			echo -n '                    <input class="xxxx" type="text" ID="SHARE'$I'" name="SHARE'$I'" value="'
			eval echo -n "\${SHARE${I}}"
			echo '" title="Enter the name of the Share" pattern="^[a-zA-Z0-9_]{1,32}$" onchange="setsmbrequired('$I')">'
			echo '                  </div>'
			echo '                  <div class="'$COLUMN4_2'">'
			echo -n '                    <input class="xxxx" type="text" ID="SHAREPATH'$I'" name="SHAREPATH'$I'" value="'
			eval echo -n "\${SHAREPATH${I}}"
			echo '" title="Enter the Path to be Shared" '$REQ' pattern="^[a-zA-Z0-9_/]{1,64}$">'
			echo '                  </div>'
			echo '                  <div class="'$COLUMN4_3'">'
			echo -n '                    <input class="xxxx" type="text" ID="SHAREMASK'$I'" name="SHAREMASK'$I'" value="'
			eval echo -n "\${SHAREMASK${I}}"
			echo '" title="Enter the File mode for new files Default=0664" '$REQ' pattern="^[0-7]{4}$">'
			echo '                  </div>'
			RO=$(eval echo "\${SHARERO${I}}")
			case "$RO" in
				yes) SHAREROyes="checked";;
				*) SHAREROyes="";;
			esac
			echo '      <div class="'$COLUMN4_4'">'
			echo '        <input type="checkbox" id="RO'${I}'" name="SHARERO'$I'" value="yes" '$SHAREROyes'>'
			echo '        <label for="RO'${I}'">&#8239;</label>'
			echo '      </div>'
			echo '      <div class="xxxx">'
			echo '        <input type="button" value="Remove" onclick="eraseshare('$I')">'
			echo '      </div>'
			echo '    </div>'
			I=$((I+1))
		done
		#--------------------------------------------------------------------------------
		echo '    <script>'
		echo '      function eraseshare(i) {'
		echo '        var box = "SHARE";'
		echo '        var Box = box.concat(i);'
		echo '        document.getElementById(Box).value = "";'
		echo '        var box = "SHAREPATH";'
		echo '        var Box = box.concat(i);'
		echo '        document.getElementById(Box).value = "";'
		echo '        var box = "SHAREMASK";'
		echo '        var Box = box.concat(i);'
		echo '        document.getElementById(Box).value = "";'
		echo '        setsmbrequired(i);'
		echo '      }'
		echo '      function setsmbrequired(id) {'
		echo '        var box = "SHARE";'
		echo '        var Box = box.concat(id);'
		echo '        var box1 = "SHAREPATH";'
		echo '        var Box1 = box1.concat(id);'
		echo '        var box2 = "SHAREMASK";'
		echo '        var Box2 = box2.concat(id);'
		echo '        if (document.getElementById(Box).value != ""){'
		echo '          document.getElementById(Box1).setAttribute("required", "");'
		echo '          document.getElementById(Box2).setAttribute("required", "");'
		echo '        }'
		echo '        else {'
		echo '          document.getElementById(Box1).required = false;'
		echo '          document.getElementById(Box2).required = false;'
		echo '        }'
		echo '      }'
		echo '    </script>'
		#----------------------------------Submit button---------------------------------
		echo '    <div class="row mx-1">'
		echo '      <div class="'$COLUMN3_1'">'
		echo '        <button class="'$BUTTON'" type="submit" name="ACTION" value="setconfig">Set Shares</button>'
		echo '        <input type="hidden" name="COMMAND" value="setconfig">'
		echo '        <input type="hidden" name="SC" value="'$SC'">'
		echo '      </div>'
		echo '    </div>'
		#--------------------------------------------------------------------------------
		echo '  </form>'
	fi
}
[ $MODE -ge $MODE_SERVER ] && pcp_samba
#----------------------------------------------------------------------------------------
pcp_border_end

#------------------------------------------LMS log text area-----------------------------
pcp_lms_logview() {
	pcp_heading5 "Show LMS logs"
	#------------------------------------------------------------------------------------
	pcp_textarea "$LMS_SERV_LOG" 'cat $LMS_SERV_LOG' 25
	pcp_textarea "$LMS_SCAN_LOG" 'cat $LMS_SCAN_LOG' 25
	#------------------------------------------------------------------------------------
	if [ -f $LMS_UPDATE_LOG ]; then
		pcp_textarea "$LMS_UPDATE_LOG" 'cat $LMS_UPDATE_LOG' 25
	fi
	#------------------------------------------------------------------------------------
}
[ "$LOGSHOW" = "yes" ] && pcp_lms_logview
#----------------------------------------------------------------------------------------

#------------------------------LMS custom convert text area------------------------------
pcp_lms_ccview() {
	pcp_heading5 "Show LMS custom_convert.conf"
	#------------------------------------------------------------------------------------
	pcp_textarea "$LMS_CC_FILE" 'cat $LMS_CC_FILE' 25
	#------------------------------------------------------------------------------------
}
[ "$CCSHOW" = "yes" -a -f $LMS_CC_FILE ] && pcp_lms_ccview
#----------------------------------------------------------------------------------------

pcp_html_end