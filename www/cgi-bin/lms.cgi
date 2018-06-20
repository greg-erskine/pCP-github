#!/bin/sh

# Version: 4.0.0 2018-06-19

. pcp-functions
. pcp-rpi-functions
. pcp-lms-functions

pcp_html_head "LMS Main Page" "SBP"

pcp_picoreplayers_toolbar
pcp_controls
pcp_banner
pcp_navigation
pcp_running_script
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
WGET="/bin/busybox wget"

#---------------------------Routines-----------------------------------------------------

pcp_install_lms() {
	echo '[ INFO ] Downloading LMS...'
	sudo -u tc pcp-load -r $PCP_REPO -w slimserver.tcz
	if [ -f $TCEMNT/tce/optional/slimserver.tcz ]; then
		echo '[ INFO ] Installing LMS...'
		sudo -u tc pcp-load -i slimserver.tcz
		sudo sed -i '/slimserver.tcz/d' $ONBOOTLST
		sudo echo 'slimserver.tcz' >> $ONBOOTLST
		[ $DEBUG -eq 1 ] && echo '[ DEBUG ] LMS is added to onboot.lst'
		[ $DEBUG -eq 1 ] && cat $ONBOOTLST
	fi
}

pcp_remove_lms() {
	sudo /usr/local/etc/init.d/slimserver stop >/dev/null 2>&1
	sudo -u tc tce-audit builddb
	sudo -u tc tce-audit delete slimserver.tcz
	sudo sed -i '/slimserver.tcz/d' $ONBOOTLST
}

pcp_remove_lms_cache() {
	sudo rm -rf $TCEMNT/tce/slimserver/
	for I in $(find /mnt -maxdepth 1 | grep -Ev 'mmcblk0p[1-9]'); do
		[ -d $I/slimserver ] && rm -rf $I/slimserver/
	done
}

pcp_install_fs() {
	RESULT=0
	echo '[ INFO ] Downloaded additional filesystem support.</p>'
	sudo -u tc pcp-load -r $PCP_REPO -w ntfs-3g.tcz
	if [ -f $TCEMNT/tce/optional/ntfs-3g.tcz ]; then
		echo '[ INFO ] Loading filesystem extensions'
		sudo -u tc tce-load -i ntfs-3g.tcz
		[ $? -eq 0 ] && echo -n . || (echo $?; RESULT=1)
		if [ $RESULT -eq 0 ]; then
			echo "ntfs-3g.tcz" >> $ONBOOTLST
			echo '[ INFO ] Filesystem support including NTFS loaded...</p>'
		else
			echo '[ ERROR ] Extensions not loaded, try again later!</p>'
		fi
	fi
}

pcp_remove_fs() {
	echo '[ INFO ] Removing Extensions</p>'
	sudo -u tc tce-audit builddb
	sudo -u tc tce-audit delete ntfs-3g.tcz
	sed -i '/ntfs-3g.tcz/d' $ONBOOTLST
	echo '[ INFO ] Extensions are marked for removal. You must reboot to finish!</p>'
}

pcp_install_exfat() {
	RESULT=0
	echo '[ INFO ] Downloaded exFat filesystem support.</p>'
	sudo -u tc pcp-load -r $PCP_REPO -w pcp-exfat-utils.tcz
	if [ -f $TCEMNT/tce/optional/pcp-exfat-utils.tcz ]; then
		echo '[ INFO ] Loading exfat extensions'
		sudo -u tc tce-load -i pcp-exfat-utils.tcz
		[ $? -eq 0 ] && echo -n . || (echo $?; RESULT=1)
		if [ $RESULT -eq 0 ]; then
			echo "pcp-exfat-utils.tcz" >> $ONBOOTLST
			echo '[ INFO ] exFat filesystem support loaded...</p>'
		else
			echo '[ ERROR ] Extensions not loaded, try again later!</p>'
		fi
	fi
}

pcp_remove_exfat() {
	echo '[ INFO ] Removing Extensions</p>'
	sudo -u tc tce-audit builddb
	sudo -u tc tce-audit delete pcp-exfat-utils.tcz
	sed -i '/pcp-exfat-utils.tcz/d' $ONBOOTLST
	echo '[ INFO ] Extensions are marked for removal. You must reboot to finish!</p>'
}

pcp_install_samba4() {
	RESULT=0
	echo '[ INFO ] Downloading Samba4...'
	sudo -u tc pcp-load -w samba4.tcz
	[ $? -eq 0 ] && echo -n . || (echo $?; RESULT=1)
	echo '<p>'
	if [ $RESULT -eq 0 ]; then
		sudo -u tc pcp-load -i samba4.tcz
		[ $? -eq 0 ] && echo -n . || (echo $?; RESULT=1)
		echo '<p>'
	fi
	if [ $RESULT -eq 0 ]; then
		echo "samba4.tcz" >> $ONBOOTLST
		echo '[ INFO ] Samba Support Loaded...</p>'
		cat << EOF > /usr/local/etc/init.d/samba
#!/bin/sh
NAME="Samba"
DESC="File Sharing"
CONF=/usr/local/etc/samba/smb.conf

startsmb(){
	grep -q "path" \$CONF
	if [ \$? -eq 0 ]; then
		echo "Starting SAMBA..."
		/usr/local/sbin/smbd
		/usr/local/sbin/nmbd
	else
		echo "Samba not Configured......exiting"
	fi
}

stopsmb(){
	echo -n "Stopping SAMBA"
	pkill nmbd
	pkill smbd
	CNT=0
	while [ \$CNT -lt 50 ]; do
		[ \$((CNT++)) ]
		PID=\$(pidof nmbd)
		[ -z "\$PID" ] && PID=\$(pidof smbd)
		[ -z "\$PID" ] && break
		sleep .1
		echo -n "."
	done
	echo "Stopped."
}

#Must Run as Root for ownership
if [ \$(/usr/bin/id -u) -ne 0 ]; then
	echo "Need to run as root." >&2
	exit 1
fi

case "\$1" in
	start)
		startsmb
	;;
	stop)
		stopsmb
	;;
	restart)
		echo "Restarting SAMBA..."
		stopsmb
		sleep 3
		startsmb
	;;
	status)
		PID=\$(pidof smbd)
		if [ -n "\$PID" ]; then
			echo "Samba Running"
			exit 0
		else
			echo "Samba Not Running"
			exit 1
		fi
	;;
	*)
		echo ""
		echo -e "Usage: /usr/local/etc/init.d/\$(basename \$0) [start|stop|restart|status]"
		echo ""
		exit 1
	;;
esac
exit 0
EOF
		chmod 755 /usr/local/etc/init.d/samba
		touch /usr/local/etc/samba/smb.conf
		echo "usr/local/etc/init.d/samba" >> /opt/.filetool.lst
		echo "usr/local/var/lib/samba" >> /opt/.filetool.lst
		echo "usr/local/etc/samba/smb.conf" >> /opt/.filetool.lst
		SAMBA="yes"
		pcp_save_to_config
		pcp_backup "nohtml"
	else
		echo '[ ERROR ] Samba4.tcz not loaded, try again later!</p>'
	fi
}

pcp_remove_samba4() {
	echo '[ INFO ] Removing Extensions</p>'
	sed -i '/samba4.tcz/d' $ONBOOTLST
	sudo -u tc tce-audit builddb
	sudo -u tc tce-audit delete samba4.tcz
	sed -i '/usr\/local\/etc\/init.d\/samba/d' /opt/.filetool.lst
	sed -i '/usr\/local\/var\/lib\/samba/d' /opt/.filetool.lst
	sed -i '/usr\/local\/etc\/samba\/smb.conf/d' /opt/.filetool.lst
	echo '[ INFO ] Extensions are marked for removal. You must reboot to finish!</p>'
}

