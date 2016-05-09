#!/bin/sh

# Version: 2.05 2016-04-15 PH
#	Original.

. pcp-lms-functions
. pcp-rpi-functions
. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "LMS Update Page" "PH"

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

if [ -e /tmp/slimupdate/update_url ]; then
	UPDATEURL=$(cat "/tmp/slimupdate/update_url")
else
	UPDATEURL=""
fi

#----------------------------------------------------------------------------------------
case "$ACTION" in
	nothing)
		;;
	*)
#		pcp_warning_message
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
echo '          <legend>Update the local Logitech Media Server (LMS)</legend>'
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

#-----------------------------------Show Update Availiable----------------------------------------
pcp_lms_update_url() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '            <form name="Update" action="writetolms.cgi">'
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	if [ "$UPDATEURL" = "" ]; then
		echo '                </td>'
		echo '                <td>'
		echo '                <p>No Update Found!</p>'
	else
		echo '                  <input type="submit" name="UPDATE" value="Update" />'
		echo '                </td>'
		echo '                <td>'
		echo '                  <p>LMS Update Found:</p>'
		echo '                  <p>'$UPDATEURL'</p>'
		echo '                  <p>Download and update LMS&nbsp;&nbsp;'
		echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
		echo '                  </p>'
		echo '                  <div id="'$ID'" class="less">'
		echo '                    <p>The update process will take some minutes and finally LMS will restart.</p>'
		echo '                  </div>'
	fi
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_BETA ] && pcp_lms_update_url

#-----------------------------------Configure LMS----------------------------------------
pcp_lms_configure_lms() {
	[ x"" = x"$LMSWEBPORT" ] && LMSPORT=9000 || LMSPORT=$LMSWEBPORT
	[ x"" = x"$(pcp_eth0_ip)" ] && LMS_SERVER_WEB=$(pcp_wlan0_ip) || LMS_SERVER_WEB=$(pcp_eth0_ip)
	LMS_SERVER_WEB_URL="http://${LMS_SERVER_WEB}:${LMSPORT}/settings/index.html"

	pcp_incr_id
	pcp_toggle_row_shade
	echo '            <form name="Configure" action="'$LMS_SERVER_WEB_URL'" target="_blank">'
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>No Update file was found, Please check LMS Server configuration.&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Click Configure Below.</p>'
	echo '                    <p>Then go to Advanced Tab, Software Updates Dropdown Box.</p>'
	echo '                    <p>Make sure Automatic Updates and Frequency are set to your needs, or .</p>'
	echo '                    <p>Check for Updates Manually.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" value="LMS Settings" />'
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
[ $MODE -ge $MODE_BETA -a -z $UPDATEURL ] && pcp_lms_configure_lms
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
exit
