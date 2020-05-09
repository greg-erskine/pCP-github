#!/bin/sh

# Version: 7.0.0 2020-05-09

. pcp-functions
. pcp-rpi-functions
. pcp-lms-functions
. pcp-wifi-functions

unset REBOOT_REQUIRED
unset MODIFY_OK
unset ERROR_FLG

pcp_html_head "Wifi WPA Settings" "GE"

pcp_controls
pcp_navbar
pcp_httpd_query_string_no_decode
[ $DEBUG -eq 0 ] && pcp_remove_query_string

[ -n "$WPA_PASSWORD" ] && ENCODED_WPA_PASSWORD="${WPA_PASSWORD}"
[ -n "$WPA_SSID" ] && ENCODED_WPA_SSID="${WPA_SSID}"
WPA_PASSWORD=""
WPA_SSID=""

COLUMN3_1="col-sm-2"
COLUMN3_2="col-sm-3"
COLUMN3_3="col-sm-7"

COLUMN2_1="$COLUMN3_1"
COLUMN2_2="col-9"

BUTTON="btn btn-primary"

# Special characters will break pcp_httpd_query_string, so if any variable could contain url encoded data
# it would need to be manually decoded like this
# [ -n "$ACTION" ] && ACTION=$($URL_DECODE $ACTION)
# in this case, no other variables can contain encoded data.

[ x"" = x"$ACTION" ] && ACTION=Initial
WPACONFIGFILE=$WPASUPPLICANTCONF

#========================================================================================
# WARNING messages
#----------------------------------------------------------------------------------------
[ $(pcp_kernel) = "pcpAudioCore" ] && ERRMSG1="Wifi may not work on the pcpAudioCore kernel." && ERROR_FLG=TRUE

if [ $(pcp_exists_wpa_supplicant) -eq 0 ]; then
	[ $(pcp_wifi_maintained_by_user) -eq 0 ] && ERRMSG3="Wifi configuration manually maintained by user not piCorePlayer." && ERROR_FLG=TRUE
	[ $(pcp_wifi_update_config) -ne 0 ] && ERRMSG4="Wifi configuration can not be maintained by piCorePlayer or wpa_cli." && ERROR_FLG=TRUE
else
	ERRMSG2="$WPASUPPLICANTCONF not found."
	ERROR_FLG=TRUE
fi

if [ "$WIFI" = "on" ]; then
	if [ $(pcp_exists_wpa_supplicant) -eq 0 ]; then
		if [ $(pcp_wifi_update_config) -eq 0 ] && [ $(pcp_wifi_maintained_by_pcp) -eq 0 ]; then
			MODIFY_OK=TRUE
		fi
	else
		MODIFY_OK=TRUE
	fi
	[ $MODIFY_OK ] || (ERRMSG5="Configuration can not be maintained by piCorePlayer."; ERROR_FLG=TRUE)
fi

pcp_wifi_error_messages() {
	if [ "$WIFI" = "on" ] && [ $ERROR_FLG ]; then

		echo '      <div>'
		echo '        <p><b>WARNINGS:</b>'
		echo '          <ul>'
		for i in 1 2 3 4 5; do
			[ x"" != x"$(eval echo \$ERRMSG${i})" ] && echo '            <li>'$(eval echo \$ERRMSG${i})'</li>'
		done
		echo '          </ul>'
		echo '        </p>'
		echo '    </div>'

	fi
}