pcp_samba_status() {
	if [ -f /usr/local/etc/init.d/samba ]; then
		/usr/local/etc/init.d/samba status 1>/dev/null
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
		pcp_table_top "Logitech Media Server (LMS)"
		echo '                <textarea class="inform" style="height:40px">'
		mount | grep -qs $MNT
		if [ "$?" = "0" ]; then
			if [ ! -x /usr/local/etc/init.d/slimserver ]; then
				echo '[ INFO ] Loading LMS extensions...'
				sudo -u tc tce-load -i slimserver.tcz
			fi
			echo '[ INFO ] Starting LMS...'
			echo -n '[ INFO ] '
			sudo /usr/local/etc/init.d/slimserver start
		else
			echo '[ ERROR ] LMS data disk not mounted at '$MNT', LMS will not start.'
		fi
		echo '                </textarea>'
		pcp_table_end
	;;
	Stop)
		pcp_table_top "Logitech Media Server (LMS)"
		echo '                <textarea class="inform" style="height:40px">'
		echo '[ INFO ] Stopping LMS...'
		echo -n '[ INFO ] '
		sudo /usr/local/etc/init.d/slimserver stop
		echo '                </textarea>'
		pcp_table_end
		sleep 2
	;;
	Restart)
		pcp_table_top "Logitech Media Server (LMS)"
		echo '                <textarea class="inform" style="height:40px">'
		echo '[ INFO ] Restarting LMS...'
		echo -n '[ INFO ] '
		sudo /usr/local/etc/init.d/slimserver stop
		echo -n '[ INFO ] '
		sudo /usr/local/etc/init.d/slimserver start
		echo '                </textarea>'
		pcp_table_end
	;;
	Install)
		pcp_table_top "Downloading Logitech Media Server (LMS)"
		pcp_sufficient_free_space 48000
		if [ $? -eq 0 ] ; then
			echo '                <textarea class="inform" style="height:160px">'
			pcp_install_lms
			if [ -f $TCEMNT/tce/optional/slimserver.tcz ]; then
				LMSERVER="yes"
				pcp_save_to_config
				pcp_backup "nohtml"
			else
				echo '[ ERROR ] Error Downloading LMS, please try again later.'
			fi
			echo '                </textarea>'
			pcp_table_end
		fi
	;;
	Remove)
		pcp_table_top "Removing Logitech Media Server (LMS)"
		echo '                <textarea class="inform" style="height:120px">'
		echo '[ INFO ] Removing LMS Extensions...'
		echo
		echo 'After a reboot these extensions will be permanently deleted:'
		LMSERVER="no"
		pcp_save_to_config
		pcp_remove_lms
		pcp_backup "nohtml"
		echo '                </textarea>'
		if [ x"$DISABLECACHE" = x ]; then
			STRING1='Press OK to remove LMS cache.......To keep the cache - Press Cancel'
			SCRIPT1='lms.cgi?ACTION=Remove_cache&REBOOT_REQUIRED=1'
			pcp_confirmation_required
		fi
		pcp_table_end
		REBOOT_REQUIRED=1
	;;
	Remove_cache)
		pcp_remove_lms_cache
	;;
	Rescan*)
		( echo "$(pcp_controls_mac_address) $RESCAN"; echo exit ) | nc 127.0.0.1 9090 > /dev/null
	;;
	Install_FS)
		pcp_table_top "Installing extra file system support"
		pcp_sufficient_free_space 4300
		if [ $? -eq 0 ] ; then
			echo '                <textarea class="inform" style="height:80px">'
			pcp_install_fs
			echo '                </textarea>'
			pcp_table_end
		fi
	;;
	Remove_FS)
		pcp_table_top "Removing extra file system support"
		echo '                <textarea class="inform" style="height:80px">'
		pcp_remove_fs
		echo '                </textarea>'
		pcp_table_end
		REBOOT_REQUIRED=1
	;;
	Install_EXFAT)
		pcp_table_top "Installing exFat file system support"
		pcp_sufficient_free_space 170
		if [ $? -eq 0 ] ; then
			echo '                <textarea class="inform" style="height:80px">'
			pcp_install_exfat
			echo '                </textarea>'
			pcp_table_end
		fi
	;;
	Remove_EXFAT)
		pcp_table_top "Removing exFat file system support"
		echo '                <textarea class="inform" style="height:80px">'
		pcp_remove_exfat
		echo '                </textarea>'
		pcp_table_end
		REBOOT_REQUIRED=1
	;;
	Install_Samba)
		pcp_table_top "Installing Samba4 Server"
		pcp_sufficient_free_space 25000
		if [ $? -eq 0 ] ; then
			echo '                <textarea class="inform" style="height:120px">'
			pcp_install_samba4
			echo '                </textarea>'
		fi
		pcp_table_end
	;;
	Remove_Samba)
		pcp_table_top "Removing Samba4 Server"
		echo '                <textarea class="inform" style="height:120px">'
		pcp_remove_samba4
		echo '                </textarea>'
		SAMBA="disabled"
		pcp_save_to_config
		pcp_backup "nohtml"
		pcp_table_end
		REBOOT_REQUIRED=1
	;;
	SambaStart)
		pcp_table_top "Starting Samba"
		pcp_textarea_inform "none" "/usr/local/etc/init.d/samba start" 40
		pcp_table_end
	;;
	SambaStop)
		pcp_table_top "Stopping Samba"
		pcp_textarea_inform "none" "/usr/local/etc/init.d/samba stop" 40
		pcp_table_end
	;;
	SambaRestart)
		pcp_table_top "Re-Starting Samba"
		pcp_textarea_inform "none" "/usr/local/etc/init.d/samba restart" 40
		pcp_table_end
	;;
	Mysb)
		pcp_table_top "Setting LMS commandline options"
		echo '                <textarea class="inform" style="height:40px">'
		echo '[ INFO ] Setting --nomysqueezebox commandline option...'
		case $NOMYSB in
			yes) pcp_lms_set_slimconfig OPTS "--nomysqueezebox" ADD;;
			no) pcp_lms_set_slimconfig OPTS "--nomysqueezebox" DEL;;
			*)pcp_warning_message;;
		esac
		[ -f $CFG_FILE ] && . $CFG_FILE
		echo '                </textarea>'
		pcp_table_end
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
[ "$?" = "0" ] && EXTRAFSYS="yes" || EXTRAFSYS="no"

#========================================================================================
# Main table
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Logitech Media Server (LMS) operations</legend>'

#------------------------------------LMS Indication--------------------------------------
if [ $(pcp_lms_status) -eq 0 ]; then
	INDICATOR=$HEAVY_CHECK_MARK
	CLASS="indicator_green"
	STATUS="running"
else
	INDICATOR=$HEAVY_BALLOT_X
	CLASS="indicator_red"
	STATUS="not running"
fi

#------------------------------------------------------------------------------------
# Determine state of check boxes.
#------------------------------------------------------------------------------------
# Function to check the LMS radio button according to config file
case "$LMSERVER" in
	yes) LMSERVERyes="checked" ;;
	no) LMSERVERno="checked" ;;
esac

# Function to check the Samba radio button according to config file
case "$SAMBA" in
	yes) SAMBAyes="checked" ;;
	*) SAMBAno="checked" ;;
esac

# Function to check the show log radio button according to selection
case "$LOGSHOW" in
	yes) LOGSHOWyes="checked" ;;
	*) LOGSHOWno="checked" ;;
esac

pcp_incr_id
pcp_start_row_shade
echo '          <table class="bggrey percent100">'
echo '            <tr class="'$ROWSHADE'">'
echo '              <td class="column150 center">'
echo '                <p class="'$CLASS'">'$INDICATOR'</p>'
echo '              </td>'
echo '              <td>'
echo '                <p>LMS is '$STATUS'&nbsp;&nbsp;'
echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                </p>'
echo '                <div id="'$ID'" class="less">'
echo '                  <ul>'
echo '                    <li><span class="indicator_green">&#x2714;</span> = LMS running.</li>'
echo '                    <li><span class="indicator_red">&#x2718;</span> = LMS not running.</li>'
echo '                  </ul>'
echo '                  <p><b>Note:</b></p>'
echo '                  <ul>'
echo '                    <li>LMS must be running to stream music to players from this pCP.</li>'
echo '                  </ul>'
echo '                </div>'
echo '              </td>'
echo '            </tr>'

#----------------------------------Padding-----------------------------------------------
pcp_toggle_row_shade
echo '            <tr class="padding '$ROWSHADE'">'
echo '              <td colspan=2></td>'
echo '            </tr>'
echo '          </table>'

#-----------------------------------Enable/disable autostart of LMS----------------------
pcp_lms_enable_lms() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '          <form name="Select" action="writetolms.cgi" method="get">'
	echo '            <table class="bggrey percent100">'
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                  <button type="submit" value="LMS autostart" '$DISABLE_LMS'>Set Autostart</button>'
	echo '                </td>'
	echo '                <td class="column100">'
	echo '                  <input type="hidden" name="ACTION" value="Startup">'
	echo '                  <input class="small1" type="radio" name="LMSERVER" value="yes" '$LMSERVERyes'>Yes'
	echo '                  <input class="small1" type="radio" name="LMSERVER" value="no" '$LMSERVERno'>No'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Automatic start of LMS when pCP boots&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Yes - will enable automatic start of LMS when pCP boots.</p>'
	echo '                    <p>No - will disable automatic start of LMS when pCP boots.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </table>'
	echo '          </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_lms_enable_lms
#----------------------------------------------------------------------------------------

#-----------------------------------Configure LMS----------------------------------------
pcp_lms_configure_lms() {

	[ x"" = x"$LMSWEBPORT" ] && LMSPORT=9000 || LMSPORT=$LMSWEBPORT
	[ x"" = x"$(pcp_eth0_ip)" ] && LMS_SERVER_WEB=$(pcp_wlan0_ip) || LMS_SERVER_WEB=$(pcp_eth0_ip)
	LMS_SERVER_WEB_URL="http://${LMS_SERVER_WEB}:${LMSPORT}"

	pcp_incr_id
	pcp_toggle_row_shade
	echo '          <form name="Configure" action="'$LMS_SERVER_WEB_URL'" target="_blank">'
	echo '            <table class="bggrey percent100">'
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" value="Configure LMS" '$DISABLE_LMS' />'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Configure LMS&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Use the standard LMS web interface to adjust the LMS settings.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </table>'
	echo '          </form>'
}
[ $MODE -ge $MODE_BETA ] && pcp_lms_configure_lms
#----------------------------------------------------------------------------------------

