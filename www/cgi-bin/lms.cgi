#!/bin/sh

# Version: 0.03 2016-04-14 PH
#	Updated warning message.
#	Added Mounting of disks.
#	Added additional file system support.
#	Added Location for LMS Server Persistent Data.
#	Added LMS Server Update Script.

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

df | grep -qs ntfs
[ "$?" = "0" ] && NTFS="yes" || NTFS="no"

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
		[ $? = 0 ] && echo -n . || (echo $?; RESULT=1)
		echo '<p>'
		echo -n '<p class="info">[ INFO ] '
		sudo -u tc tce-load -w perl5.tcz
		[ $? = 0 ] && echo -n . || (echo $?; RESULT=1)
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
#   Lets not remove the cache automatically......Todo....put a clear Cache Option on the page
#	sudo rm -rf /mnt/mmcblk0p2/tce/slimserver/
	sudo sed -i '/slimserver.tcz/d' /mnt/mmcblk0p2/tce/onboot.lst
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
	echo -n '<p class="info">[ INFO ] '
	sudo -u tc tce-load -w ntfs-3g.tcz
	[ $? = 0 ] && echo -n . || (echo $?; RESULT=1)
	echo '<p>'
	echo -n '<p class="info">[ INFO ] Loading'
	sudo -u tc tce-load -i ntfs-3g.tcz
	[ $? = 0 ] && echo -n . || (echo $?; RESULT=1)
	echo '<p>'
	if [ $RESULT = 0 ]; then
		echo "ntfs-3g.tcz" >> /mnt/mmcblk0p2/tce/onboot.lst
		echo '<p class="info">[ INFO ] NTFS Support Loaded...</p>'
	else
		echo '<p class="error">[ ERROR ] ntfs-3g.tcz not loaded, try again later!</p>'
	fi
}

pcp_remove_fs() {
	echo '<p class="info">[ INFO ] Removing Extensions</p>'
	rm -f /mnt/mmcblk0p2/tce/optional/ntfs-3g*
	rm -f /mnt/mmcblk0p2/tce/optional/filesystems*
	sed -i '/ntfs-3g.tcz/d' /mnt/mmcblk0p2/tce/onboot.lst
	echo '<p class="info">[ INFO ] Extensions Removed, Reboot to Finish</p>'
}

#----------------------------------------------------------------------------------------
case "$ACTION" in
	Start)
		case "$LMSDATA" in
			usbmount) MNT="/mnt/$MOUNTPOINT";;
			netmount1) MNT="/mnt/$NETMOUNT1POINT";;
			default) MNT="/mnt/mmcblk0p2";;
		esac
		mount | grep -qs $MNT
		if [ "$?" = "0" ]; then 
			echo '<p class="info">[ INFO ] Starting LMS...</p>'
			echo -n '<p class="info">[ INFO ] '
			sudo /usr/local/etc/init.d/slimserver start
		else
			echo '<p class="error">[ ERROR ] LMS data disk failed mount, LMS will not start.'
		fi
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
	Install_FS)
		pcp_sufficient_free_space 4000
		pcp_install_fs
		;;
	Remove_FS)
		pcp_remove_fs
		pcp_reboot_required
		;;
	*)
		pcp_warning_message
		;;
esac

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
	echo '            <form name="Configure" action="'$LMS_SERVER_WEB_URL'" target="_blank">'
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" value="Configure LMS" />'
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
		echo '                  </div>'
	fi
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_NORMAL ] && pcp_lms_install_lms
#----------------------------------------------------------------------------------------

#------------------------------------------Start LMS-------------------------------------
pcp_lms_start_lms() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '            <form name="Start" action="'$0'">'
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
	echo '            </form>'
}
[ $MODE -ge $MODE_NORMAL ] && pcp_lms_restart_lms
#----------------------------------------------------------------------------------------

