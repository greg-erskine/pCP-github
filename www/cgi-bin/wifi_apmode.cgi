#!/bin/sh

# Version: 7.0.0 2020-05-27

. pcp-functions
. pcp-rpi-functions
. pcp-lms-functions
. pcp-wifi-functions

APMODECONF="/usr/local/etc/pcp/apmode.conf"
HOSTAPDCONF="/usr/local/etc/pcp/hostapd.conf"
DNSMASQCONF="/usr/local/etc/pcp/dnsmasq.conf"

[ -f $APMODECONF ] && . $APMODECONF

pcp_html_head "WIFI AP Mode Settings" "PH"

pcp_controls
pcp_navbar
pcp_remove_query_string
pcp_httpd_query_string

[ -z $AP_BRIDGE ] && AP_BRIDGE=0

COLUMN2_1="col-2"
COLUMN2_2="col-10"

COLUMN3_1="col-sm-2"
COLUMN3_2="col-sm-3"
COLUMN3_3="col-sm-7"

#----------------------------------Routines----------------------------------------------
pcp_install_apmode() {
	pcp_message INFO "Downloading AP Mode..." "text"
	sudo -u tc pcp-load -r $PCP_REPO -w pcp-apmode.tcz
	if [ -f $TCEMNT/tce/optional/pcp-apmode.tcz ]; then
		pcp_message INFO "Installing AP Mode..." "text"
		sudo -u tc pcp-load -i firmware-atheros.tcz
		sudo -u tc pcp-load -i firmware-brcmwifi.tcz
		sudo -u tc pcp-load -i firmware-ralinkwifi.tcz
		sudo -u tc pcp-load -i firmware-rtlwifi.tcz
		sudo -u tc pcp-load -i firmware-rpi-wifi.tcz
		sudo -u tc pcp-load -i pcp-apmode.tcz
		pcp_wifi_update_wifi_onbootlst
		pcp_wifi_update_onbootlst "add" "pcp-apmode.tcz"
		[ $DEBUG -eq 1 ] && pcp_message DEBUG "pcp-apmode is added to onboot.lst" "text"
		[ $DEBUG -eq 1 ] && cat $ONBOOTLST
		pcp_message INFO "If wifi is not recognized, please reboot device..." "text"
	fi
}

pcp_remove_apmode() {
	sudo /usr/local/etc/init.d/pcp-apmode stop >/dev/null 2>&1
	sudo -u tc tce-audit builddb
	sudo -u tc tce-audit delete pcp-apmode.tcz
	sudo sed -i '/firmware-atheros.tcz/d' $ONBOOTLST
	sudo sed -i '/firmware-brcmwifi.tcz/d' $ONBOOTLST
	sudo sed -i '/firmware-rpi-wifi.tcz/d' $ONBOOTLST
	sudo sed -i '/firmware-ralinkwifi.tcz/d' $ONBOOTLST
	sudo sed -i '/firmware-rtlwifi.tcz/d' $ONBOOTLST
	sudo sed -i '/pcp-apmode.tcz/d' $ONBOOTLST
	pcp_message IINFO "Removing configuration files..." "text"
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
	pcp_message INFO "Setting Host AP SSID to $AP_SSID" "text"
	sudo sed -i "s/\(^ssid=\).*/\1$AP_SSID/" $HOSTAPDCONF
	pcp_message INFO "Setting AP Passphrase" "text"
	PSK_HEX=$(echo "$AP_PASS" | wpa_passphrase "$AP_SSID" | grep "psk=" | grep -v "#psk=" | cut -d "=" -f2)
	[ $DEBUG -eq 1 ] && echo 'PSK='$PSK_HEX
	sudo sed -i "s/\(^#wpa_passphrase=\).*/\1$AP_PASS/" $HOSTAPDCONF
	sudo sed -i "s/\(^wpa_psk=\).*/\1$PSK_HEX/" $HOSTAPDCONF
	pcp_message INFO "Setting AP Country Code to $AP_COUNTRY" "text"
	sudo sed -i "s/\(^country_code=\).*/\1$AP_COUNTRY/" $HOSTAPDCONF
	pcp_message INFO "Setting AP Channel to $AP_CHANNEL" "text"
	sudo sed -i "s/\(^channel=\).*/\1$AP_CHANNEL/" $HOSTAPDCONF
	[ $AP_CHANNEL -le 14 ] && AP_HWMODE="g" || AP_HWMODE="a"
	pcp_message INFO "Setting AP harware mode to $AP_HWMODE. (a=5GHz, g=2.4GHz)" "text"
	sudo sed -i "s/\(^hw_mode=\).*/\1$AP_HWMODE/" $HOSTAPDCONF
	pcp_message INFO "Setting AP 80211AC to $AP_80211AC" "text"
	sudo sed -i "s/\(^ieee80211ac=\).*/\1$AP_80211AC/" $HOSTAPDCONF
}

