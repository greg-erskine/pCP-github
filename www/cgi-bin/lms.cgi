#!/bin/sh

# Version: 3.11 2017-01-28
#	Added Workgroup to Samba. PH.
#	Updated freespace requirements. PH.

# Version: 3.10 2016-12-27
#	Pop-up asking to delete cache. SBP
#	Remove all traces of LMS. SBP
#	Added Samba.  PH.
#	Added GPT Disk support. PH
#	Converted lms removal to proper method to avoid removing a dependancy. PH
#	Updates for using sourceforge repo for filesystem support. PH
# 	Added pattern not not allow mount points starting with sd. PH
#	Samba Cleanup.  PH

# Version: 3.00 2016-07-01 PH
#	Mode Changes

# Version: 2.06 2016-05-07 PH
#	Cleanup

# Version: 2.05 2016-04-26 PH
#	Updated warning message.
#	Added Mounting of disks.
#	Added additional file system support.
#	Added Location for LMS Server Persistent Data.
#	Added LMS Server Update Script.
#	Turned off [Mode] Tabs in basic mode. GE.
#	Added LMS rescan in developer mode. GE.

# Version: 0.02 2016-03-19 SBP
#	Added LMS log view, space check and hide SAMBA and update LMS options.
#	Moved pcp_lms_status to pcp-lms-functions.

# Version: 0.01 2016-01-30 SBP
#	Original.

. pcp-lms-functions
. pcp-rpi-functions
. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "LMS Main Page" "SBP"

[ $MODE -ge $MODE_NORMAL ] && pcp_picoreplayers
[ $MODE -ge $MODE_ADVANCED ] && pcp_controls
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

LMS_SERV_LOG="${LOGS}/server.log"
LMS_SCAN_LOG="${LOGS}/scanner.log"
WGET="/bin/busybox wget"

#---------------------------Routines-----------------------------------------------------

pcp_install_lms() {
	echo '[ INFO ] Downloading LMS...'
	sudo -u tc pcp-load -r $PCP_REPO -w slimserver.tcz 
	if [ -f /mnt/mmcblk0p2/tce/optional/slimserver.tcz ]; then
		echo '[ INFO ] Installing LMS...'
		sudo -u tc pcp-load -i slimserver.tcz
		sudo sed -i '/slimserver.tcz/d' /mnt/mmcblk0p2/tce/onboot.lst
		sudo echo 'slimserver.tcz' >> /mnt/mmcblk0p2/tce/onboot.lst
		[ $DEBUG -eq 1 ] && echo '[ DEBUG ] LMS is added to onboot.lst'
		[ $DEBUG -eq 1 ] && cat /mnt/mmcblk0p2/tce/onboot.lst
	fi
}

pcp_remove_lms() {
	sudo /usr/local/etc/init.d/slimserver stop >/dev/null 2>&1
	sudo -u tc tce-audit builddb
	sudo -u tc tce-audit delete slimserver.tcz
	sudo sed -i '/slimserver.tcz/d' /mnt/mmcblk0p2/tce/onboot.lst
}

pcp_remove_lms_cache() {
	sudo rm -rf /mnt/mmcblk0p2/tce/slimserver/
	sudo rm -rf /mnt/"$NETMOUNT1POINT"/slimserver/
	sudo rm -rf /mnt/"$MOUNTPOINT"/slimserver/
}

pcp_lms_padding() {
	pcp_toggle_row_shade
	echo '            <tr class="padding '$ROWSHADE'">'
	echo '              <td></td>'
	echo '              <td></td>'
	echo '            </tr>'
}

pcp_install_fs() {
	RESULT=0
	echo '[ INFO ] Downloaded additional filesystem support.</p>'
	sudo -u tc pcp-load -r $PCP_REPO -w ntfs-3g.tcz
	if [ -f /mnt/mmcblk0p2/tce/optional/ntfs-3g.tcz ]; then
		echo '[ INFO ] Loading filesystem extensions'
		sudo -u tc tce-load -i ntfs-3g.tcz
		[ $? -eq 0 ] && echo -n . || (echo $?; RESULT=1)
	fi
	if [ $RESULT -eq 0 ]; then
		echo "ntfs-3g.tcz" >> /mnt/mmcblk0p2/tce/onboot.lst
		echo '[ INFO ] Filesystem support including NTFS loaded...</p>'
	else
		echo '[ ERROR ] Extensions not loaded, try again later!</p>'
	fi
}