#-----------------------------------LMS Function Form------------------------------------
echo '          <form name="LMS" action="'$0'">'
echo '            <table class="bggrey percent100">'
#-----------------------------------Rescan LMS-------------------------------------------
pcp_rescan_lms() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="ACTION" value="Rescan LMS" />'
	echo '                </td>'
	echo '                <td class="column280">'
	echo '                  <select class="large32" name="RESCAN">'
	echo '                    <option value="rescan">Look for new and changed media files</option>'
	echo '                    <option value="wipecache">Clear library and rescan everything</option>'
	echo '                  </select>'
	echo '                </td>'
	echo '                <td colspan=2>'
	echo '                  <p>Rescan LMS library&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Rescan the local LMS library.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_rescan_lms
#----------------------------------------------------------------------------------------

#------------------------------------------Install/uninstall LMS-------------------------
pcp_lms_install_lms() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	if [ ! -f $TCEMNT/tce/optional/slimserver.tcz ]; then
		echo '                  <input type="submit" name="ACTION" value="Install" />'
		echo '                </td>'
		echo '                <td colspan=2>'
		echo '                  <p>Install LMS on pCP&nbsp;&nbsp;'
		echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
		echo '                  </p>'
		echo '                  <div id="'$ID'" class="less">'
		echo '                    <p>This will install LMS on pCP.</p>'
		echo '                  </div>'
	else
		echo '                  <input type="submit" name="ACTION" value="Remove" onclick="return confirm('\''This will remove LMS from pCP.\n\nAre you sure?'\'')"/>'
		echo '                </td>'
		echo '                <td colspan=2>'
		echo '                  <p>Remove LMS from pCP&nbsp;&nbsp;'
		echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
		echo '                  </p>'
		echo '                  <div id="'$ID'" class="less">'
		echo '                    <p>This will remove LMS and all the extra packages that was added with LMS.</p>'
		echo '                    <p>You will be promted in the process whether you want to remove or keep your LMS cache.</p>'
		echo '                  </div>'
	fi
	echo '                </td>'
	echo '              </tr>'
}
[ $MODE -ge $MODE_NORMAL ] && pcp_lms_install_lms
#----------------------------------------------------------------------------------------

#------------------------------------------Remove LMS cache-------------------------
pcp_lms_remove_cache() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                    <button type="submit" name="ACTION" value="Remove_cache" onclick="return confirm('\''This will remove all LMS Cache,settings and plugins.\n\nAre you sure?'\'')" '$DISABLECACHE'>Remove cache</button>'
	echo '                </td>'
	echo '                <td colspan=2>'
	echo '                  <p>Remove LMS Cache and Preferences from pCP&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>This will remove your the LMS cache and preferences from pCP.</p>'
	echo '                    <p>This includes all installed plugins and settings.</p>'
	echo '                  </div>'
	echo '                 </td>'
	echo '               </tr>'
}
[ $MODE -ge $MODE_NORMAL ] && pcp_lms_remove_cache
#----------------------------------------------------------------------------------------

#------------------------------------------Start LMS-------------------------------------
pcp_lms_start_lms() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="ACTION" value="Start" '$DISABLE_LMS' />'
	echo '                </td>'
	echo '                <td colspan=2>'
	echo '                  <p>Start LMS&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>This will start LMS.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
}
[ $MODE -ge $MODE_NORMAL ] && pcp_lms_start_lms
#----------------------------------------------------------------------------------------

#------------------------------------------Stop LMS--------------------------------------
pcp_lms_stop_lms() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="ACTION" value="Stop" '$DISABLE_LMS' />'
	echo '                </td>'
	echo '                <td colspan=2>'
	echo '                  <p>Stop LMS&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>This will stop LMS.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
}
[ $MODE -ge $MODE_NORMAL ] && pcp_lms_stop_lms
#----------------------------------------------------------------------------------------

#---------------------------------Restart LMS--------------------------------------------
pcp_lms_restart_lms() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="ACTION" value="Restart" '$DISABLE_LMS' />'
	echo '                </td>'
	echo '                <td colspan=2>'
	echo '                  <p>Restart LMS&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>This will stop LMS and then restart it.</p>'
	echo '                    <p><b>Note:</b></p>'
	echo '                    <ul>'
	echo '                      <li>A restart of LMS is rarely needed.</li>'
	echo '                      <li>LMS running indicator will turn green.</li>'
	echo '                    </ul>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
}
[ $MODE -ge $MODE_NORMAL ] && pcp_lms_restart_lms
#----------------------------------------------------------------------------------------

#-------------------------------nomysqueezebox-------------------------------------------
pcp_lms_no_mysb() {
	pcp_incr_id
	pcp_toggle_row_shade
	case $OPTIONS in
		*--nomysqueezebox*) NOMYSByes="checked";;
		*) NOMYSBno="checked";;
	esac
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                  <button type="submit" name="ACTION" value="Mysb" '$DISABLE_LMS'>No MySB</button>'
	echo '                </td>'
	echo '                <td class="column100">'
	echo '                  <input class="small1" type="radio" name="NOMYSB" value="yes" '$NOMYSByes' >Yes'
	echo '                  <input class="small1" type="radio" name="NOMYSB" value="no" '$NOMYSBno' >No'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Set --nomysqueezebox commandline option for LMS.&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>If enabled, this tells LMS to not use any mysqueezebox integrations.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
}
[ $MODE -ge $MODE_NORMAL ] && pcp_lms_no_mysb
#----------------------------------------------------------------------------------------

#-------------------------------Show LMS logs--------------------------------------------
pcp_lms_show_logs() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" value="Show Logs" '$DISABLE_LMS'/>'
	echo '                </td>'
	echo '                <td class="column100">'
	echo '                  <input class="small1" type="radio" name="LOGSHOW" value="yes" '$LOGSHOWyes' >Yes'
	echo '                  <input class="small1" type="radio" name="LOGSHOW" value="no" '$LOGSHOWno' >No'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Show LMS logs&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Show Server and Scanner log in text area below.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
}
[ $MODE -ge $MODE_NORMAL ] && pcp_lms_show_logs
#----------------------------------------------------------------------------------------
echo '            </table>'
echo '          </form>'

#---------------------------------Update LMS--------------------------------------------
pcp_update_lms() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '          <form name="Update" action="lms-update.cgi">'
	echo '            <table class="bggrey percent100">'
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" value="LMS Update" '$DISABLE_LMS'>'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Download and update LMS&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>The update process will take some minutes and finally LMS will restart.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </table>'
	echo '          </form>'
}
[ $MODE -ge $MODE_NORMAL ] && pcp_update_lms
#----------------------------------------------------------------------------------------
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------

#========================================================================================
# Slimserver Cache and Prefs to Mounted Drive
#----------------------------------------------------------------------------------------
pcp_slimserver_persistence() {
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Save LMS Server Cache and Preferences to Mounted Drive</legend>'
	echo '          <form name="Mount" action="writetomount.cgi" method="get">'
	echo '            <table class="bggrey percent100">'
	pcp_incr_id
	pcp_start_row_shade
	COL1="75"
	COL2="150"
	COL3="210"
	COL4="380"
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column'$COL1' center"><p><b>Enabled</b></p></td>'
	echo '                <td class="column'$COL2'"><p><b>Mount Type</b></p></td>'
	echo '                <td class="column'$COL3'"><p><b>LMS Data Storage Location</b></p></td>'
	echo '                <td class="column'$COL4'">'
	echo '                    <p>This is the Location where LMS will save Data&nbsp;&nbsp;'
	echo '                      <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                    </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Including Music Database, Artwork Cache.</p>'
	echo '                    <p>and System Preferences</p>'
	echo '                  </div>'
	echo '              </tr>'
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
			pcp_toggle_row_shade
			echo '              <tr class="'$ROWSHADE'">'
			echo '                <td class="column'$COL1' center">'
			echo '                  <input class="small1" type="radio" name="LMSDATA" value="'$USBmnt'" '$USByes'>'
			echo '                </td>'
			echo '                <td class="column'$COL2'">'
			case $I in
				/dev/sd*) echo '                  <p>USB Disk</p>';;
				/dev/mmcblk0p*) echo '                  <p>microSD Card</p>';;
			esac
			echo '                </td>'
			echo '                <td class="column'$COL3'">'
			echo '                  <p>'${USBMOUNT}'/slimserver</p>'
			echo '                </td>'
			if [ -d ${USBMOUNT}/slimserver/Cache ]; then
				echo '                <td class="column'$COL4'">'
				echo '                  <p>There is a Cache folder found on this drive</p>'
				echo '                </td>'
			else
				echo '                <td></td>'
			fi
			echo '              </tr>'
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
		pcp_toggle_row_shade
		echo '              <tr class="'$ROWSHADE'">'
		echo '                <td class="column'$COL1' center">'
		echo '                  <input class="small1" type="radio" name="LMSDATA" value="'$NETmnt'" '$NETyes'>'
		echo '                </td>'
		echo '                <td class="column'$COL2'">'
		echo '                  <p>Network Disk</p>'
		echo '                </td>'
		echo '                <td class="column'$COL3'">'
		echo '                  <p>'${NETMOUNT}'/slimserver</p>'
		echo '                </td>'
		if [ -d ${NETMOUNT}/slimserver/Cache ]; then
			echo '                <td class="column'$COL4'">'
			echo '                  <p>There is a Cache folder found on this drive</p>'
			echo '                </td>'
		else
			echo '                <td></td>'
		fi
		echo '              </tr>'
	done

	case "${LMSDATA:0:4}" in
		usb:|net:)
			if [ $LMSMNTFOUND -eq 0 ]; then
				[ -f /home/tc/.slimserver.cfg ] && . /home/tc/.slimserver.cfg
				pcp_toggle_row_shade
				echo '              <tr class="'$ROWSHADE'">'
				echo '                <td class="column'$COL1' center">'
				echo '                  <input class="small1" type="radio" name="LMSDATA" value="'${LMSDATA}'" checked disabled>'
				echo '                </td>'
				echo '                <td class="column'$COL2'">'
				echo '                  <p>'$(echo ${LMSDATA:0:3} | tr [a-z] [A-Z])' Disk</p>'
				echo '                </td>'
				echo '                <td colspan="2">'
				TMP=$(echo $CACHE | awk -F"/" '{$2="/"$2"/"; print $2$3}')
				echo '                  <p>'$(echo ${LMSDATA:0:3} | tr [a-z] [A-Z])' Disk '${LMSDATA:4}' Not Mounted on '$TMP', LMS will not start</p>'
				echo '                </td>'
				echo '              </tr>'
			fi
		;;
		*);;
	esac
	
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column'$COL1' center">'
	echo '                  <input class="small1" type="radio" name="LMSDATA" value="default" '$DEFyes'>'
	echo '                </td>'
	echo '                <td class="column'$COL2'">'
	echo '                  <p>pCP Boot Disk</p>'
	echo '                </td>'
	echo '                <td class="column'$COL3'">'
	echo '                  <p>'$TCEMNT'/tce/slimserver</p>'
	echo '                </td>'
	if [ -d $TCEMNT/tce/slimserver/Cache ]; then
		echo '                <td class="column'$COL4'">'
		echo '                  <p>There is a Cache folder found on this drive</p>'
		echo '                </td>'
	else
		echo '                <td></td>'
	fi
	echo '              </tr>'

