#!/bin/sh

# Version: 4.0.1 2018-09-19

. pcp-functions
. pcp-rpi-functions
. pcp-lms-functions
. pcp-wifi-functions

APMODECONF="/usr/local/etc/pcp/apmode.conf"
HOSTAPDCONF="/usr/local/etc/pcp/hostapd.conf"
DNSMASQCONF="/usr/local/etc/pcp/dnsmasq.conf"

[ -f $APMODECONF ] && . $APMODECONF

pcp_html_head "WIFI AP Mode Settings" "PH"

pcp_picoreplayers_toolbar
pcp_controls
pcp_banner
pcp_navigation
pcp_remove_query_string
pcp_httpd_query_string

[ -z $AP_BRIDGE ] && AP_BRIDGE=0

#----------------------------------Routines----------------------------------------------
pcp_install_apmode() {
	echo '[ INFO ] Downloading AP Mode...'
	sudo -u tc pcp-load -r $PCP_REPO -w pcp-apmode.tcz
	if [ -f $TCEMNT/tce/optional/pcp-apmode.tcz ]; then
		echo '[ INFO ] Installing AP Mode...'
		sudo -u tc pcp-load -i firmware-atheros.tcz
		sudo -u tc pcp-load -i firmware-brcmwifi.tcz
		sudo -u tc pcp-load -i firmware-ralinkwifi.tcz
		sudo -u tc pcp-load -i firmware-rtlwifi.tcz
		sudo -u tc pcp-load -i firmware-rpi3-wireless.tcz
		sudo -u tc pcp-load -i pcp-apmode.tcz
		pcp_wifi_update_wifi_onbootlst
		pcp_wifi_update_onbootlst "add" "pcp-apmode.tcz"
		[ $DEBUG -eq 1 ] && echo '[ DEBUG ] pcp-apmode is added to onboot.lst'
		[ $DEBUG -eq 1 ] && cat $ONBOOTLST
		echo '[ INFO ] If wifi is not recognized, please reboot device...'
	fi
}

pcp_remove_apmode() {
	sudo /usr/local/etc/init.d/pcp-apmode stop >/dev/null 2>&1
	sudo -u tc tce-audit builddb
	sudo -u tc tce-audit delete pcp-apmode.tcz
	sudo sed -i '/firmware-atheros.tcz/d' $ONBOOTLST
	sudo sed -i '/firmware-brcmwifi.tcz/d' $ONBOOTLST
	sudo sed -i '/firmware-rpi3-wireless.tcz/d' $ONBOOTLST
	sudo sed -i '/firmware-ralinkwifi.tcz/d' $ONBOOTLST
	sudo sed -i '/firmware-rtlwifi.tcz/d' $ONBOOTLST
	sudo sed -i '/pcp-apmode.tcz/d' $ONBOOTLST
	echo "Removing configuration files..."
	rm -f $APMODECONF
	rm -f $HOSTAPDCONF
	rm -f $DNSMASQCONF
	rm -f /usr/local/etc/pcp/pcp_hosts
}

pcp_apmode_status() {
	sudo /usr/local/etc/init.d/pcp-apmode status >/dev/null 2>&1
	echo $?
}

set_hostapd_conf() {
	echo '[ INFO ] Setting Host AP SSID to '$AP_SSID
	sudo sed -i "s/\(^ssid=\).*/\1$AP_SSID/" $HOSTAPDCONF
	echo '[ INFO ] Setting AP Passphrase'
	PSK_HEX=$(echo "$AP_PASS" | wpa_passphrase "$AP_SSID" | grep "psk=" | grep -v "#psk=" | cut -d "=" -f2)
	[ $DEBUG -eq 1 ] && echo 'PSK='$PSK_HEX
	sudo sed -i "s/\(^#wpa_passphrase=\).*/\1$AP_PASS/" $HOSTAPDCONF
	sudo sed -i "s/\(^wpa_psk=\).*/\1$PSK_HEX/" $HOSTAPDCONF
	echo '[ INFO ] Setting AP Country Code to '$AP_COUNTRY
	sudo sed -i "s/\(^country_code=\).*/\1$AP_COUNTRY/" $HOSTAPDCONF
	echo '[ INFO ] Setting AP Channel to '$AP_CHANNEL
	sudo sed -i "s/\(^channel=\).*/\1$AP_CHANNEL/" $HOSTAPDCONF
	[ $AP_CHANNEL -le 14 ] && AP_HWMODE="g" || AP_HWMODE="a"
	echo '[ INFO ] Setting AP harware mode to '$AP_HWMODE'. (a=5GHz, g=2.4GHz)'
	sudo sed -i "s/\(^hw_mode=\).*/\1$AP_HWMODE/" $HOSTAPDCONF
	echo '[ INFO ] Setting AP 80211AC to '$AP_80211AC
	sudo sed -i "s/\(^ieee80211ac=\).*/\1$AP_80211AC/" $HOSTAPDCONF
}

