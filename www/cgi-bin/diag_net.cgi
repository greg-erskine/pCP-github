#!/bin/sh
# Raspberry Pi network throughput diagnostics script

# Version: 5.0.0 2019-04-20

. pcp-functions
. pcp-rpi-functions

pcp_html_head "Raspberry Pi Network Diagnostics" "PH"

pcp_banner
pcp_diagnostics
pcp_running_script
pcp_httpd_query_string

Set defaults.
[ "$IPERF3_SERVER_MODE" = "" ] && IPERF3_SERVER_MODE="no"
[ "$IPERF3_SEND" = "" ] && IPERF3_SEND="no"
[ "$IPERF3_UDP" = "" ] && IPERF3_UDP="yes"

# Maybe able to simplify the following routines?
pcp_diag_rpi_eth0_mac_address() {
	RESULT=$(pcp_eth0_mac_address)
	[ x"" = x"$RESULT" ] && echo "None" || echo $RESULT
}

pcp_diag_rpi_wlan0_mac_address() {
	RESULT=$(pcp_wlan0_mac_address)
	[ x"" = x"$RESULT" ] && echo "None" || echo $RESULT
}

pcp_diag_rpi_eth0_ip() {
	RESULT=$(pcp_eth0_ip)
	[ x"" = x"$RESULT" ] && echo "None" || echo $RESULT
}

pcp_diag_rpi_wlan0_ip() {
	RESULT=$(pcp_wlan0_ip)
	[ x"" = x"$RESULT" ] && echo "None" || echo $RESULT
}

pcp_diag_rpi_lmsip() {
	RESULT=$(pcp_lmsip)
	[ x"" = x"$RESULT" ] && echo "None" || echo $RESULT
}

pcp_install_iperf3() {
	RESULT=0
	echo '[ INFO ] Downloading iperf3.</p>'
	sudo -u tc pcp-load -r $PCP_REPO -w iperf3.tcz
	if [ -f $TCEMNT/tce/optional/iperf3.tcz ]; then
		echo '[ INFO ] Loading iperf3'
		sudo -u tc tce-load -i iperf3.tcz
		[ $? -eq 0 ] && echo -n . || (echo $?; RESULT=1)
		if [ $RESULT -eq 0 ]; then
			echo '[ INFO ] Iperf3 loaded...</p>'
		else
			echo '[ ERROR ] Extensions not loaded, try again later!</p>'
		fi
	fi
}

pcp_remove_iperf3() {
	echo '[ INFO ] Removing Extensions</p>'
	sudo -u tc tce-audit builddb
	sudo -u tc tce-audit delete iperf3.tcz
	echo '[ INFO ] Extensions are marked for removal. You must reboot to finish!</p>'
}

pcp_load_iperf3() {
	sudo -u tc pcp-load -i iperf3.tcz
}

