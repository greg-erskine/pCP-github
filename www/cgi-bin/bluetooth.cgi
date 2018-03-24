#!/bin/sh

# Version: 3.5.0 2018-03-18
#	Initial version. PH.

. pcp-functions
[ -e /usr/local/bin/pcp-bt-functions ] && . /usr/local/bin/pcp-bt-functions

pcp_html_head "Bluetooth Settings" "PH"

pcp_picoreplayers_toolbar
pcp_controls
pcp_banner
pcp_navigation
pcp_remove_query_string
pcp_httpd_query_string

#---------------------------Routines-----------------------------------------------------
pcp_install_bt() {
	echo '[ INFO ] Downloading Bluetooth extensions...'
	sudo -u tc pcp-load -r $PCP_REPO -w pcp-bt.tcz
	if [ -f $TCEMNT/tce/optional/pcp-bt.tcz ]; then
		echo '[ INFO ] Installing Bluetooth...'
		sudo -u tc pcp-load -i pcp-bt.tcz
		sudo sed -i '/pcp-bt.tcz/d' $ONBOOTLST
		echo 'pcp-bt.tcz' >> $ONBOOTLST
		mkdir -p /var/lib/bluetooth
		echo "var/lib/bluetooth" >> /opt/.filetool.lst
		[ $DEBUG -eq 1 ] && echo '[ DEBUG ] pcp-bt is added to onboot.lst'
		[ $DEBUG -eq 1 ] && cat $ONBOOTLST
	fi
}

pcp_remove_bt() {
	sudo $DAEMON_INITD stop >/dev/null 2>&1
	sudo -u tc tce-audit builddb
	sudo -u tc tce-audit delete pcp-bt.tcz
	sudo sed -i '/pcp-bt.tcz/d' $ONBOOTLST
	echo "[ INFO ] Removeing configuration files"
	rm -f $BTDEVICECONF
	sed -i '/var\/lib\/bluetooth/d' /opt/.filetool.lst
}

pcp_bt_status(){
	sudo $DAEMON_INITD status >/dev/null 2>&1
	echo $?
}

