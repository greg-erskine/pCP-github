#!/bin/sh

# Version: 3.5.0 2017-12-26
#	Initial version. PH.

. pcp-functions
. pcp-rpi-functions
. pcp-lms-functions

pcp_html_head "WIFI AP Mode Settings" "PH"

pcp_picoreplayers_toolbar
pcp_controls
pcp_banner
pcp_navigation
pcp_remove_query_string
pcp_httpd_query_string

HOSTAPDCONF=/usr/local/etc/pcp/hostapd.conf
DNSMASQCONF=/usr/local/etc/pcp/dnsmasq.conf

#---------------------------Routines-----------------------------------------------------

pcp_install_apmode() {
	echo '[ INFO ] Downloading AP Mode...'
	sudo -u tc pcp-load -r $PCP_REPO -w pcp-apmode.tcz
	if [ -f $TCEMNT/tce/optional/pcp-apmode.tcz ]; then
		echo '[ INFO ] Installing AP Mode...'
		sudo -u tc pcp-load -i pcp-apmode.tcz
		sudo sed -i '/pcp-apmode.tcz/d' $ONBOOTLST
		sudo echo 'pcp-apmode.tcz' >> $ONBOOTLST
		[ $DEBUG -eq 1 ] && echo '[ DEBUG ] pcp-apmode is added to onboot.lst'
		[ $DEBUG -eq 1 ] && cat $ONBOOTLST
	fi
}

pcp_remove_apmode() {
	sudo /usr/local/etc/init.d/pcp-apmode stop >/dev/null 2>&1
	sudo -u tc tce-audit builddb
	sudo -u tc tce-audit delete pcp-apmode.tcz
	sudo sed -i '/pcp-apmode.tcz/d' $ONBOOTLST
	echo "Removeing configuration files"
	rm -f $HOSTAPDCONF
	rm -f $DNSMASQCONF
}

pcp_apmode_status(){
	sudo /usr/local/etc/init.d/pcp-apmode status >/dev/null 2>&1
	echo $?
}

set_hostapd_conf(){
	echo '[ INFO ] Setting Host AP SSID to '$AP_SSID
	sudo sed -i "s/\(^ssid=\).*/\1$AP_SSID/" $HOSTAPDCONF
	echo '[ INFO ] Setting AP Channel to '$AP_CHANNEL
	sudo sed -i "s/\(^channel=\).*/\1$AP_CHANNEL/" $HOSTAPDCONF
	echo '[ INFO ] Setting AP Passphrase'
	PSK_HEX=$(echo "$AP_PASS" | wpa_passphrase "$AP_SSID" | grep "psk=" | grep -v "#psk=" | cut -d "=" -f2)
	[ $DEBUG -eq 1 ] && echo 'PSK='$PSK_HEX
	sudo sed -i "s/\(^#wpa_passphrase=\).*/\1$AP_PASS/" $HOSTAPDCONF
	sudo sed -i "s/\(^wpa_psk=\).*/\1$PSK_HEX/" $HOSTAPDCONF
}

set_dnsmasq_conf(){
	RANGE=$(echo $AP_IP | awk -F. '{print $1"."$2"."$3".10,"$1"."$2"."$3".100,12h"}')
	sudo sed -i "s/\(^dhcp-range=\).*/\1$RANGE/" $DNSMASQCONF
}

