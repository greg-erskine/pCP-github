#!/bin/sh

# Version: 3.00 2016-07-01 PH
#	Changed name for RPi3 internal wifi firmware extension

# Version: 2.06 2016-05-07 PH
#	Added Blacklist for RPi3 internal wifi

# Version: 0.09 2016-03-25 PH
#   Added firmware-brcmfmac43430.tcz

# Version: 0.08 2016-02-23 GE
#	Added firmware-brcmwifi.tcz.

# Version: 0.07 2015-09-19 SBP
#	Removed httpd decoding.

# Version: 0.06 2015-07-09 SBP
#	Revised method of loading wifi firmware.

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

ORIG_RPI3INTWIFI=$RPI3INTWIFI

pcp_html_head "Write WIFI Settings" "SBP" "20" "wifi.cgi"

pcp_banner
pcp_running_string
pcp_httpd_query_string
pcp_save_to_config

if [ $DEBUG -eq 1 ]; then
	echo '<p class="debug">[ DEBUG ] $WIFI: '$WIFI'<br />'
	echo '                 [ DEBUG ] $SSID: '$SSID'<br />'
	echo '                 [ DEBUG ] $PASSWORD: '$PASSWORD'<br />'
	echo '                 [ DEBUG ] $ENCRYPTION: '$ENCRYPTION'<br />'
	echo '                 [ DEBUG ] $RPI3INTWIFI: '$RPI3INTWIFI'</p>'
fi

# Only add backslash if not empty
if [ x"" != x"$SSID" ]; then
	[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] Adding slashes to $SSSID...</p>'
	SSSID=`echo "$SSID" | sed 's/\ /\\\ /g'`
	# Change SSSID back to SSID
	SSID=$SSSID
fi

# Saves SSID either empty or with backslash
[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] Refreshing '$WIFIDB'...</p>'
sudo chmod 766 /home/tc/wifi.db
sudo echo ${SSSID}$'\t'${PASSWORD}$'\t'${ENCRYPTION} > /home/tc/wifi.db

pcp_textarea "" "cat $WIFIDB" 40

#========================================================================================
# Toggle whether wifi and wireless firmware tcz are loaded during boot
#----------------------------------------------------------------------------------------
if [ "$WIFI" = "on" ]; then
	[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] wifi is on. Updating onboot.lst...</p>'
	if grep -Fxq "wifi.tcz" /mnt/mmcblk0p2/tce/onboot.lst; then
		[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] Wifi modules already loaded.</p>'
	else
		[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] Loading wifi firmware and modules.</p>'
		# Add wifi related modules back
		sudo fgrep -vxf /mnt/mmcblk0p2/tce/onboot.lst /mnt/mmcblk0p2/tce/piCorePlayer.dep >> /mnt/mmcblk0p2/tce/onboot.lst

		sudo -u tc tce-load -i firmware-atheros.tcz >/dev/null 2>&1
		[ $? -eq 0 ] && echo '<p class="info">[ INFO ] Atheros firmware loaded.</p>' || echo '<p class="error">[ ERROR ] Atheros firmware load error.</p>'
		sudo -u tc tce-load -i firmware-brcmwifi.tcz >/dev/null 2>&1
		[ $? -eq 0 ] && echo '<p class="info">[ INFO ] Broadcom firmware loaded.</p>' || echo '<p class="error">[ ERROR ] Broadcom USB firmware load error.</p>'
		sudo -u tc tce-load -i firmware-rpi3-wireless.tcz >/dev/null 2>&1
		[ $? -eq 0 ] && echo '<p class="info">[ INFO ] Broadcom firmware loaded.</p>' || echo '<p class="error">[ ERROR ] Broadcom RPi3 firmware load error.</p>'
		sudo -u tc tce-load -i firmware-ralinkwifi.tcz >/dev/null 2>&1
		[ $? -eq 0 ] && echo '<p class="info">[ INFO ] Ralink firmware loaded.</p>' || echo '<p class="error">[ ERROR ] Ralink firmware load error.</p>'
		sudo -u tc tce-load -i firmware-rtlwifi.tcz >/dev/null 2>&1
		[ $? -eq 0 ] && echo '<p class="info">[ INFO ] Realtek firmware loaded.</p>' || echo '<p class="error">[ ERROR ] Realtek firmware load error.</p>'

		sudo -u tc tce-load -i wifi.tcz >/dev/null 2>&1
		[ $? -eq 0 ] && echo '<p class="info">[ INFO ] Wifi modules loaded.</p>' || echo '<p class="error">[ ERROR ] Wifi modules load error.</p>'
	fi
fi

if [ "$WIFI" = "off" ]; then
	[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] wifi is off. Removing wifi extensions...</p>'
	sudo sed -i '/firmware-atheros.tcz/d' /mnt/mmcblk0p2/tce/onboot.lst
	sudo sed -i '/firmware-brcmwifi.tcz/d' /mnt/mmcblk0p2/tce/onboot.lst
	sudo sed -i '/firmware-rpi3-wireless.tcz/d' /mnt/mmcblk0p2/tce/onboot.lst
	sudo sed -i '/firmware-ralinkwifi.tcz/d' /mnt/mmcblk0p2/tce/onboot.lst
	sudo sed -i '/firmware-rtlwifi.tcz/d' /mnt/mmcblk0p2/tce/onboot.lst
	sudo sed -i '/wireless/d' /mnt/mmcblk0p2/tce/onboot.lst
	sudo sed -i '/wifi.tcz/d' /mnt/mmcblk0p2/tce/onboot.lst
fi

if [ "$ORIG_RPI3INTWIFI" != "$RPI3INTWIFI" ]; then
	pcp_mount_mmcblk0p1
	if [ "$RPI3INTWIFI" = "off" ]; then
		# Add a blacklist for brcmfmac
		sed -i 's/$/ blacklist=brcmfmac/' $CMDLINETXT 
	else
		sed -i 's/blacklist=brcmfmac//g' $CMDLINETXT
	fi
	pcp_textarea "" "cat $CMDLINETXT" 100
	pcp_umount_mmcblk0p1
	pcp_backup
	pcp_reboot_required
fi

pcp_textarea "" "cat $CONFIGCFG" 150
pcp_textarea "" "cat /mnt/mmcblk0p2/tce/onboot.lst" 150
pcp_textarea "" "cat /mnt/mmcblk0p2/tce/piCorePlayer.dep" 150

pcp_backup

#========================================================================================
# Connect to the wifi
#----------------------------------------------------------------------------------------
if [ "$WIFI" = "on" ]; then
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

echo '</body>'
echo '</html>'