#========================================================================================
# Main.
#----------------------------------------------------------------------------------------
case "$ACTION" in
	Initial)
		pcp_wifi_error_messages
		if [ "$WIFI" = "on" ]; then
			pcp_heading5 "Initial option"
			pcp_wifi_read_wpa_supplicant "text"
		fi
	;;
	Config)
		pcp_wifi_error_messages
		pcp_heading5 "Config option"
		pcp_save_to_config
		pcp_wifi_read_wpa_supplicant "text"
		pcp_backup "text"
		if [ "$WIFI" = "on" ]; then
			pcp_wifi_load_wifi_firmware_extns "text"
			pcp_wifi_load_wifi_extns "text"
		fi
	;;
	Save)
		pcp_wifi_error_messages
		pcp_heading5 "Save option"
		if [ "$WIFI" = "on" ]; then
			pcp_wifi_load_wifi_firmware_extns "text"
			pcp_wifi_load_wifi_extns "text"
			pcp_wifi_generate_passphrase "text"
			pcp_wifi_write_wpa_supplicant "text"
			pcp_wifi_read_wpa_supplicant "text"
			/usr/local/etc/init.d/wifi wlan0 stop
			/usr/local/etc/init.d/wifi wlan0 start
		else
			/usr/local/etc/init.d/wifi wlan0 stop
			pcp_wifi_unload_wifi_extns "text"
			pcp_wifi_unload_wifi_firmware_extns "text"
		fi
		pcp_save_to_config
		pcp_backup "text"

	;;
	Network_wait)
		pcp_wifi_error_messages
		pcp_heading5 "Network wait"
		pcp_wifi_read_wpa_supplicant "text"
		pcp_save_to_config
		pcp_backup "text"
		
	;;
	#----------------------------------DEBUG - Developer options-----------------------------
	Read)
		pcp_wifi_error_messages
		pcp_heading5 "Read option"
		pcp_wifi_read_wpa_supplicant "text"
		
	;;
	Delete)
		pcp_heading5 "Delete option"
		rm -f $WPASUPPLICANTCONF
		[ $? -eq 0 ] && pcp_message OK "$WPASUPPLICANTCONF deleted." "text"
		unset WPA_SSID WPA_PASSWORD WPA_PW WPA_PSK WPA_PASSPHRASE WPA_KEY_MGMT WPA_ENCRYPTION WPA_HIDDENSSID
		pcp_backup "text"
		
	;;
	Remove)
		pcp_heading5 "Remove option"
		pcp_wifi_unload_wifi_extns "text"
		pcp_wifi_unload_wifi_firmware_extns "text"
		pcp_backup "text"
		
	;;
	Start)
		pcp_heading5 "Start option"
		/usr/local/etc/init.d/wifi wlan0 start
		
	;;
	Stop)
		pcp_heading5 "Stop option"
		/usr/local/etc/init.d/wifi wlan0 stop
		
	;;
	Status)
		pcp_heading5 "Status option" "" "30"
		/usr/local/etc/init.d/wifi wlan0 status
		
	;;
	Convert1)
		pcp_heading5 "Convert option" "" "100"
		WPACONFIGFILE="/tmp/newconfig.cfg"
		if [ -f $WPACONFIGFILE ]; then
			pcp_wifi_read_newconfig "text"
			pcp_wifi_write_wpa_supplicant "text"
		fi
		
	;;
	Convert2)
		pcp_heading5 "Convert option" "" "100"
		WPACONFIGFILE="/tmp/wpa_supplicant.conf"
		if [ -f $WPACONFIGFILE ]; then
			pcp_wifi_read_wpa_supplicant "text"
			pcp_wifi_write_wpa_supplicant "text"
		fi
		
	;;
	*)
		[ $DEBUG -eq 1 ] && echo "Case: Invalid"
		if [ "$WIFI" = "on" ]; then
			pcp_wifi_read_wpa_supplicant
		fi
	;;
esac

#========================================================================================
# Debug information.
#----------------------------------------------------------------------------------------
if [ $DEBUG -eq 1 ]; then

	pcp_debug_variables "html" ACTION WIFI WPA_SSID WPA_PSK WPA_PW WPA_PASSWORD WPA_PASSPHRASE WPA_ENCRYPTION WPA_HIDDENSSID RPI3INTWIFI RPIBLUETOOTH

fi

