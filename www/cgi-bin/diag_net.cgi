#!/bin/sh
# Raspberry Pi network throughput diagnostics script

# Version: 7.0.0 2020-05-31

. pcp-functions
. pcp-rpi-functions

pcp_html_head "Raspberry Pi Network Diagnostics" "PH"

pcp_diagnostics
pcp_httpd_query_string

COLUMN3_1="col-sm-2"
COLUMN3_2="col-sm-3"
COLUMN3_3="col-sm-7"

LOG="${LOGDIR}/pcp_iperf.log"

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
	pcp_message INFO "Downloading iperf3." "text"
	sudo -u tc pcp-load -r $PCP_REPO -w iperf3.tcz
	if [ -f $TCEMNT/tce/optional/iperf3.tcz ]; then
		pcp_message INFO "Loading iperf3" "text"
		sudo -u tc tce-load -i iperf3.tcz
		[ $? -eq 0 ] && echo -n . || (echo $?; RESULT=1)
		if [ $RESULT -eq 0 ]; then
			pcp_message INFO "Iperf3 loaded..." "text"
		else
			pcp_message ERROR "Extensions not loaded, try again later!" "text"
		fi
	fi
}

pcp_remove_iperf3() {
	pcp_message INFO "Removing Extensions" "text"
	sudo -u tc tce-audit builddb
	sudo -u tc tce-audit delete iperf3.tcz
	pcp_message INFO "Extensions are marked for removal. You must reboot to finish!" "text"
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
		pcp_infobox_begin
		pcp_load_iperf3
		pcp_infobox_end
	;;
	Install)
		pcp_infobox_begin
		pcp_sufficient_free_space 72
		if [ $? -eq 0 ]; then
			pcp_install_iperf3
		fi
		pcp_infobox_end
	;;
	Remove)
		pcp_infobox_begin
		pcp_message INFO "Removing iperf3 Extension..." "text"
		echo
		echo 'After a reboot these extensions will be permanently deleted:'
		pcp_remove_iperf3
		pcp_backup "text"
		pcp_infobox_end
		REBOOT_REQUIRED=1
	;;
	Start)
		echo '<form id="Stop" name="Stop_Iperf" action="'$0'">'
		pcp_border_begin
		echo '  <div class="row mx-1 mt-2">'
		echo '    <div class="'$COLUMN3_1'">'
		echo '      <button class="'$BUTTON'" type="submit" name="ACTION" value="Stop">Stop</button>'
		echo '      <input type="hidden" name="IPERF3_SERVER_MODE" value="'$IPERF3_SERVER_MODE'">'
		echo '      <input type="hidden" name="IPERF3_SEND" value="'$IPERF3_SEND'">'
		echo '      <input type="hidden" name="IPERF3_UDP" value="'$IPERF3_UDP'">'
		echo '      <input type="hidden" name="IPERF_SERVER_IP" value="'$IPERF_SERVER_IP'">'
		echo '    </div>'
		echo '    <div class="col-10">'
		echo '      <p>Stop iperf testing.</p>'
		echo '    </div>'
		echo '  </div>'
		pcp_border_end
		echo '</form>'

		pcp_infobox_begin
		if [ $(pcp_squeezelite_status) -eq 0 ]; then
			pcp_message WARN "Squeezelite is running, results might be affected." "text"
			pcp_message WARN "Goto [Main Page] and [Stop] Squeezelite." "text"
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
				echo "[ INFO ] Omitting 1st second of transmission, likely due to server being faster than RPi."
			else
				DURATION="-t 20"
			fi
		fi

		if [ "$IPERF3_SERVER_MODE" = "no" ]; then
			IPERF_SERVER_PORT=$(echo $IPERF_SERVER_IP | awk -F':' '{ print $2 }')
			IP3_IP=$(echo $IPERF_SERVER_IP | awk -F':' '{ print $1 }')
			[ "$IPERF_SERVER_PORT" = "" ] && IPERF_SERVER_PORT=5201
			IPERF_COMMAND="iperf3 -c $IP3_IP -p $IPERF_SERVER_PORT -V $UDP -b 300M $DURATION $REV"
			echo "[ INFO ] Iperf will run for 20 seconds, then output will show..."
		else
			echo "[ INFO ] Iperf running in server mode. Press stop to quit."
			echo "[ INFO ] Set Client to use IP Address: $(pcp_eth0_ip) or $(pcp_wlan0_ip)"
			IPERF_COMMAND="iperf3 -s -V"
		fi
		[ $DEBUG -eq 1 ] && echo "[ DEBUG ] Iperf command: $IPERF_COMMAND"

		$IPERF_COMMAND | tee -a $LOG
		if [ $? -ne 0 ]; then
			echo "[ ERROR ] Iperf3 connection error, check to be sure server is running on selected <host>:<port>"
		fi
		pcp_infobox_end

		echo '<script>'
		echo '  document.getElementById("Stop").style.display="none";'
		echo '</script>'
	;;