set_apmode_conf() {
	echo '[ INFO ] Setting Bridge mode to '$AP_BRIDGE
	echo "AP_BRIDGE=$AP_BRIDGE" > $APMODECONF
}

set_dnsmasq_conf() {
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
		sleep 2
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
		sleep 5
		echo -n '[ INFO ] '
		sudo /usr/local/etc/init.d/pcp-apmode start
		echo '                </textarea>'
		pcp_table_end
		sleep 2
	;;
	Setconfig)
		pcp_table_top "AP Mode configuration"
		echo '                <textarea class="inform" style="height:180px">'
		echo '[ INFO ] Setting AP Mode Configuration...'
		set_apmode_conf
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
		pcp_backup "nohtml"
		echo '                </textarea>'
		pcp_table_end
	;;
	Update)
		pcp_table_top "AP Mode"
		pcp_sufficient_free_space 4700
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
echo '      <form name="AP mode" action="'$0'">'
echo '        <div class="row">'
echo '          <fieldset>'
echo '            <legend>Wifi Access Point (AP)</legend>'
echo '            <table class="bggrey percent100">'

#----------------------------------AP Mode Indication------------------------------------
if [ $(pcp_apmode_status) -eq 0 ]; then
	pcp_green_tick "running"
else
	pcp_red_cross "not running"
fi
#----------------------------------------------------------------------------------------
# Determine state of check boxes.
#----------------------------------------------------------------------------------------
case "$APMODE" in
	yes) APMODEyes="checked" ;;
	no) APMODEno="checked" ;;
esac
[ -f $TCEMNT/tce/optional/pcp-apmode.tcz ] && DISABLE_AP="" || DISABLE_AP="disabled"

pcp_incr_id
pcp_start_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="column150 center">'
echo '                  <p class="'$CLASS'">'$INDICATOR'</p>'
echo '                </td>'
echo '                <td colspan="2">'
echo '                  <p>AP Mode is '$STATUS'&nbsp;&nbsp;'
echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                  </p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <ul>'
echo '                      <li><span class="indicator_green">&#x2714;</span> = AP Mode running.</li>'
echo '                      <li><span class="indicator_red">&#x2718;</span> = AP Mode not running.</li>'
echo '                    </ul>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'
#----------------------------------Padding-----------------------------------------------
pcp_toggle_row_shade
echo '              <tr class="padding '$ROWSHADE'">'
echo '                <td colspan="3"></td>'
echo '              </tr>'
#----------------------------------Enable/disable autostart of AP Mode-------------------
pcp_ap_enable() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                  <button type="submit" name="ACTION" value="Autostart" '$DISABLE_AP'>Set Autostart</button>'
	echo '                </td>'
	echo '                <td class="column150">'
	echo '                  <input class="small1" type="radio" name="APMODE" value="yes" '$APMODEyes'>Yes&nbsp;&nbsp;'
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
}
[ $MODE -ge $MODE_BETA ] && pcp_ap_enable
#----------------------------------------------------------------------------------------

