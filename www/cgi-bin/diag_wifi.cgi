#!/bin/sh
# Wifi diagnostics script

# Version: 7.0.0 2020-05-11

. pcp-functions
. pcp-rpi-functions
. pcp-wifi-functions
. pcp-pastebin-functions

MAC=$(echo $(pcp_wlan0_mac_address) | sed 's/://g')
LOG="${LOGDIR}/pcp_diagwifi_${MAC:6}.log"
WPACONFIGFILE=$WPASUPPLICANTCONF

pcp_html_head "Wifi Diagnostics" "GE"

pcp_navbar

[ $(pcp_wifi_using_wifi) -eq 0 ] || pcp_wifi_not_using_wifi

#========================================================================================
# Routine to display:
#  - USB wifi adapters found during boot process.
#  - built-in wifi adapters.
#  - other wifi relevant info.
#
# Note:
#  - Some of the standard RPi USB devices are jumped to focus on wifi device.
#  - p = print, n = next, a = append
#----------------------------------------------------------------------------------------
pcp_diag_wifi_dmesg() {
	echo "dmesg" >>$LOG
	echo ========================================================================================= >>$LOG
	dmesg | sed -n '{
		/New USB device found, idVendor=1d6b/ n
		/New USB device found, idVendor=0424/ n
		/New USB device found, idVendor=/{
			p
			n
			p
			n
			p
			n
			p
			n
			p
			a\
.
		}
	}' | tee -a $LOG

	dmesg | sed -n '{
		/brcmfmac: brcmf_fw_map_chip_to_name:/ n
		/brcmfmac: brcmf_c_preinit_dcmds:/{
			p
			n
			p
			n
			p
			a\
.
		}
	}' | tee -a $LOG

	dmesg | sed -n '{
		/usbcore: registered new interface driver usbfs/ n
		/usbcore: registered new interface driver hub/ n
		/usbcore: registered new device driver usb/ n
		/usbcore: registered new interface driver lan78xx/ n
		/usbcore: registered new interface driver smsc95xx/ n
		/usbcore: registered new interface driver usb-storage/ n
		/usbcore: registered new interface driver usbhid/ n
		/usbcore:/{
			p
			a\
.
		}
	}' | tee -a $LOG

	dmesg | grep "cfg80211:" | tee -a $LOG
	echo "." | tee -a $LOG

	echo >>$LOG
}

#========================================================================================
# Routine to generate a list of wifi related modules. Some of the standard RPi modules
# have been filtered to focus on wifi modules.
#----------------------------------------------------------------------------------------
pcp_diag_wifi_lsmod() {
	echo "lsmod" >>$LOG
	echo ========================================================================================= >>$LOG
	lsmod | grep -vE "^snd|^ctr|^ccm|^arc4|^uio|^i2c|^crc|^spi|^bcm2|^evdev|^regmap|^squashfs|^zram|^zsmalloc|^lz4|^fixed" | tee -a $LOG
	echo >>$LOG
}

#========================================================================================
# Routine to report on wifi USB adapters. Some of the standard RPi USB devices have been
# filtered to focus on wifi USB adapters.
#----------------------------------------------------------------------------------------
pcp_diag_wifi_lsusb() {
	echo "wifi usb report (lsusb)" >>$LOG
	echo ========================================================================================= >>$LOG
	USB=$(lsusb | grep -vE "ID 0424|ID 1d6b")
	if [ "$USB" = "" ]; then
		echo "None found." | tee -a $LOG
	else
		lsusb | grep -vE "ID 0424|ID 1d6b" | tee -a $LOG
	fi
	echo >>$LOG
}

#========================================================================================
# Routine to display wpa_supplicant.conf.
#----------------------------------------------------------------------------------------
pcp_diag_wifi_wpa_suplicant() {
	echo "wpa supplicant configuration (wpa_supplicant.conf)" >>$LOG
	echo ========================================================================================= >>$LOG
	cat $WPASUPPLICANTCONF | tee -a $LOG
	echo >>$LOG
}

#========================================================================================
# Routine to display onboot.lst.
#----------------------------------------------------------------------------------------
pcp_diag_wifi_onbootlst() {
	echo "Extensions in onboot.lst (onboot.lst)" >>$LOG
	echo ========================================================================================= >>$LOG
	cat $ONBOOTLST | tee -a $LOG
	echo >>$LOG
}