esac

COLUMN3_1="col-sm-2"
COLUMN3_2="col-sm-3"
COLUMN3_3="col-sm-7"
#========================================================================================
# Raspberry Pi Network Performance Diagnostics
#----------------------------------------------------------------------------------------
pcp_heading5 "Raspberry Pi Network"
pcp_border_begin
#-------------------------------------Row 1----------------------------------------------
echo '      <div class="row mx-1">'
echo '        <div class="'$COLUMN3_1' text-sm-right">'
echo '          <p>Model:</p>'
echo '        </div>'
echo '        <div class="'$COLUMN3_1'">'
echo '          <p>'$(pcp_rpi_model)'</p>'
echo '        </div>'
echo '        <div class="'$COLUMN3_1' text-sm-right">'
echo '          <p>eth0 IP:</p>'
echo '        </div>'
echo '        <div class="'$COLUMN3_1'">'
echo '          <p>'$(pcp_diag_rpi_eth0_ip)'</p>'
echo '        </div>'
echo '        <div class="'$COLUMN3_1' text-sm-right">'
echo '          <p>Physical MAC:</p>'
echo '        </div>'
echo '        <div class="'$COLUMN3_1'">'
echo '          <p>'$(pcp_diag_rpi_eth0_mac_address)'</p>'
echo '        </div>'
echo '      </div>'
#-------------------------------------Row 2----------------------------------------------
echo '      <div class="row mx-1">'
echo '        <div class="'$COLUMN3_1' text-sm-right">'
echo '          <p>Revison:</p>'
echo '        </div>'
echo '        <div class="'$COLUMN3_1'">'
echo '          <p>'$(pcp_rpi_revision)'</p>'
echo '        </div>'
echo '        <div class="'$COLUMN3_1' text-sm-right">'
echo '          <p>wlan0 IP:</p>'
echo '        </div>'
echo '        <div class="'$COLUMN3_1'">'
echo '          <p>'$(pcp_diag_rpi_wlan0_ip)'</p>'
echo '        </div>'
echo '        <div class="'$COLUMN3_1' text-sm-right">'
echo '          <p>Wireless MAC:</p>'
echo '        </div>'
echo '        <div class="'$COLUMN3_1'">'
echo '          <p>'$(pcp_diag_rpi_wlan0_mac_address)'</p>'
echo '        </div>'
echo '      </div>'
#-------------------------------------Row 3----------------------------------------------
echo '      <div class="row mx-1">'
echo '        <div class="'$COLUMN3_1' text-sm-right">'
echo '          <p>PCB Revison:</p>'
echo '        </div>'
echo '        <div class="'$COLUMN3_1'">'
echo '          <p>'$(pcp_rpi_pcb_revision)'</p>'
echo '        </div>'
echo '        <div class="'$COLUMN3_1' text-sm-right">'
echo '          <p>LMS IP:</p>'
echo '        </div>'
echo '        <div class="'$COLUMN3_1'">'
echo '          <p>'$(pcp_diag_rpi_lmsip)'</p>'
echo '        </div>'
echo '        <div class="'$COLUMN3_1' text-sm-right">'
echo '          <p>Controls MAC:</p>'
echo '        </div>'
echo '        <div class="'$COLUMN3_1'">'
echo '          <p>'$(pcp_controls_mac_address)'</p>'
echo '        </div>'
echo '      </div>'
#----------------------------------------------------------------------------------------
pcp_border_end