REBOOT_REQUIRED=0
case "$ACTION" in
	Autostart)
		pcp_table_top "AP Mode Configuration"
		echo '                <textarea class="inform" style="height:60px">'
		[ "$APMODE" = "yes" ] && echo '[ INFO ] Enabling pCP AP Mode at boot...' || echo '[ INFO ] Disabling pCP AP Mode at boot...'
		pcp_save_to_config
		pcp_backup "nohtml"
		echo '                </textarea>'
		pcp_table_end
	;;
	Start)
		pcp_table_top "AP Mode"
		echo '                <textarea class="inform" style="height:40px">'
		if [ ! -x /usr/local/etc/init.d/pcp-apmode ]; then
			echo '[ INFO ] Loading pCP AP Mode extensions...'
			sudo -u tc tce-load -i pcp-apmode.tcz
		fi
		echo '[ INFO ] Starting AP Mode...'
		echo -n '[ INFO ] '
		sudo /usr/local/etc/init.d/pcp-apmode start
		echo '                </textarea>'
		pcp_table_end
	;;
	Stop)
		pcp_table_top "AP Mode"
		echo '                <textarea class="inform" style="height:40px">'
		echo '[ INFO ] Stopping AP Mode...'
		echo -n '[ INFO ] '
		sudo /usr/local/etc/init.d/pcp-apmode stop
		echo '                </textarea>'
		pcp_table_end
		sleep 2
	;;
	Install)
		pcp_table_top "Downloading AP Mode"
		pcp_sufficient_free_space 4500
		if [ $? -eq 0 ] ; then
			echo '                <textarea class="inform" style="height:160px">'
			pcp_install_apmode
			if [ -f $TCEMNT/tce/optional/pcp-apmode.tcz ]; then
				APMODE="yes"
				AP_IP="10.10.10.1"
				pcp_save_to_config
				pcp_backup "nohtml"
			else
				echo '[ ERROR ] Error Downloading AP Mode, please try again later.'
			fi
			echo '                </textarea>'
			pcp_table_end
		fi
	;;
	Remove)
		pcp_table_top "Removing AP Mode Extensions from pCP"
		echo '                <textarea class="inform" style="height:120px">'
		echo '[ INFO ] Removing AP Mode Extensions...'
		echo
		echo 'After a reboot these extensions will be permanently deleted:'
		APMODE="no"
		pcp_save_to_config
		pcp_remove_apmode
		pcp_backup "nohtml"
		echo '                </textarea>'
		pcp_table_end
		REBOOT_REQUIRED=1
	;;
	Restart)
		pcp_table_top "AP Mode"
		echo '                <textarea class="inform" style="height:60px">'
		echo '[ INFO ] Restarting AP Mode...'
		echo -n '[ INFO ] '
		sudo /usr/local/etc/init.d/pcp-apmode stop
		echo -n '[ INFO ] '
		sudo /usr/local/etc/init.d/pcp-apmode start
		echo '                </textarea>'
		pcp_table_end
	;;
	Setconfig)
		pcp_table_top "AP Mode configuration"
		echo '                <textarea class="inform" style="height:120px">'
		echo '[ INFO ] Setting AP Mode Configuration...'
		set_hostapd_conf
		if [ $(echo $AP_IP | awk -F. '{print $4}') -ne 1 ]; then
			echo '[ WARN ] Router IP address must end in .1'
			AP_IP=$(echo $AP_IP | sed 's/[^.]*$/1/')
		fi
		echo '[ INFO ] Setting IP to '$AP_IP
		pcp_save_to_config
		set_dnsmasq_conf
		echo -n '[ INFO ] Restarting AP.....'
		sudo /usr/local/etc/init.d/pcp-apmode restart
		[ $? -eq 0 ] && echo 'Done' || echo 'Error'
		echo '                </textarea>'
		pcp_backup "nohtml"
		pcp_table_end
	;;
	Update)
		pcp_table_top "AP Mode"
		pcp_sufficient_free_space 4500
		echo '                <textarea class="inform" style="height:100px">'
		echo '[ INFO ] Updating AP Mode Extensions...'
		sudo -u tc pcp-update pcp-apmode.tcz
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
echo '          <legend>Wifi Access Point Configuration</legend>'
echo '          <table class="bggrey percent100">'

#------------------------------------LMS Indication--------------------------------------
if [ $(pcp_apmode_status) -eq 0 ]; then
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
# Function to check the radio button according to config file
case "$APMODE" in
	yes) APMODEyes="checked" ;;
	no) APMODEno="checked" ;;
esac
[ -f $TCEMNT/tce/optional/pcp-apmode.tcz ] && DISABLE_AP="" || DISABLE_AP="disabled"