pcp_remove_fs() {
	echo '[ INFO ] Removing Extensions</p>'
	rm -f /mnt/mmcblk0p2/tce/optional/ntfs-3g*
	rm -f /mnt/mmcblk0p2/tce/optional/filesystems*
	sed -i '/ntfs-3g.tcz/d' /mnt/mmcblk0p2/tce/onboot.lst
	echo '[ INFO ] Extensions Removed, Reboot to Finish</p>'
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
		echo "samba4.tcz" >> /mnt/mmcblk0p2/tce/onboot.lst
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
	sed -i '/samba4.tcz/d' /mnt/mmcblk0p2/tce/onboot.lst
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
			usbmount) MNT="/mnt/$MOUNTPOINT";;
			netmount1) MNT="/mnt/$NETMOUNT1POINT";;
			default) MNT="/mnt/mmcblk0p2";;
		esac
		pcp_table_top "Logitech Media Server (LMS)"
		echo '                <textarea class="inform" style="height:40px">'
		mount | grep -qs $MNT
		if [ "$?" = "0" ]; then
			echo '[ INFO ] Starting LMS...'
			echo -n '[ INFO ] '
			sudo /usr/local/etc/init.d/slimserver start
		else
			echo '[ ERROR ] LMS data disk not mounted, LMS will not start.'
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
		echo '                <textarea class="inform" style="height:160px">'
		pcp_install_lms
		if [ -f /mnt/mmcblk0p2/tce/optional/slimserver.tcz ]; then
			LMSERVER="yes"
			pcp_save_to_config
			pcp_backup "nohtml"
		else
			echo '[ ERROR ] Error Downloading LMS, please try again later.'
		fi
		echo '                </textarea>'
		pcp_table_end
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
		echo '                <textarea class="inform" style="height:80px">'
		pcp_install_fs
		echo '                </textarea>'
		pcp_table_end
	;;
	Remove_FS)
		pcp_table_top "Removing extra file system support"
		echo '                <textarea class="inform" style="height:80px">'
		pcp_remove_fs
		echo '                </textarea>'
		pcp_table_end
		REBOOT_REQUIRED=1
	;;
	Install_Samba)
		pcp_table_top "Installing Samba4 Server"
		pcp_sufficient_free_space 25000
		echo '                <textarea class="inform" style="height:120px">'
		pcp_install_samba4
		echo '                </textarea>'
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
	*)
		pcp_warning_message
	;;
esac
[ $REBOOT_REQUIRED -eq 1 ] && pcp_reboot_required

#--------Set Variables that need to be checked after the above Case Statement -----------
# logic to activate/inactivate buttons depending upon whether LMS is installed or not 
if [ -f /mnt/mmcblk0p2/tce/optional/slimserver.tcz ]; then
	DISABLED=""
else
	DISABLED="disabled"
fi

# logic to activate/inactivate buttons depending upon whether LMS cache is present or not 
if [ -d /mnt/mmcblk0p2/tce/slimserver ] || [ -d /mnt/"$MOUNTPOINT"/slimserver/Cache ] || [ -d /mnt/"$NETMOUNT1POINT"/slimserver/Cache ]; then
	DISABLECACHE=""
else
	DISABLECACHE="disabled"
fi

df | grep -qs ntfs
[ "$?" = "0" ] && NTFS="yes" || NTFS="no"

#========================================================================================
# Main table
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Logitech Media Server (LMS) operations</legend>'
echo '          <table class="bggrey percent100">'

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
echo '            <tr class="'$ROWSHADE'">'
echo '              <td class="column150 centre">'
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
#----------------------------------------------------------------------------------------

pcp_lms_padding

#-----------------------------------Enable/disable autostart of LMS----------------------
pcp_lms_enable_lms() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '            <form name="Select" action="writetolms.cgi" method="get">'
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" value="LMS autostart" '$DISABLED' />'
	echo '                </td>'
	echo '                <td class="column100">'
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
	echo '            </form>'
}
[ $MODE -ge $MODE_NORMAL ] && pcp_lms_enable_lms
#----------------------------------------------------------------------------------------

