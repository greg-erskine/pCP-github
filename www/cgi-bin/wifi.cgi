#!/bin/sh

# Version: 3.5.0 2018-02-21
#	Add page button for AP mode. PH.
#	Add Bluetooth enable/disable. PH.
#	HTML5 and cosmetic cleanup. GE.

# Version: 3.20 2017-03-08
#	Changed pcp_picoreplayers_toolbar and pcp_controls. GE.
#	Fixed pcp-xxx-functions issues. GE.
#	Changed RPi3 wifi disable to overlay. PH.

# Version: 3.02 2016-09-15
#	Minor update. GE.

# Version: 2.06 2016-04-27
#	Add ability to blacklist RPi3 built-in wifi. PH.

# Version: 0.01 2014-06-25
#	Original. GE.

. pcp-functions
. pcp-rpi-functions
. pcp-lms-functions

pcp_html_head "WIFI Settings" "SBP" "nobody"

echo ''
echo '<body onload=frmLoad()>'

#========================================================================================
# Javascript to disable form fields when wifi is off
#----------------------------------------------------------------------------------------
echo '<script>'
echo 'var enbl = "'$WIFI'";'
echo 'var encr = "'$ENCRYPTION'";'
echo ''
echo 'function frmLoad() {'
#echo '    document.forms[0].SAVE.disabled=true;'
echo '    if(enbl=="on"){'
echo '        document.forms[0].WIFI[0].checked=true;'
echo '    }'
echo '    else{'
echo '        document.forms[0].WIFI[1].checked=true;'
echo '        document.forms[0].SSID.disabled=true;'
echo '        document.forms[0].PASSWORD.disabled=true;'
echo '        document.forms[0].ENCRYPTION.disabled=true;'
echo '        document.forms[1].APmode.disabled=false;'
echo '    }'
echo '    switch(encr) {'
echo '         case "WPA":'
echo '            document.forms[0].ENCRYPTION[0].selected=true;'
echo '            break;'
echo '         case "WEP":'
echo '            document.forms[0].ENCRYPTION[1].selected=true;'
echo '            break;'
echo '         case "OPEN":'
echo '            document.forms[0].ENCRYPTION[2].selected=true;'
echo '            break;'
echo '    }'
echo '}'
echo ''
echo 'function enableWL() {'
echo '    document.forms[0].SAVE.disabled=false;'
echo '    document.forms[0].SSID.disabled=false;'
echo '    document.forms[0].PASSWORD.disabled=false;'
echo '    document.forms[0].ENCRYPTION.disabled=false;'
echo '    document.forms[1].APmode.disabled=true;'
echo '}'
echo ''
echo 'function disableWL() {'
echo '    document.forms[0].SAVE.disabled=false;'
echo '    document.forms[0].SSID.disabled=true;'
echo '    document.forms[0].PASSWORD.disabled=true;'
echo '    document.forms[0].ENCRYPTION.disabled=true;'
echo '    document.forms[1].APmode.disabled=false;'
echo '}'
echo ''
echo 'function enableSAVE() {'
echo '    document.forms[0].SAVE.disabled=false;'
echo '}'
echo 'function validate() {'
echo '    if (document.setwifi.RPI3INTWIFI.value == "on" && document.setwifi.RPIBLUETOOTH.value == "on"){'
echo '      alert("RPI Wifi and Bluetooth\nmust NOT be enabled at the same time");'
echo '      return false;'
echo '    }'
echo '    return ( true );'
echo '}'
echo '</script>'

pcp_picoreplayers_toolbar
pcp_controls
pcp_banner
pcp_navigation
pcp_httpd_query_string

