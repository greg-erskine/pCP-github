#!/bin/sh

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

echo '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">'
echo '<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">'
echo ''
echo '<head>'
echo '  <meta http-equiv="Cache-Control" content="no-cache" />'
echo '  <meta http-equiv="Pragma" content="no-cache" />'
echo '  <meta http-equiv="Expires" content="0" />'
echo '  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
echo '  <title>pCP - WIFI Settings</title>'
echo '  <meta name="author" content="Steen" />'
echo '  <meta name="description" content="WIFI Settings" />'
echo '  <link rel="stylesheet" type="text/css" href="../css/piCorePlayer.css" />'
echo ''
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

echo '<form name="setwifi" action="writetowifi.cgi" method="get">'
echo '  <table class="sframe" cellspacing="0" cellpadding="0" width="960">'
echo '    <tr>'
echo '      <td class="sframe">'
echo '        <table class="cfgframe" cellspacing="2" cellpadding="0" width="100%" align="center">'
echo '          <tr>'
echo '            <td colspan="3" class="header"><nobr>Set Wireless configuration.</nobr></td>'
echo '          </tr>'
echo '          <tr>'
echo '            <td class="title" width=20%>Wireless</td>'
echo '            <td class="content" width=40%>'
echo '              <input type="radio" name="WIFI" id="WIFI" onclick=enableWL() value="on">On&nbsp;'
echo '              <input type="radio" name="WIFI" id="WIFI" onclick=disableWL() value="off">Off'
echo '            </td>'
echo '          </tr>'
echo '          <tr>'
echo '            <td class="title">SSID</td>'
echo '            <td class="content">'
echo '              <input type="text" name="SSID" id="SSID" onChange="enableSAVE();" maxlength="32" size="32" value='\"$SSID\"'>'
echo '            </td>'
echo '          </tr>'
echo '          <tr>'
echo '            <td class="title">Password</td>'
echo '            <td class="content">'
echo '              <input type="password" name="PASSWORD" id="PASSWORD" onChange="enableSAVE();" maxlength="64" size="80" value='$PASSWORD'>'
echo '            </td>'
echo '          </tr>'
echo '          <tr>'
echo '            <td class="title">Security Mode</td>'
echo '            <td class="content">'
echo '              <select name="ENCRYPTION" id="ENCRYPTION" onChange="enableSAVE();">'
echo '                <option value="WPA">WPA or WPA2</option>'
echo '                <option value="WEP">WEP</option>'
echo '                <option value="OPEN">Open (No Encyrption)</option>'
echo '              </select>'
echo '            </td>'
echo '          </tr>'
echo '          <tr>'
echo '            <td colspan=2 class="btnline" >'
echo '              <input type="submit" name="SAVE" value="Save">&nbsp;'
echo '            </td>'
echo '          </tr>'
echo '        </table>'
echo '      </td>'
echo '    </tr>'
echo '  </table>'
echo '</form>'

available_networks_1() {
	#=========================================================================================
	# (c) Robert Shingledecker 2011-2012 v1.4
	# This routine has been based on code from the piCore script wifi.sh
	# /usr/local/bin/wifi.sh
	#-----------------------------------------------------------------------------------------

	unset WIFI && CNT=0
	until [ -n "$WIFI" ]
	do
		[ $((CNT++)) -gt 10 ] && break || sleep 1
		WIFI="$(iwconfig 2>/dev/null | awk '{if (NR==1)print $1}')"
	done
	if [ -z "$WIFI" ]; then
		echo "No wifi devices found!"
		exit 1
	fi
	ifconfig "$WIFI" up 2>/dev/null
	(for i in `seq 5`
	do
		iwlist "$WIFI" scanning
		[ "$?" == 0 ] && break
		sleep 1
	done ) | awk -v wifi=$WIFI '
	BEGIN {
		RS="\n"
		FS=":"
		i = 0
		title = "Available Wifi Networks for "wifi":"
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
			qual[i] = c[1] * 10 / 7
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
		printf "%s\n", title
		print "-------------------------------------------------------------------------------------------"
		print "        SSID                 Quality  Level      Channel     Encryption       Address"
		print "-------------------------------------------------------------------------------------------"
		for (l=1; l<15; l++) {
			++j
			if ( j <= i ) printf "%2d. %-25s %3d%1s   %4s   %2d %8s   %-3s %-4s  %18s\n", j, sid[j], qual[j], "%", level[j], chan[j], freq[j], enc[j], type[j], addr[j]
		}
		print "-------------------------------------------------------------------------------------------"
	} '
}