#-----------------------------------Configure LMS----------------------------------------
pcp_lms_configure_lms() {

	[ x"" = x"$LMSWEBPORT" ] && LMSPORT=9000 || LMSPORT=$LMSWEBPORT
	[ x"" = x"$(pcp_eth0_ip)" ] && LMS_SERVER_WEB=$(pcp_wlan0_ip) || LMS_SERVER_WEB=$(pcp_eth0_ip)
	LMS_SERVER_WEB_URL="http://${LMS_SERVER_WEB}:${LMSPORT}"

	pcp_incr_id
	pcp_toggle_row_shade
	echo '            <form name="Configure" action="'$LMS_SERVER_WEB_URL'" target="_blank">'
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" value="Configure LMS" '$DISABLED' />'
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
	echo '            </form>'
}
[ $MODE -ge $MODE_BETA ] && pcp_lms_configure_lms
#----------------------------------------------------------------------------------------

#-----------------------------------Rescan LMS-------------------------------------------
pcp_rescan_lms() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '            <form name="Rescan" action="'$0'">'
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
	echo '                <td>'
	echo '                  <p>Rescan LMS library&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Rescan the local LMS library.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_rescan_lms
#----------------------------------------------------------------------------------------

#------------------------------------------Install/uninstall LMS-------------------------
pcp_lms_install_lms() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '            <form name="Install" action="'$0'">'
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	if [ ! -f /mnt/mmcblk0p2/tce/optional/slimserver.tcz ]; then
		echo '                  <input type="submit" name="ACTION" value="Install" />'
		echo '                </td>'
		echo '                <td>'
		echo '                  <p>Install LMS on pCP&nbsp;&nbsp;'
		echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
		echo '                  </p>'
		echo '                  <div id="'$ID'" class="less">'
		echo '                    <p>This will install LMS on pCP.</p>'
		echo '                  </div>'
	else
		echo '                  <input type="submit" name="ACTION" value="Remove" />'
		echo '                </td>'
		echo '                <td>'
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
	echo '            </form>'
}
[ $MODE -ge $MODE_NORMAL ] && pcp_lms_install_lms
#----------------------------------------------------------------------------------------

#------------------------------------------Remove LMS cache-------------------------
pcp_lms_remove_cache() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '            <form name="Remove_cache" action="'$0'">'
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                    <button type="submit" name="ACTION" value="Remove_cache" '$DISABLECACHE'>Remove cache</button>'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Remove LMS cache from pCP&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>This will remove your LMS cache from pCP.</p>'
	echo '                  </div>'
	echo '                 </td>'
	echo '               </tr>'
	echo '              </form>'
}
[ $MODE -ge $MODE_NORMAL ] && pcp_lms_remove_cache
#----------------------------------------------------------------------------------------

#------------------------------------------Start LMS-------------------------------------
pcp_lms_start_lms() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '            <form name="Start" action="'$0'">'
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="ACTION" value="Start" '$DISABLED' />'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Start LMS&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>This will start LMS.</p>'
	echo '                    </ul>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_NORMAL ] && pcp_lms_start_lms
#----------------------------------------------------------------------------------------

#------------------------------------------Stop LMS--------------------------------------
pcp_lms_stop_lms() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '            <form name="Stop" action="'$0'">'
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="ACTION" value="Stop" '$DISABLED' />'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Stop LMS&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>This will stop LMS.</p>'
	echo '                    </ul>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_NORMAL ] && pcp_lms_stop_lms
#----------------------------------------------------------------------------------------

#---------------------------------Restart LMS--------------------------------------------
pcp_lms_restart_lms() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '            <form name="Restart" action="'$0'">'
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="ACTION" value="Restart" '$DISABLED' />'
	echo '                </td>'
	echo '                <td>'
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
	echo '            </form>'
}
[ $MODE -ge $MODE_NORMAL ] && pcp_lms_restart_lms
#----------------------------------------------------------------------------------------

#---------------------------------Update LMS--------------------------------------------
pcp_update_lms() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '            <form name="Update" action="lms-update.cgi">'
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" value="LMS Update" '$DISABLED'>'
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
	echo '            </form>'
}
[ $MODE -ge $MODE_NORMAL ] && pcp_update_lms
#----------------------------------------------------------------------------------------