#========================================================================================
# piCorePlayer
#----------------------------------------------------------------------------------------
pcp_heading5 "piCorePlayer"
pcp_border_begin
echo '      <div class="row mx-1">'
echo '        <div class="'$COLUMN3_1' text-sm-right">'
echo '          <p>Version:</p>'
echo '        </div>'
echo '        <div class="'$COLUMN3_1'">'
echo '          <p>'$(pcp_picoreplayer_version)'</p>'
echo '        </div>'
echo '        <div class="'$COLUMN3_1' text-sm-right">'
echo '          <p>pCP name:</p>'
echo '        </div>'
echo '        <div class="'$COLUMN3_1'">'
echo '          <p>'$NAME'</p>'
echo '        </div>'
echo '        <div class="'$COLUMN3_1' text-sm-right">'
echo '          <p>Hostname:</p>'
echo '        </div>'
echo '        <div class="'$COLUMN3_1'">'
echo '          <p>'$HOST'</p>'
echo '        </div>'
echo '      </div>'
pcp_border_end

#========================================================================================
# Network Performance
#----------------------------------------------------------------------------------------
echo '    <form name="IPERF" action="'$0'">'
pcp_heading5 "Network Performance (iperf3)"
pcp_border_begin
#----------------------------------------------------------------------------------------
pcp_incr_id
echo '      <div class="row mx-1">'
echo '        <div class="col-12">'
echo '          <p>For help setting up an iperf server on another machine. Please goto <a href="https://software.es.net/iperf/" target="_blank">ESNet</a> or <a href="https://iperf.fr/" target="_blank">iperf.fr</a></p>'
echo '        </div>'
echo '      </div>'
#----------------------------------------------------------------------------------------
if [ ! -f $TCEMNT/tce/optional/iperf3.tcz ]; then
	echo '      <div class="row mx-1">'
	echo '        <div class="'$COLUMN3_1'">'
	echo '          <input class="'$BUTTON'"'
	echo '                 type="submit"'
	echo '                 name="ACTION"'
	echo '                 value="Install"'
	echo '          >'
	echo '        </div>'
	echo '        <div class="col-10">'
	echo '          <p>Install iperf3 on pCP&nbsp;&nbsp;'
	pcp_helpbadge
	echo '          </p>'
	echo '          <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '            <p>This will install iperf3 network performance testing.</p>'
	echo '            <p>You will need to run iperf3 on another machine, preferrably your LMS server.</p>'
	echo '          </div>'
	echo '        </div>'
	echo '      </div>'
else
	echo '      <div class="row mx-1">'
	echo '        <div class="'$COLUMN3_1'">'
	echo '          <input class="'$BUTTON'"'
	echo '                 type="submit"'
	echo '                 name="ACTION"'
	echo '                 value="Remove"'
	echo '                 onclick="return confirm('\''This will remove LMS from pCP.\n\nAre you sure?'\'')"'
	echo '          >'
	echo '        </div>'
	echo '        <div class="col-10">'
	echo '          <p>Remove iperf3 from pCP&nbsp;&nbsp;'
	pcp_helpbadge
	echo '          </p>'
	echo '          <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '            <p>This will remove the iperf3 extension.</p>'
	echo '          </div>'
	echo '        </div>'
	echo '      </div>'
fi
#----------------------------------------------------------------------------------------
if [ -x /usr/local/bin/iperf3 ]; then
	[ "$IPERF3_SERVER_MODE" = "no" ] && IPERF3_SERVER_MODEno="checked" || IPERF3_SERVER_MODEyes="checked"
	pcp_incr_id
	echo '      <div class="row mx-1">'
	echo '        <div class="'$COLUMN3_1'">'
	echo '          <button class="'$BUTTON'" type="submit" name="ACTION" value="Server_Mode" >Change Mode</button>'
	echo '        </div>'
	echo '        <div class="'$COLUMN3_2'">'
	echo '          <input id="rad1" type="radio" name="IPERF3_SERVER_MODE" value="yes" '$IPERF3_SERVER_MODEyes'>'
	echo '          <label for="rad1">Server</label>'
	echo '          <input id="rad2" type="radio" name="IPERF3_SERVER_MODE" value="no" '$IPERF3_SERVER_MODEno'>'
	echo '          <label for="rad2">Client</label>'
	echo '        </div>'
	echo '        <div class="'$COLUMN3_3'">'
	echo '          <p>Set iperf to server mode&nbsp;&nbsp;'
	pcp_helpbadge
	echo '          </p>'
	echo '          <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '            <p>Server - This device will run in server mode.</p>'
	echo '            <p>Client - This device will run in client mode.</p>'
	echo '          </div>'
	echo '        </div>'
	echo '      </div>'