set_apmode_conf() {
	pcp_message INFO "Setting Bridge mode to $AP_BRIDGE" "text"
	echo "AP_BRIDGE=$AP_BRIDGE" > $APMODECONF
}

set_dnsmasq_conf() {
	RANGE=$(echo $AP_IP | awk -F. '{print $1"."$2"."$3".10,"$1"."$2"."$3".100,12h"}')
	sudo sed -i "s/\(^dhcp-range=\).*/\1$RANGE/" $DNSMASQCONF
}

REBOOT_REQUIRED=0
case "$ACTION" in
	Autostart)
		pcp_infobox_begin
		if [ "$APMODE" = "yes" ]; then
			pcp_message INFO "Enabling pCP AP Mode at boot..." "text"
		else
			pcp_message INFO "Disabling pCP AP Mode at boot..." "text"
		fi
		pcp_save_to_config
		pcp_backup "text"
		pcp_infobox_end
	;;
	Start)
		pcp_infobox_begin
		if [ ! -x /usr/local/etc/init.d/pcp-apmode ]; then
			pcp_message INFO "Loading pCP AP Mode extensions..." "text"
			sudo -u tc tce-load -i pcp-apmode.tcz
		fi
		pcp_message INFO "Starting AP Mode..." "text"
		echo -n '[ INFO ] '
		sudo /usr/local/etc/init.d/pcp-apmode start
		sleep 2
		pcp_infobox_begin
	;;
	Stop)
		pcp_infobox_begin
		pcp_message INFO "Stopping AP Mode..." "text"
		echo -n '[ INFO ] '
		sudo /usr/local/etc/init.d/pcp-apmode stop
		sleep 2
		pcp_infobox_end
	;;
	Install)
		pcp_infobox_begin
		pcp_sufficient_free_space 4500
		if [ $? -eq 0 ] ; then
			pcp_install_apmode
			if [ -f $TCEMNT/tce/optional/pcp-apmode.tcz ]; then
				APMODE="yes"
				AP_IP="10.10.10.1"
				pcp_save_to_config
				pcp_backup "text"
			else
				pcp_message ERROR "Error Downloading AP Mode, please try again later." "text"
			fi
		fi
		pcp_infobox_end
	;;
	Remove)
		pcp_infobox_begin
		pcp_message INFO "Removing AP Mode Extensions..." "text"
		echo
		echo 'After a reboot these extensions will be permanently deleted:'
		APMODE="no"
		pcp_save_to_config
		pcp_remove_apmode
		pcp_backup "text"
		REBOOT_REQUIRED=1
		pcp_infobox_end
	;;
	Restart)
		pcp_infobox_begin
		pcp_message INFO "Restarting AP Mode..." "text"
		echo -n '[ INFO ] '
		sudo /usr/local/etc/init.d/pcp-apmode stop
		sleep 5
		echo -n '[ INFO ] '
		sudo /usr/local/etc/init.d/pcp-apmode start
		sleep 2
		pcp_infobox_end
	;;
	Setconfig)
		pcp_infobox_begin
		pcp_message INFO "Setting AP Mode Configuration..." "text"
		set_apmode_conf
		set_hostapd_conf
		if [ $(echo $AP_IP | awk -F. '{print $4}') -ne 1 ]; then
			echo '[ WARN ] Router IP address must end in .1'
			AP_IP=$(echo $AP_IP | sed 's/[^.]*$/1/')
		fi
		pcp_message INFO "Setting IP to $AP_IP" "text"
		pcp_save_to_config
		set_dnsmasq_conf
		echo -n '[ INFO ] Restarting AP.....'
		sudo /usr/local/etc/init.d/pcp-apmode restart
		[ $? -eq 0 ] && echo 'Done' || echo 'Error'
		pcp_backup "text"
		pcp_infobox_end
	;;
	Update)
		pcp_infobox_begin
		pcp_sufficient_free_space 4700
		pcp_message INFO "Updating AP Mode Extensions..." "text"
		sudo -u tc pcp-update pcp-apmode.tcz
		case $? in
			0) pcp_message INFO "Reboot Required to finish update" "text"; REBOOT_REQUIRED=1;;
			2) pcp_message INFO "No Update Available" "text";;
			*) pcp_message ERROR "Try again later" "text";;
		esac
		pcp_infobox_end
	;;
	*)
	;;