#-------------------------------Show LMS logs--------------------------------------------
pcp_lms_show_logs() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '            <form name="Show" action="'$0'" method="get">'
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" value="Show Logs" />'
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
	echo '            </form>'
}
[ $MODE -ge $MODE_NORMAL ] && pcp_lms_show_logs
#----------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------
echo '          </table>'
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
		usbmount) USByes="checked";;
		netmount1) NETyes="checked";;
		default) DEFyes="checked";;
	esac
	if [ "$MOUNTUUID" != "no" -o -n "$USByes" ]; then
		pcp_toggle_row_shade
		echo '              <tr class="'$ROWSHADE'">'
		echo '                <td class="column'$COL1' center">'
		echo '                  <input class="small1" type="radio" name="LMSDATA" value="usbmount" '$USByes'>'
		echo '                </td>'
		echo '                <td class="column'$COL2'">'
		echo '                  <p>USB Disk</p>'
		echo '                </td>'
		echo '                <td class="column'$COL3'">'
		if [ -n "$USByes" -a  ! -d /mnt/"$MOUNTPOINT"/slimserver ]; then
			echo '                  <p>Disk Not Found, LMS Disabled</p>'
		else
			echo '                  <p>/mnt/'$MOUNTPOINT'/slimserver</p>'
		fi
		echo '                </td>'
		if [ -d /mnt/"$MOUNTPOINT"/slimserver/Cache ]; then
			echo '                <td class="column'$COL4'">'
			echo '                  <p>There is a Cache folder found on this drive</p>'
			echo '                </td>'
		else
			echo '                <td></td>'
		fi
		echo '              </tr>'
	fi
	if [ "$NETMOUNT1" = "yes" -o -n "$NETyes" ]; then
		pcp_toggle_row_shade
		echo '              <tr class="'$ROWSHADE'">'
		echo '                <td class="column'$COL1' center">'
		echo '                  <input class="small1" type="radio" name="LMSDATA" value="netmount1" '$NETyes'>'
		echo '                </td>'
		echo '                <td class="column'$COL2'">'
		echo '                  <p>Network Disk</p>'
		echo '                </td>'
		echo '                <td class="column'$COL3'">'
		if [ -n "$NETyes" -a  ! -d /mnt/"$NETMOUNT1POINT"/slimserver ]; then
			echo '                  <p>Disk Not Found, LMS Disabled</p>'
		else
			echo '                  <p>/mnt/'$NETMOUNT1POINT'/slimserver</p>'
		fi
		echo '                </td>'
		if [ -d /mnt/"$NETMOUNT1POINT"/slimserver/Cache ]; then
			echo '                <td class="column'$COL4'">'
			echo '                  <p>There is a Cache folder found on this drive</p>'
			echo '                </td>'
		else
			echo '                <td></td>'
		fi
		echo '              </tr>'
	fi
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column'$COL1' center">'
	echo '                  <input class="small1" type="radio" name="LMSDATA" value="default" '$DEFyes'>'
	echo '                </td>'
	echo '                <td class="column'$COL2'">'
	echo '                  <p>Local SDCard</p>'
	echo '                </td>'
	echo '                <td class="column'$COL3'">'
	echo '                  <p>/mnt/mmcblk0p2/tce/slimserver</p>'
	echo '                </td>'
	if [ -d /mnt/mmcblk0p2/tce/slimserver/Cache ]; then
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
	DISABLE="0"
	for i in `mount | awk '{print $5}'`; do
		case "$i" in
			*fat*|*squash*|proc|tmpfs|sysfs|devpts|ext*) ;;
			*) DISABLE="1" ;;
		esac
	done
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	if [ "$NTFS" = "no" ]; then
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
	elif [ "$DISABLE" = "0" ]; then
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
		echo '                    <p>as there are currently active mounts using this support</p>'
		echo '                  </div>'
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
	fdisk -V 2>&1 | grep -q -i busybox
	[ $? -eq 0 ] && BBFDISK=1 || BBFDISK=0
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
	echo '                <td class="column100">'
	echo '                  <p>Mount Point</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <p>/mnt/ <input class="large12" type="text" name="MOUNTPOINT" value="'$MOUNTPOINT'" required pattern="(?!sd)(?!mmcblk)^[a-zA-Z0-9_]{1,32}$"><p>'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>This is the mount point for the below drive.&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>The drive will be mounted by UUID to this path and will be automounted on startup.</p>'
	echo '                    <p>Alpha-numeric pathnames required (up to 32 characters).</p>'
	echo '                    <p>Do not use hardware device names like sda1 or mmcblk0.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </table>'
	echo '            <table class="bggrey percent100">'
	COL1="75"
	COL2="150"
	COL3="100"
	COL4="100"
	COL5="300"
	COL6="100"
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column'$COL1' center"><p><b>Enabled</b></p></td>'
	echo '                <td class="column'$COL2'"><p><b>Device</b></p></td>'
	echo '                <td class="column'$COL3'"><p><b>Label</b></p></td>'
	echo '                <td class="column'$COL4'"><p><b>FS Type</b></p></td>'
	echo '                <td class="column'$COL5'"><p><b>UUID</b></p></td>'
	echo '                <td class="column'$COL6'"><p><b>Size</b></p></td>'
	echo '              </tr>'

	DISKFOUND="no"
	case "$MOUNTUUID" in
		no)
			NOUUIDyes="checked"
			DISKFOUND="yes"
		;;
		*)  #the contents are a UUID
			NOUUIDyes=""
		;;
	esac

	ALLPARTS=$(fdisk -l | awk '$1 ~ /dev/{printf "%s\n",$1}')
	for i in $ALLPARTS; do
		if [ "$i" != "/dev/mmcblk0p1" -a "$i" != "/dev/mmcblk0p2" ]; then
			PART=$i
			LBL=$(blkid $i -s LABEL| awk -F"LABEL=" '{print $NF}' | tr -d "\"")
			UUID=$(blkid $i -s UUID| awk -F"UUID=" '{print $NF}' | tr -d "\"")
			PTTYPE=$(blkid $i -s TYPE| awk -F"TYPE=" '{print $NF}' | tr -d "\"")
			if [ $BBFDISK -eq 1 ]; then
				SIZE=$(fdisk -l | grep $i | tr -s " " | cut -d " " -f4 | tr -d +)
				[ $SIZE -gt 10485760 ] && SIZExB="`expr $SIZE / 1048576` GB" || SIZExB="`expr $SIZE / 1024` MB"
			else
				SIZE=$(fdisk -l | grep $i | tr -s " " | cut -d " " -f5 | tr -d +)
				SIZExB="${SIZE}B"
			fi
			
			case "$MOUNTUUID" in
				"$UUID")
					UUIDyes="checked"
					DISKFOUND="yes"
				;;
				*) UUIDyes=""
				;;
			esac
			pcp_toggle_row_shade
			if [ "$NTFS" = "no" ]; then
				case "$PTTYPE" in
					*fat*|ext*) DISABLE="";;
					*) DISABLE="Disabled"; UUID="Please install extra Filesystems" ;;
				esac
			fi
			echo '                <tr class="'$ROWSHADE'">'
			echo '                  <td class="column'$COL1' center">'
			echo '                    <input class="small1" type="radio" name="MOUNTUUID" value="'$UUID'" '$UUIDyes' '$DISABLE'>'
			echo '                  </td>'
			echo '                  <td class="column'$COL2'">'
			echo '                    <p>'$PART'</p>'
			echo '                  </td>'
			echo '                  <td class="column'$COL3'">'
			echo '                    <p>'$LBL'</p>'
			echo '                  </td>'
			echo '                  <td class="column'$COL4'">'
			echo '                    <p>'$PTTYPE'</p>'
			echo '                  </td>'
			echo '                  <td class="column'$COL5'">'
			echo '                    <p>'$UUID'</p>'
			echo '                  </td>'
			echo '                  <td class="column'$COL6'">'
			echo '                    <p>'$SIZExB'</p>'
			echo '                  </td>'
			echo '                </tr>'
		fi
	done
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column'$COL1' center">'
	echo '                  <input class="small1" type="radio" name="MOUNTUUID" value="no" '$NOUUIDyes'>'
	echo '                </td>'
	echo '                <td colspan="5">'
	echo '                  <p>Disk Mount Disabled</p>'
	echo '                </td>'
	echo '              </tr>'
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
		echo '                  </td>'
		echo '              </tr>'
	fi
	if [ "$DISKFOUND" = "no" ]; then
		pcp_toggle_row_shade
		echo '              <tr class="'$ROWSHADE'">'
		echo '                  <td class="column'$COL1' center">'
		echo '                    <input class="small1" type="radio" name="MOUNTUUID" value="no" checked>'
		echo '                  </td>'
		echo '                  <td colspan="5">'
		echo '                    <p>Previously selected disk '$MOUNTUUID' not Found. Please Insert and Reboot system, or select a new Disk</p>'
		echo '                  </td>'
		echo '                </tr>'
	fi
