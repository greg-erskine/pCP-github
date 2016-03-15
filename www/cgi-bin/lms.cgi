#!/bin/sh

# Version: 0.02 2016-03-10 SBP
#	Added LMS log view, space check and hide SAMBA and update LMS options.
#	Moved pcp_lms_status to pcp-lms-functions.

# Version: 0.01 2016-01-30 SBP
#	Original.

. pcp-lms-functions
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

#Read from slimserver.cfg file
CFG_FILE="/home/tc/.slimserver.cfg"
TCEDIR=$(readlink "/etc/sysconfig/tcedir")

if [ -f "$CFG_FILE" ]; then
        . $CFG_FILE
fi

#Set Default Settings if not defined in CFG_FILE
[ -n "$CACHE" ] || CACHE=$TCEDIR/slimserver/Cache
[ -n "$LOGS" ] || LOGS=/var/log/slimserver
[ -n "$PREFS" ] || PREFS=$TCEDIR/slimserver/prefs
[ -n "$LMSUSER" ] || LMSUSER=tc
[ -n "$LMSGROUP" ] || LMSGROUP=staff

LMS_SERV_LOG=$LOGS'/server.log'
LMS_SCAN_LOG=$LOGS'/scanner.log'
WGET="/bin/busybox wget"
LMSREPOSITORY="https://sourceforge.net/projects/picoreplayer/files/tce/7.x/LMS"

#---------------------------Routines---------------------------------------------------------------------

pcp_download_lms() {
	cd /tmp
	sudo rm -f /tmp/LMS
	sudo mkdir /tmp/LMS
	echo '<p class="info">[ INFO ] Downloading LMS from repository...</p>'
	[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Repo: '${LMSREPOSITORY}'</p>'
	echo '<p class="info">[ INFO ] Download will take a few minutes. Please wait...</p>'

	$WGET -s ${LMSREPOSITORY}/slimserver-CPAN.tcz
	if [ $? = 0 ]; then
		RESULT=0
		echo '<p class="info">[ INFO ] Downloading Logitech Media Server LMS...'
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
		[ $? = 0 ] && echo -n . || (echo $?; RESULT=1)

		sudo -u tc tce-load -w gcc_libs.tcz
		sudo -u tc tce-load -w perl5.tcz

		if [ $RESULT = 0 ]; then
			echo '<p class="ok">[ OK ] Download successful.</p>'
			sudo /usr/local/etc/init.d/slimserver stop >/dev/null 2>&1
			sudo chown -R tc:staff /tmp/LMS
			sudo chmod -R 755 /tmp/LMS
			sudo cp -a /tmp/LMS/. /mnt/mmcblk0p2/tce/optional/
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


#-----------------------------------------------------------------------

case $ACTION in
	Start)
		sudo /usr/local/etc/init.d/slimserver start
		;;
	Stop)
		sudo /usr/local/etc/init.d/slimserver stop
		sleep 2
		;;
	Restart)
		sudo /usr/local/etc/init.d/slimserver stop
		sudo /usr/local/etc/init.d/slimserver start
		;;
	Install)
		pcp_download_lms
		pcp_install_lms
		pcp_backup
		pcp_reboot_required
		;;
	Remove)
		pcp_remove_lms
		pcp_backup
		pcp_reboot_required
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
pcp_main_lms_indication() {

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
	if [ $LOGSHOW = yes ]; then
		LOGSHOWyes="checked"
		else 
		LOGSHOWno="checked"
	fi



	#------------------------------------------------------------------------------------
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
}
pcp_main_lms_indication
#----------------------------------------------------------------------------------------

#------------------------------------------Padding---------------------------------------
pcp_main_padding() {
	pcp_toggle_row_shade
	echo '            <tr class="padding '$ROWSHADE'">'
	echo '              <td></td>'
	echo '              <td></td>'
	echo '            </tr>'
}
pcp_main_padding

#------------------------------------------Enable/disable autostart of LMS---------------------

pcp_LMS_enable() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '                  <form name="Select" action="writetolms.cgi" method="get">'
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                    <input type="submit" value="LMS autostart" />'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="small1" type="radio" name="LMSERVER" value="yes" '$LMSERVERyes'>Yes'
	echo '                  <input class="small1" type="radio" name="LMSERVER" value="no" '$LMSERVERno'>No'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Automatic start of LMS Server when pCP boots&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Yes - will enable automatic start of LMS when pCP boots.</p>'
	echo '                    <p>No - will disable automatic start of LMS when pCP boots.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '                  </form>'
}
pcp_LMS_enable