#--------------------------------------Submit button-------------------------------------
	pcp_incr_id
	pcp_toggle_row_shade
	echo '                <tr class="'$ROWSHADE'">'
	echo '                  <td  class="column150 center">'
	echo '                    <input type="hidden" name="MOUNTTYPE" value="slimconfig">'
	echo '                    <button type="submit" name="ACTION" value="Set">Set LMS Data</button>'
	echo '                  </td>'
	echo '                  <td  class="column210">'
	echo '                    <p>Set the Data Location Only.</p>'
	echo '                  </td>'
	echo '                  <td  class="column150 center">'
	echo '                    <button type="submit" name="ACTION" value="Move">Move LMS Data</button>'
	echo '                  </td>'
	echo '                  <td  class="column380">'
	echo '                    <p>Set the Data Location and Move Cache to that location</p>'
	echo '                  </td>'
	echo '                </tr>'
#----------------------------------------------------------------------------------------
	echo '            </table>'
	echo '          </form>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_slimserver_persistence

#========================================================================================
# Extra File System Support
#----------------------------------------------------------------------------------------
pcp_extra_filesys() {
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Install and Enable additional FileSystems</legend>'
	echo '          <form name="Start" action="'$0'" method="get">'
	echo '            <table class="bggrey percent100">'
	pcp_incr_id
	pcp_start_row_shade
	DISABLE_REMOVEFS="0"
	DISABLE_REMOVEEXFAT="0"
	for I in `mount | awk '{print $5}'`; do
		case "$I" in
			fat*|vfat|*squash*|proc|tmpfs|sysfs|devpts|ext*) ;;
			exfat|fuseblk) DISABLE_REMOVEEXFAT="1";;
			*) DISABLE_REMOVEFS="1" ;;
		esac
	done
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	if [ "$EXTRAFSYS" = "no" ]; then
		echo '                    <button type="submit" name="ACTION" value="Install_FS">Install</button>'
		echo '                  </td>'
		echo '                  <td>'
		echo '                    <p>Install additional Filesystems for pCP&nbsp;&nbsp;'
		echo '                      <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
		echo '                    </p>'
		echo '                  <div id="'$ID'" class="less">'
		echo '                    <p>This will install Filesystem support for pCP.</p>'
		echo '                    <p>FAT/vFAT/FAT32 ext2/3/4 are builtin to pCP by default</p>'
		echo '                    <p>These extra filesystems include network and ntfs filesystems.</p>'
		echo '                  </div>'
	elif [ "$DISABLE_REMOVEFS" = "0" ]; then
		echo '                  <button type="submit" name="ACTION" value="Remove_FS">Remove</button>'
		echo '                </td>'
		echo '                <td>'
		echo '                  <p>Remove additional Filesystems from pCP&nbsp;&nbsp;'
		echo '                     <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
		echo '                  </p>'
		echo '                  <div id="'$ID'" class="less">'
		echo '                    <p>This will remove all but the default Filesystem Support from pCP.</p>'
		echo '                    <p>FAT/vFAT/FAT32 ext2/3/4 are builtin to pCP by default</p>'
		echo '                  </div>'
	else
		echo '                  <button type="submit" name="ACTION" value="Remove_FS" Disabled>Remove</button>'
		echo '                </td>'
		echo '                <td>'
		echo '                  <p>Additional Filesystems are in Use&nbsp;&nbsp;'
		echo '                     <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
		echo '                  </p>'
		echo '                  <div id="'$ID'" class="less">'
		echo '                    <p>Unable to remove additional Filesystem Support from pCP.</p>'
		echo '                    <p>as there are currently active drives mounted using this support.</p>'
		echo '                  </div>'
	fi
	echo '                </td>'
	echo '              </tr>'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	if [ "$EXTRAFSYS" = "yes" ]; then
		pcp_incr_id
		pcp_toggle_row_shade
		[ -x /usr/local/sbin/mount.exfat ] && EXFATFS="yes" || EXFATFS="no"
		if [ "$EXFATFS" = "no" ]; then
			echo '                    <button type="submit" name="ACTION" value="Install_EXFAT">Install exFat</button>'
			echo '                  </td>'
			echo '                  <td>'
			echo '                    <p>Install exFat filesystem for pCP&nbsp;&nbsp;'
			echo '                      <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
			echo '                    </p>'
			echo '                  <div id="'$ID'" class="less">'
			echo '                    <p>This will install Filesystem support for pCP.</p>'
			echo '                    <p>FAT/vFAT/FAT32 ext2/3/4 are builtin to pCP by default</p>'
			echo '                    <p>This is only for exFat Support.</p>'
			echo '                  </div>'
		elif [ "$DISABLE_REMOVEEXFAT" = "0" ]; then
			echo '                  <button type="submit" name="ACTION" value="Remove_EXFAT">Remove exFat</button>'
			echo '                </td>'
			echo '                <td>'
			echo '                  <p>Remove additional Filesystems from pCP&nbsp;&nbsp;'
			echo '                     <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
			echo '                  </p>'
			echo '                  <div id="'$ID'" class="less">'
			echo '                    <p>This will remove exFat Support from pCP.</p>'
			echo '                    <p>FAT/vFAT/FAT32 ext2/3/4 are builtin to pCP by default</p>'
			echo '                  </div>'
		else
			echo '                  <button type="submit" name="ACTION" value="Remove_EXFAT" Disabled>Remove exFat</button>'
			echo '                </td>'
			echo '                <td>'
			echo '                  <p>exFat Filesystems are in Use&nbsp;&nbsp;'
			echo '                     <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
			echo '                  </p>'
			echo '                  <div id="'$ID'" class="less">'
			echo '                    <p>Unable to remove exFat Filesystem Support from pCP.</p>'
			echo '                    <p>as there are currently active drives mounted using this support.</p>'
			echo '                  </div>'
		fi
	fi
	echo '                </td>'
	echo '              </tr>'
	echo '            </table>'
	echo '          </form>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_extra_filesys
#----------------------------------------------------------------------------------------