pcp_incr_id
pcp_start_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td class="column150 center">'
echo '                <p class="'$CLASS'">'$INDICATOR'</p>'
echo '              </td>'
echo '              <td>'
echo '                <p>AP Mode is '$STATUS'&nbsp;&nbsp;'
echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                </p>'
echo '                <div id="'$ID'" class="less">'
echo '                  <ul>'
echo '                    <li><span class="indicator_green">&#x2714;</span> = AP Mode running.</li>'
echo '                    <li><span class="indicator_red">&#x2718;</span> = AP Mode not running.</li>'
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

#-----------------------------------Enable/disable autostart of AP Mode------------------
pcp_ap_enable() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '            <form name="Autostart" action="'$0'">'
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                  <button type="submit" name="ACTION" value="Autostart" '$DISABLE_AP'>Set Autostart</button>'
	echo '                </td>'
	echo '                <td class="column100">'
	echo '                  <input class="small1" type="radio" name="APMODE" value="yes" '$APMODEyes'>Yes'
	echo '                  <input class="small1" type="radio" name="APMODE" value="no" '$APMODEno'>No'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Automatic start of AP Mode when pCP boots&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Yes - will enable automatic start of AP Mode when pCP boots.</p>'
	echo '                    <p>No - will disable automatic start of AP Mode when pCP boots.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_BETA ] && pcp_ap_enable
#----------------------------------------------------------------------------------------

#------------------------------------------Install/uninstall AP Mode---------------------
pcp_ap_install() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '            <form name="Install" action="'$0'">'
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	if [ ! -f $TCEMNT/tce/optional/pcp-apmode.tcz ]; then
		echo '                  <input type="submit" name="ACTION" value="Install" />'
		echo '                </td>'
		echo '                <td>'
		echo '                  <p>Install AP Mode on pCP&nbsp;&nbsp;'
		echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
		echo '                  </p>'
		echo '                  <div id="'$ID'" class="less">'
		echo '                    <p>This will install AP Mode on pCP.</p>'
		echo '                  </div>'
	else
		echo '                  <input type="submit" name="ACTION" value="Update" />'
		echo '                </td>'
		echo '                <td class="column150 center">'
		echo '                  <input type="submit" name="ACTION" value="Remove" onclick="return confirm('\''This will remove AP Mode from pCP.\n\nAre you sure?'\'')"/>'
		echo '                </td>'
		echo '                <td>'
		echo '                  <p>Update or Remove AP Mode from pCP&nbsp;&nbsp;'
		echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
		echo '                  </p>'
		echo '                  <div id="'$ID'" class="less">'

		echo '                    <p>This will remove AP Mode and all the extra packages that were added with Hostapd.</p>'
		echo '                  </div>'
	fi
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_BETA ] && pcp_ap_install
#----------------------------------------------------------------------------------------

#------------------------------------------Start and Stop AP Mode---------------------
pcp_ap_startstop() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '            <form name="Start" action="'$0'">'
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="ACTION" value="Start" '$DISABLE_AP'/>'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Start AP Mode on pCP&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>This will start AP Mode on pCP.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '            <form name="Stop" action="'$0'">'
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="ACTION" value="Stop" onclick="return confirm('\''STOP AP Mode.\n\nAre you sure?'\'')" '$DISABLE_AP'/>'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Stop AP Mode on pCP.&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>This will Stop AP Mode on pCP.</p>'
	echo '                    <p>You may loose access to your device, unless it is already connected to hardwire connection.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '            <form name="Restart" action="'$0'">'
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="ACTION" value="Restart" '$DISABLE_AP'/>'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Restart AP Mode on pCP&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>This will restart AP Mode on pCP.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_BETA ] && pcp_ap_startstop
#----------------------------------------------------------------------------------------