#--------------------------------------Submit button-------------------------------------
	pcp_incr_id
	pcp_toggle_row_shade
	echo '                <tr class="'$ROWSHADE'">'
	echo '                  <td  class="column150 center">'
	if [ "$LMSDATA" = "usbmount" ]; then
		echo '                    <button type="submit" name="ACTION" value="Save" Disabled>Set USB Mount</button>'
		echo '                  </td>'
		echo '                  <td  class="colspan5">'
		echo '                    <p> LMS is currently using this disk for Data.&nbsp;&nbsp;'
		echo '                      <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
		echo '                    </p>'
		echo '                    <div id="'$ID'" class="less">'
		echo '                      <p>Must Move LMS Data to another disk (SDcard or Network Share).</p>'
		echo '                      <p>in order to change this mount.</p>'
		echo '                    </div>'
	else
		echo '                    <input type="hidden" name="MOUNTTYPE" value="localdisk">'
		echo '                    <button type="submit" name="ACTION" value="Save">Set USB Mount</button>'
	fi
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
[ $MODE -ge $MODE_ADVANCED ] && pcp_mount_usbdrives

#========================================================================================
# Network Disk Mounting Operations
#----------------------------------------------------------------------------------------
pcp_mount_netdrives() {
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Setup Network Disk Mount</legend>'
	echo '          <form name="Mount" action="writetomount.cgi" method="get">'
	echo '            <table class="bggrey percent100">'
	pcp_incr_id
	pcp_start_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column100">'
	echo '                  <p class="row">Mount Point</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <p>/mnt/ <input class="large12" type="text" name="NETMOUNT1POINT" value="'$NETMOUNT1POINT'" required pattern="(?!sd)(?!mmcblk)^[a-zA-Z0-9_]{1,32}$"></p>'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>This is the mount point for the below network share.&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>The network share will be mounted by to this path and will be automounted on startup.</p>'
	echo '                    <p>Alpha-numeric pathnames required (up to 32 characters).</p>'
	echo '                    <p>Do not use hardware device names like sda1 or mmcblk0.</p>'
	echo '                    <p>&#60;Server IP address&#62; is only the IP address.  Do not enter any / or :</p>'
	echo '                    <p>&#60;Server Share&#62 for CIFS is the share name only (DO not use /).</p>'
	echo '                    <p>&#60;Server Share&#62 for NFS is the complete volume i.e. /volume1/Media (DO not use :).</p>'
	echo '                    <p>&#60;Options&#62 are a comma delimited list of mount options. Ref mount man pages.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </table>'

	case "$NETMOUNT1" in
		yes)
			NETMOUNT1yes="checked"
			NETMOUNT1no=""
		;;
		*)
			NETMOUNT1yes=""
			NETMOUNT1no="checked"
		;;
	esac

	echo '            <table class="bggrey percent100">'
	COL1="75"
	COL2="150"
	COL3="110"
	COL4="100"
	COL5="100"
	COL6="100"
	COL7="150"
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column'$COL1' center"><p><b>Enabled</b></p></td>'
	echo '                <td class="column'$COL2'"><p><b>Server IP Address</b></p></td>'
	echo '                <td class="column'$COL3'"><p><b>Server Share</b></p></td>'
	echo '                <td class="column'$COL4'"><p><b>Share Type</b></p></td>'
	echo '                <td class="column'$COL5'"><p><b>Username<b></p></td>'
	echo '                <td class="column'$COL6'"><p><b>Password</b></p></td>'
	echo '                <td class="column'$COL7'"><p><b>Options</b></p></td>'
	echo '              </tr>'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column'$COL1' center">'
	echo '                  <input class="small1" type="radio" name="NETMOUNT1" value="yes" '$NETMOUNT1yes'>'
	echo '                </td>'
	echo '                <td class="column'$COL2'">'
	echo '                  <input class="large10" type="text" name="NETMOUNT1IP" value="'$NETMOUNT1IP'" title="Enter the IP Address of the Remote Server" pattern="((^|\.)((25[0-5])|(2[0-4]\d)|(1\d\d)|([1-9]?\d))){4}$">'
	echo '                </td>'
	echo '                <td class="column'$COL3'">'
	echo '                  <input class="large8" type="text" name="NETMOUNT1SHARE" value="'$NETMOUNT1SHARE'" title="Enter the Name of the Share&#13;Do not enter / or :" pattern="^[a-zA-Z0-9_/]{1,32}$">'
	echo '                </td>'
	echo '                <td class="column'$COL4'">'

	case "$NETMOUNT1FSTYPE" in
		cifs) CIFS1yes="selected" ;;
		nfs) NFS1yes="selected" ;;
	esac

	echo '                  <select class="large6" name="NETMOUNT1FSTYPE" title="Only cifs(samba) and nfs shares are supported">'
	echo '                    <option value="cifs" '$CIFS1yes'>CIFS</option>'
	echo '                    <option value="nfs" '$NFS1yes'>NFS</option>'
	echo '                  </select>'
	echo '                </td>'
	echo '                <td class="column'$COL5'">'
	echo '                  <input class="large6" type="text" name="NETMOUNT1USER" value="'$NETMOUNT1USER'" title="Enter the Username for the remote share.&#13;Not used with NFS">'
	echo '                </td>'
	echo '                <td class="column'$COL6'">'
	echo '                  <input class="large6" type="text" name="NETMOUNT1PASS" value="'$NETMOUNT1PASS'" title="Enter the Password for the remote share.&#13;Not used with NFS">'
	echo '                </td>'
	echo '                <td class="column'$COL7'">'
	echo '                  <input class="large15" type="text" name="NETMOUNT1OPTIONS" value="'$NETMOUNT1OPTIONS'" title="Enter any comma delimeted mount option&#13;i.e. uid=1001,gid=50" >'
	echo '                </td>'
	echo '              </tr>'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column'$COL1' center">'
	echo '                  <input class="small1" type="radio" name="NETMOUNT1" value="no" '$NETMOUNT1no'>'
	echo '                </td>'
	echo '                <td colspan="6">'
	echo '                  <p>Net Mount Disabled</p>'
	echo '                </td>'
	echo '              </tr>'
