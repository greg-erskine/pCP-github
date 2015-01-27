#!/bin/sh

# Version: 0.10 2015-01-27 GE
#	Only display "Available wifi networks" if $WIFI = on
#	Added scanning message to give impression of reduced delay.
#	Reduced "CNT -gt" from 10 to 5 to speed up display in WIFI2 loop.
#	Fixed "Available wifi networks" format to work with 8192cu and rt2x00usb.

# Version: 0.09 2015-01-25 SBP
#	Added check for wifi adaptor present.
#	Added descriptions and more/less help.

# Version: 0.08 2014-12-20 GE
#	Using pcp_html_head now.
#	HTML5 formatting.

# Version: 0.07 2014-10-10 SBP
#	Added if [ $WIFI = on ] condition.

# Version: 0.06 2014-09-30 GE
#	Added footer when No wifi devices found!.

# Version: 0.05 2014-09-13 GE
#	Added new available networks routine.
#	Added double quotes around $SSID to handle spaces in SSID.
#	Changed ESSID to SSID.
#	Some reformatting.

# Version: 0.04 2014-08-31 GE
#	Increased password length from 32 to 64.
#	Added some missing html tags.
#	Some reformatting.

# Version: 0.03 2014-08-28 GE
#	Formatted wifi scanning section.
#	Enabled Save button.
#	Changed "WLAN Service" to "Wireless".
#	Changed "Enable/Disable" to "On/Off".
#	Removed "Save" button enable message.

# Version: 0.02 2014-08-22 SBP
#	Added wifi scanning section.

# Version: 0.01 2014-06-25 GE
#	Original.

. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "WIFI Settings" "SBP"

echo '<script type="text/javascript">'

echo 'var enbl = "'$WIFI'";'
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
echo '    }'
echo '}'
echo ''
echo 'function enableWL() {'
echo '    document.forms[0].SAVE.disabled=false;'
echo '    document.forms[0].SSID.disabled=false;'
echo '    document.forms[0].PASSWORD.disabled=false;'
echo '    document.forms[0].ENCRYPTION.disabled=false;'
echo '}'
echo ''
echo 'function disableWL() {'
echo '    document.forms[0].SAVE.disabled=false;'
echo '    document.forms[0].SSID.disabled=true;'
echo '    document.forms[0].PASSWORD.disabled=true;'
echo '    document.forms[0].ENCRYPTION.disabled=true;'
echo '}'
echo ''
echo 'function enableSAVE() {'
echo '    document.forms[0].SAVE.disabled=false;'
echo '}'

#####################
# Fix required here #
#####################
echo '</script>'
echo '</head>'
echo ''
echo '<body onload=frmLoad()>'

pcp_controls
pcp_banner
pcp_navigation

if [ $DEBUG = 1 ]; then
	echo '<p class="debug">[ DEBUG ] $WIFI: '$WIFI'<br />'
	echo '                 [ DEBUG ] $SSID: '$SSID'<br />'
	echo '                 [ DEBUG ] $PASSWORD: '$PASSWORD'<br />'
	echo '                 [ DEBUG ] $ENCRYPTION: '$ENCRYPTION'</p>'
fi

echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <form name="setwifi" action="writetowifi.cgi" method="get">'
echo '        <div class="row">'
echo '          <fieldset>'
echo '            <legend>Set wifi configuration</legend>'
echo '            <table class="bggrey percent100">'
echo '              <tr class="even">'
echo '                <td class="column150">'
echo '                  <p>Wifi</p>'
echo '                </td>'
echo '                <td class="column380">'
echo '                  <input class="small1" type="radio" name="WIFI" id="WIFI" onclick=enableWL() value="on">On&nbsp;'
echo '                  <input class="small1" type="radio" name="WIFI" id="WIFI" onclick=disableWL() value="off">Off'
echo '                </td>'
echo '                <td>'
echo '                  <p>Set wifi on or off&nbsp;&nbsp;'
echo '                    <a class="moreless" id="ID01a" href=# onclick="return more('\''ID01'\'')">more></a>'
echo '                  </p>'
echo '                  <div id="ID01" class="less">'
echo '                    <ul>'
echo '                      <li>Selecting wifi on will enable the remaining fields.</li>'
echo '                      <li>A reboot is required when wifi is turned on.</li>'
echo '                      <li>Turn wifi on if you have compatible USB wifi adaptor installed.</li>'
echo '                      <li>Setting wifi to off will improve boot times.</li>'
echo '                    </ul>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'
echo '              <tr class="odd">'
echo '                <td class="column150">'
echo '                  <p>SSID</p>'
echo '                </td>'
echo '                <td class="column380">'
echo '                  <input class="large15" type="text" name="SSID" id="SSID" onChange="enableSAVE();" maxlength="32" value='\"$SSID\"'>'
echo '                </td>'
echo '                <td>'
echo '                  <p>Enter your wifi network SSID&nbsp;&nbsp;'
echo '                    <a class="moreless" id="ID02a" href=# onclick="return more('\''ID02'\'')">more></a>'
echo '                  </p>'
echo '                  <div id="ID02" class="less">'
echo '                    <ul>'
echo '                      <li>Service Set Identifier (SSID).</li>'
echo '                      <li>Use valid alphanumeric characters only.</li>'
echo '                      <li>Maximum length of 32 characters.</li>'
echo '                    </ul>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'
echo '              <tr class="even">'
echo '                <td class="column150">'
echo '                  <p>Password</p>'
echo '                </td>'
echo '                <td class="column380">'
echo '                  <input class="large30" type="password" name="PASSWORD" id="PASSWORD" onChange="enableSAVE();" maxlength="64" value='$PASSWORD'>'
echo '                </td>'
echo '                <td>'
echo '                  <p>Enter your wifi network password&nbsp;&nbsp;'
echo '                    <a class="moreless" id="ID03a" href=# onclick="return more('\''ID03'\'')">more></a>'
echo '                  </p>'
echo '                  <div id="ID03" class="less">'
echo '                    <ul>'
echo '                      <li>Use valid alphanumeric characters only.</li>'
echo '                      <li>Maximum length of 64 characters.</li>'
echo '                    </ul>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'
echo '              <tr class="odd">'
echo '                <td class="column150">'
echo '                  <p>Security Mode</p>'
echo '                </td>'
echo '                <td class="column380">'
echo '                  <select name="ENCRYPTION" id="ENCRYPTION" onChange="enableSAVE();">'
echo '                    <option value="WPA">WPA or WPA2</option>'
echo '                    <option value="WEP">WEP</option>'
echo '                    <option value="OPEN">Open (No Encyrption)</option>'
echo '                  </select>'
echo '                </td>'
echo '                <td>'
echo '                  <p>Set to your wifi network security level&nbsp;&nbsp;'
echo '                    <a class="moreless" id="ID04a" href=# onclick="return more('\''ID04'\'')">more></a>'
echo '                  </p>'
echo '                  <div id="ID04" class="less">'
echo '                    <p>Recommended: WPA or WPA2</p>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'
echo '              <tr>'
echo '                <td colspan=3>'
echo '                  <input type="submit" name="SAVE" value="Save">'
echo '                </td>'
echo '              </tr>'
echo '            </table>'
echo '          </fieldset>'
echo '        </div>'
echo '      </form>'
echo '    </td>'
echo '  </tr>'
echo '</table>'

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
		echo -en "1. USB wifi adaptor missing - insert adaptor\n"
		echo -en "2. wifi drivers and firmware missing - reboot required"
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
		pcp_footer
		pcp_refresh_button
		echo '</body>'
		echo '</html>'
		exit
	fi
	ifconfig "$WIFI2" up 2>/dev/null
	(for i in `seq 5`
	do
		iwlist "$WIFI2" scanning
		[ "$?" == 0 ] && break
		sleep 1
	done ) | awk -v wifi=$WIFI2 '
	BEGIN {
		RS="\n"
		FS=":"
		i = 0
	}
	function rsort(qual,level,sid,enc,chan,freq,type,addr,n,i,j,t) {
###		for (i = 2; i <= n; i++)
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
			if ( i == 0  || sid[i] != "" ) i++
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
			split(q,c," ")
###			qual[i] = c[1] * 10 / 7
			qual[i] = c[1]
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
		print "-------------------------------------------------------------------------------------------"
		print "        SSID                 Quality  Level      Channel     Encryption       Address"
		print "-------------------------------------------------------------------------------------------"
		for (l=1; l<15; l++) {
			++j
			if ( j <= i ) printf "%2d. %-25s %3d%1s   %4s   %2d %8s   %-3s %-4s  %18s\n", j, sid[j], qual[j], " ", level[j], chan[j], freq[j], enc[j], type[j], addr[j]
		}
		print "-------------------------------------------------------------------------------------------"
	} '
}

#----------------------------------------------------------------------------------------

if [ $WIFI = on ]; then
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <form name="wifi_networks" method="get">'
	echo '        <div class="row">'
	echo '          <fieldset>'
	echo '            <legend>Available wifi networks</legend>'
	echo '            <table class="bggrey percent100">'
	echo '              <tr class="odd">'
	echo '                <td>'

	pcp_textarea_inform "none" "available_networks" 110

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

pcp_footer
pcp_refresh_button

echo '</body>'
echo '</html>'