#------------------------------------------Install/uninstall LMS---------------------------------------
pcp_lms_start() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150 center">'
	echo '                <form name="Start" action="'$0'" method="get">'
		if [ ! -f /mnt/mmcblk0p2/tce/optional/slimserver.tcz ]; then
				pcp_sufficient_free_space 40000
	echo '                  <input type="submit" name="ACTION" value="Install" />'
		else
	echo '                  <input type="submit" name="ACTION" value="Remove" />'
		fi
	echo '                </form>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>Install or remove LMS from pCP&nbsp;&nbsp;'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <p>Install, this will install LMS on pCP.</p>'
	echo '                  <p>Remove, this will remove LMS and all the extra packages that was added with LMS.</p>'
	echo '                  </ul>'
	echo '                </div>'
	echo '              </td>'
	echo '            </tr>'
}
pcp_lms_start
#----------------------------------------------------------------------------------------

#------------------------------------------Start LMS---------------------------------------
pcp_lms_start() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150 center">'
	echo '                <form name="Start" action="'$0'" method="get">'
	echo '                  <input type="submit" name="ACTION" value="Start" />'
	echo '                </form>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>Start LMS&nbsp;&nbsp;'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <p>This will start LMS.</p>'
	echo '                  </ul>'
	echo '                </div>'
	echo '              </td>'
	echo '            </tr>'
}
pcp_lms_start
#----------------------------------------------------------------------------------------

#------------------------------------------Stop LMS--------------------------------------
pcp_lms_stop() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150 center">'
	echo '                <form name="Stop" action="'$0'" method="get">'
	echo '                  <input type="submit" name="ACTION" value="Stop" />'
	echo '                </form>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>Stop LMS&nbsp;&nbsp;'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <p>This will stop LMS.</p>'
	echo '                  </ul>'
	echo '                </div>'
	echo '              </td>'
	echo '            </tr>'
}
pcp_lms_stop
#----------------------------------------------------------------------------------------

#-------------------------------Restart - LMS--------------------------------------------
pcp_lms_restart() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150 center">'
	echo '                <form name="Restart" action="'$0'" method="get">'
	echo '                  <input type="submit" name="ACTION" value="Restart" />'
	echo '                </form>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>Restart LMS&nbsp;&nbsp;'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <p>This will kill LMS and then restart it.</p>'
	echo '                  <p><b>Note:</b></p>'
	echo '                  <ul>'
	echo '                    <li>A restart of LMS is rarely needed.</li>'
	echo '                    <li>LMS running indicator will turn green.</li>'
	echo '                  </ul>'
	echo '                </div>'
	echo '              </td>'
	echo '            </tr>'
}
pcp_lms_restart
#----------------------------------------------------------------------------------------

#-------------------------------Show LMS logs --------------------------------------------
pcp_lms_logshow() {

	pcp_incr_id
	pcp_toggle_row_shade
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150 center">'
	echo '                <form name="logshow" action="'$0'" method="get">'
	echo '                    <input type="submit" value="Show Logs" />'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="small1" type="radio" name="LOGSHOW" value="yes" '$LOGSHOWyes' >Yes'
	echo '                  <input class="small1" type="radio" name="LOGSHOW" value="no" '$LOGSHOWno' >No'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Show LMS logs below&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Show Server and Scanner log in text area below.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
}
pcp_lms_logshow
#----------------------------------------------------------------------------------------

#------------------------------------------Padding---------------------------------------
[ $MODE -le $MODE_BASIC ] && pcp_main_padding
#----------------------------------------------------------------------------------------

#------------------------------------------Update LMS------------------------------------
pcp_lms_update() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150 center">'
	echo '                <form name="InSitu" action="upd_lms.cgi" method="get">'
	echo '                  <input type="submit" value="Update LMS" />'
	echo '                </form>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>Update LMS&nbsp;&nbsp;'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <p>This will update LMS.</p>'
	echo '                  <p><b>Note:</b></p>'
	echo '                </div>'
	echo '              </td>'
	echo '            </tr>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_lms_update
#----------------------------------------------------------------------------------------

#------------------------------------------LMS log text area---------------------------
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
	echo '          </table>'
	echo '          <table class="bggrey percent100">'
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

if [ $LOGSHOW = yes ]; then
	pcp_lms_logview
fi
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

#----------------------------------------------------------------------------------------
echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------

pcp_footer
pcp_mode
pcp_copyright

echo '</body>'
echo '</html>'