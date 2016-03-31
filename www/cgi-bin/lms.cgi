#!/bin/sh

# Version: 0.03 2016-03-28 GE
#	Updated warning message.

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

LMS_SERV_LOG=${LOGS}/server.log
LMS_SCAN_LOG=${LOGS}/scanner.log
WGET="/bin/busybox wget"
LMSREPOSITORY="https://sourceforge.net/projects/picoreplayer/files/tce/7.x/LMS"

#---------------------------Routines-----------------------------------------------------
pcp_download_lms() {
	cd /tmp
	sudo rm -f /tmp/LMS
	sudo mkdir /tmp/LMS
	echo '<p class="info">[ INFO ] Downloading Logitech Media Server (LMS) from repository...</p>'
	[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Repo: '${LMSREPOSITORY}'</p>'
	echo '<p class="info">[ INFO ] Download will take a few minutes. Please wait...</p>'

	$WGET -s ${LMSREPOSITORY}/slimserver-CPAN.tcz
	if [ $? = 0 ]; then
		RESULT=0
		echo '<p class="info">[ INFO ] Downloading LMS'
		$WGET ${LMSREPOSITORY}/slimserver-CPAN.tcz/download -O /tmp/LMS/slimserver-CPAN.tcz
		[ $? = 0 ] && echo -n . || (echo $?; RESULT=1)
		$WGET ${LMSREPOSITORY}/slimserver-CPAN.tcz.dep/download -O /tmp/LMS/slimserver-CPAN.tcz.dep
		[ $? = 0 ] && echo -n . || (echo $?; RESULT=1)
		$WGET ${LMSREPOSITORY}/slimserver-CPAN.tcz.md5.txt/download -O /tmp/LMS/slimserver-CPAN.tcz.md5.txt
		[ $? = 0 ] && echo -n . || (echo $?; RESULT=1)
		$WGET ${LMSREPOSITORY}/slimserver.tcz.md5.txt/download -O /tmp/LMS/slimserver.tcz.md5.txt
		[ $? = 0 ] && echo -n . || (echo $?; RESULT=1)
		$WGET ${LMSREPOSITORY}/slimserver.tcz.dep/download -O /tmp/LMS/slimserver.tcz.dep
		[ $? = 0 ] && echo -n . || (echo $?; RESULT=1)
		$WGET ${LMSREPOSITORY}/slimserver.tcz/download -O /tmp/LMS/slimserver.tcz
		[ $? = 0 ] && echo . || (echo $?; RESULT=1)

		echo -n '<p class="info">[ INFO ] '
		sudo -u tc tce-load -w gcc_libs.tcz
		echo '<p>'
		echo -n '<p class="info">[ INFO ] '
		sudo -u tc tce-load -w perl5.tcz
		echo '<p>'

		if [ $RESULT = 0 ]; then
			echo '<p class="ok">[ OK ] Download successful.</p>'
			sudo /usr/local/etc/init.d/slimserver stop >/dev/null 2>&1
			sudo chown -R tc:staff /tmp/LMS
			sudo chmod 664 /tmp/LMS/*
			sudo cp -a /tmp/LMS/* /mnt/mmcblk0p2/tce/optional/
			sudo rm -f /tmp/LMS
		else
			echo '<p class="error">[ ERROR ] LMS download unsuccessful, try again!</p>'
		fi
	else
		echo '<p class="error">[ ERROR ] LMS not available in repository, try again later!</p>'
	fi
}

pcp_install_lms() {
	echo '<p class="info">[ INFO ] Installing LMS...</p>'
	[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] LMS is added to onboot.lst</p>'
	sudo sed -i '/slimserver.tcz/d' /mnt/mmcblk0p2/tce/onboot.lst
	sudo echo 'slimserver.tcz' >> /mnt/mmcblk0p2/tce/onboot.lst
}

pcp_remove_lms() {
	echo '<p class="info">[ INFO ] Removing LMS...</p>'
	sudo /usr/local/etc/init.d/slimserver stop >/dev/null 2>&1
	sudo rm -f /mnt/mmcblk0p2/tce/optional/slimserver-CPAN*
	sudo rm -f /mnt/mmcblk0p2/tce/optional/slimserver.tcz*
	sudo rm -f /mnt/mmcblk0p2/tce/optional/gcc_libs.tcz
	sudo rm -f /mnt/mmcblk0p2/tce/optional/perl5.tcz
	sudo rm -f /mnt/mmcblk0p2/tce/optional/perl5.tcz.md5.txt
	sudo rm -rf /mnt/mmcblk0p2/tce/slimserver/
	sudo sed -i '/slimserver.tcz/d' /mnt/mmcblk0p2/tce/onboot.lst
}

pcp_lms_padding() {
	pcp_toggle_row_shade
	echo '            <tr class="padding '$ROWSHADE'">'
	echo '              <td></td>'
	echo '              <td></td>'
	echo '            </tr>'
}

#========================================================================================
# Warning message
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
	echo '                <p style="color:white"><b>Note:</b> This is our first implementation of Logitech Media Server (LMS), so there are some limitations.</p>'
	echo '                <ul>'
	echo '                  <li style="color:white">Support for USB drives only.</li>'
	echo '                  <li style="color:white">LMS upgrade is via command line only.</li></br>'
	echo '                  <li style="color:white">Many thanks to Paul123 and jgrulich.</li>'
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
#----------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------
case $ACTION in
	Start)
		echo '<p class="info">[ INFO ] Starting LMS...</p>'
		echo -n '<p class="info">[ INFO ] '
		sudo /usr/local/etc/init.d/slimserver start
		;;
	Stop)
		echo '<p class="info">[ INFO ] Stopping LMS...</p>'
		echo -n '<p class="info">[ INFO ] '
		sudo /usr/local/etc/init.d/slimserver stop
		sleep 2
		;;
	Restart)
		echo '<p class="info">[ INFO ] Restarting LMS...</p>'
		echo -n '<p class="info">[ INFO ] '
		sudo /usr/local/etc/init.d/slimserver stop
		echo -n '<p class="info">[ INFO ] '
		sudo /usr/local/etc/init.d/slimserver start
		;;
	Install)
		pcp_sufficient_free_space 40000
		pcp_download_lms
		pcp_install_lms
		LMSERVER="yes"
		pcp_save_to_config
		pcp_backup
		pcp_reboot_required
		;;
	Remove)
		pcp_remove_lms
		LMSERVER="no"
		pcp_save_to_config
		pcp_backup
		pcp_reboot_required
		;;
	Mount)
		sudo rebuildfstab
		sleep 1
		DRIVES=$(fdisk -l | grep '^/dev/s' | awk -F "/" {'print $3'} | awk {'print $1'})
		for i in $(echo $DRIVES); do
		pcp_mount_device $i
		done
		pcp_backup
		;;
	*)
		pcp_warning_message
		;;
esac

#========================================================================================
# Main piCorePlayer operations
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Logitech Media Server (LMS) operations</legend>'
echo '          <table class="bggrey percent100">'

#------------------------------------LMS Indication--------------------------------------
if [ $(pcp_lms_status) = 0 ]; then
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
	no) SAMBAno="checked" ;;
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
	echo '                  <input type="submit" value="LMS autostart" />'
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
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                  <form name="Configure" action="'$LMS_SERVER_WEB_URL'" method="get" target="_blank">'
	echo '                    <input type="submit" value="Configure LMS" />'
	echo '                  </form>'
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
}
[ $MODE -ge $MODE_BETA ] && pcp_lms_configure_lms
#----------------------------------------------------------------------------------------

echo '            <form name="Start" action="'$0'" method="get">'

#------------------------------------------Install/uninstall LMS-------------------------
pcp_lms_install_lms() {
	pcp_incr_id
	pcp_toggle_row_shade
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
		echo '                  </div>'
	fi

	echo '                </td>'
	echo '              </tr>'
}
[ $MODE -ge $MODE_NORMAL ] && pcp_lms_install_lms
#----------------------------------------------------------------------------------------

#------------------------------------------Start LMS-------------------------------------
pcp_lms_start_lms() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="ACTION" value="Start" />'
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
}
[ $MODE -ge $MODE_NORMAL ] && pcp_lms_start_lms
#----------------------------------------------------------------------------------------

#------------------------------------------Stop LMS--------------------------------------
pcp_lms_stop_lms() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="ACTION" value="Stop" />'
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
}
[ $MODE -ge $MODE_NORMAL ] && pcp_lms_stop_lms
#----------------------------------------------------------------------------------------

#---------------------------------Restart LMS--------------------------------------------
pcp_lms_restart_lms() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="ACTION" value="Restart" />'
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
}
[ $MODE -ge $MODE_NORMAL ] && pcp_lms_restart_lms
#----------------------------------------------------------------------------------------


#---------------------------------Mount USB drives--------------------------------------------
pcp_mount() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="ACTION" value="Mount" />'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Scan and mount available USB drives&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Please attach your USB drive then pCP will scan and mount the drives so LMS can find your music.</p>'
	echo '                    <p><b>Note:</b></p>'
	echo '                    <ul>'
	echo '                      <li>For now only FAT32 and linux partitions are supported NTFS is work in progress.</li>'
	echo '                    </ul>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
}
[ $MODE -ge $MODE_NORMAL ] && pcp_mount
#----------------------------------------------------------------------------------------


#-------------------------------Show LMS logs--------------------------------------------
pcp_lms_show_logs() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" value="Show Logs" />'
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



#------------------------------------------Update LMS------------------------------------
pcp_lms_update() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" value="Update LMS" />'
	echo '                </td>'
	echo '                <td class="column100">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Update LMS&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>This will update LMS.</p>'
	echo '                    <p><b>Note:</b></p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_lms_update
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
[ $LOGSHOW = yes ] && pcp_lms_logview
#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------

#------------------------------------------SAMBA mode fieldset---------------------------
if [ $MODE -ge $MODE_DEVELOPER ]; then
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>SAMBA operations</legend>'
	echo '          <table class="bggrey percent100">'
fi

#----------------------------------------------------------------------------------------

pcp_samba_indication() {

	if [ $(pcp_samba_status) = 0 ]; then
		SB_IMAGE="green.png"
		SB_STATUS="running"
	else
		SB_IMAGE="red.png"
		SB_STATUS="not running"
	fi

	pcp_incr_id
	pcp_start_row_shade
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150">'
	echo '                <p class="centre"><img src="../images/'$SB_IMAGE'" alt="'$SB_STATUS'"></p>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>Samba is '$SB_STATUS'&nbsp;&nbsp;'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <ul>'
	echo '                    <li>GREEN = Samba running.</li>'
	echo '                    <li>RED = Samba not running.</li>'
	echo '                  </ul>'
	echo '                  <p><b>Note:</b></p>'
	echo '                  <ul>'
	echo '                    <li>Samba must be running to access music folder from computers on network.</li>'
	echo '                  </ul>'
	echo '                </div>'
	echo '              </td>'
	echo '            </tr>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_samba_indication

#------------------------------------------Enable/download Samba-------------------------
pcp_samba_enable() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                  <form name="Enable" action="writetolms.cgi" method="get">'
	echo '                    <input type="submit" value="Enable" />'
	echo '                  </form>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="small1" type="radio" name="SAMBA" value="yes" '$SAMBAyes'>Yes'
	echo '                  <input class="small1" type="radio" name="SAMBA" value="no" '$SAMBAno'>No'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Enable and download Samba file server  <a href="samba_conf.cgi" style="color: #FF0000;">Click to configure</a>&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Download Samba from repro.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_samba_enable

#------------------------------------------Start SAMBA-----------------------------------
pcp_samba_start() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150 center">'
	echo '                <form name="Stop" action="samba.cgi" method="get">'
	echo '                  <input type="submit" value="Start" />'
	echo '                </form>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>Start Samba file server&nbsp;&nbsp;'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <p>This will start Samba file server.</p>'
	echo '                  <p>Click [Start] to start Samba.</p>'
	echo '                  <p><b>Note:</b></p>'
	echo '                  <ul>'
	echo '                    <li>Samba running indicator will turn green.</li>'
	echo '                  </ul>'
	echo '                </div>'
	echo '              </td>'
	echo '            </tr>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_samba_start
#----------------------------------------------------------------------------------------

#------------------------------------------Stop------------------------------------------
pcp_samba_stop() {
	pcp_incr_id
	pcp_start_row_shade
	pcp_toggle_row_shade
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150 center">'
	echo '                <form name="Stop" action="stop.cgi" method="get">'
	echo '                  <input type="submit" value="Stop" />'
	echo '                </form>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>Stop Samba file server&nbsp;&nbsp;'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <p>This will stop Samba file server.</p>'
	echo '                  <p>Click [Stop] to stop Samba file server.</p>'
	echo '                  <p><b>Note:</b></p>'
	echo '                  <ul>'
	echo '                    <li>Samba running indicator will turn red.</li>'
	echo '                  </ul>'
	echo '                </div>'
	echo '              </td>'
	echo '            </tr>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_samba_stop
#----------------------------------------------------------------------------------------

pcp_footer
pcp_mode
pcp_copyright

echo '</body>'
echo '</html>'