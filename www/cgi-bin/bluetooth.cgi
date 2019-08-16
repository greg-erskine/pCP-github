#!/bin/sh

# Version: 6.0.0 2019-08-16

. pcp-functions
. pcp-rpi-functions
[ -x /usr/local/bin/pcp-bt-functions ] && . /usr/local/bin/pcp-bt-functions

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
	sudo -u tc pcp-load -r $PCP_REPO -w pcp-bt6.tcz
	if [ -f $TCEMNT/tce/optional/pcp-bt6.tcz ]; then
		echo '[ INFO ] Installing Bluetooth...'
		sudo -u tc pcp-load -i pcp-bt6.tcz
		sudo sed -i '/pcp-bt6.tcz/d' $ONBOOTLST
		echo 'pcp-bt6.tcz' >> $ONBOOTLST
		mkdir -p /var/lib/bluetooth
		echo "var/lib/bluetooth" >> /opt/.filetool.lst
		[ $DEBUG -eq 1 ] && echo '[ DEBUG ] pcp-bt6 is added to onboot.lst'
		[ $DEBUG -eq 1 ] && cat $ONBOOTLST
	fi
}

pcp_remove_bt() {
	sudo $DAEMON_INITD stop >/dev/null 2>&1
	sudo -u tc tce-audit builddb
	sudo -u tc tce-audit delete pcp-bt6.tcz
	sudo sed -i '/pcp-bt6.tcz/d' $ONBOOTLST
	echo "[ INFO ] Removeing configuration files"
	rm -f $BTDEVICECONF
	sed -i '/var\/lib\/bluetooth/d' /opt/.filetool.lst
}

pcp_bt_status() {
	sudo $DAEMON_INITD status >/dev/null 2>&1
	echo $?
}

pcp_bt_pairable_status() {
	sudo $PAIR_DAEMON_INITD status >/dev/null 2>&1
	echo $?
}

pcp_bt_discover() {
	bluetoothctl discoverable on
	/usr/local/bin/pcp-pairing-agent.py --pair_mode --timeout 60
}

pcp_bt_disconnect_device() {
	bluetoothctl disconnect $1 >/dev/null
	if [ $? -eq 0 ]; then
		echo 0
	else
		echo 1
	fi
}

pcp_bt_save_config() {
	echo '[ INFO ] Saving Device Config: '$BTNAME
	[ -f $BTDEVICECONF ] || touch $BTDEVICECONF
	I=1
	while [ $I -lt $NUMDEVICES ]; do
		sed -i '/'$(eval echo "\${BTMAC${I}}")'/d' $BTDEVICECONF
		eval echo "\${BTMAC${I}}#\${BTPLAYERNAME${I}}#\${BTDELAY${I}}" >> $BTDEVICECONF
		I=$((I + 1))
	done
}