#========================================================================================
# USB Disk Mounting Operations
#----------------------------------------------------------------------------------------
pcp_mount_usbdrives() {
	#Used to identify which fdisk, fdisk -V fails under busybox, but not util-linux.
	fdisk -V 2>&1 | grep -q -i busybox
	[ $? -eq 0 ] && BBFDISK=1 || BBFDISK=0
	# Read config file
	NUM_USB_CONF=0
	NUM_USB_CONF_ENABLED=0
	if [ -f  ${USBMOUNTCONF} ]; then
		while read LINE; do
			case $LINE in
				[*)	NUM_USB_CONF=$((NUM_USB_CONF+1))
					# Assume disk is not plugged in, then enable in section below.
					eval DISKFOUND${NUM_USB_CONF}="no"
				;;
				*USBDISK*)
					eval USBDISK${NUM_USB_CONF}=$(pcp_trimval "${LINE}")
					[ $(eval echo \${USBDISK${NUM_USB_CONF}}) = "enabled" ] && $((NUM_USB_CONF_ENABLED+1))
				;;
				*POINT*) eval MOUNTPOINT${NUM_USB_CONF}=$(pcp_trimval "${LINE}");;
				*UUID*) eval MOUNTUUID${NUM_USB_CONF}=$(pcp_trimval "${LINE}");;
				*);;
			esac
		done < $USBMOUNTCONF
	fi
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Pick from the following detected USB disks to mount</legend>'
	echo '          <form name="Mount" action="writetomount.cgi" method="get">'
	echo '            <table class="bggrey percent100">'
	pcp_incr_id
	pcp_start_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td>'
	echo '                  <p>Mount USB Disk&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>If Checked, the USB disk will be mounted by to the mount point and will be automounted on startup.</p>'
	echo '                    <p>&#60;Mount Point&#62; the name of the mount point for the drive. Alpha-numeric pathnames required (up to 32 characters).</p>'
	echo '                    <p>&nbsp;&nbsp;&nbsp;Do not use hardware device names like sda1 or mmcblk0.</p>'
	echo '                    <p>All other fields are for identification purposes.</p>'
	echo '                    <br />'
	echo '                    <p>GPT Partitioned disks require the additional util-linux.tcz extension.</p>'
	echo '                    <p>UTF-8 Support for fat32 requires the additional filesystem extensions.</p>'
	
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </table>'
	echo '            <table class="bggrey percent100">'
	COL1="75"
	COL2="150"
	COL3="120"
	COL4="100"
	COL5="75"
	COL6="300"
	COL7="75"
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column'$COL1' center"><p><b>Enabled</b></p></td>'
	echo '                <td class="column'$COL2'"><p><b>Mount Point</b></p></td>'
	echo '                <td class="column'$COL3'"><p><b>Device</b></p></td>'
	echo '                <td class="column'$COL4'"><p><b>Label</b></p></td>'
	echo '                <td class="column'$COL5'"><p><b>FS Type</b></p></td>'
	echo '                <td class="column'$COL6'"><p><b>UUID</b></p></td>'
	echo '                <td class="column'$COL7'"><p><b>Size</b></p></td>'
	echo '              </tr>'

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
				SIZE=$(fdisk -l | grep $I | sed "s/*//" | tr -s " " | cut -d " " -f7 | tr -d + )
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
					*)  USBDISKyes=""
						PNT=""
						REQUIRED=""
					;;
				esac
			J=$((J+1))
			done
			pcp_toggle_row_shade
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
				*)	if [ "$EXTRAFSYS" = "no" ]; then
						DISABLE="Disabled"
						UUID="Please install extra Filesystems"
					else
						DISABLE=""
					fi
				;;
			esac

			#Keepenabled is due to sumitting a disabled checkbox does not submit current value
			if [ "${LMSDATA:4}" = "$UUID" ]; then
				DISABLE="disabled"
				KEEPENABLED="USBDISK${NUM_USB_ATTACHED}"
			fi
			echo '                <tr class="'$ROWSHADE'">'
			echo '                  <td class="column'$COL1' center">'
			echo '                    <input class="small1" type="checkbox" id="USB'${NUM_USB_ATTACHED}'" name="USBDISK'${NUM_USB_ATTACHED}'" value="enabled" onchange="setrequired('${NUM_USB_ATTACHED}')" '$USBDISKyes' '$DISABLE'>'
			echo '                    <input type="hidden" name="MOUNTUUID'${NUM_USB_ATTACHED}'" value="'$UUID'">'
			echo '                  </td>'
			echo '                  <td class="column'$COL2'">'
			echo '                    <p>/mnt/ <input class="large6" type="text" id="USBPOINT'${NUM_USB_ATTACHED}'" name="MOUNTPOINT'${NUM_USB_ATTACHED}'" value="'$PNT'" '$REQUIRED' pattern="(?!sd)(?!mmcblk)^[a-zA-Z0-9_]{1,32}$"><p>'
			echo '                  </td>'
			echo '                  <td class="column'$COL3'">'
			echo '                    <p>'$PART'</p>'
			echo '                  </td>'
			echo '                  <td class="column'$COL4'">'
			echo '                    <p>'$LBL'</p>'
			echo '                  </td>'
			echo '                  <td class="column'$COL5'">'
			echo '                    <p>'$PTTYPE'</p>'
			echo '                  </td>'
			echo '                  <td class="column'$COL6'">'
			echo '                    <p>'$UUID'</p>'
			echo '                  </td>'
			echo '                  <td class="column'$COL7'">'
			echo '                    <p>'$SIZExB'</p>'
			echo '                  </td>'
			echo '                </tr>'
		fi
	done

	fdisk -l | grep -q "Found valid GPT"
	if [ $? -eq 0 ]; then
		pcp_toggle_row_shade
		echo '              <tr class="'$ROWSHADE'">'
		echo '                <td class="column'$COL1' center">'
		echo '                </td>'
		echo '                <td colspan="4">'
		echo '                  <p>Disk with GPT partition table Found! Install extension "util-linux.tcz" for compatability</p>'
		echo '                </td>'
		echo '                <td  class="column150 center">'
		echo '                  <button type="submit" name="ACTION" value="gptfdisk">Install Support</button>'
		echo '                </td>'
		echo '              </tr>'
	fi
	J=1
	while [ $J -le $NUM_USB_CONF ]
	do
		if [ $(eval echo \${USBDISK${J}}) = "enabled" ]; then
			UUID=$(eval echo "\${MOUNTUUID${J}}")
			TST=$(eval echo "\${DISKFOUND${J}}")
			PNT=$(eval echo "\${MOUNTPOINT${J}}")
			if [ "$TST" = "no" ]; then
				#Drive is actually not attached, but we needed it to be.
				NUM_USB_ATTACHED=$((NUM_USB_ATTACHED+1))
				pcp_toggle_row_shade
				echo '              <tr class="'$ROWSHADE'">'
				echo '                  <td class="column'$COL1' center">'
				echo '                    <input class="small1" type="checkbox" id="USB'${NUM_USB_ATTACHED}'" name="USBDISK'${NUM_USB_ATTACHED}'" value="enabled" checked>'
				echo '                    <input type="hidden" name="MOUNTUUID'${NUM_USB_ATTACHED}'" value="'$UUID'">'
				echo '                    <input type="hidden" name="MOUNTPOINT'${NUM_USB_ATTACHED}'" value="'$PNT'">'
				echo '                  </td>'
				echo '                  <td colspan="5">'
				echo '                    <p>Previously selected disk '$UUID' not Found. Please insert and reboot system, or uncheck to disable disk.</p>'
				echo '                  </td>'
				echo '                </tr>'
			fi
		fi
	J=$((J+1))
	done
#--------------------------------------Submit button-------------------------------------
	pcp_incr_id
	pcp_toggle_row_shade
	echo '                <tr class="'$ROWSHADE'">'
	echo '                  <td class="column150 center">'
	echo '                    <input type="hidden" name="MOUNTTYPE" value="localdisk">'
	echo '                    <input type="hidden" name="NUMDRIVES" value="'$NUM_USB_ATTACHED'">'
	echo '                    <button type="submit" name="ACTION" value="Save">Set USB Mount</button>'
	echo '                  </td>'
	echo '                  <td class="column150 center">'
	echo '                    <button type="submit" name="ACTION" value="Permissions" onclick="return confirm('\''This will set user ownership and write permissions to user tc on all mounted USB disks.\n\nAre you sure?'\'')">Set Write Permissions</button>'
	echo '                  </td>'
	case $LMSDATA in
		usb*)
			# Checkbox is disabled due to lms using for cache storage, Keep the specific box enabled
			echo '                  <input type="hidden" name="'$KEEPENABLED'" value="enabled">'
			echo '                  <td colspan=5>'
			echo '                    <p> LMS is currently using disk '${LMSDATA:4}' for Data.&nbsp;&nbsp;'
			echo '                      <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
			echo '                    </p>'
			echo '                    <div id="'$ID'" class="less">'
			echo '                      <p>Must Move LMS Data to another disk (SDcard or Network Share).</p>'
			echo '                      <p>in order to change this mount.</p>'
			echo '                    </div>'
			echo '                  </td>'
		;;
		*)
			echo '                  <td colspan=5>'
			if [ "$EXTRAFSYS" = "no" ]; then
				echo '                    <p> For UTF-8 support on FAT formatted drives, please install extra filesystems above.</p>'
			fi
			echo '                  </td>'

		;;
	esac
	echo '                </tr>'
	echo '            </table>'
	echo '          </form>'
	echo '          <script>'
	echo '            function setrequired(id) {'
	echo '              var box = "USB";'
	echo '              var Box = box.concat(id);'
	echo '              var box1 = "USBPOINT";'
	echo '              var Box1 = box1.concat(id);'
	echo '              if (document.getElementById(Box).checked){'
	echo '                document.getElementById(Box1).setAttribute("required", "");'
	echo '              }'
	echo '              else {'
	echo '                document.getElementById(Box1).required = false;'
	echo '              }'
	echo '            }'
	echo '          </script>'