esac
[ $REBOOT_REQUIRED -eq 1 ] && pcp_reboot_required

#----------------------------------AP Mode Indication------------------------------------
if [ $(pcp_apmode_status) -eq 0 ]; then
	pcp_green_tick "running"
else
	pcp_red_cross "not running"
fi

case "$APMODE" in
	yes) APMODEyes="checked" ;;
	no) APMODEno="checked" ;;
esac
[ -f $TCEMNT/tce/optional/pcp-apmode.tcz ] && DISABLE_AP="" || DISABLE_AP="disabled"

pcp_border_begin
echo '    <div class="row mx-1 mt-3">'
echo '      <div class="col-1 text-md-right">'$INDICATOR'</div>'
pcp_incr_id
echo '      <div class="col-sm-11 col-11">'
echo '        <p>AP Mode is '$STATUS'&nbsp;&nbsp;'
pcp_helpbadge
echo '        </p>'
echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
echo '          <ul>'
echo '            <li>'$(pcp_bi_check)' = AP Mode running.</li>'
echo '            <li>'$(pcp_bi_x)' = AP Mode not running.</li>'
echo '          </ul>'
echo '        </div>'
echo '      </div>'
echo '    </div>'
pcp_border_end
#----------------------------------------------------------------------------------------

pcp_border_begin
pcp_heading5 "Wifi Access Point (AP)"
echo '  <form name="AP mode" action="'$0'">'
#----------------------------------Enable/disable autostart of AP Mode-------------------
pcp_ap_enable() {
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <button class="'$BUTTON'" type="submit" name="ACTION" value="Autostart" '$DISABLE_AP'>Set Autostart</button>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <input id="rad1" type="radio" name="APMODE" value="yes" '$APMODEyes'>'
	echo '        <label for="rad1">Yes&nbsp;&nbsp;</label>'
	echo '        <input id="rad2" type="radio" name="APMODE" value="no" '$APMODEno'>'
	echo '        <label for="rad2">No</label>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <p>Automatic start of AP Mode when pCP boots&nbsp;&nbsp;'
	pcp_helpbadge
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>Yes - will enable automatic start of AP Mode when pCP boots.</p>'
	echo '          <p>No - will disable automatic start of AP Mode when pCP boots.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_SERVER ] && pcp_ap_enable
#----------------------------------------------------------------------------------------

#----------------------------------Install/uninstall AP Mode-----------------------------
pcp_ap_install() {
	pcp_incr_id
	
	if [ ! -f $TCEMNT/tce/optional/pcp-apmode.tcz ]; then
		echo '    <div class="row mx-1">'
		echo '      <div class="'$COLUMN2_1'">'
		echo '        <input class="'$BUTTON'" type="submit" name="ACTION" value="Install">'
		echo '      </div>'
		echo '      <div class="'$COLUMN2_2'">'
		echo '        <p>Install AP Mode on pCP&nbsp;&nbsp;'
		pcp_helpbadge
		echo '          </p>'
		echo '          <div id="dt'$ID'" class="'$COLLAPSE'">'
		echo '            <p>This will install AP Mode on pCP.</p>'
		echo '          </div>'
		echo '        </div>'
		echo '      </div>'
	else
		echo '      <div class="row mx-1">'
		echo '        <div class="'$COLUMN3_1'">'
		echo '          <input class="'$BUTTON'" type="submit" name="ACTION" value="Update">'
		echo '        </div>'
		echo '        <div class="'$COLUMN3_2'">'
		echo '          <input class="'$BUTTON'" type="submit" name="ACTION" value="Remove" onclick="return confirm('\''This will remove AP Mode from pCP.\n\nAre you sure?'\'')">'
		echo '        </div>'
		echo '        <div class="'$COLUMN3_3'">'
		echo '          <p>Update or Remove AP Mode from pCP&nbsp;&nbsp;'
		pcp_helpbadge
		echo '        </p>'
		echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
		echo '          <p>This will remove AP Mode and all the extra packages that were added with Hostapd.</p>'
		echo '        </div>'
		echo '      </div>'
		echo '    </div>'
	fi
}
[ $MODE -ge $MODE_SERVER ] && pcp_ap_install
#----------------------------------------------------------------------------------------