#========================================================================================
# Main.
#----------------------------------------------------------------------------------------
echo '<script>'
echo 'var wifi_current_state="'$WIFI'";'
echo 'function validate() {'
echo '    if ( wifi_current_state == "on" && document.setwifi.WIFI[0].checked == true ){' 
echo '      if ( document.setwifi.WPA_PASSWORD.value == "" || document.setwifi.WPA_PASSWORD.value == "********" || document.setwifi.WPA_SSID.value == "" || document.setwifi.WPA_COUNTRY.value == "" ){'
echo '        alert("SSID, Password and Country Code\nMUST be entered!");'
echo '        return false;'
echo '      }'
echo '    }'
echo '  return true;'
echo '}'
echo '</script>'

pcp_heading5 "Set wifi configuration"

echo '  <form id="setwifi" name="setwifi" action="'$0'" method="get">'

#----------------------------------------------------------------------------------------
if [ "$WIFI" = "on" ]; then
	WIFIon="checked"
	COLUMN1="$COLUMN3_1"
	[ $(pcp_wifi_maintained_by_user) -eq 0 ] && COLUMN2="$COLUMN3_1" || COLUMN2="$COLUMN3_1"
else
	WIFIoff="checked"
	COLUMN1="$COLUMN3_1"
	COLUMN2="$COLUMN3_2"
fi
#--------------------------------------Wifi on/off---------------------------------------
pcp_incr_id

echo '    <div class="row">'
echo '      <div class="'$COLUMN3_1'">'
echo '        <p>Wifi</p>'
echo '      </div>'
echo '      <div class="'$COLUMN3_2'">'
echo '        <input id="wifi1" type="radio" name="WIFI" value="on" '$WIFIon'>'
echo '        <label for="wifi1">On&nbsp;&nbsp;&nbsp;</label>'
echo '        <input id="wifi2" type="radio" name="WIFI" value="off" '$WIFIoff'>'
echo '        <label for="wifi2">Off</label>'
echo '      </div>'
echo '      <div class="'$COLUMN3_3'">'
echo '        <p>Set wifi on or off&nbsp;&nbsp;'
echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
echo '        </p>'
echo '        <div id="dt'$ID'" class="collapse">'
echo '          <p>&lt;On|Off&gt;</p>'
echo '          <ul>'
echo '            <li>Turning wifi on will enable the remaining fields.</li>'
echo '            <li>Turn wifi on if you have Raspberry Pi with built-in wifi.</li>'
echo '            <li>Turn wifi on if you have compatible USB wifi adapter installed.</li>'
echo '            <li>Set wifi to off if you are not using wifi.</li>'
echo '          </ul>'
echo '        </div>'
echo '      </div>'
echo '    </div>'

#----------------------------------------------------------------------------------------
if [ "$WIFI" = "on" ] && [ $(pcp_wifi_maintained_by_user) -ne 0 ]; then
#--------------------------------------SSID----------------------------------------------
	pcp_incr_id

	echo '    <div class="row">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <p>SSID</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <input class="form-control"'
	echo '               id="ssid"'
	echo '               type="text"'
	echo '               name="WPA_SSID"'
	echo '               value="'$WPA_SSID'"'
	echo '               maxlength="32"'
	echo '        >'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <p>Enter wifi network SSID&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="collapse">'
	echo '          <ul>'
	echo '            <li>Service Set Identifier (SSID).</li>'
	echo '            <li>Use valid alphanumeric characters only.</li>'
	echo '            <li>Maximum length of 32 characters.</li>'
	echo '          </ul>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'

	echo '    <script type="text/javascript">'
	echo '      var enc = "'$ENCODED_WPA_SSID'";'
	echo '      document.getElementById("ssid").value = decodeURIComponent(enc.replace(/\+/g, "%20"));'
	echo '    </script>'