#========================================================================================
# Routine to display wifi extensions installed.
#----------------------------------------------------------------------------------------
pcp_diag_wifi_extensions_installed() {
	echo "Wifi extensions installed" >>$LOG
	echo ========================================================================================= >>$LOG
	pcp_wifi_all_extensions_installed "text" | tee -a $LOG
	echo >>$LOG
}

#========================================================================================
# Routine to report on the wifi interface using the wireless specific iwconfig tool.
#----------------------------------------------------------------------------------------
pcp_diag_wifi_iwconfig() {
	echo "iwconfig" >>$LOG
	echo ========================================================================================= >>$LOG
	iwconfig wlan0 | tee -a $LOG
	echo >>$LOG
}

#========================================================================================
# Routine to report on the wifi interface using the generic interface ifconfig tool.
#----------------------------------------------------------------------------------------
pcp_diag_wifi_ifconfig() {
	echo "ifconfig" >>$LOG
	echo ========================================================================================= >>$LOG
	ifconfig wlan0 | tee -a $LOG
	echo >>$LOG
}

#========================================================================================
# Routine to get wireless statistics from specific nodes.
#----------------------------------------------------------------------------------------
pcp_diag_wifi_iwlist() {
	echo "iwlist" >>$LOG
	echo ========================================================================================= >>$LOG
	iwlist wlan0 scan | tee -a $LOG
	echo >>$LOG
}

#========================================================================================
# Routine to get available wifi networks.
#----------------------------------------------------------------------------------------
pcp_diag_wifi_available_networks() {
	echo "Available wifi networks" >>$LOG
	echo ========================================================================================= >>$LOG
	pcp_wifi_available_networks | tee -a $LOG
	echo >>$LOG
}

#========================================================================================
# Routines to ping LMS.
#----------------------------------------------------------------------------------------
pcp_diag_wifi_ping_lms() {
	echo "Ping LMS test" >>$LOG
	echo ========================================================================================= >>$LOG
	ping -c20 -I wlan0 $(pcp_lmsip) | tee -a $LOG
	echo >>$LOG
}

#========================================================================================
# Routines to get pCP variables or display "None/no" if not set.
#----------------------------------------------------------------------------------------
pcp_diag_wifi_wlan0_ip() {
	RESULT=$(pcp_wlan0_ip)
	[ x"" = x"$RESULT" ] && echo "None" || echo $RESULT
}

pcp_diag_wifi_wlan0_mac_address() {
	RESULT=$(pcp_wlan0_mac_address)
	[ x"" = x"$RESULT" ] && echo "None" || echo $RESULT
}

pcp_diag_wifi_password() {
	[ x"" = x"$PASSWORD" ] && echo "None" || echo $PASSWORD
}

pcp_diag_wifi_hiddenssid() {
	[ x"" = x"$WPA_HIDDENSSID" ] && echo "no" || echo $WPA_HIDDENSSID
}

#========================================================================================
# Create the log file. Start with some basic information.
#----------------------------------------------------------------------------------------
pcp_wifi_read_wpa_supplicant "none"

pcp_log_header $0
echo ========================================================================================= >>$LOG
echo "Wifi:        "$WIFI >>$LOG
echo "SSID:        "$WPA_SSID >>$LOG
echo "Password:    "$WPA_PASSWORD >>$LOG
echo "Passphrase:  "$WPA_PASSPHRASE >>$LOG
echo "Security:    "$WPA_ENCRYPTION >>$LOG
echo "Country:     "$WPA_COUNTRY >>$LOG
echo "Hidden SSID: "$(pcp_diag_wifi_hiddenssid) >>$LOG
echo "MAC address: "$(pcp_diag_wifi_wlan0_mac_address) >>$LOG
echo "Uptime:      "$(pcp_uptime_days) >>$LOG
echo ========================================================================================= >>$LOG
echo >>$LOG

#========================================================================================
# Raspberry Pi
#----------------------------------------------------------------------------------------
echo '<hr>'
pcp_heading5 "Wifi diagnostics"