#----------------------------------------------------------------------------------------
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_mount_usbdrives

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
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	if [ "$EXTRAFSYS" = "no" ]; then
		echo '        <fieldset disabled="disabled">'
	else
		echo '        <fieldset>'
	fi
	echo '          <legend>Setup Network Disk Mount</legend>'
	echo '          <form name="Mount" action="writetomount.cgi" method="get">'
	echo '            <table class="bggrey percent100">'
	pcp_incr_id
	pcp_start_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td>'
	echo '                  <p>Mount Remote Network Share&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Field usage.</p>'
	echo '                    <ul>'
	echo '                      <li>If Enabled is checked, the network share will be mounted by to the mount point and will be automounted on startup.</li>'
	echo '                      <li>&#60;Mount Point&#62; the name of the mount point for the drive. Alpha-numeric pathnames required (up to 32 characters).'
	echo '                        <ul>'
	echo '                          <li>Do not use hardware device names like sda1 or mmcblk0.</li>'
	echo '                        </ul>'
	echo '                      </li>'
	echo '                      <li>&#60;Server IP address&#62; is only the IP address.  Do not enter any / or :</li>'
	echo '                      <li>&#60;Server Share&#62; for CIFS is the share name only (DO not use /).</li>'
	echo '                      <li>&#60;Server Share&#62; for NFS is the complete volume i.e. /volume1/Media (DO not use :).</li>'
	echo '                      <li>&#60;Username&#62; Username if needed for cifs mount.</li>'
	echo '                      <li>&#60;Password&#62; Password if needed for cifs mount.</li>'
	echo '                      <li>&#60;Options&#62; are a comma delimited list of mount options. Ref mount man pages.'
	echo '                        <ul>'
	echo '                          <li>vers=3.0 - The linux kernel now defaults to SMB and NFS version 3.0, lower versions must be specified.</li>'
	echo '                          <li>uid=1001 - mounts the drive with user &quot;tc&quot;.  Useful if using ssh sessions to write data to share.</li>'
	echo '                          <li>gid=50 - mounts the drive with group &quot;staff&quot;.  Useful if using ssh sessions to write data to share.</li>'
	echo '                        </ul>'
	echo '                      </li>'
	echo '                    </ul>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </table>'
	echo '            <table class="bggrey percent100">'
	COL1="75"
	COL2="150"
	COL3="120"
	COL4="100"
	COL5="100"
	COL6="100"
	COL7="100"
	COL8="150"
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column'$COL1' center"><p><b>Enabled</b></p></td>'
	echo '                <td class="column'$COL2'"><p><b>Mount Point</b></p></td>'
	echo '                <td class="column'$COL3'"><p><b>IP Address</b></p></td>'
	echo '                <td class="column'$COL4'"><p><b>Share Name</b></p></td>'
	echo '                <td class="column'$COL5'"><p><b>Share Type</b></p></td>'
	echo '                <td class="column'$COL6'"><p><b>Username</b></p></td>'
	echo '                <td class="column'$COL7'"><p><b>Password</b></p></td>'
	echo '                <td class="column'$COL8'"><p><b>Options</b></p></td>'
	echo '              </tr>'

	I=1
	NUM_NET_CONF=$((NUM_NET_CONF+1))  # Adds a blank line to the form fields
	while [ $I -le $NUM_NET_CONF ]; do
		TST=$(eval echo \${NETENABLE${I}})
		case "$TST" in
			yes|no)
				[ "$TST" = "yes" ] && NETENABLEyes="checked" || NETENABLEyes=""
				REQUIRED="required"
				PNT=$(eval echo \${NETMOUNTPOINT${I}})
				IP=$(eval echo \${NETMOUNTIP${I}})
				SHARE=$(eval echo \${NETMOUNTSHARE${I}})
				FSTYPE=$(eval echo \${NETMOUNTFSTYPE${I}})
				USER=$(eval echo \${NETMOUNTUSER${I}})
				PASS=$(eval echo \${NETMOUNTPASS${I}})
				OPTIONS=$(eval echo \${NETMOUNTOPTIONS${I}})
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
		pcp_toggle_row_shade
		echo '              <tr class="'$ROWSHADE'">'
		echo '                <td class="column'$COL1' center">'
		echo '                  <input class="small1" type="checkbox" id="NET'${I}'" name="NETENABLE'${I}'" value="yes" onchange="setnetrequired('${I}')" '$NETENABLEyes' '$DISABLE'>'
		echo '                </td>'
		echo '                <td class="column'$COL2'">'
		echo '                  <p>/mnt/<input class="large6" type="text" id="NETPOINT'${I}'" name="NETMOUNTPOINT'${I}'" value="'$PNT'" '$REQUIRED' pattern="(?!sd)(?!mmcblk)^[a-zA-Z0-9_]{1,32}$"><p>'
		echo '                </td>'
		echo '                <td class="column'$COL3'">'
		echo '                  <input class="large8" type="text" id="NETIP'${I}'" name="NETMOUNTIP'${I}'" value="'$IP'" title="Enter the IP Address of the Remote Server" '$REQUIRED' pattern="((^|\.)((25[0-5])|(2[0-4]\d)|(1\d\d)|([1-9]?\d))){4}$">'
		echo '                </td>'
		echo '                <td class="column'$COL4'">'
		echo '                  <input class="large6" type="text" id="NETSHARE'${I}'" name="NETMOUNTSHARE'${I}'" value="'$SHARE'" title="Enter the Name of the Share&#13;Do not enter / or :" '$REQUIRED' pattern="^[a-zA-Z0-9_\-\ ]{1,32}$">'
		echo '                </td>'
		echo '                <td class="column'$COL5'">'

	case "$FSTYPE" in
			cifs) CIFS1yes="selected"; USERdisable="";;
			nfs) NFS1yes="selected"; USERdisable="Disabled" ;;
		esac

		echo '                  <select class="large6" id="NETFS'${I}'" name="NETMOUNTFSTYPE'${I}'" title="Only cifs(samba) and nfs shares are supported" onchange="setfstype('${I}')">'
		echo '                    <option value="cifs" '$CIFS1yes'>CIFS</option>'
		echo '                    <option value="nfs" '$NFS1yes'>NFS</option>'
		echo '                  </select>'
		echo '                </td>'
		echo '                <td class="column'$COL6'">'
		echo '                  <input class="large6" type="text" id="NETUSER'${I}'" name="NETMOUNTUSER'${I}'" value="'$USER'" title="Enter the Username for the remote share.&#13;Not used with NFS" '$USERdisable'>'
		echo '                </td>'
		echo '                <td class="column'$COL7'">'
		echo '                  <input class="large6" type="text" id="NETPASS'${I}'" name="NETMOUNTPASS'${I}'" value="'$PASS'" title="Enter the Password for the remote share.&#13;Not used with NFS" '$USERdisable'>'
		echo '                </td>'
		echo '                <td class="column'$COL8'">'
		echo '                  <input class="large10" type="text" id="NETOPTS'${I}'" name="NETMOUNTOPTIONS'${I}'" value="'$OPTIONS'" title="Enter any comma delimeted mount option&#13;i.e. uid=1001,gid=50,vers=2.0" >'
		echo '                </td>'
		echo '              </tr>'
		echo '              <script>'
		echo '                var share = "'${SHARE}'";'
		echo '                ShareBox = "NETSHARE'${I}'";'
		echo '                document.getElementById(ShareBox).value = decodeURIComponent(share.replace(/\+/g, "%20"));'
		echo '              </script>'
		I=$((I+1))
	done
	echo '                <script>'
	echo '                  function setnetrequired(id) {'
	echo '                    var box = "NET";'
	echo '                    var Box = box.concat(id);'
	echo '                    var box1 = "NETPOINT";'
	echo '                    var Box1 = box1.concat(id);'
	echo '                    var box2 = "NETIP";'
	echo '                    var Box2 = box2.concat(id);'
	echo '                    var box3 = "NETSHARE";'
	echo '                    var Box3 = box3.concat(id);'
	echo '                    if (document.getElementById(Box).checked){'
	echo '                      document.getElementById(Box1).setAttribute("required", "");'
	echo '                      document.getElementById(Box2).setAttribute("required", "");'
	echo '                      document.getElementById(Box3).setAttribute("required", "");'
	echo '                      setcifsopts(id);'
	echo '                    }'
	echo '                    else {'
	echo '                      document.getElementById(Box1).required = false;'
	echo '                      document.getElementById(Box2).required = false;'
	echo '                      document.getElementById(Box3).required = false;'
	echo '                    }'
	echo '                  }'
	echo '                  function setcifsopts(id) {'
	echo '                    var box = "NET";'
	echo '                    var Box = box.concat(id);'
	echo '                    var box4 = "NETOPTS";'
	echo '                    var Box4 = box4.concat(id);'
	echo '                    var box5 = "NETFS";'
	echo '                    var Box5 = box5.concat(id);'
	echo '                    if (document.getElementById(Box).checked && (document.getElementById(Box5).value == "cifs")){'
	echo '                      var x = document.getElementById(Box4).value;'
	echo '                      x = ( x.length > 0 ) ? x.concat(",") : x;'
	echo '                      x = ( x.indexOf("uid=") != -1 ) ? x : x.concat("uid=1001");'
	echo '                      x = ( x.indexOf("gid=") != -1 ) ? x : x.concat(",gid=50");'
	echo '                      x = ( x.substr(x.length - 1) == ",") ? x.substring(0, x.length - 1) : x;'
	echo '                      document.getElementById(Box4).value = x;'
	echo '                    }'
	echo '                  }'
	echo '                  function setfstype(id) {'
	echo '                    var box = "NETFS";'
	echo '                    var Box = box.concat(id);'
	echo '                    var box1 = "NETUSER";'
	echo '                    var Box1 = box1.concat(id);'
	echo '                    var box2 = "NETPASS";'
	echo '                    var Box2 = box2.concat(id);'
	echo '                    if (document.getElementById(Box).value == "nfs" ){'
	echo '                      document.getElementById(Box1).setAttribute("disabled", "");'
	echo '                      document.getElementById(Box2).setAttribute("disabled", "");'
	echo '                    }'
	echo '                    else {'
	echo '                      document.getElementById(Box1).disabled = false;'
	echo '                      document.getElementById(Box2).disabled = false;'
	echo '                      setcifsopts(id);'
	echo '                    }'
	echo '                  }'
	echo '                </script>'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column'$COL1' center">'
	echo '                  <input class="small1" type="checkbox" name="CLEARUNUSED" value="yes">'
	echo '                </td>'
	echo '                <td colspan=7>'
	echo '                  <p> Check this box to clear configuration data for unused shares.</p>'
	echo '                </td>'
	echo '              </tr>'
	#--------------------------------------Submit button-------------------------------------
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	if [ "$EXTRAFSYS" = "no" ]; then
		echo '                <td class="column150 center">'
		echo '                  <button type="submit" name="ACTION" value="Save" Disabled>Set NET Mount</button>'
		echo '                </td>'
		echo '                <td colspan=7>'
		echo '                  <p>Mounting network drives requires extra filesystem support.&nbsp;&nbsp;'
		echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
		echo '                  </p>'
		echo '                  <div id="'$ID'" class="less">'
		echo '                    <p>Please add additional filesystems using the option above.</p>'
		echo '                  </div>'
	elif [ "${LMSDATA:0:4}" = "net:" ]; then
		echo '                <td class="column150 center">'
		echo '                  <input type="hidden" name="'$KEEPENABLED'" value="yes">'
		echo '                  <input type="hidden" name="MOUNTTYPE" value="networkshare">'
		echo '                  <input type="hidden" name="NUMNET" value="'$NUM_NET_CONF'">'
		echo '                  <button type="submit" name="ACTION" value="Save">Set NET Mount</button>'
		echo '                </td>'
		echo '                <td colspan=7>'
		echo '                  <p> LMS is currently using network drive '${LMSDATA:4}' for Data.&nbsp;&nbsp;'
		echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
		echo '                  </p>'
		echo '                  <div id="'$ID'" class="less">'
		echo '                    <p>Must Move LMS Data to another disk (SDcard or USB Disk).</p>'
		echo '                    <p>in order to change this mount.</p>'
		echo '                  </div>'
	else
		echo '                <td class="column150 center" colspan=8>'
		echo '                  <input type="hidden" name="MOUNTTYPE" value="networkshare">'
		echo '                  <input type="hidden" name="NUMNET" value="'$NUM_NET_CONF'">'
		echo '                  <button type="submit" name="ACTION" value="Save">Set NET Mount</button>'
	fi
	echo '                </td>'
	echo '              </tr>'