REBOOT_REQUIRED=0
case "$ACTION" in
	Stop)
		pkill iperf3
	;;
	Load)
		pcp_table_top "Loading Iperf3"
		echo '                <textarea class="inform" style="height:60px">'
		pcp_load_iperf3
		echo '                </textarea>'
		pcp_table_end
	;;
	Install)
		pcp_table_top "Downloading Iperf3"
		pcp_sufficient_free_space 72
		if [ $? -eq 0 ] ; then
			echo '                <textarea class="inform" style="height:160px">'
			pcp_install_iperf3
			echo '                </textarea>'
			pcp_table_end
		fi
	;;
	Remove)
		pcp_table_top "Removing Iperf3"
		echo '                <textarea class="inform" style="height:120px">'
		echo '[ INFO ] Removing iperf3 Extension...'
		echo
		echo 'After a reboot these extensions will be permanently deleted:'
		pcp_remove_iperf3
		pcp_backup "nohtml"
		echo '                </textarea>'
		pcp_table_end
		REBOOT_REQUIRED=1
	;;
	Start)
		echo '<form id="Stop" name="Stop Iperf" action="'$0'">'
		pcp_table_top "Iperf3 Control"
		pcp_start_row_shade
		echo '            <tr class="'$ROWSHADE'">'
		echo '                <td class="column150 center">'
		echo '                  <button type="submit" name="ACTION" value="Stop" >Stop</button>'
		echo '                  <input type="hidden" name="IPERF3_SERVER_MODE" value="'$IPERF3_SERVER_MODE'">'
		echo '                  <input type="hidden" name="IPERF3_SEND" value="'$IPERF3_SEND'">'
		echo '                  <input type="hidden" name="IPERF3_UDP" value="'$IPERF3_UDP'">'
		echo '                  <input type="hidden" name="IPERF_SERVER_IP" value="'$IPERF_SERVER_IP'">'
		echo '                </td>'
		echo '                <td>'
		echo '                  <p>Stop iperf testing.</p>'
		echo '                </td>'
		echo '              </tr>'
		pcp_table_end
		echo '</form>'
		
		pcp_table_top "Iperf3 Output"
		echo '                <textarea class="inform" style="height:240px">'
		if [ $(pcp_squeezelite_status) -eq 0 ]; then
			echo '[ WARN ] Squeezelite is running, results might be affected'
			echo '[ WARN ] Goto Main menu and stop squeezelite'
		fi

		REV=""
		if [ "$IPERF3_SERVER_MODE" = "no" ]; then 
			if [ "$IPERF3_UDP" = "no" ]; then
				UDP=""
				echo "[ INFO ] Iperf running in TCP Mode."
			else
				UDP="-u"
				echo "[ INFO ] Iperf running in UDP Mode."
			fi
			if [ "$IPERF3_SEND" = "no" ]; then
				REV="-R"
				echo "[ INFO ] Iperf running in Receive Mode."
			else
				REV=""
				echo "[ INFO ] Iperf running in Send Mode."
			fi
			if [ "$IPERF3_UDP" = "yes" -a "$IPERF3_SEND" = "no" ]; then
				DURATION="-t 21 -O 1"
				echo "[ INFO ] Ommiting 1st second of transmission, likely due to server being faster than rpi."
			else
				DURATION="-t 20"
			fi
		fi

		if [ "$IPERF3_SERVER_MODE" = "no" ]; then
			IPERF_SERVER_PORT=$(echo $IPERF_SERVER_IP | awk -F':' '{ print $2 }')
			IP3_IP=$(echo $IPERF_SERVER_IP | awk -F':' '{ print $1 }')
			[ "$IPERF_SERVER_PORT" = "" ] && IPERF_SERVER_PORT=5201
			IPERF_COMMAND="iperf3 -c $IP3_IP -p $IPERF_SERVER_PORT -V $UDP -b 300M $DURATION $REV"
			echo "[ INFO ] Iperf will run for 20 seconds, then output will show......."
		else
			echo "[ INFO ] Iperf running in server mode.  Press stop to quit."
			echo "[ INFO ] Set Client to use IP Address: $(pcp_eth0_ip) or $(pcp_wlan0_ip)"
			IPERF_COMMAND="iperf3 -s -V"
		fi
		[ $DEBUG -eq 1 ] && echo "[ DEBUG ] Iperf command: $IPERF_COMMAND"
		
		$IPERF_COMMAND
		if [ $? -ne 0 ]; then
			echo "[ ERROR ] Iperf3 connection error, check to be sure server is running on selected <host>:<port>"
		fi
		echo '                </textarea>'
		pcp_table_end

		echo '<script>'
		echo '  document.getElementById("Stop").style.display="none";'
		echo '</script>'
	;;
esac


#========================================================================================
# Raspberry Pi Network Performance Diagnostics
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Raspberry Pi Network</legend>'
echo '          <table class="bggrey percent100">'
#-------------------------------------Row 1----------------------------------------------
pcp_start_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td class="column150">'
echo '                <p>Model:</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>'$(pcp_rpi_model)'</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>eth0 IP:</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>'$(pcp_diag_rpi_eth0_ip)'</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>Physical MAC:</p>'
echo '              </td>'
echo '              <td>'
echo '                <p>'$(pcp_diag_rpi_eth0_mac_address)'</p>'
echo '              </td>'
echo '            </tr>'
#-------------------------------------Row 2----------------------------------------------
pcp_toggle_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td class="column150">'
echo '                <p>Revison:</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>'$(pcp_rpi_revision)'</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>wlan0 IP:</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>'$(pcp_diag_rpi_wlan0_ip)'</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>Wireless MAC:</p>'
echo '              </td>'
echo '              <td>'
echo '                <p>'$(pcp_diag_rpi_wlan0_mac_address)'</p>'
echo '              </td>'
echo '            </tr>'
#-------------------------------------Row 3----------------------------------------------
pcp_toggle_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td class="column150">'
echo '                <p>PCB Revison:</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>'$(pcp_rpi_pcb_revision)'</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>LMS IP:</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>'$(pcp_diag_rpi_lmsip)'</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>Controls MAC:</p>'
echo '              </td>'
echo '              <td>'
echo '                <p>'$(pcp_controls_mac_address)'</p>'
echo '              </td>'
echo '            </tr>'
#----------------------------------------------------------------------------------------
echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#========================================================================================
# piCorePlayer
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>piCorePlayer</legend>'
echo '          <table class="bggrey percent100">'
pcp_start_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td class="column150">'
echo '                <p>Version:</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>'$(pcp_picoreplayer_version)'</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>pCP name:</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>'$NAME'</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>Hostname:</p>'
echo '              </td>'
echo '              <td>'
echo '                <p>'$HOST'</p>'
echo '              </td>'
echo '            </tr>'
echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'

#========================================================================================
# Network Performance
#----------------------------------------------------------------------------------------
echo '<form name="IPERF" action="'$0'">'
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Network Performance (iperf3)</legend>'
echo '          <table class="bggrey percent100">'
pcp_incr_id
pcp_start_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '                <td class="column150 center">'
if [ ! -f $TCEMNT/tce/optional/iperf3.tcz ]; then
	echo '                  <input type="submit" name="ACTION" value="Install" />'
	echo '                </td>'
	echo '                <td colspan=2>'
	echo '                  <p>Install iperf3 on pCP&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>This will install iperf3 network performance testing.</p>'
	echo '                    <p>You will need to run iperf3 on another machine, preferrably your LMS server.</p>'
	echo '                  </div>'
