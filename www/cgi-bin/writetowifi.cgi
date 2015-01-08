#!/bin/sh

# Version: 0.03 2015-01-06 SBP
#   Added function to remove wifi modules from loading during boot
#   if wifi is not chosen.

# Version: 0.02 2014-12-13 GE
#	Using pcp_html_head now.
#	HTML5 formatting.

# Version: 0.01 2014 SBP
#   Original version.

. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "Write WIFI Settings" "SBP" "20" "wifi.cgi"

pcp_banner
pcp_running_string
pcp_httpd_query_string

# Decode variables using httpd
SSID=`sudo /usr/local/sbin/httpd -d $SSID`
PASSWORD=`sudo /usr/local/sbin/httpd -d $PASSWORD`
ENCRYPTION=`sudo /usr/local/sbin/httpd -d $ENCRYPTION`
WIFI=`sudo /usr/local/sbin/httpd -d $WIFI`

echo '<h1>[ INFO ] You provided the following information</h1>'
echo '<p class="info">[ INFO ] WIFI is: '$WIFI'<br />'
echo '                [ INFO ] Your wifi SSID is: '$SSID'<br />'
echo '                [ INFO ] Your password is: '$PASSWORD'<br />'
echo '                [ INFO ] Encryption method is: '$ENCRYPTION'</p>'

# NEW section to save the parameters to the wifi.db
# This is a new version in order to saving space and backslash in SSID which is needed in wifi.db
# so a name like "steens wifi" should be saved as  "steens\ wifi"

# Only add backslash if not empty
if [ x"" = x"$SSID" ]; then
	break
else
	SSSID=`echo "$SSID" | sed 's/\ /\\\ /g'`
	# Change SSSID back to SSID
	SSID=$SSSID
fi

# Saves SSID either empty or with backslash
sudo chmod 766 /home/tc/wifi.db
sudo echo ${SSSID}$'\t'${PASSWORD}$'\t'${ENCRYPTION} > /home/tc/wifi.db

echo '<h1>[ INFO ] Current wifi.db</h1>'
echo '<textarea name="TextBox" cols="120" rows="2">'
cat $WIFIDB
echo '</textarea>'

# Add " " around variables
SSID="\"${SSID}"\"
PASSWORD="\"${PASSWORD}"\"
ENCRYPTION="\"${ENCRYPTION}"\"
WIFI="\"${WIFI}"\"

# Save the parameters to the config file
sudo sed -i "s/\(SSID *=*\).*/\1$SSID/" $CONFIGCFG
sudo sed -i "s/\(PASSWORD *=*\).*/\1$PASSWORD/" $CONFIGCFG
sudo sed -i "s/\(ENCRYPTION *=*\).*/\1$ENCRYPTION/" $CONFIGCFG
sudo sed -i "s/\(WIFI *=*\).*/\1$WIFI/" $CONFIGCFG


#======================================================================#
# Toggle whether wifi and wireless firmware tcz are loaded during boot #
#======================================================================#
if [ $WIFI == "\"on\"" ]; then
		if grep -Fxq "wifi.tcz" /mnt/mmcblk0p2/tce/onboot.lst
		then
			REBOOT=no
		else
			REBOOT=yes
		fi
	# Add wifi related modules back
	sudo fgrep -vxf /mnt/mmcblk0p2/tce/onboot.lst /mnt/mmcblk0p2/tce/piCorePlayer.dep >> /mnt/mmcblk0p2/tce/onboot.lst

# add a reboot button if needed
if [ $REBOOT = "yes" ]; then
echo "har vist yes"
echo '          <tr class="odd">'
echo '            <td class="column150 center">'
echo '              <form name="Reboot" action="javascript:pcp_confirm('\''Reboot piCorePlayer?'\'','\''reboot.cgi'\'')" method="get" id="Reboot">'
echo '                <input type="submit" value="Reboot" />'
echo '              </form>'
echo '            </td>'
echo '            <td>'
echo '              <p><h1>[ INFO ] Reboot is needed before you can use wifi</h1></p>'
echo '            </td>'
echo '          </tr>'
fi

fi


if [ $WIFI == "\"off\"" ]; then
	sudo sed -i '/firmware-ralinkwifi.tcz/d' /mnt/mmcblk0p2/tce/onboot.lst
	sudo sed -i '/firmware-rtlwifi.tcz/d' /mnt/mmcblk0p2/tce/onboot.lst
	sudo sed -i '/firmware-atheros.tcz/d' /mnt/mmcblk0p2/tce/onboot.lst
	sudo sed -i '/wireless/d' /mnt/mmcblk0p2/tce/onboot.lst
	sudo sed -i '/wifi.tcz/d' /mnt/mmcblk0p2/tce/onboot.lst
fi

pcp_show_config_cfg
pcp_backup

#========================================================================================
# Connect to the wifi
#----------------------------------------------------------------------------------------
if [ $WIFI == "\"on\"" ]; then
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

pcp_go_back_button

echo '</body>'
echo '</html>'