#----------------------------------------------------------------------------------------
	echo '            </table>'
	echo '          </form>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_mount_netdrives
#----------------------------------------------------------------------------------------
#========================================================================================
# Samba Share Drive Support
#----------------------------------------------------------------------------------------
pcp_samba() {
#------------------------------------Samba Indication--------------------------------------
	if [ $(pcp_samba_status) -eq 0 ]; then
		SMBINDICATOR=$HEAVY_CHECK_MARK
		CLASS="indicator_green"
		STATUS="running"
	else
		SMBINDICATOR=$HEAVY_BALLOT_X
		CLASS="indicator_red"
		STATUS="not running"
	fi
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Setup Samba Share</legend>'
	echo '          <form name="Samba_Setup" action="'$0'" method="get">'
	echo '            <table class="bggrey percent100">'
	pcp_incr_id
	pcp_start_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                  <p class="'$CLASS'">'$SMBINDICATOR'</p>'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Samba is '$STATUS'&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <ul>'
	echo '                      <li><span class="indicator_green">&#x2714;</span> = Samba running.</li>'
	echo '                      <li><span class="indicator_red">&#x2718;</span> = Samba not running.</li>'
	echo '                    </ul>'
	echo '                    <p><b>Note:</b></p>'
	echo '                    <ul>'
	echo '                      <li>Samba must be running to share files from this pCP.</li>'
	echo '                    </ul>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
#----------------------------------------------------------------------------------------
	pcp_lms_padding
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	if [ "$SAMBA" = "disabled" ]; then
		echo '                  <button type="submit" name="ACTION" value="Install_Samba">Install</button>'
		echo '                </td>'
		echo '                <td>'
		echo '                  <p>Install Samba for pCP&nbsp;&nbsp;'
		echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
		echo '                  </p>'
		echo '                  <div id="'$ID'" class="less">'
		echo '                    <p>This will install Samba Extension for SMB Share support for pCP.</p>'
		echo '                  </div>'
	else
		echo '                  <button type="submit" name="ACTION" value="Remove_Samba">Remove</button>'
		echo '                </td>'
		echo '                <td>'
		echo '                  <p>Remove Samba from pCP&nbsp;&nbsp;'
		echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
		echo '                  </p>'
		echo '                  <div id="'$ID'" class="less">'
		echo '                    <p>This will remove Samba Extension for SMB Share support for pCP.</p>'
		echo '                  </div>'
	fi
	echo '                </td>'
	echo '              </tr>'
	echo '            </table>'
	echo '          </form>'

	if [ "$SAMBA" != "disabled" ]; then
		if [ -f $SAMBACONF ]; then
#			This will read the config file.
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
					[*)	SC=$((SC+1)); eval SHARE${SC}=$(trimshare "${LINE}");;
					path*) eval SHAREPATH${SC}=$(pcp_trimval "${LINE}");;
					create\ mask*) eval SHAREMASK${SC}=$(pcp_trimval "${LINE}");;
					writeable*) eval SHARERO${SC}="no";;
					read\ only*) eval SHARERO${SC}="yes";;
					*);;
				esac
			done < $SAMBACONF
		fi
		echo '            <form name="Samba_Write" action="writetosamba.cgi" method="get">'
		echo '              <table class="bggrey percent100">'
		pcp_incr_id
		pcp_toggle_row_shade
		echo '                <tr class="'$ROWSHADE'">'
		echo '                  <td class="column150 center">'
		echo '                    <button type="submit" name="COMMAND" value="autostart">SMB Autostart</button>'
		echo '                  </td>'
		echo '                  <td class="column100">'
		echo '                    <input class="small1" type="radio" name="SAMBA" value="yes" '$SAMBAyes'>Yes'
		echo '                    <input class="small1" type="radio" name="SAMBA" value="no" '$SAMBAno'>No'
		echo '                  </td>'
		echo '                  <td>'
		echo '                    <p>Automatic start of SAMBA when pCP boots&nbsp;&nbsp;'
		echo '                      <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
		echo '                    </p>'
		echo '                    <div id="'$ID'" class="less">'
		echo '                      <p>Yes - will enable automatic start of SAMBA when pCP boots.</p>'
		echo '                      <p>No - will disable automatic start of SAMBA when pCP boots.</p>'
		echo '                    </div>'
		echo '                  </td>'
		echo '                </tr>'
		echo '              </table>'
		echo '            </form>'
		pcp_incr_id
		pcp_toggle_row_shade
		echo '            <form name="Samba_Run" action="'$0'">'
		echo '              <table class="bggrey percent100">'
		echo '                <tr class="'$ROWSHADE'">'
		echo '                  <td class="column150 center">'
		echo '                    <input type="submit" name="ACTION" value="SambaStart" />'
		echo '                  </td>'
		echo '                  <td>'
		echo '                    <p>Start SAMBA&nbsp;&nbsp;'
		echo '                      <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
		echo '                    </p>'
		echo '                    <div id="'$ID'" class="less">'
		echo '                      <p>This will start SAMBA.</p>'
		echo '                    </div>'
		echo '                  </td>'
		echo '                </tr>'
		pcp_incr_id
		pcp_toggle_row_shade
		echo '                <tr class="'$ROWSHADE'">'
		echo '                  <td class="column150 center">'
		echo '                    <input type="submit" name="ACTION" value="SambaStop" />'
		echo '                  </td>'
		echo '                  <td>'
		echo '                    <p>Stop SAMBA&nbsp;&nbsp;'
		echo '                      <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
		echo '                    </p>'
		echo '                    <div id="'$ID'" class="less">'
		echo '                      <p>This will stop SAMBA.</p>'
		echo '                    </div>'
		echo '                  </td>'
		echo '                </tr>'
		pcp_incr_id
		pcp_toggle_row_shade
		echo '                <tr class="'$ROWSHADE'">'
		echo '                  <td class="column150 center">'
		echo '                    <input type="submit" name="ACTION" value="SambaRestart" />'
		echo '                  </td>'
		echo '                  <td>'
		echo '                    <p>Restart SAMBA&nbsp;&nbsp;'
		echo '                      <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
		echo '                    </p>'
		echo '                    <div id="'$ID'" class="less">'
		echo '                      <p>This will stop SAMBA and then restart it.</p>'
		echo '                      <p><b>Note:</b></p>'
		echo '                        <ul>'
		echo '                          <li>A restart of SAMBA is rarely needed.</li>'
		echo '                          <li>SAMBA running indicator will turn green.</li>'
		echo '                        </ul>'
		echo '                    </div>'
		echo '                  </td>'
		echo '                </tr>'
		echo '              </table>'
		echo '            </form>'
		pcp_incr_id
		pcp_toggle_row_shade
		echo '            <form name="Passwd" action="writetosamba.cgi" method="get">'
		echo '              <table class="bggrey percent100">'
		echo '                <tr class="'$ROWSHADE'">'
		echo '                  <td class="column150 center">'
		if [ "$STATUS" = "running" ]; then
			PWDISABLE=""
		else
			PWDISABLE="disabled"
		fi
		echo '                    <button type="submit" name="COMMAND" value="setpw" '$PWDISABLE'>Set Password</button>'
		echo '                  </td>'
		echo '                  <td class="column100 ">'
		echo '                    <p class="row">UserName: tc</p>'
		echo '                  </td>'
		echo '                  <td class="column75">'
		echo '                    <p class="row">Password:</p>'
		echo '                  </td>'
		echo '                  <td class="column150">'
		echo '                    <p><input class="large12" type="password" name="SAMBAPASS" value="" '$PWDISABLE'></p>'
		echo '                  </td>'
		echo '                  <td>'
		if [ "$STATUS" = "running" ]; then
			echo '                    <p>Username and Password to be used to access share.&nbsp;&nbsp;'
			echo '                      <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
			echo '                    </p>'
			echo '                    <div id="'$ID'" class="less">'
			echo '                      <p>Needs done 1st time.  Note this value is cached by alot of machines and may not change immediately in the browser.</p>'
			echo '                    </div>'
		else
			echo '                    <p>Samba has to be running to set password!</p>'
		fi
		echo '                  </td>'
		echo '                </tr>'
		echo '              </table>'
		echo '            </form>'
		pcp_incr_id
		pcp_toggle_row_shade
		echo '            <form name="Select" action="writetosamba.cgi" method="get">'
		echo '              <table class="bggrey percent100">'
		echo '                <tr class="'$ROWSHADE'">'
		echo '                  <td class="column150 center">'
		echo '                    <p class="row">Server Name</p>'
		echo '                  </td>'
		echo '                  <td class="column210">'
		echo '                    <p><input class="large12" type="text" name="NETBIOS" value="'$NETBIOS'" required></p>'
		echo '                  </td>'
		echo '                  <td colspan=3>'
		echo '                    <p>This is the Server name that will show up in your network browser.&nbsp;&nbsp;'
		echo '                      <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
		echo '                    </p>'
		echo '                    <div id="'$ID'" class="less">'
		echo '                      <p>Note this value is cached by alot of machines and may not change immediately in the browser.</p>'
		echo '                    </div>'
		echo '                  </td>'
		echo '                </tr>'
		pcp_incr_id
		pcp_toggle_row_shade
		echo '                <tr class="'$ROWSHADE'">'
		echo '                  <td class="column150 center">'
		echo '                    <p class="row">Server WorkGroup</p>'
		echo '                  </td>'
		echo '                  <td class="column210">'
		echo '                    <p><input class="large12" type="text" name="WGROUP" value="'$WGROUP'" required></p>'
		echo '                  </td>'
		echo '                  <td colspan=3>'
		echo '                    <p>This is the Server Work Group that will show up in your network browser.&nbsp;&nbsp;'
		echo '                      <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
		echo '                    </p>'
		echo '                    <div id="'$ID'" class="less">'
		echo '                      <p>Note this value is cached by alot of machines and may not change immediately in the browser.</p>'
		echo '                    </div>'
		echo '                  </td>'
		echo '                </tr>'
		COL1="150"
		COL2="150"
		COL3="150"
		COL4="100"
		COL5="150"
		COL6="100"
		COL7="150"
		pcp_toggle_row_shade
		echo '                <tr class="'$ROWSHADE'">'
		echo '                  <td class="column'$COL1' center"><p><b>Share Name</b></p></td>'
		echo '                  <td class="column'$COL2'"><p><b>Share Path</b></p></td>'
		echo '                  <td class="column'$COL3'"><p><b>Create File Mode</b></p></td>'
		echo '                  <td class="column'$COL4' center"><p><b>Read ONLY</b></p></td>'
		echo '                  <td> </td>'
		echo '                </tr>'
		I=1
		SC=$((SC+1))
		while [ $I -le $SC ]
		do
			TST=$(eval echo "\${SHARE${I}}")
			[ "$TST" != "" ] && REQ="required" || REQ=""
			pcp_toggle_row_shade
			echo '                <tr class="'$ROWSHADE'">'
			echo '                  <td class="column'$COL1' center">'
			echo -n '                    <input class="large8" type="text" ID="SHARE'$I'" name="SHARE'$I'" value="'
			eval echo -n "\${SHARE${I}}"
			echo '" title="Enter the name of the Share" pattern="^[a-zA-Z0-9_]{1,32}$" onchange="setsmbrequired('$I')">'
			echo '                  </td>'
			echo '                  <td class="column'$COL2'">'
			echo -n '                    <input class="large12" type="text" ID="SHAREPATH'$I'" name="SHAREPATH'$I'" value="'
			eval echo -n "\${SHAREPATH${I}}"
			echo '" title="Enter the Path to be Shared" '$REQ' pattern="^[a-zA-Z0-9_/]{1,64}$">'
			echo '                  </td>'
			echo '                  <td class="column'$COL3'">'
			echo -n '                    <input class="large8" type="text" ID="SHAREMASK'$I'" name="SHAREMASK'$I'" value="'
			eval echo -n "\${SHAREMASK${I}}"
			echo '" title="Enter the File mode for new files Default=0664" '$REQ' pattern="^[0-7]{4}$">'
			echo '                  </td>'
			RO=$(eval echo "\${SHARERO${I}}")
			case "$RO" in
				yes) SHAREROyes="checked";;
				*) SHAREROyes="";;
			esac
			echo '                  <td class="column'$COL4' center">'
			echo '                    <input class="small1" type="checkbox" name="SHARERO'$I'" value="yes" '$SHAREROyes'>'
			echo '                  </td>'
			echo '                  <td class="column'$COL5' center">'
			echo '                    <input type="button" value="Remove" onclick="eraseshare('$I')">'
			echo '                  </td>'
			echo '                </tr>'
			I=$((I+1))
		done
		echo '                <script>'
		echo '                  function eraseshare(i) {'
		echo '                    var box = "SHARE";'
		echo '                    var Box = box.concat(i);'
		echo '                    document.getElementById(Box).value = "";'
		echo '                    var box = "SHAREPATH";'
		echo '                    var Box = box.concat(i);'
		echo '                    document.getElementById(Box).value = "";'
		echo '                    var box = "SHAREMASK";'
		echo '                    var Box = box.concat(i);'
		echo '                    document.getElementById(Box).value = "";'
		echo '                    setsmbrequired(i);'
		echo '                  }'
		echo '                  function setsmbrequired(id) {'
		echo '                    var box = "SHARE";'
		echo '                    var Box = box.concat(id);'
		echo '                    var box1 = "SHAREPATH";'
		echo '                    var Box1 = box1.concat(id);'
		echo '                    var box2 = "SHAREMASK";'
		echo '                    var Box2 = box2.concat(id);'
		echo '                    if (document.getElementById(Box).value != ""){'
		echo '                      document.getElementById(Box1).setAttribute("required", "");'
		echo '                      document.getElementById(Box2).setAttribute("required", "");'
		echo '                    }'
		echo '                    else {'
		echo '                      document.getElementById(Box1).required = false;'
		echo '                      document.getElementById(Box2).required = false;'
		echo '                    }'
		echo '                  }'
		echo '                </script>'

		#--------------------------------------Submit button-------------------------------------
		pcp_toggle_row_shade
		echo '                <tr class="'$ROWSHADE'">'
		echo '                  <td class="column150 center">'
		echo '                    <input type="hidden" name="COMMAND" value="setconfig">'
		echo '                    <input type="hidden" name="SC" value="'$SC'">'
		echo '                    <button type="submit" name="ACTION" value="setconfig">Set Samba</button>'
		echo '                  </td>'
		echo '                  <td colspan=4> </td>'
		echo '                </tr>'