available_networks() {
	#=========================================================================================
	# (c) Robert Shingledecker 2011-2012 v1.4
	# This routine has been based on code from the piCore script wifi.sh
	# /usr/local/bin/wifi.sh
	#-----------------------------------------------------------------------------------------
	unset WIFI2 && CNT=0
	echo -en "Scanning"
	until [ -n "$WIFI2" ]
	do
		[ $((CNT++)) -gt 5 ] && break || sleep 1
		echo -en "."
		WIFI2="$(iwconfig 2>/dev/null | awk '{if (NR==1)print $1}')"
	done
	if [ -z "$WIFI2" ]; then
		echo -en "\n\nNo wifi devices found!\n\n"
		echo -en "Possible error:\n\n"
		echo -en "1. USB wifi adapter missing - insert adapter.\n"
		echo -en "2. wifi drivers and firmware missing - reboot required."
		echo '</textarea>'
		echo '                </td>'
		echo '              </tr>'
		echo '            </table>'
		echo '          </fieldset>'
		echo '        </div>'
		echo '      </form>'
		echo '    </td>'
		echo '  </tr>'
		echo '</table>'
		pcp_refresh_button
		pcp_footer
		pcp_copyright
		echo '</body>'
		echo '</html>'
		exit
	fi
	ifconfig "$WIFI2" up 2>/dev/null
	(for i in `seq 5`
	do
		iwlist "$WIFI2" scanning
		[ $? -eq 0 ] && break
		sleep 1
	done ) | awk -v wifi=$WIFI2 '
	BEGIN {
		RS="\n"
		FS=":"
		i = 0
	}
	function rsort(qual,level,sid,enc,chan,freq,type,addr,n,i,j,t) {
		for (i = 2; i <= n; i++)
			for (j = i; j > 1 && qual[j]+0 > qual[j-1]+0; j--) {
				# swap qual[j] and qual[j-1]
				t = qual[j]; qual[j] = qual[j-1]; qual[j-1] = t
				t = level[j]; level[j] = level[j-1]; level[j-1] = t
				t = sid[j];  sid[j]  = sid[j-1];  sid[j-1]  = t
				t = enc[j];  enc[j]  = enc[j-1];  enc[j-1]  = t
				t = chan[j]; chan[j] = chan[j-1]; chan[j-1] = t
				t = freq[j]; freq[j] = freq[j-1]; freq[j-1] = t
				t = type[j]; type[j] = type[j-1]; type[j-1] = t
				t = addr[j]; addr[j] = addr[j-1]; addr[j-1] = t
			}
	}
	# main ()
	{
		if ($1 ~ /Cell/) {
			if ( i == 0 || sid[i] != "" ) i++
			addr[i] = $2":"$3":"$4":"$5":"$6":"$7
			gsub(" ","",addr[i])
		}
		if ($1 ~ /Frequency/) {
			split($2,c," ")
			chan[i] = c[4]
			gsub("\)","",chan[i])
			freq[i] = "("c[1]c[2]")"
			gsub(" ","",freq[i])
		}
		if ($1 ~ /Quality/) {
			q = $2
			if (index($1,"=")) {
				split($1,c,"=")
				q = c[2]
				level[i] = c[3]
				gsub(" ","",level[i])
			}
			split(q,c,"/")
			qual[i] = c[1] * 100 / c[2]
		}
		if ($1 ~ /Encr/){
			enc[i] = $2
		}
		if ($1 ~ /ESSID/) {
			sid[i] = $2
			gsub("\"","",sid[i])
		}
		if (enc[i] ~ /off/) type[i]="NONE"
		if ($2 ~ /WPA/) type[i]="WPA"
		if ($2 ~ /WPA2 /) type[i]="WPA2"
		if (type[i] == "" ) type[i]="WEP"
	}
	END {
		rsort(qual,level,sid,enc,chan,freq,type,addr,NR)
		print ""
		print "---------------------------------------------------------------------------------------------"
		print "       SSID                 Quality   Level       Channel      Encryption       Address"
		print "---------------------------------------------------------------------------------------------"
		for (l=1; l<15; l++) {
			++j
			#                     |NO. |SSID |Qual  |Level |Channel   |Encrypt   |Address      
			if ( j <= i ) printf "%2d. %-25s %3d    %7s    %2d %10s   %-3s %-4s  %18s\n", j, sid[j], qual[j], level[j], chan[j], freq[j], enc[j], type[j], addr[j]
		}
		print "---------------------------------------------------------------------------------------------"
	} '
}
#----------------------------------------------------------------------------------------

if [ $DEBUG -eq 1 ]; then
	echo '<p class="debug">[ DEBUG ] $WIFI: '$WIFI'<br />'
	echo '                 [ DEBUG ] $SSID: '$SSID'<br />'
	echo '                 [ DEBUG ] $PASSWORD: '$PASSWORD'<br />'
	echo '                 [ DEBUG ] $ENCRYPTION: '$ENCRYPTION'<br />'
	echo '                 [ DEBUG ] $RPI3INTWIFI: '$RPI3INTWIFI'<br />'
	echo '                 [ DEBUG ] $RPIBLUETOOTH: '$RPIBLUETOOTH'</p>'