REBOOT_REQUIRED=0
case "$ACTION" in
	Forget*)
		pcp_table_top "Bluetooth Configuration"
		I=$(echo ${ACTION#Forget})
		echo '                <textarea class="inform" style="height:60px">'
		DEVICE=$(eval echo "\${BTMAC${I}}")
		echo '[ INFO ] Forgetting Device...'$DEVICE
		RET=$(pcp_bt_forget_device $DEVICE)
		case $RET in
			0)echo '[ INFO ] Device has been removed.';pcp_backup "text";;
			1)echo '[ ERROR ] Error removing device.';;
		esac
		rm -f /tmp/*.out
		rm -f /tmp/*.dd
		echo '                </textarea>'
		pcp_table_end
	;;
	Disconnect*)
		pcp_table_top "Disconnecting Device"
		I=$(echo ${ACTION#Disconnect})
		echo '                <textarea class="inform" style="height:120px">'
		DEVICE=$(eval echo "\${BTMAC${I}}")
		echo '[ INFO ] Disconnecting...'$DEVICE
		RET=$(pcp_bt_disconnect_device $DEVICE)
		case $RET in
			0)echo '[ INFO ] Device has been disconnected';;
			1)echo '[ ERROR ] Error disconnecting device.';;
		esac
		echo '                </textarea>'
		pcp_table_end
	;;
	Install)
		pcp_table_top "Downloading Bluetooth"
		pcp_sufficient_free_space 36000
		if [ $? -eq 0 ] ; then
			echo '                <textarea class="inform" style="height:160px">'
			pcp_install_bt
			if [ ! -f $TCEMNT/tce/optional/pcp-bt6.tcz ]; then
				echo '[ ERROR ] Error Downloading Bluetooth, please try again later.'
			fi
			echo '                </textarea>'
			pcp_table_end
		fi
	;;
	Remove)
		pcp_table_top "Removing Bluetooth Extensions from pCP"
		echo '                <textarea class="inform" style="height:120px">'
		echo '[ INFO ] Removing AP Mode Extensions...'
		echo
		echo 'After a reboot these extensions will be permanently deleted:'
		pcp_remove_bt
		pcp_backup "text"
		echo '                </textarea>'
		pcp_table_end
		REBOOT_REQUIRED=1
	;;
	Power*)
		POWER=$(echo ${ACTION#Power_})
		pcp_table_top "BT Controller Power"
		echo '                <textarea class="inform" style="height:40px">'
		echo 'Turning the BT Controller power '$POWER'...'
		bluetoothctl power $POWER
		sleep 0.5
		echo '                </textarea>'
		pcp_table_end
	;;
	Pair)
		pcp_table_top "Pair Device"
		echo '                <textarea class="inform" style="height:120px">'
		pcp_bt_pair $DEVICE
		if [ $? -eq 0 ]; then
			echo '[ INFO ] Pairing Successful'
			pcp_backup "text"
		fi
		echo '                </textarea>'
		rm -f /tmp/btscan.out 
		pcp_table_end
	;;
	Discover)
		pcp_table_top "Enabling Device Discovery"
		echo '                <textarea class="inform" style="height:120px">'
		echo '[ INFO ] Device will be discoverable for 60 seconds'
		pcp_bt_discover
		echo '                </textarea>'
		pcp_table_end
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
	Restart_pair)
		pcp_table_top "Bluetooth"
		echo '                <textarea class="inform" style="height:60px">'
		echo '[ INFO ] Restarting Bluetooth Pairing Daemon...'
		echo -n '[ INFO ] '
		sudo $PAIR_DAEMON_INITD stop
		echo -n '[ INFO ] '
		sudo $PAIR_DAEMON_INITD start
		echo '                </textarea>'
		pcp_table_end
	;;
	Scan)
		pcp_table_top "Bluetooth Scanning"
		echo '                <textarea class="inform" style="height:180px">'
		echo '[ INFO ] Scanning 10 seconds for Bluetooth Devices, make sure device is in pair mode...'
		echo '[ INFO ] If device is not found at end of scan, scan can be re-ran...'
		pcp_bt_newscan 10 > /tmp/btscan.out
		echo '[ INFO ] Found Devices'
		bluetoothctl devices
		echo '                </textarea>'
		pcp_table_end
		rm -f /tmp/paired*
	;;
	Save)
		pcp_table_top "Select Previously paired device"
		echo '                <textarea class="inform" style="height:120px">'
		pcp_bt_save_config
		pcp_backup "text"
		echo '[ INFO ] You might need to turn the speaker off, then back on to load updated config.'
		echo '                </textarea>'
		pcp_table_end
	;;
	Update)
		pcp_table_top "Update Bluetooth"
		pcp_sufficient_free_space 4500
		echo '                <textarea class="inform" style="height:100px">'
		echo '[ INFO ] Updating pCP Bluetooth Extensions...'
		sudo -u tc pcp-update pcp-bt6.tcz
		case $? in
			0) echo '[ INFO ] Reboot Required to finish update'; REBOOT_REQUIRED=1;;
			2) echo '[ INFO ] No Update Available';;
			*) echo '[ ERROR ] Try again later';;
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

#------------------------------------Indication------------------------------------------
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
if [ $(pcp_bt_pairable_status) -eq 0 ]; then
	PAIR_INDICATOR=$HEAVY_CHECK_MARK
	PAIR_CLASS="indicator_green"
	PAIR_STATUS="running"
else
	PAIR_INDICATOR=$HEAVY_BALLOT_X
	PAIR_CLASS="indicator_red"
	PAIR_STATUS="not running"
fi

#----------------------------------------------------------------------------------------
# Determine state of check boxes.
#----------------------------------------------------------------------------------------
# Function to check the show log radio button according to selection
case "$LOGSHOW" in
	yes) LOGSHOWyes="checked" ;;
	*) LOGSHOWno="checked" ;;
esac

[ -f $TCEMNT/tce/optional/pcp-bt6.tcz ] && DISABLE_BT="" || DISABLE_BT="disabled"

pcp_bt_status_indicators() {
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
	echo '                    <li>Controller address '$(pcp_bt_controller_address)
	echo '                    <li>If the controller address is listed, try turning the power on below.</li>'
	echo '                    <li>If using RPi built-in bluetooth, make sure controller is enabled at the bottom of this page.</li>'
	echo '                    <li>Check kernel messages in diagnostics <a href="diagnostics.cgi#dmesg">dmesg</a>.</li>'
	echo '                  </ul>'
	echo '                </div>'
	echo '              </td>'
	echo '            </tr>'
	[ "$PWR_STATUS" = "Off" ] && pcp_showmore $ID
	pcp_incr_id
	pcp_toggle_row_shade
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150 center">'
	echo '                <p class="'$CD_CLASS'">'$CD_INDICATOR'</p>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>BT Speaker Daemon is '$CD_STATUS'&nbsp;&nbsp;'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <ul>'
	echo '                    <li><span class="indicator_green">&#x2714;</span> = BT Speaker Daemon is running.</li>'
	echo '                    <li><span class="indicator_red">&#x2718;</span> = BT Speaker Daemon is not running.</li>'
	echo '                  </ul>'
	echo '                </div>'
	echo '              </td>'
	echo '            </tr>'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150 center">'
	echo '                <p class="'$PAIR_CLASS'">'$PAIR_INDICATOR'</p>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>BT Pairing Daemon for incoming connections is '$PAIR_STATUS'&nbsp;&nbsp;'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <ul>'
	echo '                    <li>This is critical to be running to pair a phone.'
	echo '                    <li><span class="indicator_green">&#x2714;</span> = BT Pairing Daemon is running.</li>'
	echo '                    <li><span class="indicator_red">&#x2718;</span> = BT Pairing Daemon is not running.</li>'
	echo '                  </ul>'
	echo '                </div>'
	echo '              </td>'
	echo '            </tr>'
}
[ $MODE -ge $MODE_BETA ] && pcp_bt_status_indicators

#----------------------------------------------------------------------------------------
echo '            <tr class="padding '$ROWSHADE'">'
echo '              <td></td>'
echo '              <td></td>'
echo '            </tr>'
echo '          </table>'

pcp_bt_beta_mode_required() {
	echo '          <table class="bggrey percent100">'
	echo '            <tr class="warning">'
	echo '              <td>'
	echo '                <p><b>Warning:</b> Beta Mode is required for Bluetooth functions to be enabled.</p>'
	echo '              </td>'
	echo '            </tr>'
	echo '          </table>'
}

#------------------------------------------Install/uninstall BT Mode---------------------
pcp_bt_install() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '          <form name="Install" action="'$0'">'
	echo '            <table class="bggrey percent100">'
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	if [ ! -f $TCEMNT/tce/optional/pcp-bt6.tcz ]; then
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
	echo '            </table>'
	echo '          </form>'
}
[ $MODE -ge $MODE_BETA ] && pcp_bt_install || pcp_bt_beta_mode_required
#----------------------------------------------------------------------------------------

#------------------------------------------Start and Stop BT Daemon----------------------
pcp_bt_startstop() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '          <form name="Power" action="'$0'">'
	echo '            <table class="bggrey percent100">'
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	if [ "$PWR_STATUS" = "On" ]; then
		echo '                  <button type="submit" name="ACTION" value="Power_off" '$DISABLE_BT'>Power Off</button>'
		P="off"
	else
		echo '                  <button type="submit" name="ACTION" value="Power_on" '$DISABLE_BT'>Power On</button>'
		P="on"
	fi
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Turn the BT Controller '$P'&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>This will turn '$P' the Bluetooth Controller.</p>'
	echo '                    <p>If turned off, nothing will be able to connect to this pCP device via bluetooth.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </table>'
	echo '          </form>'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '          <form name="Restart" action="'$0'">'
	echo '            <table class="bggrey percent100">'
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                  <button type="submit" name="ACTION" value="Restart" '$DISABLE_BT'>Restart</button>'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Restart Bluetooth Speaker Daemon on pCP&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>This will restart the Bluetooth Speaker Daemon on pCP.</p>'
	echo '                    <p>If the speaker is already connected, this may disconnect speaker/squeezelite.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </table>'
	echo '          </form>'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '            <form name="Restart2" action="'$0'">'
	echo '            <table class="bggrey percent100">'
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                  <button type="submit" name="ACTION" value="Restart_pair" '$DISABLE_BT'>Restart</button>'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Restart Bluetooth Pairing Daemon on pCP&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>This will restart the Bluetooth Pairing Daemon on pCP.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </table>'
	echo '          </form>'
}
[ $MODE -ge $MODE_BETA ] && pcp_bt_startstop
#-------------------_------------Show BT logs--------------------------------------------
pcp_bt_show_logs() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '          <form name="Show" action="'$0'" method="get">'
	echo '            <table class="bggrey percent100">'
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
	echo '            </table>'
	echo '          </form>'
}
[ $MODE -ge $MODE_NORMAL ] && pcp_bt_show_logs
#----------------------------------------------------------------------------------------
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
#------------------------------------------Scan/Pair BT ---------------------
pcp_bt_scan() {
	pcp_incr_id
	pcp_start_row_shade
	echo '          <form name="Discover" action="'$0'">'
	echo '            <table class="bggrey percent100">'
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="ACTION" value="Discover" '$DISABLE_BT'/>'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Set this device to be discoverable.  Look for '$(hostname)' on your device.&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>This will allow pCP to be discoverable and pairable by your phone or other device.</p>'
	echo '                    <p>Integrates with Streamer to play from you phone over bluetooth to your LMS system.</p>'
	echo '                    <p>&nbsp;&nbsp;Install Streamer from the <a href="tweaks.cgi#Audio">Tweaks Page</a>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </table>'
	echo '          </form>'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '          <form name="Scan" action="'$0'">'
	echo '            <table class="bggrey percent100">'
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
	echo '            </table>'
	echo '          </form>'

	if [ -f /tmp/btscan.out ]; then
		PAIR_DISABLED=""
		sed '/^'$BTDEVICE'/! s/selected/notselected/' < /tmp/btscan.out >/tmp/btscan.dd
		sed -i 's/ \#/\#/' /tmp/btscan.dd
	else
		echo "0#No Device#selected" >/tmp/btscan.dd
		PAIR_DISABLED="disabled"
	fi

	pcp_incr_id
	pcp_toggle_row_shade
	if [ "$PAIR_DISABLED" = "" ]; then
		echo '          <form name="Pair" action="'$0'">'
		echo '            <table class="bggrey percent100">'
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
			echo '                  <p>Run a Scan to Find Devices.</p>'
		fi
		echo '                </td>'
		echo '              </tr>'
		echo '            </table>'
		echo '          </form>'
	else
		echo '          <table class="bggrey percent100">'
		echo '            <tr class="'$ROWSHADE'">'
		echo '              <td class="column150 center"></td>'
		echo '              <td class="colspan=2">'
		echo '                 <p>Run scan to discover/pair to a new device.</p>'
		echo '              </td>'
		echo '            </tr>'
		echo '         </table>'
	fi
	COL1="column100"
	COL2="column150"
	COL3="column150"
	COL4="column150"
	COL5="column120"
	COL6="column150"
	COL7="column150"

	pcp_toggle_row_shade
	echo '          <table class="bggrey percent100">'
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="'$COL1'"><p><b>Connected</b></p></td>'
	echo '              <td class="'$COL2'"><p><b>BT Mac Address</b></p></td>'
	echo '              <td class="'$COL3'"><p><b>BT Name</b></p></td>'
	echo '              <td class="'$COL4'"><p><b>Player Name</b></p></td>'
	echo '              <td class="'$COL5'"><p><b>BT Delay</b></p></td>'
	echo '              <td class="'$COL6'"><p><b>Disconnect Device</b></p></td>'
	echo '              <td class="'$COL7'"><p><b>Forget Device</b></p></td>'
	echo '            </tr>'
	echo '          </table>'

	pcp_bt_paired_devices
	if [ -f $PAIRED_LIST ]; then
		I=1
		echo '          <form name="Select" action="'$0'">'
		echo '            <table class="bggrey percent100">'
		while read line; do
			BTMAC=$(echo $line | cut -d'#' -f1)
			BTNAME=$(echo $line | cut -d'#' -f2)
			BTPLAYERNAME=$(cat $BTDEVICECONF | grep $BTMAC | cut -d'#' -f2)
			BTDELAY=$(cat $BTDEVICECONF | grep $BTMAC | cut -d'#' -f3)
			[ "$BTPLAYERNAME" = "" ] && BTPLAYERNAME=$BTNAME
			[ "$BTDELAY" == "" ] && BTDELAY=10000
			REQUIRED="required"

			if [ $(bluetoothctl info $BTMAC | grep "Connected" | cut -d':' -f2) = "yes" ]; then
				DEV_INDICATOR=$HEAVY_CHECK_MARK
				DEV_CLASS="indicator_green"
			else
				DEV_INDICATOR=$HEAVY_BALLOT_X
				DEV_CLASS="indicator_red"
			fi

			pcp_incr_id
			pcp_toggle_row_shade
			echo '              <tr class="'$ROWSHADE'">'
			echo '                <td class="'$COL1' center">'
			echo '                  <p class="'$DEV_CLASS'">'$DEV_INDICATOR'</p>'
			echo '                </td>'
			echo '                <td class="'$COL2'">'
			echo '                  <input type="hidden" id="idBTMAC'${I}'" name="BTMAC'${I}'" value="'$BTMAC'">'
			echo '                  <input class="large10" type="text" name="MAC" value="'$BTMAC'" title="Bluetooth MAC Address" '$REQUIRED' disabled>'
			echo '                </td>'
			echo '                <td class="'$COL3'">'
			echo '                  <input type="hidden" id="idBTNAME'${I}'" name="BTNAME'${I}'" value="'$BTNAME'">'
			echo '                  <input class="large10" type="text" name="NAME" value="'$BTNAME'" title="Bluetooth Device Name" '$REQUIRED' disabled>'
			echo '                </td>'
			echo '                <td class="'$COL4'">'
			echo '                  <input class="large10" type="text" id="idBTPLAYERNAME'${I}'" name="BTPLAYERNAME'${I}'" value="'$BTPLAYERNAME'" title="Bluetooth Player Name" '$REQUIRED'>'
			echo '                </td>'
			echo '                <td class="'$COL5'">'
			echo '                  <input class="large6" type="text" id="idBTDELAY'${I}'" name="BTDELAY'${I}'" value="'$BTDELAY'" title="Bluetooth Delay" '$REQUIRED'>'
			echo '                </td>'
			echo '                <td class="'$COL6'">'
			echo '                  <button type="submit" name="ACTION" value="Disconnect'${I}'">Disconnect</button>'
			echo '                </td>'
			echo '                <td class="'$COL7'">'
			echo '                  <button type="submit" name="ACTION" value="Forget'${I}'">Forget</button>'
			echo '                </td>'
			echo '              </tr>'
			I=$((I + 1))
		done < $PAIRED_LIST
		echo '              <tr class="'$ROWSHADE'">'
		echo '                <td class="'$COL1' center">'
		echo '                  <input type="hidden" name="NUMDEVICES" value="'$I'">'
		echo '                  <input type="submit" name="ACTION" value="Save" />'
		echo '                </td>'
		echo '                <td colspan="6"></td>'
		echo '              </tr>'
		echo '            </table>'
		echo '          </form>'
	else
		pcp_toggle_row_shade
		echo '          <table class="bggrey percent100">'
		echo '            <tr class="'$ROWSHADE'">'
		echo '              <td class="column200">'
		echo '                <p>No Paired Device</p>'
		echo '              </td>'
		echo '            </tr>'
		echo '          </table>'
	fi
}
[ $MODE -ge $MODE_BETA ] && pcp_bt_scan

#----------------------------------------------------------------------------------------
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------

if [ $(pcp_rpi_has_inbuilt_wifi) -eq 0 ] || [ $TEST -eq 1 ]; then
#--------------------------------------Built-in Wifi-------------------------------------
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <form id="rpiwifi" name="builtinwifi" action="writetowifi.cgi" method="get">'
	echo '        <div class="row">'
	echo '          <fieldset>'
	echo '            <legend>RPi Built in WiFi/BT</legend>'
	echo '            <table class="bggrey percent100">'
	pcp_start_row_shade
	pcp_incr_id
	case "$RPI3INTWIFI" in
		on) RPIWIFIyes="checked" ;;
		off) RPIWIFIno="checked" ;;
	esac
	COL1="column150"
	COL2="column150"
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL1'">'
	echo '                  <p>RPi built-in Wifi</p>'
	echo '                </td>'
	echo '                <td class="'$COL2'">'
	echo '                  <input class="small1" type="radio" name="RPI3INTWIFI" value="on" '$RPIWIFIyes'>On&nbsp;&nbsp;&nbsp;'
	echo '                  <input class="small1" type="radio" name="RPI3INTWIFI" value="off" '$RPIWIFIno'>Off'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Turn off Raspberry Pi built-in wifi&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>This will load an overlay that disables built-in wifi.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
#--------------------------------------Built-in Bluetooth--------------------------------
	case "$RPIBLUETOOTH" in
		on) RPIBLUETOOTHyes="checked" ;;
		off) RPIBLUETOOTHno="checked" ;;
	esac
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL1'">'
	echo '                  <p>RPi built-in Bluetooth</p>'
	echo '                </td>'
	echo '                <td class="'$COL2'">'
	echo '                  <input class="small1" type="radio" name="RPIBLUETOOTH" value="on" '$RPIBLUETOOTHyes'>On&nbsp;&nbsp;&nbsp;'
	echo '                  <input class="small1" type="radio" name="RPIBLUETOOTH" value="off" '$RPIBLUETOOTHno'>Off'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Turn off Raspberry Pi built-in bluetooth&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>This will load an overlay that disables built-in bluetooth.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
#--------------------------------------Buttons------------------------------------------
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td colspan="3">'
	echo '                  <input type="hidden" name="FROM_PAGE" value="bluetooth.cgi">'
	echo '                  <input type="submit" name="ACTION" value="Save">'
	echo '                </td>'
	echo '              </tr>'
	echo '            </table>'
	echo '          </fieldset>'
	echo '        </div>'
	echo '      </form>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
fi
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