available_networks_2() {
	#=========================================================================================
	# Section added from old wifi page
	#-----------------------------------------------------------------------------------------
	#save scan results to a temp file
	sudo iwlist wlan0 scanning > /tmp/wifiscan
	#check if the scanning was ok with wlan0
	scan_ok=$(grep "wlan" /tmp/wifiscan)
	if [ -z "$scan_ok" ]; then
		killall -9 wpa_supplicant
		iwlist wlan0-1 scanning > /tmp/wifiscan
	fi
	#check if the scanning was ok
	scan_ok=$(grep "wlan" /tmp/wifiscan)
	#if scan was not ok, finish the script
	if [ -z "$scan_ok" ]; then
		echo '<p class="error">[ ERROR ] WIFI scanning failed.</p>'
		pcp_footer
		echo '</body>'
		echo '</html>'
		exit
	fi
	if [ -f /tmp/ssids ]; then
		rm /tmp/ssids
	fi
	#save number of scanned cells
	n_results=$(grep -c "ESSID:" /tmp/wifiscan)
	i=1
	while [ "$i" -le "$n_results" ]; do
		if [ $i -lt 10 ]; then
			cell=$(echo "Cell 0$i - Address:")
		else
			cell=$(echo "Cell $i - Address:")
		fi
		j=`expr $i + 1`
		if [ $j -lt 10 ]; then
			nextcell=$(echo "Cell 0$j - Address:")
		else
			nextcell=$(echo "Cell $j - Address:")
		fi
		#store only one cell info in a temp file
		awk -v v1="$cell" '$0 ~ v1 {p=1}p' /tmp/wifiscan | awk -v v2="$nextcell" '$0 ~ v2 {exit}1' > /tmp/onecell

		oneaddress=$(grep " Address:" /tmp/onecell | awk '{print $5}')
		onessid=$(grep "ESSID:" /tmp/onecell | awk '{ sub(/^[ \t]+/, ""); print }' | awk '{gsub("ESSID:", "");print}')
		oneencryption=$(grep "Encryption key:" /tmp/onecell | awk '{ sub(/^[ \t]+/, ""); print }' | awk '{gsub("Encryption key:on", "(secure)");print}' | awk '{gsub("Encryption key:off", "(open)  ");print}')
		onepower=$(grep "Quality=" /tmp/onecell | awk '{ sub(/^[ \t]+/, ""); print }' | awk '{gsub("Quality=", "");print}' | awk -F '/70' '{print $1}')
		onepower=$(awk -v v3=$onepower 'BEGIN{ print v3 * 10 / 7}')
		onepower=${onepower%.*}
		onepower="(Signal strength: $onepower%)"
		if [ -n "$oneaddress" ]; then                                                                                                            
			echo "$onessid  $oneaddress $oneencryption $onepower" >> /tmp/ssids                                                              
		else                                                                                                                                     
			echo "$onessid  $oneencryption $onepower" >> /tmp/ssids                                                                          
		fi
		i=`expr $i + 1`
	done
	rm /tmp/onecell
	#add numbers at beginning of line
	awk '{printf("%5d : %s\n", NR,$0)}' /tmp/ssids > /tmp/sec_ssids
	#generate file with only numbers and names
	grep ESSID /tmp/wifiscan | awk '{ sub(/^[ \t]+/, ""); print }' | awk '{printf("%5d : %s\n", NR,$0)}' | awk '{gsub("ESSID:", "");print}' > /tmp/ssids

	echo '<textarea name="TextBox" cols="118" rows="8">'
	echo 'Available WIFI networks:'
	cat /tmp/sec_ssids #show ssids list
	echo '</textarea>'
}

echo '<textarea name="TextBox" cols="118" rows="12">'
available_networks_1
echo '</textarea>'

#echo '<p>&nbsp;</p>'
#available_networks_2

pcp_refresh_button
pcp_footer

echo '</body>'
echo '</html>'