#----------------------------------Start AP Mode-----------------------------------------
pcp_ap_startstop() {
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN2_1'">'
	echo '        <input class="'$BUTTON'" type="submit" name="ACTION" value="Start" '$DISABLE_AP'>'
	echo '      </div>'
	echo '      <div class="'$COLUMN2_2'">'
	echo '        <p>Start AP Mode on pCP&nbsp;&nbsp;'
	pcp_helpbadge
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>This will start AP Mode on pCP.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
#----------------------------------Stop AP Mode------------------------------------------
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN2_1'">'
	echo '        <input class="'$BUTTON'" type="submit" name="ACTION" value="Stop" onclick="return confirm('\''STOP AP Mode.\n\nAre you sure?'\'')" '$DISABLE_AP'>'
	echo '      </div>'
	echo '      <div class="'$COLUMN2_2'">'
	echo '        <p>Stop AP Mode on pCP&nbsp;&nbsp;'
	pcp_helpbadge
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>This will Stop AP Mode on pCP.</p>'
	echo '          <p>You may loose access to your device, unless it is already connected to hardwire connection.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
#----------------------------------Restart AP Mode---------------------------------------
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN2_1'">'
	echo '        <input class="'$BUTTON'" type="submit" name="ACTION" value="Restart" '$DISABLE_AP'>'
	echo '      </div>'
	echo '      <div class="'$COLUMN2_2'">'
	echo '        <p>Restart AP Mode on pCP&nbsp;&nbsp;'
	pcp_helpbadge
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>This will restart AP Mode on pCP.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_SERVER ] && pcp_ap_startstop
#----------------------------------------------------------------------------------------
echo '  </form>'
pcp_border_end

#----------------------------------------------------------------------------------------
pcp_border_begin
pcp_heading5 "Wifi Access Point (AP) Configuration"
echo '  <form name="AP mode configuration" action="'$0'">'
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
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <p>AP SSID*</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <input class="form-control form-control-sm"'
	echo '               type="text"'
	echo '               name="AP_SSID"'
	echo '               value="'$AP_SSID'"'
	echo '               required'
	echo '        >'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <p>This is the SSID of the AP&nbsp;&nbsp;'
	pcp_helpbadge
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>Set the SSID of your AP.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
#----------------------------------AP Mode password--------------------------------------
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <p>AP Password*</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <input class="form-control form-control-sm"'
	echo '               type="password"'
	echo '               name="AP_PASS"'
	echo '               value="'$AP_PASS'"'
	echo '               required'
	echo '               pattern=".{8,63}"'
	echo '        >'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <p>WPA2 Passphrase to be used to access AP&nbsp;&nbsp;'
	pcp_helpbadge
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>Default password is piCorePlayer.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
#----------------------------------AP Mode country code----------------------------------
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <p>AP Country Code*</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <input class="form-control form-control-sm"'
	echo '               type="text"'
	echo '               name="AP_COUNTRY"'
	echo '               value="'$AP_COUNTRY'"'
	echo '               required'
	echo '               pattern="[A-Z]{2}"'
	echo '               title="Use Capital Letters."'
	echo '        >'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <p>This is the two character Wireless Country Code of the AP&nbsp;&nbsp;'
	pcp_helpbadge
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>Country Codes are two Letters. Reference <a href=https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2 target="_blank">Country Code List</a>.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
#----------------------------------AP Mode channel---------------------------------------
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <p>AP Channel*</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '          <select class="custom-select custom-select-sm" name="AP_CHANNEL">'
	iwlist wlan0 channel | grep Channel | tr -s ' ' | awk -F' ' '{ print $2 }' > /tmp/chanlist
	cat /tmp/chanlist | sed "s/^$AP_CHANNEL/$AP_CHANNEL selected/" | awk -F' ' '{ print "<option value=\""$1"\" "$2">"$1"</option>" }'
	echo '        </select>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <p>This is the Wireless Channel of the AP&nbsp;&nbsp;'
	pcp_helpbadge
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>Channels reported available by wlan0.</p>'
	echo '          <p>Not all channels are available for all country codes.</p>'
	echo '          <p>38,42,46 are valid US channels, however they are not working on RPi3B+ in US.</p>'
	echo '          <p>Check <a href="diagnostics.cgi#dmesg" target="_blank">dmesg</a> to validate if channel is getting set properly.</p>'
	echo '          <ul>'
	iwlist wlan0 channel | grep Channel | tr -s ' ' | awk -F':' '{ print "                      <li>"$1":"$2"</li>" }'
	echo '          </ul>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