else
	echo '                  <input type="submit" name="ACTION" value="Remove" onclick="return confirm('\''This will remove LMS from pCP.\n\nAre you sure?'\'')"/>'
	echo '                </td>'
	echo '                <td colspan=2>'
	echo '                  <p>Remove iperf3 from pCP&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>This will remove the iperf3 extension.</p>'
	echo '                  </div>'
fi
echo '                </td>'
echo '              </tr>'

if [ -x /usr/local/bin/iperf3 ]; then
	[ "$IPERF3_SERVER_MODE" = "no" ] && IPERF3_SERVER_MODEno="checked" || IPERF3_SERVER_MODEyes="checked"
	pcp_incr_id
	pcp_toggle_row_shade
	echo '            <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                  <button type="submit" name="ACTION" value="Server_Mode" >Change Mode</button>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="small1" type="radio" name="IPERF3_SERVER_MODE" value="yes" '$IPERF3_SERVER_MODEyes'>Yes'
	echo '                  <input class="small1" type="radio" name="IPERF3_SERVER_MODE" value="no" '$IPERF3_SERVER_MODEno'>No'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Set iperf to server mode&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Yes - This device will run in server mode.</p>'
	echo '                    <p>No - This device will run in client mode.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'

	if [ "$IPERF3_SERVER_MODE" = "no" ]; then
		pcp_incr_id
		pcp_toggle_row_shade
		echo '              <tr class="'$ROWSHADE'">'
		echo '                <td class="column150 center">'
		echo '                  <p class="row">Iperf3 Server IP</p>'
		echo '                </td>'
		echo '                <td class="column210">'
		echo '                  <input class="large15"'
		echo '                         type="text"'
		echo '                         name="IPERF_SERVER_IP"'
		echo '                         value="'$IPERF_SERVER_IP'"'
		echo '                         title="Iperf3 server IP"'
		echo '                         pattern="\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(\:\d{1,5})?"'
		echo '                  >'
		echo '                </td>'
		echo '                <td>'
		echo '                  <p>Connect to the specified iperf3 server&nbsp;&nbsp;'
		echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
		echo '                  </p>'
		echo '                  <div id="'$ID'" class="less">'
		echo '                    <p>&lt;server&gt;[:&lt;port&gt;]</p>'
		echo '                    <p>Default port: 5201</p>'
		echo '                    <p class="error"><b>Note:</b> Do not include the port number unless you have changed the default Server port number.</p>'
								  if [ "$LMSERVER" = "no" ]; then
		echo   '                    <p>Current LMS IP is (If that is where your iperf3 server is running:</p>'
		echo   '                    <ul>'
		echo   '                      <li>'$(pcp_lmsip)'</li>'
		echo   '                    </ul>'
								  fi
		echo '                  </div>'
		echo '                </td>'
		echo '              </tr>'
	fi
	pcp_incr_id
	pcp_toggle_row_shade
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150 center">'
	echo '                <button type="submit" name="ACTION" value="Start" >Start</button>'
	echo '              </td>'
	echo '              <td class="column210">'
	if [ "$IPERF3_SERVER_MODE" = "no" ]; then
		[ "$IPERF3_SEND" = "no" ] && IPERF3_SENDno="checked" || IPERF3_SENDyes="checked"
		echo '                <input class="small1" type="radio" name="IPERF3_SEND" value="yes" '$IPERF3_SENDyes'>Upload'
		echo '                <input class="small1" type="radio" name="IPERF3_SEND" value="no" '$IPERF3_SENDno'>Download'
	fi
	echo '              </td>'
	echo '              <td>'
	echo '                <p>Start iperf testing</p>'
	echo '              </td>'
	echo '            </tr>'

	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150 center">'
	echo '              </td>'
	echo '              <td class="column210">'
	if [ "$IPERF3_SERVER_MODE" = "no" ]; then
		[ "$IPERF3_UDP" = "yes" ] && IPERF3_UDPyes="checked" || IPERF3_UDPno="checked"
		echo '                <input class="small1" type="radio" name="IPERF3_UDP" value="yes" '$IPERF3_UDPyes'>UDP&nbsp;&nbsp;&nbsp;&nbsp;'
		echo '                <input class="small1" type="radio" name="IPERF3_UDP" value="no" '$IPERF3_UDPno'>TCP'
	fi
	echo '              </td>'
	echo '              <td>'
	echo '              </td>'
	echo '            </tr>'




	echo '            <tr class="padding '$ROWSHADE'">'
	echo '              <td colspan=3></td>'
	echo '            </tr>'
else
	pcp_incr_id
	pcp_toggle_row_shade
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150 center">'
	echo '                <button type="submit" name="ACTION" value="Load" >Load</button>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>Load iperf extension.</p>'
	echo '              </td>'
	echo '            </tr>'
	echo '            <tr class="padding '$ROWSHADE'">'
	echo '              <td colspan=2></td>'
	echo '            </tr>'
fi

	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'

pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'

