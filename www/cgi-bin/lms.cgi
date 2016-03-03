#!/bin/sh

# Version: 0.01 2016-01-30 SBP
#	Original.

. pcp-lms-functions
. pcp-functions
pcp_variables
. $CONFIGCFG

DEBUG=1

pcp_html_head "LMS Main Page" "SBP"

[ $MODE -ge $MODE_NORMAL ] && pcp_picoreplayers
[ $MODE -ge $MODE_ADVANCED ] && pcp_controls
pcp_banner
pcp_navigation
pcp_running_script
pcp_httpd_query_string

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
esac

pcp_lms_status() {
	RESULT=$(sudo /usr/local/etc/init.d/slimserver status)
	echo $RESULT
}

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

	if [ "x" != "x$(pcp_lms_status)" ]; then
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
	echo '                    <li>LMS must be running to stream music to players.</li>'
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

#------------------------------------------Enable/download LMS---------------------------

pcp_LMS_enable() {
	pcp_incr_id
	pcp_toggle_row_shade
	
		echo '                  <form name="Enable" action="writetolms.cgi" method="get">'
	
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'

	echo '                    <input type="submit" value="Enable" />'

	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="small1" type="radio" name="LMSERVER" value="yes" '$LMSERVERyes'>Yes'
	echo '                  <input class="small1" type="radio" name="LMSERVER" value="no" '$LMSERVERno'>No'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Enable and download LMS Server&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Download LMS from repo.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	
		echo '                  </form>'
}

pcp_LMS_enable

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
[ $MODE -ge $MODE_NORMAL ] && pcp_lms_update
#----------------------------------------------------------------------------------------

#------------------------------------------SAMBA mode fieldset---------------------------
if [ $MODE -ge $MODE_ADVANCED ]; then
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
pcp_samba_indication

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
pcp_samba_enable

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
pcp_samba_start
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
pcp_samba_stop
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