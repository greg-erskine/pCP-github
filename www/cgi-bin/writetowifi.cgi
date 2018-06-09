#!/bin/sh

# Version: 4.0.0 2018-06-09

. pcp-functions

ORIG_RPI3INTWIFI=$RPI3INTWIFI
ORIG_RPIBLUETOOTH=$RPIBLUETOOTH
REBOOT_REQUIRED=0

pcp_html_head "Write WIFI Settings" "SBP"

pcp_banner
pcp_running_script
pcp_httpd_query_string

if [ $DEBUG -eq 1 ]; then
	pcp_table_textarea_top "Debug" "" "40"
	echo '[ DEBUG ] $RPI3INTWIFI: '$RPI3INTWIFI
	echo '[ DEBUG ] $ORIG_RPI3INTWIFI: '$ORIG_RPI3INTWIFI
	echo '[ DEBUG ] $RPIBLUETOOTH: '$RPIBLUETOOTH
	echo '[ DEBUG ] $ORIG_RPIBLUETOOTH: '$ORIG_RPIBLUETOOTH
	pcp_table_textarea_end
fi

if [ "$ORIG_RPI3INTWIFI" != "$RPI3INTWIFI" -o "$ORIG_RPIBLUETOOTH" != "$RPIBLUETOOTH" ]; then
	pcp_table_textarea_top "Setting Boot Configuration" "" "100"
	pcp_mount_bootpart_nohtml
	if [ "$ORIG_RPI3INTWIFI" != "$RPI3INTWIFI" ]; then
		if [ "$RPI3INTWIFI" = "off" ]; then
			echo '[ INFO  ] Disabling rpi internal wifi.'
			echo "dtoverlay=pi3-disable-wifi" >> $CONFIGTXT 
		else
			echo '[ INFO  ] Enabling rpi internal wifi.'
			sed -i '/dtoverlay=pi3-disable-wifi/d' $CONFIGTXT
		fi
	fi
	if [ "$ORIG_RPIBLUETOOTH" != "$RPIBLUETOOTH" ]; then
		if [ "$RPIBLUETOOTH" = "off" ]; then
			echo '[ INFO  ] Disabling rpi internal bluetooth.'
			echo "dtoverlay=pi3-disable-bt" >> $CONFIGTXT 
		else
			echo '[ INFO  ] Enabling rpi internal bluetooth.'
			sed -i '/dtoverlay=pi3-disable-bt/d' $CONFIGTXT
		fi
	fi

	if [ $DEBUG -eq 1 ]; then
		echo "Current boot config.cfg"
		cat "$CONFIGCFG"
	fi
	pcp_umount_bootpart_nohtml
	pcp_save_to_config
	pcp_backup "nohtml"
	pcp_table_textarea_end
	REBOOT_REQUIRED=1
fi

[ $REBOOT_REQUIRED -eq 1 ] && pcp_reboot_required

[ $DEBUG -eq 1 ] && pcp_go_back_button || pcp_redirect_button "Wifi Page" "wifi.cgi" 10

echo '</body>'
echo '</html>'