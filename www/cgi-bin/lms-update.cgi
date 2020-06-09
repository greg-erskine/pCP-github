#!/bin/sh

# Version: 7.0.0 2020-06-09

. pcp-functions
. pcp-rpi-functions
. pcp-lms-functions

pcp_html_head "LMS Update Page" "PH"

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

LMS_SERV_LOG="${LOGS}/server.log"
LMS_SCAN_LOG="${LOGS}/scanner.log"
WGET="/bin/busybox wget"

REBOOT_REQUIRED=0

COLUMN2_1="col-sm-2"
COLUMN2_2="col-10"
#---------------------------Routines-----------------------------------------------------
if [ -e /tmp/slimupdate/update_url ]; then
	UPDATEURL=$(cat "/tmp/slimupdate/update_url")
else
	UPDATEURL=""
fi

#========================================================================================
# Main table
#----------------------------------------------------------------------------------------
pcp_heading5 "Update the local Logitech Media Server (LMS)"

#------------------------------------LMS Indication--------------------------------------
if [ $(pcp_lms_status) -eq 0 ]; then
	pcp_green_tick "running"
else
	pcp_red_cross "not running"
fi

case $ACTION in
	Nightly)
		pcp_border_begin
		echo '    <div class="row mx-1">'
		echo '      <div class="col-1 col-lg-1 ml-1 text-right">'$INDICATOR'</div>'
		pcp_incr_id
		echo '      <div class="col-10 col-lg-3">'
		echo '        <p>LMS is '$STATUS'&nbsp;&nbsp;'
		pcp_helpbadge
		echo '        </p>'
		echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
		echo '          <ul>'
		echo '            <li>'$(pcp_bi_check)' = LMS running.</li>'
		echo '            <li>'$(pcp_bi_x)' = LMS not running.</li>'
		echo '          </ul>'
		echo '          <p><b>Note:</b></p>'
		echo '          <ul>'
		echo '            <li>LMS must be running to stream music to players from this pCP.</li>'
		echo '          </ul>'
		echo '        </div>'
		echo '      </div>'
		echo '    </div>'
		#----------------------------------------------------------------------------------------

		#---------------------------------Show Update Available----------------------------------
		pcp_lms_update_url() {
			if [ "$UPDATEURL" = "" ]; then
				echo '    <div class="row mx-1">'
				echo '      <div class="'$COLUMN2_2'">'
				echo '        <p>No Update Found!</p>'
				echo '      </div>'
				echo '    </div>'
			else
				echo '    <div class="row mx-1">'
				echo '      <div class="'$COLUMN2_1'">'
				echo '        <form name="Update" action="writetolms.cgi">'
				echo '          <input class="'$BUTTON'" type="submit" name="ACTION" value="Update">'
				echo '        </form>'
				echo '      </div>'
				pcp_incr_id
				echo '      <div class="'$COLUMN2_2'">'
				echo '        <p>LMS Update Found:</p>'
				echo '        <p>'$UPDATEURL'</p>'
				echo '        <p>Download and update LMS&nbsp;&nbsp;'
				pcp_helpbadge
				echo '        </p>'
				echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
				echo '          <p>The update process will take some minutes and finally LMS will restart.</p>'
				echo '        </div>'
				echo '      </div>'
				echo '    </div>'
			fi
		}
		[ $MODE -ge $MODE_SERVER ] && pcp_lms_update_url

		#-----------------------------------Configure LMS--------------------------------
		pcp_lms_configure_lms() {
			[ x"" = x"$LMSWEBPORT" ] && LMSPORT=9000 || LMSPORT=$LMSWEBPORT
			[ x"" = x"$(pcp_eth0_ip)" ] && LMS_SERVER_WEB=$(pcp_wlan0_ip) || LMS_SERVER_WEB=$(pcp_eth0_ip)
			LMS_SERVER_WEB_URL="http://${LMS_SERVER_WEB}:${LMSPORT}/settings/index.html"

			pcp_incr_id
			echo '            <div class="row mx-1">'
			echo '              <div class="col-12">'
			echo '                <p>No Update file was found, please check LMS Server configuration&nbsp;&nbsp;'
			pcp_helpbadge
			echo '                </p>'
			echo '                <div id="dt'$ID'" class="'$COLLAPSE'">'
			echo '                  <p>Click Configure Below.</p>'
			echo '                  <p>Then go to Advanced Tab, Software Updates Dropdown Box.</p>'
			echo '                  <p>Make sure Automatic Updates and Frequency are set to your needs, or</p>'
			echo '                  <p>Check for Updates Manually.</p>'
			echo '                </div>'
			echo '              </div>'
			echo '            </div>'
			pcp_incr_id
			echo '            <div class="row mx-1">'
			echo '              <div class="'$COLUMN2_1'">'
			echo '                <form name="Configure" action="'$LMS_SERVER_WEB_URL'" target="_blank">'
			echo '                  <input class="'$BUTTON'" type="submit" value="LMS Settings">'
			echo '                </form>'
			echo '              </div>'
			echo '              <div class="'$COLUMN2_2'">'
			echo '                <p>Configure LMS&nbsp;&nbsp;'
			pcp_helpbadge
			echo '                </p>'
			echo '                <div id="dt'$ID'" class="'$COLLAPSE'">'
			echo '                  <p>Use the standard LMS web interface to adjust the LMS settings.</p>'
			echo '                </div>'
			echo '              </div>'
			echo '            </div>'
		}
		[ $MODE -ge $MODE_SERVER -a -z $UPDATEURL ] && pcp_lms_configure_lms
		#--------------------------------------------------------------------------------
		pcp_border_end
	;;
	Binary)
		pcp_infobox_begin
		pcp_message INFO "Checking for slimserver-CPAN.tcz updates..." "text"
		sudo -u tc pcp-update slimserver-CPAN.tcz
		[ $? -eq 0 ] && REBOOT_REQUIRED=1
		pcp_infobox_end
	;;
esac

[ $REBOOT_REQUIRED = 1 ] && pcp_reboot_required

pcp_redirect_button "Go to LMS" "lms.cgi" 15

pcp_html_end
exit