#----------------------------------------------------------------------------------------
	if [ "$IPERF3_SERVER_MODE" = "no" ]; then
		echo '      <div class="row mx-1">'
		echo '        <div class="'$COLUMN3_1'">'
		echo '          <p>Iperf3 Server IP</p>'
		echo '        </div>'
		echo '        <div class="'$COLUMN3_2'">'
		echo '          <input class="form-control form-control-sm"'
		echo '                 type="text"'
		echo '                 name="IPERF_SERVER_IP"'
		echo '                 value="'$IPERF_SERVER_IP'"'
		echo '                 title="Iperf3 server IP"'
		echo '                 pattern="\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(\:\d{1,5})?"'
		echo '          >'
		echo '        </div>'
		pcp_incr_id
		echo '        <div class="'$COLUMN3_3'">'
		echo '          <p>Connect to the specified iperf3 server&nbsp;&nbsp;'
		pcp_helpbadge
		echo '          </p>'
		echo '          <div id="dt'$ID'" class="'$COLLAPSE'">'
		echo '            <p>&lt;server&gt;[:&lt;port&gt;]</p>'
		echo '            <p>Default port: 5201</p>'
		echo '            <p class="error"><b>Note:</b> Do not include the port number unless you have changed the default Server port number.</p>'
		                  if [ "$LMSERVER" = "no" ]; then
		echo   '            <p>Current LMS IP is (If that is where your iperf3 server is running):</p>'
		echo   '            <ul>'
		echo   '              <li>'$(pcp_lmsip)'</li>'
		echo   '            </ul>'
		                  fi
		echo '          </div>'
		echo '        </div>'
		echo '      </div>'
	fi
	#------------------------------------------------------------------------------------
	pcp_incr_id
	echo '      <div class="row mx-1">'
	echo '        <div class="'$COLUMN3_1'">'
	echo '          <button class="'$BUTTON'" type="submit" name="ACTION" value="Start" >Start</button>'
	echo '        </div>'
	echo '        <div class="'$COLUMN3_2'">'
	if [ "$IPERF3_SERVER_MODE" = "no" ]; then
		[ "$IPERF3_SEND" = "no" ] && IPERF3_SENDno="checked" || IPERF3_SENDyes="checked"
		echo '          <input id="rad3" type="radio" name="IPERF3_SEND" value="yes" '$IPERF3_SENDyes'>'
		echo '          <label for="rad3">Upload</label>'
		echo '          <input id="rad4" type="radio" name="IPERF3_SEND" value="no" '$IPERF3_SENDno'>'
		echo '          <label for="rad4">Download</label>'
	fi
	echo '        </div>'
	echo '        <div class="'$COLUMN3_3'">'
	echo '          <p>Start iperf testing</p>'
	echo '        </div>'
	echo '      </div>'
	#------------------------------------------------------------------------------------
	echo '      <div class="row mx-1">'
	echo '        <div class="'$COLUMN3_1'">'
	echo '        </div>'
	echo '        <div class="col-10">'
	if [ "$IPERF3_SERVER_MODE" = "no" ]; then
		[ "$IPERF3_UDP" = "yes" ] && IPERF3_UDPyes="checked" || IPERF3_UDPno="checked"
		echo '          <input id="rad5" type="radio" name="IPERF3_UDP" value="yes" '$IPERF3_UDPyes'>'
		echo '          <label for="rad5">UDP&nbsp;&nbsp;&nbsp;</label>'
		echo '          <input id="rad6" type="radio" name="IPERF3_UDP" value="no" '$IPERF3_UDPno'>'
		echo '          <label for="rad6">TCP</label>'
	fi
	echo '        </div>'
	echo '      </div>'
	#------------------------------------------------------------------------------------
else
	pcp_incr_id
	echo '      <div class="row mx-1">'
	echo '        <div class="'$COLUMN3_1'">'
	echo '          <button class="'$BUTTON'" type="submit" name="ACTION" value="Load" >Load</button>'
	echo '        </div>'
	echo '        <div class="col-10">'
	echo '          <p>Load iperf extension.</p>'
	echo '        </div>'
	echo '      </div>'
fi
#----------------------------------------------------------------------------------------
pcp_border_end

pcp_html_end