fi

#========================================================================================
# Main.
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <form name="setwifi" action="writetowifi.cgi" method="get">'
echo '        <div class="row">'
echo '          <fieldset>'
echo '            <legend>Set wifi configuration</legend>'
echo '            <table class="bggrey percent100">'
#--------------------------------------Wifi on/off---------------------------------------
pcp_incr_id
pcp_start_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="column150">'
echo '                  <p>Wifi</p>'
echo '                </td>'
echo '                <td class="column380">'
echo '                  <input class="small1" type="radio" onclick=enableWL() name="WIFI" value="on">On&nbsp;'
echo '                  <input class="small1" type="radio" onclick=disableWL() name="WIFI" value="off">Off'
echo '                </td>'
echo '                <td>'
echo '                  <p>Set wifi on or off&nbsp;&nbsp;'
echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                  </p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <ul>'
echo '                      <li>Selecting wifi on will enable the remaining fields.</li>'
echo '                      <li>A reboot is required when wifi is turned on.</li>'
echo '                      <li>Turn wifi on if you have compatible USB wifi adaptor installed.</li>'
echo '                      <li>Setting wifi to off will improve boot times.</li>'
echo '                    </ul>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'
#--------------------------------------SSID----------------------------------------------
pcp_incr_id
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="column150">'
echo '                  <p>SSID</p>'
echo '                </td>'
echo '                <td class="column380">'
echo '                  <input class="large15" type="text" name="SSID" value="'$SSID'" onChange="enableSAVE();" maxlength="32">'
echo '                </td>'
echo '                <td>'
echo '                  <p>Enter your wifi network SSID&nbsp;&nbsp;'
echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                  </p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <ul>'
echo '                      <li>Service Set Identifier (SSID).</li>'
echo '                      <li>Use valid alphanumeric characters only.</li>'
echo '                      <li>Maximum length of 32 characters.</li>'
echo '                    </ul>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'
#--------------------------------------Password------------------------------------------
pcp_incr_id
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="column150">'
echo '                  <p>Password</p>'
echo '                </td>'
echo '                <td class="column380">'
echo '                  <input class="large30" type="password" name="PASSWORD" value='$PASSWORD' onChange="enableSAVE();" maxlength="64">'
echo '                </td>'
echo '                <td>'
echo '                  <p>Enter your wifi network password&nbsp;&nbsp;'
echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                  </p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <ul>'
echo '                      <li>Use valid alphanumeric characters only.</li>'
echo '                      <li>Maximum length of 64 characters.</li>'
echo '                    </ul>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'
#--------------------------------------Security Mode-------------------------------------
pcp_incr_id
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="column150">'
echo '                  <p>Security Mode</p>'
echo '                </td>'
echo '                <td class="column380">'
echo '                  <select class="large15" name="ENCRYPTION" onChange="enableSAVE();">'
echo '                    <option value="WPA">WPA or WPA2</option>'
echo '                    <option value="WEP">WEP</option>'
echo '                    <option value="OPEN">Open (No Encyrption)</option>'
echo '                  </select>'
echo '                </td>'
echo '                <td>'
echo '                  <p>Set to your wifi network security level&nbsp;&nbsp;'
echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                  </p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <p>&lt;WPA|WEP|Open&gt;</p>'
echo '                    <p>Recommended: WPA or WPA2</p>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'
#--------------------------------------Built-in Wifi-------------------------------------
if ([ $(pcp_rpi_is_model_3B) -eq 0 ] || [ $(pcp_rpi_is_model_zerow) -eq 0 ]); then
	case "$RPI3INTWIFI" in
		on) RPI3WIFIyes="checked" ;;
		off) RPI3WIFIno="checked" ;;
		*);;
	esac
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>RPi Built-in Wifi</p>'
	echo '                </td>'
	echo '                <td class="column380">'
	echo '                  <input class="small1" type="radio" name="RPI3INTWIFI" value="on" '$RPI3WIFIyes'>On&nbsp;'
	echo '                  <input class="small1" type="radio" name="RPI3INTWIFI" value="off" '$RPI3WIFIno'>Off'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Turn off Raspberry Pi 3B / Zero-W built-in wifi card&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>This will load an overlay that disables RPi3/Zero-W onboard wifi.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