REBOOT_REQUIRED=0
case "$ACTION" in
	Forget)
		pcp_table_top "Bluetooth Configuration"
		echo '                <textarea class="inform" style="height:60px">'
		echo '[ INFO ] Forgetting Device ...'$DEVICE
		RET=$(pcp_bt_forget_device $DEVICE)
		case $RET in
			0)echo '[ INFO ] Device has been removed.';pcp_backup "nohtml";;
			1)echo '[ ERROR ] Error removing device.';;
		esac
		rm -f /tmp/*.out
		rm -f /tmp/*.dd
		echo '                </textarea>'
		pcp_table_end
	;;
	Install)
		pcp_table_top "Downloading Bluetooth"
		pcp_sufficient_free_space 4500
		if [ $? -eq 0 ] ; then
			echo '                <textarea class="inform" style="height:160px">'
			pcp_install_bt
			if [ -f $TCEMNT/tce/optional/pcp-bt.tcz ]; then
				APMODE="yes"
				pcp_save_to_config
				pcp_backup "nohtml"
			else
				echo '[ ERROR ] Error Downloading AP Mode, please try again later.'
			fi
			echo '                </textarea>'
			pcp_table_end
		fi
	;;
	Pair)
		pcp_table_top "Pair Device"
		echo '                <textarea class="inform" style="height:120px">'
		pcp_bt_pair $DEVICE
		if [ $? -eq 0 ]; then
			echo '[ INFO ] Pairing Successful'
			pcp_backup "nohtml"
			echo '[ INFO ] Restarting Connect Daemon'
			sudo $DAEMON_INITD restart
		fi
		echo '                </textarea>'
		pcp_table_end
	;;
	Remove)
		pcp_table_top "Removing Bluetooth Extensions from pCP"
		echo '                <textarea class="inform" style="height:120px">'
		echo '[ INFO ] Removing AP Mode Extensions...'
		echo
		echo 'After a reboot these extensions will be permanently deleted:'
		pcp_remove_bt
		pcp_backup "nohtml"
		echo '                </textarea>'
		pcp_table_end
		REBOOT_REQUIRED=1
	;;
	Restart)
		pcp_table_top "Bluetooth"
		echo '                <textarea class="inform" style="height:60px">'
		echo '[ INFO ] Restarting Bluetooth Connect Daemon...'
		echo -n '[ INFO ] '
		sudo $DAEMON_INITD stop
		echo -n '[ INFO ] '
		sudo $DAEMON_INITD start
		echo '                </textarea>'
		pcp_table_end
	;;
	Scan)
		pcp_table_top "Bluetooth Scanning"
		echo '                <textarea class="inform" style="height:60px">'
		echo '[ INFO ] Scanning for Bluetooth Devices, make sure device is in pair mode...'
		pcp_bt_scan > /tmp/btscan.out
		echo '                </textarea>'
		pcp_table_end
	;;
	Select)
		pcp_table_top "Select Previously paired device"
		echo '                <textarea class="inform" style="height:120px">'
		pcp_bt_write_config $DEVICE
		echo '[ INFO ] Selecting Device: '$BTNAME
		pcp_backup "nohtml"
		echo '[ INFO ] Restarting Connect Daemon'
		sudo $DAEMON_INITD restart
		echo '                </textarea>'
		pcp_table_end
	;;
	Start)
		pcp_table_top "Bluetooth"
		echo '                <textarea class="inform" style="height:40px">'
		if [ ! -x $DAEMON_INITD ]; then
			echo '[ INFO ] Loading pCP AP Mode extensions...'
			sudo -u tc tce-load -i pcp-bt.tcz
		fi
		echo '[ INFO ] Starting Bluetooth Connect Daemon...'
		echo -n '[ INFO ] '
		sudo $DAEMON_INITD start
		echo '                </textarea>'
		pcp_table_end
	;;
	Stop)
		pcp_table_top "Bluetooth"
		echo '                <textarea class="inform" style="height:40px">'
		echo '[ INFO ] Stopping Bluetooth Connect Daemon...'
		echo -n '[ INFO ] '
		sudo $DAEMON_INITD stop
		echo '                </textarea>'
		pcp_table_end
	;;
	Update)
		pcp_table_top "Update Bluetooth"
		pcp_sufficient_free_space 4500
		echo '                <textarea class="inform" style="height:100px">'
		echo '[ INFO ] Updating AP Mode Extensions...'
		sudo -u tc pcp-update pcp-bt.tcz
		case $? in
			0) echo '[ INFO ] Reboot Required to finish update'; REBOOT_REQUIRED=1;;
			2) echo '[ INFO ] No Update Availiable';;
			*) echo '[ ERROR] Try again later';;
		esac
		echo '                </textarea>'
		pcp_table_end
	;;
	*)
	;;
esac
[ $REBOOT_REQUIRED -eq 1 ] && pcp_reboot_required

#========================================================================================
# Main table
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Bluetooth Speaker Setup</legend>'
echo '          <table class="bggrey percent100">'

#------------------------------------Indication--------------------------------------
if [ $(pcp_bt_power_status) -eq 0 ]; then
	PWR_INDICATOR=$HEAVY_CHECK_MARK
	PWR_CLASS="indicator_green"
	PWR_STATUS="On"
else
	PWR_INDICATOR=$HEAVY_BALLOT_X
	PWR_CLASS="indicator_red"
	PWR_STATUS="Off"
fi
if [ $(pcp_bt_status) -eq 0 ]; then
	CD_INDICATOR=$HEAVY_CHECK_MARK
	CD_CLASS="indicator_green"
	CD_STATUS="running"
else
	CD_INDICATOR=$HEAVY_BALLOT_X
	CD_CLASS="indicator_red"
	CD_STATUS="not running"
fi
if [ $(pcp_bt_device_connected) -eq 0 ]; then
	DEV_INDICATOR=$HEAVY_CHECK_MARK
	DEV_CLASS="indicator_green"
	DEV_STATUS="Connected"
else
	DEV_INDICATOR=$HEAVY_BALLOT_X
	DEV_CLASS="indicator_red"
	DEV_STATUS="Not Connected"
fi

#------------------------------------------------------------------------------------
# Determine state of check boxes.
#------------------------------------------------------------------------------------
# Function to check the radio button according to config file
case "$APMODE" in
	yes) APMODEyes="checked" ;;
	no) APMODEno="checked" ;;
esac
# Function to check the show log radio button according to selection
case "$LOGSHOW" in
	yes) LOGSHOWyes="checked" ;;
	*) LOGSHOWno="checked" ;;
esac

[ -f $TCEMNT/tce/optional/pcp-bt.tcz ] && DISABLE_BT="" || DISABLE_BT="disabled"

pcp_incr_id
pcp_start_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td class="column150 center">'
echo '                <p class="'$PWR_CLASS'">'$PWR_INDICATOR'</p>'
echo '              </td>'
echo '              <td>'
echo '                <p>BT Controller is '$PWR_STATUS'&nbsp;&nbsp;'
echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                </p>'
echo '                <div id="'$ID'" class="less">'
echo '                  <ul>'
echo '                    <li><span class="indicator_green">&#x2714;</span> = BT Controller Power is on.</li>'
echo '                    <li><span class="indicator_red">&#x2718;</span> = BT Controller Power is off.</li>'
echo '                    <li>Controller address '$BTCONTROLLER
echo '                    <li>If the controller power remains off.</li>'
echo '                    <li>If using Rpi internal bluetooth, make sure controller is enabled on the <a href="wifi.cgi">Wifi Page</a></li>'
echo '                    <li>Check kernel messages in diagnostics <a href="diagnostics.cgi#dmesg">dmesg</a></li>'
echo '                  </ul>'
echo '                </div>'
echo '              </td>'
echo '            </tr>'
pcp_incr_id
pcp_toggle_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td class="column150 center">'
echo '                <p class="'$CD_CLASS'">'$CD_INDICATOR'</p>'
echo '              </td>'
echo '              <td>'
echo '                <p>Connect Daemon is '$CD_STATUS'&nbsp;&nbsp;'
echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                </p>'
echo '                <div id="'$ID'" class="less">'
echo '                  <ul>'
echo '                    <li><span class="indicator_green">&#x2714;</span> = Connect Daemon is running.</li>'
echo '                    <li><span class="indicator_red">&#x2718;</span> = Connect Daemon is not running.</li>'
echo '                  </ul>'
echo '                </div>'
echo '              </td>'
echo '            </tr>'
pcp_incr_id
pcp_toggle_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td class="column150 center">'
echo '                <p class="'$DEV_CLASS'">'$DEV_INDICATOR'</p>'
echo '              </td>'
echo '              <td>'
echo '                <p>BT Device is '$DEV_STATUS'&nbsp;&nbsp;'
echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                </p>'
echo '                <div id="'$ID'" class="less">'
echo '                  <ul>'
echo '                    <li><span class="indicator_green">&#x2714;</span> = Device is connected.</li>'
echo '                    <li><span class="indicator_red">&#x2718;</span> = Device is not connected.</li>'
echo '                  </ul>'
echo '                </div>'
echo '              </td>'
echo '            </tr>'
#----------------------------------------------------------------------------------------
pcp_toggle_row_shade
echo '            <tr class="padding '$ROWSHADE'">'
echo '              <td></td>'
echo '              <td></td>'
echo '            </tr>'

#------------------------------------------Install/uninstall AP Mode---------------------
pcp_bt_install() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '            <form name="Install" action="'$0'">'
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	if [ ! -f $TCEMNT/tce/optional/pcp-bt.tcz ]; then
		echo '                  <input type="submit" name="ACTION" value="Install" />'
		echo '                </td>'
		echo '                <td>'
		echo '                  <p>Install Bluetooth on pCP&nbsp;&nbsp;'
		echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
		echo '                  </p>'
		echo '                  <div id="'$ID'" class="less">'
		echo '                    <p>This will install the required bluetooth extensions on pCP for bluetooth speakers.</p>'
		echo '                  </div>'
	else
		echo '                  <input type="submit" name="ACTION" value="Update" />'
		echo '                </td>'
		echo '                <td class="column150 center">'
		echo '                  <input type="submit" name="ACTION" value="Remove" onclick="return confirm('\''This will remove Bluetooth from pCP.\n\nAre you sure?'\'')"/>'
		echo '                </td>'
		echo '                <td>'
		echo '                  <p>Update or Remove Bluetooth from pCP&nbsp;&nbsp;'
		echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
		echo '                  </p>'
		echo '                  <div id="'$ID'" class="less">'

		echo '                    <p>This will remove Bluetooth extension and all the extra packages that were added.</p>'
		echo '                  </div>'
	fi
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_BETA ] && pcp_bt_install
#----------------------------------------------------------------------------------------
#------------------------------------------Start and Stop BT Daemon---------------------
pcp_bt_startstop() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '            <form name="Start" action="'$0'">'
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="ACTION" value="Start" '$DISABLE_BT'/>'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Start Bluetooth Connect Daemon on pCP&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>This will start the Bluetooth Connect Daemon on pCP.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '            <form name="Stop" action="'$0'">'
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="ACTION" value="Stop" '$DISABLE_BT'/>'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Stop Bluetooth Connect Daemon on pCP.&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>This will restart the Bluetooth Connect Daemon on pCP.</p>'
	echo '                    <p>It the speaker is already connected, this will not affect connection status/playback.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '            <form name="Restart" action="'$0'">'
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="ACTION" value="Restart" '$DISABLE_BT'/>'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Restart Bluetooth Connect Daemon on pCP&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>This will restart the Bluetooth Connect Daemon on pCP.</p>'
	echo '                    <p>It the speaker is already connected, this will not affect connection status/playback.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_BETA ] && pcp_bt_startstop
#-------------------_------------Show BT logs--------------------------------------------
pcp_bt_show_logs() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '            <form name="Show" action="'$0'" method="get">'
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" value="Show Logs" '$DISABLE_BT'/>'
	echo '                </td>'
	echo '                <td class="column100">'
	echo '                  <input class="small1" type="radio" name="LOGSHOW" value="yes" '$LOGSHOWyes' >Yes'
	echo '                  <input class="small1" type="radio" name="LOGSHOW" value="no" '$LOGSHOWno' >No'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Show Bluetooth logs&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Show Bluetooth log in text area below.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_NORMAL ] && pcp_bt_show_logs
#----------------------------------------------------------------------------------------
echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------

#========================================================================================
# Pair/Select table
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Device Pairing/Selection</legend>'
echo '          <table class="bggrey percent100">'
#------------------------------------------Scan/Pair BT ---------------------
pcp_bt_scan() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '            <form name="Scan" action="'$0'">'
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="ACTION" value="Scan" '$DISABLE_BT'/>'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Scan for Bluetooth Devices&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>This will Scan for Bluetooth devices, make sure the device is in pair mode.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'

	if [ -f /tmp/btscan.out ]; then
		# Mark the currently paired device as selected.
		sed '/^'$BTDEVICE'/! s/selected/notselected/' < /tmp/btscan.out >/tmp/btscan.dd
		#Remove unneeded space
		sed -i 's/ \#/\#/' /tmp/btscan.dd
		PAIR_DISABLED=""
	else
		if [ "$BTNAME" != "" ]; then
			echo "$BTDEVICE#$BTNAME#selected" >/tmp/btscan.dd
		else
			echo "0#No Device#selected" >/tmp/btscan.dd
		fi
		PAIR_DISABLED="disabled"
	fi
	pcp_incr_id
	pcp_toggle_row_shade
	if [ "$PAIR_DISABLED" = "" ]; then
		echo '            <form name="Pair" action="'$0'">'
		echo '              <tr class="'$ROWSHADE'">'
		echo '                <td class="column150 center">'
		echo '                  <input type="submit" name="ACTION" value="Pair" onclick="return confirm('\''Make sure device is in pairing mode.\n\nContinue?'\'')" '$PAIR_DISABLED'/>'
		echo '                </td>'
		echo '                <td class="column200">'
		echo '                  <select name="DEVICE">'
		awk -F'#' '{ print "<option value=\""$1"\" "$3">"$2"</option>" }' /tmp/btscan.dd
		echo '                  </select>'
		echo '                </td>'
		echo '                <td>'
		if [ "$BTNAME" != "" ]; then
			echo '                  <p>Select device to pair. List also includes previously paired devices.</p>'
		else
			echo '                  <p>Run a Scan to Find Devices</p>'
		fi
		echo '                </td>'
		echo '              </tr>'
		echo '            </form>'
	else
		echo '              <tr class="'$ROWSHADE'">'
		echo '                <td class="column150 center"></td>'
		echo '                <td class="colspan=2">'
		echo '                   <p>Run scan to discover/pair to a new device.</p>'
		echo '                </td>'
		echo '              </tr>'
	fi

	pcp_bt_paired_devices
	if [ -f $PAIRED_LIST ]; then
		# Mark the currently paired device as selected.
		sed '/^'$BTDEVICE'/! s/selected/notselected/' < $PAIRED_LIST > /tmp/paired.dd
		#Remove unneeded space
		sed -i 's/ \#/\#/' /tmp/paired.dd
		SELECT_DISABLED=""
	else
		echo "0#No Device#selected" >/tmp/paired.dd
		SELECT_DISABLED="disabled"
	fi
	pcp_incr_id
	pcp_toggle_row_shade
	echo '            <form name="Select" action="'$0'">'
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="ACTION" value="Select" '$SELECT_DISABLED'/>'
	echo '                </td>'
	echo '                <td class="column200">'
	echo '                  <select name="DEVICE">'
	awk -F'#' '{ print "<option value=\""$1"\" "$3">"$2"</option>" }' /tmp/paired.dd
	echo '                  </select>'
	echo '                </td>'
	echo '                <td>'
	if [ "$BTNAME" != "" ]; then
		echo '                  <p>Select from previosly paired device to change output device.</p>'
	else
		echo '                  <p>Run a Scan to Find Devices</p>'
	fi
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
	
	if [ -f /tmp/paired.dd ]; then
		FORGET_DISABLED=""
	else
		echo "0#No Device#selected" >/tmp/paired.dd
		FORGET_DISABLED="disabled"
	fi
	pcp_incr_id
	pcp_toggle_row_shade
	echo '            <form name="Forget" action="'$0'">'
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="ACTION" value="Forget" onclick="return confirm('\''Forget Device.\n\nContinue?'\'')"'$SELECT_DISABLED'/>'
	echo '                </td>'
	echo '                <td class="column200">'
	echo '                  <select name="DEVICE">'
	awk -F'#' '{ print "<option value=\""$1"\" "$3">"$2"</option>" }' /tmp/paired.dd
	echo '                  </select>'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Select device to forget.</p>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
	
	
}
[ $MODE -ge $MODE_BETA ] && pcp_bt_scan

#----------------------------------------------------------------------------------------
echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------

#------------------------------------------LMS log text area-----------------------------
pcp_bt_logview() {
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Show Bluetooth logs</legend>'
	echo '          <table class="bggrey percent100">'
	echo '            <tr>'
	echo '              <td>'
	                      pcp_textarea_inform "$BT_LOG" 'cat $BT_LOG' 250
	echo '              </td>'
	echo '            </tr>'
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
}
[ "$LOGSHOW" = "yes" ] && pcp_bt_logview
#----------------------------------------------------------------------------------------


pcp_footer
[ $MODE -ge $MODE_NORMAL ] && pcp_mode
pcp_copyright

echo '</body>'
echo '</html>'