#--------------------------------------Password------------------------------------------
	pcp_incr_id

	echo '    <div class="row">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <p>PSK Password</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <input class="form-control"'
	echo '               type="text"'
	echo '               name="WPA_PASSWORD"'
#	echo '               value="'$WPA_PASSWORD'"'
	echo '               value="********"'
	echo '               maxlength="64"'
	echo '        >'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <p>Enter wifi network password&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="collapse">'
	echo '          <ul>'
#	echo '            <li>Use valid alphanumeric characters only.</li>'
	echo '            <li>Maximum length of 64 characters.</li>'
	echo '            <li>Press [Save] to convert password to secure passphrase.</li>'
	echo '            <li>Password is not stored anywhere.</li>'
	echo '          </ul>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
#--------------------------------------Passphrase----------------------------------------
	pcp_incr_id
	
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <p>PSK Passphrase</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <input class="form-control"'
	echo '               type="text"'
	echo '               value="'$WPA_PASSPHRASE'"'
	echo '               maxlength="64"'
	echo '               disabled'
	echo '        >'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <p>Readonly wifi network passphrase&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="collapse">'
	echo '          <ul>'
	echo '            <li>Usually auto-generated from SSID and wifi password.</li>'
	echo '            <li>Maximum length of 64 characters.</li>'
	echo '          </ul>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
#----------------------------------------Country Code------------------------------------
	pcp_incr_id
	
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <p>Country Code</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <input class="form-control"'
	echo '               type="text"'
	echo '               name="WPA_COUNTRY"'
	echo '               value="'$WPA_COUNTRY'"'
	echo '               pattern="[A-Z]{2}"'
	echo '               title="Use Capital Letters."'
	echo '        >'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <p>Two character Wireless Country Code&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="collapse">'
	echo '          <p>Country Codes are two Letters.</p>'
	echo '          <p>Reference <a href=https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2 target="_blank">Country Code List</a>.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
#--------------------------------------Security Mode-------------------------------------
	case "$WPA_ENCRYPTION" in
		WPA-PSK) WPA_ENCRYPTIONwpa="checked" ;;
		WEP) WPA_ENCRYPTIONwep="checked" ;;
		OPEN) WPA_ENCRYPTIONopen="checked" ;;
		*) WPA_ENCRYPTIONwpa="checked" ;;
	esac
	pcp_incr_id
	
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <p>Security Mode</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <input id="1wifi1" type="radio" name="WPA_ENCRYPTION" value="WPA-PSK" '$WPA_ENCRYPTIONwpa'>'
	echo '        <label for="1wifi1">WPA-PSK&nbsp;&nbsp;</label>'
	echo '        <input id="1wifi2" type="radio" name="WPA_ENCRYPTION" value="WEP" '$WPA_ENCRYPTIONwep'>'
	echo '        <label for="1wifi2">WEP</label>'
	echo '        <input id="1wifi3" type="radio" name="WPA_ENCRYPTION" value="WEP" '$WPA_ENCRYPTIONopen'>'
	echo '        <label for="1wifi3">OPEN</label>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <p>Set wifi network security level&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="collapse">'
	echo '          <p>&lt;WPA-PSK|WEP|Open&gt;</p>'
	echo '          <p>Recommended: WPA-PSK</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
#--------------------------------------Hidden SSID---------------------------------------
	case "$WPA_HIDDENSSID" in
		0) WPA_HIDDENSSIDno="checked" ;;
		1) WPA_HIDDENSSIDyes="checked" ;;
		*) WPA_HIDDENSSIDno="checked" ;;
	esac

	pcp_incr_id

	echo '    <div class="row">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <p>Hidden SSID</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <input id="2wifi1" type="radio" name="WPA_HIDDENSSID" value="1" '$WPA_HIDDENSSIDyes'>'
	echo '        <label for="2wifi1">Yes&nbsp;&nbsp;</label>'
	echo '        <input id="2wifi2" type="radio" name="WPA_HIDDENSSID" value="0" '$WPA_HIDDENSSIDno'>'
	echo '        <label for="2wifi2">No</label>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <p>Set hiddden SSID&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="collapse">'
	echo '          <p>Select yes to use a hidden SSID.</p>'
	echo '          <p><b>Note: </b>We do not recommend the use of a hidden SSID. '
	echo '          This option is only for the convenience of users that have already setup a hidden SSID.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