#----------------------------------Install/uninstall AP Mode-----------------------------
pcp_ap_install() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	if [ ! -f $TCEMNT/tce/optional/pcp-apmode.tcz ]; then
		echo '                <td class="column150 center">'
		echo '                  <input type="submit" name="ACTION" value="Install">'
		echo '                </td>'
		echo '                <td>'
		echo '                  <p>Install AP Mode on pCP&nbsp;&nbsp;'
		echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
		echo '                  </p>'
		echo '                  <div id="'$ID'" class="less">'
		echo '                    <p>This will install AP Mode on pCP.</p>'
		echo '                  </div>'
		echo '                </td>'
	else
		echo '                <td class="column150 center">'
		echo '                  <input type="submit" name="ACTION" value="Update">'
		echo '                </td>'
		echo '                <td class="column150 center">'
		echo '                  <input type="submit" name="ACTION" value="Remove" onclick="return confirm('\''This will remove AP Mode from pCP.\n\nAre you sure?'\'')">'
		echo '                </td>'
		echo '                <td>'
		echo '                  <p>Update or Remove AP Mode from pCP&nbsp;&nbsp;'
		echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
		echo '                  </p>'
		echo '                  <div id="'$ID'" class="less">'
		echo '                    <p>This will remove AP Mode and all the extra packages that were added with Hostapd.</p>'
		echo '                  </div>'
		echo '                </td>'
	fi
	echo '              </tr>'
}
[ $MODE -ge $MODE_BETA ] && pcp_ap_install
#----------------------------------------------------------------------------------------

#----------------------------------Start AP Mode-----------------------------------------
pcp_ap_startstop() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="ACTION" value="Start" '$DISABLE_AP'>'
	echo '                </td>'
	echo '                <td colspan="2">'
	echo '                  <p>Start AP Mode on pCP&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>This will start AP Mode on pCP.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
#----------------------------------Stop AP Mode------------------------------------------
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="ACTION" value="Stop" onclick="return confirm('\''STOP AP Mode.\n\nAre you sure?'\'')" '$DISABLE_AP'>'
	echo '                </td>'
	echo '                <td colspan="2">'
	echo '                  <p>Stop AP Mode on pCP&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>This will Stop AP Mode on pCP.</p>'
	echo '                    <p>You may loose access to your device, unless it is already connected to hardwire connection.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
#----------------------------------Restart AP Mode---------------------------------------
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="ACTION" value="Restart" '$DISABLE_AP'>'
	echo '                </td>'
	echo '                <td colspan="2">'
	echo '                  <p>Restart AP Mode on pCP&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>This will restart AP Mode on pCP.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
}
[ $MODE -ge $MODE_BETA ] && pcp_ap_startstop
#----------------------------------------------------------------------------------------
echo '            </table>'
echo '          </fieldset>'
echo '        </div>'
echo '      </form>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <form name="AP mode configuration" action="'$0'">'
echo '        <div class="row">'
echo '          <fieldset>'
echo '            <legend>Wifi Access Point (AP) Configuration</legend>'
echo '            <table class="bggrey percent100">'
#----------------------------------Configure AP Mode-------------------------------------
pcp_ap_configure(){
	AP_SSID=$(cat $HOSTAPDCONF | grep -e "^ssid=" | cut -d "=" -f2)
	AP_PASS=$(cat $HOSTAPDCONF | grep -e "^\#wpa_passphrase=" | cut -d "=" -f2)
	AP_HWMODE=$(cat $HOSTAPDCONF | grep -e "^hw_mode=" | cut -d "=" -f2)
	AP_CHANNEL=$(cat $HOSTAPDCONF | grep -e "^channel=" | cut -d "=" -f2)
	AP_COUNTRY=$(cat $HOSTAPDCONF | grep -e "^country_code=" | cut -d "=" -f2)
	AP_80211AC=$(cat $HOSTAPDCONF | grep -e "^ieee80211ac=" | cut -d "=" -f2)
#----------------------------------AP Mode SSID------------------------------------------
	pcp_incr_id
	pcp_start_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p class="row">AP SSID</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="large15"'
	echo '                         type="text"'
	echo '                         name="AP_SSID"'
	echo '                         value="'$AP_SSID'"'
	echo '                         required'
	echo '                  >*'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>This is the SSID of the AP&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Set the SSID of your AP.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
#----------------------------------AP Mode password--------------------------------------
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p class="row">AP Password</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="large15"'
	echo '                         type="password"'
	echo '                         name="AP_PASS"'
	echo '                         value="'$AP_PASS'"'
	echo '                         required'
	echo '                         pattern=".{8,63}"'
	echo '                  >*'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>WPA2 Passphrase to be used to access AP&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Default password is piCorePlayer.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
#----------------------------------AP Mode country code----------------------------------
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p class="row">AP Country Code</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="large15"'
	echo '                         type="text"'
	echo '                         name="AP_COUNTRY"'
	echo '                         value="'$AP_COUNTRY'"'
	echo '                         required'
	echo '                         pattern="[A-Z]{2}"'
	echo '                         title="Use Capital Letters."'
	echo '                  >*'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>This is the two character Wireless Country Code of the AP&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Country Codes are two Letters. Reference <a href=https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2 target="_blank">Country Code List</a>.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
#----------------------------------AP Mode channel---------------------------------------
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p class="row">AP Channel</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                    <select name="AP_CHANNEL">'
	iwlist wlan0 channel | grep Channel | tr -s ' ' | awk -F' ' '{ print $2 }' > /tmp/chanlist
	cat /tmp/chanlist | sed "s/^$AP_CHANNEL/$AP_CHANNEL selected/" | awk -F' ' '{ print "<option value=\""$1"\" "$2">"$1"</option>" }'
	echo '                  </select>*'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>This is the Wireless Channel of the AP&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Channels reported available by wlan0.</p>'
	echo '                    <p>Not all channels are available for all country codes.</p>'
	echo '                    <p>38,42,46 are valid US channels, however they are not working on RPi3B+ in US.</p>'
	echo '                    <p>Check <a href="diagnostics.cgi#dmesg" target="_blank">dmesg</a> to validate if channel is getting set properly.</p>'
	echo '                    <ul>'
	iwlist wlan0 channel | grep Channel | tr -s ' ' | awk -F':' '{ print "                      <li>"$1":"$2"</li>" }'
	echo '                    </ul>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
#----------------------------------Enable/disable wireless ac----------------------------
	pcp_incr_id
	pcp_toggle_row_shade
	case $AP_80211AC in
		1)AP_80211ACyes="checked";;
		*)AP_80211ACno="checked";;
	esac
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p class="row">Wireless AC</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="small1" type="radio" name="AP_80211AC" value="1" '$AP_80211ACyes'>Yes&nbsp;&nbsp;'
	echo '                  <input class="small1" type="radio" name="AP_80211AC" value="0" '$AP_80211ACno'>No'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Enable Wireless AC function of the radio&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Yes - Wireless AC is enabled.</p>'
	echo '                    <p>No - Wireless AC is disabled, only G or N is used.</p>'
	echo '                    <p>RPi3B+ supports wireless AC.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