#----------------------------------Wifi / Wifi MAC---------------------------------------
echo '            <div class="row">'
echo '              <div class="col">'
echo '                <p>Wifi</p>'
echo '              </div>'
echo '              <div class="col">'
echo '                <p>'$WIFI'</p>'
echo '              </div>'
echo '              <div class="col">'
echo '                <p></p>'
echo '              </div>'
echo '              <div class="col">'
echo '                <p></p>'
echo '              </div>'
echo '              <div class="col">'
echo '                <p>Wifi MAC:</p>'
echo '              </div>'
echo '              <div class="col">'
echo '                <p>'$(pcp_diag_wifi_wlan0_mac_address)'</p>'
echo '              </div>'
echo '            </div>'
#----------------------------------SSID / Wifi IP----------------------------------------
echo '            <div class="row">'
echo '              <div class="col">'
echo '                <p>SSID:</p>'
echo '              </div>'
echo '              <div class="col">'
echo '                <p>'$WPA_SSID'</p>'
echo '              </div>'
echo '              <div class="col">'
echo '                <p>Wifi IP:</p>'
echo '              </div>'
echo '              <div class="col">'
echo '                <p>'$(pcp_diag_wifi_wlan0_ip)'</p>'
echo '              </div>'
echo '            </div>'
#----------------------------------Password / Security-----------------------------------
echo '            <div class="row">'
echo '              <div class="col">'
echo '                <p>Password:</p>'
echo '              </div>'
echo '              <div class="col">'
echo '                <p>'$WPA_PASSWORD'</p>'
echo '              </div>'
echo '              <div class="col">'
echo '                <p>Security:</p>'
echo '              </div>'
echo '              <div class="col">'
echo '                <p>'$WPA_ENCRYPTION'</p>'
echo '              </div>'
echo '            </div>'
#----------------------------------Passphrase--------------------------------------------
echo '            <div class="row">'
echo '              <div class="col">'
echo '                <p>Passphrase:</p>'
echo '              </div>'
echo '              <div class="col">'
echo '                <p>'$WPA_PASSPHRASE'</p>'
echo '              </div>'
echo '            </div>'
#----------------------------------Country/Hidden SSID-------------------------------------------
echo '            <div class="row">'
echo '              <div class="col">'
echo '                <p>Country:</p>'
echo '              </div>'
echo '              <div class="col">'
echo '                <p>'$WPA_COUNTRY'</p>'
echo '              </div>'
echo '              <div class="col">'
echo '                <p>Hidden SSID:</p>'
echo '              </div>'
echo '              <div class="col">'
echo '                <p>'$(pcp_diag_wifi_hiddenssid)'</p>'
echo '              </div>'
echo '            </div>'
#----------------------------------------------------------------------------------------

#----------------------------------Uptime------------------------------------------------
if [ $(pcp_uptime_seconds) -lt 86400 ]; then
	pcp_green_tick "No reboot required."
else
	pcp_red_cross "Reboot recommended."
fi

echo '  <div class="row">'
echo '    <div class="col">'
echo '      <p>Uptime:</p>'
echo '    </div>'
echo '    <div class="col">'
echo '      <p>'$(pcp_uptime_days)'</p>'
echo '    </div>'
echo '    <div class="col">'
echo '      <p><span class="'$CLASS'">'$INDICATOR'</span>&nbsp;&nbsp;'$STATUS'</p>'
echo '    </div>'
echo '  </div>'
#----------------------------------------------------------------------------------------
pcp_textarea "dmesg:" "pcp_diag_wifi_dmesg" "12"

pcp_textarea "Loaded modules:" "pcp_diag_wifi_lsmod" "11"

pcp_textarea "lsusb results:" "pcp_diag_wifi_lsusb" "2"

pcp_textarea "/etc/wpa_supplicant.conf:" "pcp_diag_wifi_wpa_suplicant" "14"

pcp_textarea "${ONBOOTLST}:" "pcp_diag_wifi_onbootlst" "10"

pcp_textarea "wifi extensions installed:" "pcp_diag_wifi_extensions_installed" "9"

pcp_textarea "iwconfig results:" "pcp_diag_wifi_iwconfig" "11"

pcp_textarea "ifconfig results:" "pcp_diag_wifi_ifconfig" "9"

pcp_textarea "iwlist results:" "pcp_diag_wifi_iwlist" "10"

pcp_textarea "Available wifi networks" "pcp_wifi_available_networks" 15

pcp_textarea "ping LMS results:" "pcp_diag_wifi_ping_lms" "25"

echo '  <div class="row">'
echo '    <ul>'
echo '      <li>You need to learn what is normal for your network.</li>'
echo '      <li>Check the ping time is consistent and only a few ms.</li>'
echo '      <li>Check for 0% packet loss.</li>'
echo '    </ul>'
echo '  </div>'
#----------------------------------------------------------------------------------------

pcp_pastebin_button "wifi"

pcp_html_end