#----------------------------------------------------------------------------------------
		echo '              </table>'
		echo '            </form>'
	fi
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
}
[ $MODE -ge $MODE_BETA ] && pcp_samba
#----------------------------------------------------------------------------------------

#------------------------------------------LMS log text area-----------------------------
pcp_lms_logview() {
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Show LMS logs</legend>'
	echo '          <table class="bggrey percent100">'
	echo '            <tr>'
	echo '              <td>'
	                      pcp_textarea_inform "$LMS_SERV_LOG" 'cat $LMS_SERV_LOG' 250
	echo '              </td>'
	echo '            </tr>'
	echo '            <tr>'
	echo '              <td>'
	                      pcp_textarea_inform "$LMS_SCAN_LOG" 'cat $LMS_SCAN_LOG' 250
	echo '              </td>'
	echo '            </tr>'
	if [ -f $LMS_UPDATE_LOG ]; then
		echo '            <tr>'
		echo '              <td>'
							  pcp_textarea_inform "$LMS_UPDATE_LOG" 'cat $LMS_UPDATE_LOG' 250
		echo '              </td>'
		echo '            </tr>'
	fi
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
}
[ "$LOGSHOW" = "yes" ] && pcp_lms_logview
#----------------------------------------------------------------------------------------

pcp_footer
[ $MODE -ge $MODE_NORMAL ] && pcp_mode
pcp_copyright

echo '</body>'
echo '</html>'
