#!/bin/sh

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

[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] $WIFI: '$WIFI'</p>'

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
echo '            <td class="title">ESSID</td>'
echo '            <td class="content">'
echo '              <input type="text" name="SSID" id="SSID" onChange="enableSAVE();" maxlength="32" size="32" value='$SSID'>'
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

# new section from old wifi page
sudo iwlist wlan0 scanning > /tmp/wifiscan			#save scan results to a temp file
scan_ok=$(grep "wlan" /tmp/wifiscan)				#check if the scanning was ok with wlan0
if [ -z "$scan_ok" ]; then
	killall -9 wpa_supplicant
	iwlist wlan0-1 scanning > /tmp/wifiscan
fi
scan_ok=$(grep "wlan" /tmp/wifiscan) 				#check if the scanning was ok
if [ -z "$scan_ok" ]; then							#if scan was not ok, finish the script
	echo '<p class="error">[ ERROR ] WIFI scanning failed.</p>'
	pcp_footer
	echo '</body>'
	echo '</html>'
	exit
fi
if [ -f /tmp/ssids ]; then
	rm /tmp/ssids
fi
n_results=$(grep -c "ESSID:" /tmp/wifiscan)			#save number of scanned cell
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
	awk -v v1="$cell" '$0 ~ v1 {p=1}p' /tmp/wifiscan | awk -v v2="$nextcell" '$0 ~ v2 {exit}1' > /tmp/onecell #store only one cell info in a temp file

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
awk '{printf("%5d : %s\n", NR,$0)}' /tmp/ssids > /tmp/sec_ssids #add numbers at beginning of line
grep ESSID /tmp/wifiscan | awk '{ sub(/^[ \t]+/, ""); print }' | awk '{printf("%5d : %s\n", NR,$0)}' | awk '{gsub("ESSID:", "");print}' > /tmp/ssids #generate file with only numbers and names
echo '<textarea name="TextBox" cols="118" rows="8">'
echo 'Available WIFI networks:'
cat /tmp/sec_ssids #show ssids list
echo '</textarea>'

pcp_footer

echo '</body>'
echo '</html>'