#--------------------------------------Submit button-------------------------------------
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	if [ "$NTFS" = "no" ]; then
		echo '                    <button type="submit" name="ACTION" value="Save" Disabled>Set NET Mount</button>'
		echo '                  </td>'
		echo '                  <td  class="colspan5">'
		echo '                    <p>Mounting network drives requires extra filesystem support.&nbsp;&nbsp;'
		echo '                      <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
		echo '                    </p>'
		echo '                    <div id="'$ID'" class="less">'
		echo '                      <p>Please add additional filesystems using the option above.</p>'
		echo '                    </div>'
	elif [ "$LMSDATA" = "netmount1" ]; then
		echo '                    <button type="submit" name="ACTION" value="Save" Disabled>Set NET Mount</button>'
		echo '                  </td>'
		echo '                  <td  class="colspan5">'
		echo '                    <p>LMS is currently using this disk for Data.&nbsp;&nbsp;'
		echo '                      <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
		echo '                    </p>'
		echo '                    <div id="'$ID'" class="less">'
		echo '                      <p>Must Move LMS Data to another disk (SDcard or USB Disk).</p>'
		echo '                      <p>in order to change this mount.</p>'
		echo '                    </div>'
	else
		echo '                  <input type="hidden" name="MOUNTTYPE" value="networkshare">'
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
	echo '          <form name="Start" action="'$0'" method="get">'
	echo '            <table class="bggrey percent100">'
	pcp_incr_id
	pcp_start_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 centre">'
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
			trimval() {
				echo $1 | cut -d '=' -f2 | xargs 
			}
			trimshare() {
				echo $1 | tr -d '[]' 
			}

			while read LINE; do
				case $LINE in
					*global*) GLOBAL=1;;
					netbios*) NETBIOS=$(trimval "${LINE}");;
					workgroup*) WGROUP=$(trimval "${LINE}");;
					[*)	SC=$((SC+1)); eval SHARE${SC}=$(trimshare "${LINE}");;
					path*) eval SHAREPATH${SC}=$(trimval "${LINE}");;
					create\ mask*) eval SHAREMASK${SC}=$(trimval "${LINE}");;
					writeable*) eval SHARERO${SC}="no";;
					read\ only*) eval SHARERO${SC}="yes";;
					*);;
				esac
			done < $SAMBACONF
		fi	
		echo '            <table class="bggrey percent100">'
		echo '              <form name="Select" action="writetosamba.cgi" method="get">'
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
		echo '              </form>'
		pcp_incr_id
		pcp_toggle_row_shade
		echo '              <form name="Start" action="'$0'">'
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
		echo '              </form>'
		pcp_incr_id
		pcp_toggle_row_shade
		echo '              <form name="Stop" action="'$0'">'
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
		echo '              </form>'
		pcp_incr_id
		pcp_toggle_row_shade
		echo '              <form name="Restart" action="'$0'">'
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
		echo '                        <li>A restart of SAMBA is rarely needed.</li>'
		echo '                        <li>SAMBA running indicator will turn green.</li>'
		echo '                    </div>'
		echo '                  </td>'
		echo '                </tr>'
		echo '              </form>'
		echo '            </table>'
		pcp_incr_id
		pcp_toggle_row_shade
		echo '            <table class="bggrey percent100">'
		echo '              <form name="Select" action="writetosamba.cgi" method="get">'
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
			echo '                    <p>Samba has to be running to set password!</p'
		fi
		echo '                  </td>'
		echo '                </tr>'
		echo '              </form>'
		pcp_incr_id
		pcp_toggle_row_shade
		echo '              <form name="Select" action="writetosamba.cgi" method="get">'
		echo '                <tr class="'$ROWSHADE'">'
		echo '                  <td class="column150 center">'
		echo '                    <p class="row">Server Name</p>'
		echo '                  </td>'
		echo '                  <td class="column210">'
		echo '                    <p><input class="large12" type="text" name="NETBIOS" value="'$NETBIOS'" required"></p>'
		echo '                  </td>'
		echo '                  <td>'
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
		echo '                    <p><input class="large12" type="text" name="WGROUP" value="'$WGROUP'" required"></p>'
		echo '                  </td>'
		echo '                  <td>'
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
		echo '                  <td class="column'$COL4' center"><p><b>Read ONLY<b></p></td>'
		echo '                </tr>'
		I=1
		SC=$((SC+1))
		while [ $I -le $SC ]
		do
			pcp_toggle_row_shade
			echo '                <tr class="'$ROWSHADE'">'
			echo '                  <td class="column'$COL1' center">'
			echo -n '                    <input class="large8" type="text" ID="SHARE'$I'" name="SHARE'$I'" value="'
			eval echo -n "\${SHARE${I}}"
			echo '" title="Enter the name of the Share" pattern="^[a-zA-Z0-9_]{1,32}$">'
			echo '                  </td>'
			echo '                  <td class="column'$COL2'">'
			echo -n '                    <input class="large12" type="text" ID="SHAREPATH'$I'" name="SHAREPATH'$I'" value="'
			eval echo -n "\${SHAREPATH${I}}"
			echo '" title="Enter the Path to be Shared" pattern="^[a-zA-Z0-9_/]{1,32}$">'
			echo '                  </td>'
			echo '                  <td class="column'$COL3'">'
			echo -n '                    <input class="large8" type="text" ID="SHAREMASK'$I'" name="SHAREMASK'$I'" value="'
			eval echo -n "\${SHAREMASK${I}}"
			echo '" title="Enter the File mode for new files Default=0664" pattern="^[0-7]{4}$">'
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
		echo '                <script type="text/javascript">'
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
		echo '                </tr>'
#----------------------------------------------------------------------------------------
		echo '              </form>'
		echo '            </table>'
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