#----------------------------------AP Mode IP address------------------------------------
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p class="row">AP IP Address</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="large15"'
	echo '                         type="text"'
	echo '                         name="AP_IP"'
	echo '                         value="'$AP_IP'"'
	echo '                         required'
	echo '                         pattern="((^|\.)((25[0-5])|(2[0-4]\d)|(1\d\d)|([1-9]?\d))){4}$"'
	echo '                  >*'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>This is the IP address used for the AP&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Clients that connect to this AP will get a DHCP address in starting at .10 of the same IP range.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
#----------------------------------AP Mode Bridge Mode------------------------------------
	pcp_incr_id
	pcp_toggle_row_shade
	case $AP_BRIDGE in
		1)AP_BRIDGEyes="checked";;
		*)AP_BRIDGEno="checked";;
	esac
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p class="row">Bridge Mode</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="small1" type="radio" name="AP_BRIDGE" value="1" '$AP_BRIDGEyes'>Yes&nbsp;&nbsp;'
	echo '                  <input class="small1" type="radio" name="AP_BRIDGE" value="0" '$AP_BRIDGEno'>No'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Use Bridge mode, instead of Router mode.&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Yes - wlan0 is bridged to eth0.</p>'
	echo '                    <p>No - wlan0 is a NAT router.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
#----------------------------------Buttons-----------------------------------------------
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td colspan="3" class="column150 center">'
	echo '                  <button type="submit" name="ACTION" value="Setconfig">Set AP Config</button>'
	echo '                </td>'
	echo '              </tr>'
}
[ $MODE -ge $MODE_BETA ] && pcp_ap_configure
#----------------------------------------------------------------------------------------

echo '            </table>'
echo '          </fieldset>'
echo '        </div>'
echo '      </form>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------

pcp_footer
[ $MODE -ge $MODE_NORMAL ] && pcp_mode
pcp_copyright

echo '</body>'
echo '</html>'
