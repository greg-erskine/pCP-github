#!/bin/sh

# Version: 3.5.0 2017-12-30
#	Added enable/disable rpi bluetooth. PH.

# Version: 3.21 2017-05-20
#	Changed to allow booting from USB on RPI3. PH.

# Version: 3.20 2017-03-08
#	Fixed pcp-xxx-functions issues. GE.
#	Changed rpi3 wifi disable to overlay. PH.

# Version: 3.00 2016-07-01 PH
#	Changed name for RPi3 internal wifi firmware extension

. pcp-functions

ORIG_RPI3INTWIFI=$RPI3INTWIFI
ORIG_RPIBLUETOOTH=$RPIBLUETOOTH
REBOOT_REQUIRED=0

pcp_html_head "Write WIFI Settings" "SBP" "20" "wifi.cgi"

pcp_banner
pcp_running_script
pcp_httpd_query_string
pcp_save_to_config

if [ $DEBUG -eq 1 ]; then
	echo '<p class="debug">[ DEBUG ] $WIFI: '$WIFI'<br />'
	echo '                 [ DEBUG ] $SSID: '$SSID'<br />'
	echo '                 [ DEBUG ] $PASSWORD: '$PASSWORD'<br />'
	echo '                 [ DEBUG ] $ENCRYPTION: '$ENCRYPTION'<br />'
	echo '                 [ DEBUG ] $RPI3INTWIFI: '$RPI3INTWIFI'<br />'
	echo '                 [ DEBUG ] $ORIG_RPI3INTWIFI: '$ORIG_RPI3INTWIFI'<br />'
	echo '                 [ DEBUG ] $RPIBLUETOOTH: '$RPIBLUETOOTH'<br />'
	echo '                 [ DEBUG ] $ORIG_RPIBLUETOOTH: '$ORIG_RPIBLUETOOTH'</p>'
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
	if grep -Fxq "wifi.tcz" $ONBOOTLST; then
		[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] Wifi modules already loaded.</p>'
	else
		[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] Loading wifi firmware and modules.</p>'
		# Add wifi related modules back
		sudo fgrep -vxf $ONBOOTLST $TCEMNT/tce/piCorePlayer.dep >> $ONBOOTLST

		sudo -u tc tce-load -i firmware-atheros.tcz >/dev/null 2>&1
		[ $? -eq 0 ] && echo '<p class="info">[ INFO ] Atheros firmware loaded.</p>' || echo '<p class="error">[ ERROR ] Atheros firmware load error.</p>'
		sudo -u tc tce-load -i firmware-brcmwifi.tcz >/dev/null 2>&1
		[ $? -eq 0 ] && echo '<p class="info">[ INFO ] Broadcom USB firmware loaded.</p>' || echo '<p class="error">[ ERROR ] Broadcom USB firmware load error.</p>'
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
	sudo sed -i '/firmware-atheros.tcz/d' $ONBOOTLST
	sudo sed -i '/firmware-brcmwifi.tcz/d' $ONBOOTLST
	sudo sed -i '/firmware-rpi3-wireless.tcz/d' $ONBOOTLST
	sudo sed -i '/firmware-ralinkwifi.tcz/d' $ONBOOTLST
	sudo sed -i '/firmware-rtlwifi.tcz/d' $ONBOOTLST
	sudo sed -i '/wireless/d' $ONBOOTLST
	sudo sed -i '/wifi.tcz/d' $ONBOOTLST
fi

if [ "$ORIG_RPI3INTWIFI" != "$RPI3INTWIFI" ]; then
	pcp_mount_bootpart
	if [ "$RPI3INTWIFI" = "off" ]; then
		echo '<p class="info">[ INFO  ] Disabling rpi internal wifi.</p>'
		echo "dtoverlay=pi3-disable-wifi" >> $CONFIGTXT 
	else
		echo '<p class="info">[ INFO  ] Enabling rpi internal wifi.</p>'
		sed -i '/dtoverlay=pi3-disable-wifi/d' $CONFIGTXT
	fi
	[ $DEBUG -eq 1 ] && pcp_textarea "" "cat $CONFIGTXT" 100
	pcp_umount_bootpart
	REBOOT_REQUIRED=1
fi
if [ "$ORIG_RPIBLUETOOTH" != "$RPIBLUETOOTH" ]; then
	pcp_mount_bootpart
	if [ "$RPIBLUETOOTH" = "off" ]; then
		echo '<p class="info">[ INFO  ] Disabling rpi internal bluetooth.</p>'
		echo "dtoverlay=pi3-disable-bt" >> $CONFIGTXT 
	else
		echo '<p class="info">[ INFO  ] Enabling rpi internal bluetooth.</p>'
		sed -i '/dtoverlay=pi3-disable-bt/d' $CONFIGTXT
	fi
	[ $DEBUG -eq 1 ] && pcp_textarea "" "cat $CONFIGTXT" 100
	pcp_umount_bootpart
	REBOOT_REQUIRED=1
fi

pcp_textarea "" "cat $CONFIGCFG" 150
pcp_textarea "" "cat $ONBOOTLST" 150
pcp_textarea "" "cat $TCEMNT/tce/piCorePlayer.dep" 150

pcp_backup
[ $REBOOT_REQUIRED -eq 1 ] && pcp_reboot_required

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