fi
#--------------------------------------Buttons------------------------------------------

echo '    <div class="row">'
echo '      <div class="'$COLUMN2_1'">'

if [ "$WIFI" = "on" ]; then
	echo '        <input class="'$BUTTON'" type="submit" name="ACTION" value="Save" onclick="return(validate());">'
	echo '        <input class="'$BUTTON'"type="button" name="DIAGNOSTICS" onClick="location.href='\'''diag_wifi.cgi''\''" value="Diagnostics">'
	echo '        <input type="hidden" name="WPA_PASSPHRASE" value="'$WPA_PASSPHRASE'">'
else
	echo '        <button class="'$BUTTON'" type="submit" name="ACTION" value="Config">Save</button>'
fi

echo '      </div>'
echo '    </div>'

#--------------------------------------DEBUG---------------------------------------------
if [ $MODE -ge $MODE_DEVELOPER ]; then
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <input type="submit" name="ACTION" value="Read">'
	echo '        <input type="submit" name="ACTION" value="Delete">'
	echo '        <input type="submit" name="ACTION" value="Remove">'
	echo '        <input type="submit" name="ACTION" value="Start">'
	echo '        <input type="submit" name="ACTION" value="Stop">'
	echo '        <input type="submit" name="ACTION" value="Status">'
	echo '      </div>'
	echo '    </div>'
fi
#----------------------------------------------------------------------------------------
echo '  </form>'

#----------------------------------------------------------------------------------------

if [ $(pcp_rpi_has_inbuilt_wifi) -eq 0 ] || [ $TEST -eq 1 ]; then

	pcp_heading5 "RPi Built in WiFi/BT"

	echo '  <form id="rpiwifi" name="builtinwifi" action="writetowifi.cgi" method="get">'
#--------------------------------------Built-in Wifi-------------------------------------
	case "$RPI3INTWIFI" in
		on) RPIWIFIyes="checked" ;;
		off) RPIWIFIno="checked" ;;
	esac

	pcp_incr_id

	echo '    <div class="row">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <p>RPi built-in Wifi</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <input id="intwifi1" type="radio" name="RPI3INTWIFI" value="on" '$RPIWIFIyes'>'
	echo '        <label for="intwifi1">On&nbsp;&nbsp;&nbsp;</label>'
	echo '        <input id="intwifi2" type="radio" name="RPI3INTWIFI" value="off" '$RPIWIFIno'>'
	echo '        <label for="intwifi2">Off</label>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <p>Turn off Raspberry Pi built-in wifi&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="collapse">'
	echo '          <p>This will load an overlay that disables built-in wifi.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
#--------------------------------------Built-in Bluetooth--------------------------------
	case "$RPIBLUETOOTH" in
		on) RPIBLUETOOTHyes="checked" ;;
		off) RPIBLUETOOTHno="checked" ;;
	esac

	pcp_incr_id

	echo '    <div class="row">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <p>RPi built-in Bluetooth</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <input id="blue1" type="radio" name="RPIBLUETOOTH" value="on" '$RPIBLUETOOTHyes'>'
	echo '        <label for="blue1">On&nbsp;&nbsp;&nbsp;</label>'
	echo '        <input id="blue2" type="radio" name="RPIBLUETOOTH" value="off" '$RPIBLUETOOTHno'>'
	echo '        <label for="blue2">Off</label>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <p>Turn off Raspberry Pi built-in bluetooth&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="collapse">'
	echo '          <p>This will load an overlay that disables built-in bluetooth.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
#--------------------------------------Buttons------------------------------------------
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <input class="'$BUTTON'" type="submit" name="ACTION" value="Save">'
	echo '        <input type="hidden" name="FROM_PAGE" value="wifi.cgi">'
	echo '      </div>'
	echo '    </div>'
#----------------------------------------------------------------------------------------
	echo '  </form>'
fi
#----------------------------------------------------------------------------------------

if [ $DEBUG -eq 1 ]; then
#--------------------------------------DEBUG---------------------------------------------
	pcp_table_top "[ DEBUG ] $WPASUPPLICANTCONF tests"
	[ $(pcp_exists_wpa_supplicant) -eq 0 ] &&
	echo '<p>[ INFO ] '$WPASUPPLICANTCONF' exists</p>' || echo '<p>[ ERROR ] '$WPASUPPLICANTCONF' does not exists.</p>'
	[ $(pcp_wifi_maintained_by_pcp) -eq 0 ] &&
	echo '<p>[ INFO ] '$WPASUPPLICANTCONF' "Maintained by piCorePlayer"</p>' || echo '<p>[ ERROR ] '$WPASUPPLICANTCONF' not "Maintained by piCorePlayer".</p>'
	pcp_table_end
#--------------------------------------DEBUG---------------------------------------------
	WPACONFIGFILE="/tmp/newconfig.cfg"
	pcp_heading5 "[ DEBUG ] $WPACONFIGFILE"
	pcp_textarea "none" "cat ${WPACONFIGFILE}" 80
	if [ -f $WPACONFIGFILE ]; then
		pcp_toggle_row_shade
		echo '    <div class="row">'
		echo '      <div class="'$COLUMN3_1'">'
		echo '        <form name="wpatest1" action="'$0'" method="get">'
		echo '          <input class="'$BUTTON'" type="submit" name="ACTION" value="Convert1">'
		echo '        </form>'
		echo '      </div>'
		echo '    </div>'
	else
		pcp_message ERROR "$WPACONFIGFILE not found." "html"
	fi

#--------------------------------------DEBUG---------------------------------------------
	WPACONFIGFILE="/tmp/wpa_supplicant.conf"
	pcp_heading5 "[ DEBUG ] $WPACONFIGFILE"
	pcp_textarea "none" "cat ${WPACONFIGFILE}" 12
	if [ -f $WPACONFIGFILE ]; then
		echo '    <div class="row">'
		echo '      <div class="'$COLUMN3_1'">'
		echo '        <form name="wpatest2" action="'$0'" method="get">'
		echo '          <input class="'$BUTTON'" type="submit" name="ACTION" value="Convert2">'
		echo '        </form>'
		echo '      </div>'
		echo '    </div>'
	else
		pcp_message ERROR "$WPACONFIGFILE not found." "html"
	fi

#--------------------------------------DEBUG---------------------------------------------
	
	pcp_textarea "[ DEBUG ] $WPASUPPLICANTCONF" "cat ${WPASUPPLICANTCONF}" 150
	
#--------------------------------------DEBUG---------------------------------------------
	pcp_table_top "[ DEBUG ] Installed extensions"
	pcp_wifi_all_extensions_installed "html"
	
#--------------------------------------DEBUG---------------------------------------------

	pcp_textarea "[ DEBUG ] $FILETOOLLST" "cat $FILETOOLLST" 150
	
#--------------------------------------DEBUG---------------------------------------------

	pcp_textarea "[ DEBUG ] $ONBOOTLST" "cat $ONBOOTLST" 150
	
#----------------------------------------------------------------------------------------
fi

#---------------/usr/local/etc/pcp/wpa_supplicant.conf maintained by user----------------
if [ "$WIFI" = "on" ]; then
	if [ $(pcp_wifi_maintained_by_user) -eq 0 ]; then

		pcp_textarea "/usr/local/etc/pcp/wpa_supplicant.conf maintained by user" "cat ${WPASUPPLICANTCONF}" 150

	fi
#-----------------------------------------Wifi information-------------------------------
	[ x"" = x"$(pcp_wlan0_mac_address)" ] && WLANMAC=" is missing - insert wifi adapter and [Save] to connect." || WLANMAC=$(pcp_wlan0_mac_address)
	[ x"" = x"$(pcp_wlan0_ip)" ] && WLANIP=" is missing - [Reboot] or [Save] to connect." || WLANIP=$(pcp_wlan0_ip)

	pcp_heading5 "Wifi information"

	echo '    <div class="row">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <input class="'$BUTTON'" form="setwifi" type="submit" name="SUBMIT" value="Scan">'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <p>Wifi MAC: '$WLANMAC'</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <p>Wifi IP: '$WLANIP'</p>'
	echo '      </div>'
	echo '    </div>'

#-------------------------------------Display available wifi networks--------------------
	if [ "$SUBMIT" = "Scan" ]; then
		pcp_textarea "Available wifi networks" "pcp_wifi_available_networks" 110
	fi
#----------------------------------------------------------------------------------------
fi
#----------------------------------------------------------------------------------------

#========================================================================================
# AP Mode Page Link
#----------------------------------------------------------------------------------------
wifi_apmode_page() {
	[ "$WIFI" = "on" ] && DISABLED="disabled" || unset DISABLED

	pcp_incr_id

	pcp_heading5 "Wireless Access Point (WAP) configuration page"

	echo '    <div class="row">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <form action="wifi_apmode.cgi" method="get">'
	echo '          <input class="'$BUTTON'" type="submit" name="APmode" value="WAP Mode" '$DISABLED'>'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <p>Setup piCorePlayer as a Wireless Access Point (WAP)&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="collapse">'
	echo '          <p>Disable wifi client above to enable this button.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_SERVER ] && wifi_apmode_page
#----------------------------------------------------------------------------------------

#-----------------------------------Network wait-----------------------------------------
pcp_heading5 "Network wait"

pcp_incr_id

echo '  <form id="Network_wait" name="Network_wait" action="'$0'" method="get">'
echo '    <div class="row">'
echo '      <div class="'$COLUMN3_1'">'
echo '        <p>Network wait</p>'
echo '      </div>'
echo '      <div class="'$COLUMN3_2'">'
echo '        <input class="form-control"'
echo '               type="text"'
echo '               name="NETWORK_WAIT"'
echo '               value="'$NETWORK_WAIT'"'
echo '               pattern="\d*"'
echo '               title="Use numbers."'
echo '        >'
echo '      </div>'
echo '      <div class="'$COLUMN3_3'">'
echo '        <p>Adjust network wait&nbsp;&nbsp;'
echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
echo '        </p>'
echo '        <div id="dt'$ID'" class="collapse">'
echo '          <p>&lt;xx&gt;</p>'
echo '          <p><b>Default: </b>50 (25 seconds)</p>'
echo '          <p>During the boot process, some USB wifi adapters take a long time to be set by DHCP.</p>'
echo '          <p>Usually the default value of 50 (25 seconds) is long enough.</p>'
echo '          <p>If you have a slow USB wifi adapter, DHCP server or network it may be benficial to increase the network wait time.</p>'
echo '          <p>You can check the startup log to see how long piCorePayer waited for the network. ie. Waiting for network. Done (1).</p>'
echo '          <p><b>Note: </b>piCorePlayer uses half second increments, so 50 equals 25 seconds wait time.</p>'
echo '        </div>'
echo '      </div>'
echo '    </div>'
echo '    <div class="row">'
echo '      <td colspan="3">'
echo '        <button class="'$BUTTON'" type="submit" name="ACTION" value="Network_wait">Save</button>'
echo '      </div>'
echo '    </div>'
echo '  </form>'
#----------------------------------------------------------------------------------------

pcp_wifi_html_end