#------------------------------------------Configure      AP Mode---------------------
pcp_ap_configure(){
	AP_SSID=$(cat $HOSTAPDCONF | grep -e "^ssid=" | cut -d "=" -f2)
	AP_CHANNEL=$(cat $HOSTAPDCONF | grep -e "^channel=" | cut -d "=" -f2)
	AP_PASS=$(cat $HOSTAPDCONF | grep -e "^\#wpa_passphrase=" | cut -d "=" -f2)

	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <form name="setconfig" action="'$0'">'
	echo '                <tr class="'$ROWSHADE'">'
	echo '                  <td class="column150 center">'
	echo '                    <p class="row">AP SSID</p>'
	echo '                  </td>'
	echo '                  <td class="column210">'
	echo '                    <p><input class="large12" type="text" name="AP_SSID" value="'$AP_SSID'" required"></p>'
	echo '                  </td>'
	echo '                  <td>'
	echo '                    <p>This is the SSID of the AP.&nbsp;&nbsp;'
	echo '                      <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                    </p>'
	echo '                    <div id="'$ID'" class="less">'
	echo '                      <p>Set the SSID of your AP.</p>'
	echo '                    </div>'
	echo '                  </td>'
	echo '                </tr>'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '                <tr class="'$ROWSHADE'">'
	echo '                  <td class="column150 center">'
	echo '                    <p class="row">AP Channel</p>'
	echo '                  </td>'
	echo '                  <td class="column210">'
	echo '                    <p><input class="large12" type="text" name="AP_CHANNEL" value="'$AP_CHANNEL'" required"></p>'
	echo '                  </td>'
	echo '                  <td>'
	echo '                    <p>This is the Wireless Channel of the AP.&nbsp;&nbsp;'
	echo '                      <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                    </p>'
	echo '                    <div id="'$ID'" class="less">'
	echo '                      <p>Set the SSID of your AP.</p>'
	echo '                    </div>'
	echo '                  </td>'
	echo '                </tr>'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '                <tr class="'$ROWSHADE'">'
	echo '                  <td class="column150 center">'
	echo '                    <p class="row">IP Address of the AP</p>'
	echo '                  </td>'
	echo '                  <td class="column210">'
	echo '                    <p><input class="large12" type="text" name="AP_IP" value="'$AP_IP'" required pattern="((^|\.)((25[0-5])|(2[0-4]\d)|(1\d\d)|([1-9]?\d))){4}$"></p>'
	echo '                  </td>'
	echo '                  <td>'
	echo '                    <p>This is the IP address used for the AP.&nbsp;&nbsp;'
	echo '                      <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                    </p>'
	echo '                    <div id="'$ID'" class="less">'
	echo '                      <p>Clients that connect to this AP will get a DHCP address in starting at .10 of the same IP range.</p>'
	echo '                    </div>'
	echo '                  </td>'
	echo '                </tr>'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '                <tr class="'$ROWSHADE'">'
	echo '                  <td class="column150 center">'
	echo '                    <p class="row">Password:</p>'
	echo '                  </td>'
	echo '                  <td class="column210">'
	echo '                    <p><input class="large12" type="password" name="AP_PASS" value="'$AP_PASS'" required pattern=".{8,63}"></p>'
	echo '                  </td>'
	echo '                  <td>'
	echo '                    <p>WPA2 Passphrase to be used to access AP.&nbsp;&nbsp;'
	echo '                      <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                    </p>'
	echo '                    <div id="'$ID'" class="less">'
	echo '                      <p>Default password is piCorePlayer.</p>'
	echo '                    </div>'
	echo '                  </td>'
	echo '                </tr>'
	#--------------------------------------Submit button-------------------------------------
	pcp_toggle_row_shade
	echo '                <tr class="'$ROWSHADE'">'
	echo '                  <td class="column150 center">'
#	echo '                    <input type="hidden" name="COMMAND" value="setconfig">'
	echo '                    <button type="submit" name="ACTION" value="Setconfig">Set AP Config</button>'
	echo '                  </td>'
	echo '                </tr>'
	echo '              </form>'
}
[ $MODE -ge $MODE_BETA ] && pcp_ap_configure
#----------------------------------------------------------------------------------------
echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------

pcp_footer
[ $MODE -ge $MODE_NORMAL ] && pcp_mode
pcp_copyright

echo '</body>'
echo '</html>'