#----------------------------------Enable/disable wireless ac----------------------------
	pcp_incr_id
	case $AP_80211AC in
		1)AP_80211ACyes="checked";;
		*)AP_80211ACno="checked";;
	esac
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <p>Wireless AC</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <input id="rad3" type="radio" name="AP_80211AC" value="1" '$AP_80211ACyes'>'
	echo '        <label for="rad3">Yes&nbsp;&nbsp;</label>'
	echo '        <input id="rad4" type="radio" name="AP_80211AC" value="0" '$AP_80211ACno'>'
	echo '        <label for="rad4">No</label>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <p>Enable Wireless AC function of the radio&nbsp;&nbsp;'
	pcp_helpbadge
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>Yes - Wireless AC is enabled.</p>'
	echo '          <p>No - Wireless AC is disabled, only G or N is used.</p>'
	echo '          <p>RPi3B+ supports wireless AC.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
#----------------------------------AP Mode IP address------------------------------------
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <p>AP IP Address*</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <input class="form-control form-control-sm"'
	echo '               type="text"'
	echo '               name="AP_IP"'
	echo '               value="'$AP_IP'"'
	echo '               required'
	echo '               pattern="((^|\.)((25[0-5])|(2[0-4]\d)|(1\d\d)|([1-9]?\d))){4}$"'
	echo '        >'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <p>This is the IP address used for the AP&nbsp;&nbsp;'
	pcp_helpbadge
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>Clients that connect to this AP will get a DHCP address in starting at .10 of the same IP range.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
#----------------------------------AP Mode Bridge Mode------------------------------------
	pcp_incr_id
	case $AP_BRIDGE in
		1)AP_BRIDGEyes="checked";;
		*)AP_BRIDGEno="checked";;
	esac
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <p>Bridge Mode</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <input id="br1" type="radio" name="AP_BRIDGE" value="1" '$AP_BRIDGEyes'>'
	echo '        <label for="br1">Yes&nbsp;&nbsp;</label>'
	echo '        <input id="br2" type="radio" name="AP_BRIDGE" value="0" '$AP_BRIDGEno'>'
	echo '        <label for="br2">No</label>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <p>Use Bridge mode, instead of Router mode&nbsp;&nbsp;'
	pcp_helpbadge
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>Yes - wlan0 is bridged to eth0.</p>'
	echo '          <p>No - wlan0 is a NAT router.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
#----------------------------------Buttons-----------------------------------------------
	echo '    <div class="row mx-1 mb-2">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <button class="'$BUTTON'" type="submit" name="ACTION" value="Setconfig">Set AP Config</button>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_SERVER ] && pcp_ap_configure
#----------------------------------------------------------------------------------------
echo '  </form>'
pcp_border_end
#----------------------------------------------------------------------------------------

pcp_html_end
exit