#--------------------------------------Built-in Bluetooth--------------------------------
	case "$RPIBLUETOOTH" in
		on) RPIBLUETOOTHyes="checked" ;;
		off) RPIBLUETOOTHno="checked" ;;
		*);;
	esac
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>RPi Built-in Bluetooth</p>'
	echo '                </td>'
	echo '                <td class="column380">'
	echo '                  <input class="small1" type="radio" name="RPIBLUETOOTH" value="on" '$RPIBLUETOOTHyes'>On&nbsp;'
	echo '                  <input class="small1" type="radio" name="RPIBLUETOOTH" value="off" '$RPIBLUETOOTHno'>Off'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Turn off Raspberry Pi 3B / Zero-W built-in bluetooth&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>This will load an overlay that disables RPi3/Zero-W onboard bluetooth.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
fi
#--------------------------------------Buttons------------------------------------------
pcp_incr_id
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td colspan=3>'
echo '                  <input type="submit" name="SAVE" value="Save/Connect" onclick="return(validate());">'
[ $MODE -ge $MODE_ADVANCED ] &&
echo '                  <input type="button" name="DIAGNOSTICS" onClick="location.href='\'''diag_wifi.cgi''\''" value="Diagnostics">'
echo '                </td>'
echo '              </tr>'
echo '            </table>'
echo '          </fieldset>'
echo '        </div>'
echo '      </form>'
#--------------------------------------Display Wifi information--------------------------
if [ "$WIFI" = "on" ]; then
	[ x"" = x"$(pcp_wlan0_mac_address)" ] && WLANMAC=" is missing - reboot or connect required." || WLANMAC=$(pcp_wlan0_mac_address)
	[ x"" = x"$(pcp_wlan0_ip)" ] && WLANIP=" is missing - reboot or connect required." || WLANIP=$(pcp_wlan0_ip)

	echo '      <form name="scan" action="wifi.cgi" method="get">'
	echo '        <div class="row">'
	echo '          <fieldset>'
	echo '            <legend>Wifi information</legend>'
	echo '            <table class="bggrey percent100">'
	pcp_start_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <input type="submit" name="SUBMIT" value="Scan">'
	echo '                </td>'
	echo '                <td class="column380">'
	echo '                  <p>Wifi MAC: '$WLANMAC'</p>'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Wifi IP: '$WLANIP'</p>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </table>'
	echo '          </fieldset>'
	echo '        </div>'
	echo '      </form>'
fi
#--------------------------------------Display Available wifi networks-------------------
if [ "$SUBMIT" = "Scan" ] && [ "$WIFI" = "on" ]; then
	echo '      <form name="wifi_networks" method="get">'
	echo '        <div class="row">'
	echo '          <fieldset>'
	echo '            <legend>Available wifi networks</legend>'
	echo '            <table class="bggrey percent100">'
	pcp_start_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td>'
	                        pcp_textarea_inform "none" "available_networks" 110
	echo '                </td>'
	echo '              </tr>'
	echo '            </table>'
	echo '          </fieldset>'
	echo '        </div>'
	echo '      </form>'
fi
#----------------------------------------------------------------------------------------
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------

#========================================================================================
# AP Mode Page Link
#----------------------------------------------------------------------------------------
wifi_apmode_page(){
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>AP mode configuration page</legend>'
	echo '          <table class="bggrey percent100">'
	pcp_incr_id
	pcp_start_row_shade
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150 center">'
	echo '                <form action="wifi_apmode.cgi" method="get">'
	echo '                  <input type="submit" name="APmode" value="pCP AP Mode">'
	echo '                </form>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>Setup your piCorePlayer as a wifi AP&nbsp;&nbsp;'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <p>Disable wifi client above to enable this button.</p>'
	echo '                </div>'
	echo '              </td>'
	echo '            </tr>'
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
}
[ $MODE -ge $MODE_BETA ] && wifi_apmode_page
#----------------------------------------------------------------------------------------

pcp_footer
[ $MODE -ge $MODE_NORMAL ] && pcp_mode
pcp_copyright

echo '</body>'
echo '</html>'