#---------------------------------Update LMS--------------------------------------------
pcp_update_lms() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '            <form name="Update" action="writetolms.cgi">'
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="UPDATE" value="Update" />'
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
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column'$COL1' center"><p><b>Enabled</b></p></td>'
	echo '                <td class="column'$COL2'"><p><b>Mount Type</b></p></td>'
	echo '                <td class="column'$COL3'"><p><b>LMS Data Storage Location</b></p></td>'
	echo '                <td>'
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
		echo '                <td></td>'
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
		echo '                <td></td>'
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
	echo '                <td></td>'
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
[ $MODE -ge $MODE_BETA ] && pcp_slimserver_persistence
	

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
	if [ ! -f /mnt/mmcblk0p2/tce/optional/ntfs-3g.tcz ]; then
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
[ $MODE -ge $MODE_BETA ] && pcp_extra_filesys
#----------------------------------------------------------------------------------------

#========================================================================================
# USB Disk Mounting Operations
#----------------------------------------------------------------------------------------
pcp_mount_usbdrives() {
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
	echo '                  <p>/mnt/ <input class="large12" type="text" name="MOUNTPOINT" value="'$MOUNTPOINT'" required pattern="^[a-zA-Z0-9_]{1,32}$"><p>'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>This is the mount point for the below drive.&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>The drive will be mounted by UUID to this path and will be automounted on startup.</p>'
	echo '                    <p>Alpha-numeric pathnames required (up to 32 characters).</p>'
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
			SIZE=$(fdisk -l | grep $i | tr -s " " | cut -d " " -f4 | tr -d +)
			[ $SIZE -gt 10485760 ] && SIZExB="`expr $SIZE / 1048576` GB" || SIZExB="`expr $SIZE / 1024` MB"
			case "$MOUNTUUID" in
				"$UUID")
					UUIDyes="checked"
					DISKFOUND="yes"
				;;
				*) UUIDyes="" ;;
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
[ $MODE -ge $MODE_BETA ] && pcp_mount_usbdrives

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
	echo '                  <p>/mnt/ <input class="large12" type="text" name="NETMOUNT1POINT" value="'$NETMOUNT1POINT'" required pattern="^[a-zA-Z0-9_]{1,32}$"></p>'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>This is the mount point for the below network share.&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>The network share will be mounted by to this path and will be automounted on startup.</p>'
	echo '                    <p>IP address is only the IP address.  Do not enter any / or :</p>'
	echo '                    <p>Share for CIFS is the share name only (DO not use /).</p>'
#	echo '                    <p>Share for NFS is the complete volume i.e. /volume1/Media (DO not use :).</p>'
	echo '                    <p>Share for NFS is not working yet.</p>'
	echo '                    <p>Options are a comma delimited list of mount options. Ref mount man pages.</p>'
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

#	echo '                  <select class="large6" name="NETMOUNT1FSTYPE" title="Only cifs(samba) and nfs shares are supported">'
	echo '                  <select class="large6" name="NETMOUNT1FSTYPE" title="Only cifs(samba) are supported at this time">'
	echo '                    <option value="cifs" '$CIFS1yes'>CIFS</option>'
#	echo '                    <option value="nfs" '$NFS1yes'>NFS</option>'
	echo '                  </select>'
	echo '                </td>'
	echo '                <td class="column'$COL5'">'
	echo '                  <input class="large6" type="text" name="NETMOUNT1USER" value="'$NETMOUNT1USER'" title="Enter the Username for the remote share.">'
	echo '                </td>'
	echo '                <td class="column'$COL6'">'
	echo '                  <input class="large6" type="text" name="NETMOUNT1PASS" value="'$NETMOUNT1PASS'" title="Enter the Password for the remote share.">'
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
[ $MODE -ge $MODE_BETA ] && pcp_mount_netdrives
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

pcp_footer
pcp_mode
pcp_copyright

echo '</body>'
echo '</html>'
exit

#-------------Steen Delete Samba Stuff???? - scp should be used to copy files to pCP -------------------------------
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
