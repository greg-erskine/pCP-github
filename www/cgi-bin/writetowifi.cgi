#!/bin/sh

# Version: 0.05 2015-06-10 GE
#	Tidy up of code.

# Version: 0.04 2015-03-24 GE
#	Removed comments to Steen.

# Version: 0.03 2015-01-06 SBP
#	Added function to remove wifi modules from loading during boot if wifi is not chosen.

# Version: 0.02 2014-12-13 GE
#	Using pcp_html_head now.
#	HTML5 formatting.

# Version: 0.01 2014 SBP
#	Original version.

. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "Write WIFI Settings" "SBP" "20" "wifi.cgi"

pcp_banner
pcp_running_string
pcp_httpd_query_string

# Decode variables using httpd
WIFI=`sudo $HTPPD -d $WIFI`
if [ $WIFI = on ]; then
	SSID=`sudo $HTPPD -d $SSID`
	PASSWORD=`sudo $HTPPD -d $PASSWORD`
	ENCRYPTION=`sudo $HTPPD -d $ENCRYPTION`
fi

if [ $DEBUG = 1 ]; then
	echo '<p class="debug">[ DEBUG ] $WIFI: '$WIFI'<br />'
	echo '                 [ DEBUG ] $SSID: '$SSID'<br />'
	echo '                 [ DEBUG ] $PASSWORD: '$PASSWORD'<br />'
	echo '                 [ DEBUG ] $ENCRYPTION: '$ENCRYPTION'</p>'
fi

# Only add backslash if not empty
if [ x"" != x"$SSID" ]; then
	[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Adding slashes to $SSSID...</p>'
	SSSID=`echo "$SSID" | sed 's/\ /\\\ /g'`
	# Change SSSID back to SSID
	SSID=$SSSID
fi

# Saves SSID either empty or with backslash
[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Refreshing '$WIFIDB'...</p>'
sudo chmod 766 /home/tc/wifi.db
sudo echo ${SSSID}$'\t'${PASSWORD}$'\t'${ENCRYPTION} > /home/tc/wifi.db

pcp_textarea "" "cat $WIFIDB" 30 log

# Save the parameters to the config file, add double quotes
sudo sed -i "s/\(SSID=\).*/\1\"$SSID\"/" $CONFIGCFG
sudo sed -i "s/\(PASSWORD=\).*/\1\"$PASSWORD\"/" $CONFIGCFG
sudo sed -i "s/\(ENCRYPTION=\).*/\1\"$ENCRYPTION\"/" $CONFIGCFG
sudo sed -i "s/\(WIFI=\).*/\1\"$WIFI\"/" $CONFIGCFG

#========================================================================================
# Toggle whether wifi and wireless firmware tcz are loaded during boot
#----------------------------------------------------------------------------------------
if [ $WIFI = on ]; then
	[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] wifi is on. Updating onboot.lst...</p>'
	if grep -Fxq "wifi.tcz" /mnt/mmcblk0p2/tce/onboot.lst; then
		[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Reboot NOT required.</p>'
		REBOOT=no
	else
		[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Reboot required.</p>'
		REBOOT=yes
	fi
	# Add wifi related modules back
	sudo fgrep -vxf /mnt/mmcblk0p2/tce/onboot.lst /mnt/mmcblk0p2/tce/piCorePlayer.dep >> /mnt/mmcblk0p2/tce/onboot.lst
fi

if [ $WIFI = off ]; then
	[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] wifi is off. Removing wifi extensions...</p>'
	sudo sed -i '/firmware-ralinkwifi.tcz/d' /mnt/mmcblk0p2/tce/onboot.lst
	sudo sed -i '/firmware-rtlwifi.tcz/d' /mnt/mmcblk0p2/tce/onboot.lst
	sudo sed -i '/firmware-atheros.tcz/d' /mnt/mmcblk0p2/tce/onboot.lst
	sudo sed -i '/wireless/d' /mnt/mmcblk0p2/tce/onboot.lst
	sudo sed -i '/wifi.tcz/d' /mnt/mmcblk0p2/tce/onboot.lst
fi

pcp_textarea "" "cat $CONFIGCFG" 150 log
pcp_textarea "" "cat /mnt/mmcblk0p2/tce/onboot.lst" 150 log
pcp_textarea "" "cat /mnt/mmcblk0p2/tce/piCorePlayer.dep" 150 log

pcp_backup

#========================================================================================
# Connect to the wifi
#----------------------------------------------------------------------------------------
if [ $WIFI = on ]; then
	echo '<textarea name="TextBox" cols="120" rows="20">'
	echo 'ifconfig wlan0 down'
	sudo ifconfig wlan0 down
	echo 'ifconfig wlan0 up'
	sudo ifconfig wlan0 up
	sudo wifi.sh -a
	echo ''
	ifconfig
	echo ''
	iwconfig
	echo '</textarea>'
fi

echo '<br />'
echo '<br />'
echo '<form name="go_back" action="wifi.cgi" method="get">'
echo '  <input type="submit" value="Go back" />'
echo '</form>'

# Add a reboot button if needed
if [ $REBOOT = yes ]; then
	echo '<br />'
	echo '<br />'
	echo '<form name="Reboot" action="javascript:pcp_confirm('\''Reboot piCorePlayer?'\'','\''reboot.cgi'\'')" method="get">'
	echo '  <span class="error"><input type="submit" value="Reboot" />&nbsp;&nbsp;Reboot required before you can use wifi.</span>'
	echo '</form>'
fi

echo '</body>'
echo '</html>'