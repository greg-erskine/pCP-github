#!/bin/sh
# Wifi diagnostics script

# Version: 6.0.0 2019-10-29

. pcp-functions
. pcp-rpi-functions
. pcp-wifi-functions
. pcp-pastebin-functions

MAC=$(echo $(pcp_wlan0_mac_address) | sed 's/://g')
LOG="${LOGDIR}/pcp_diagwifi_${MAC:6}.log"
WPACONFIGFILE=$WPASUPPLICANTCONF

pcp_html_head "Wifi Diagnostics" "GE"

pcp_banner
pcp_diagnostics
pcp_running_script

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
# Table row padding.
#----------------------------------------------------------------------------------------
pcp_padding() {
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td>'
	echo '                  <p></p>'
	echo '                </td>'
	echo '              </tr>'
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
COL="column120"
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Wifi diagnostics</legend>'
echo '          <table class="bggrey percent100">'
#----------------------------------Wifi / Wifi MAC---------------------------------------
pcp_start_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td class="'$COL'">'
echo '                <p>Wifi</p>'
echo '              </td>'
echo '              <td class="'$COL'">'
echo '                <p>'$WIFI'</p>'
echo '              </td>'
echo '              <td class="'$COL'">'
echo '                <p></p>'
echo '              </td>'
echo '              <td class="'$COL'">'
echo '                <p></p>'
echo '              </td>'
echo '              <td class="'$COL'">'
echo '                <p>Wifi MAC:</p>'
echo '              </td>'
echo '              <td class="'$COL'">'
echo '                <p>'$(pcp_diag_wifi_wlan0_mac_address)'</p>'
echo '              </td>'
echo '            </tr>'
#----------------------------------SSID / Wifi IP----------------------------------------
pcp_toggle_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td class="'$COL'">'
echo '                <p>SSID:</p>'
echo '              </td>'
echo '              <td class="'$COL'">'
echo '                <p>'$WPA_SSID'</p>'
echo '              </td>'
echo '              <td class="'$COL'">'
echo '                <p></p>'
echo '              </td>'
echo '              <td class="'$COL'">'
echo '                <p></p>'
echo '              </td>'
echo '              <td class="'$COL'">'
echo '                <p>Wifi IP:</p>'
echo '              </td>'
echo '              <td class="'$COL'">'
echo '                <p>'$(pcp_diag_wifi_wlan0_ip)'</p>'
echo '              </td>'
echo '            </tr>'
#----------------------------------Password / Security-----------------------------------
pcp_toggle_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td class="'$COL'">'
echo '                <p>Password:</p>'
echo '              </td>'
echo '              <td class="'$COL'">'
echo '                <p>'$WPA_PASSWORD'</p>'
echo '              </td>'
echo '              <td class="'$COL'">'
echo '                <p></p>'
echo '              </td>'
echo '              <td class="'$COL'">'
echo '                <p></p>'
echo '              </td>'
echo '              <td class="'$COL'">'
echo '                <p>Security:</p>'
echo '              </td>'
echo '              <td class="'$COL'">'
echo '                <p>'$WPA_ENCRYPTION'</p>'
echo '              </td>'
echo '            </tr>'
#----------------------------------Passphrase--------------------------------------------
pcp_toggle_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td class="'$COL'">'
echo '                <p>Passphrase:</p>'
echo '              </td>'
echo '              <td colspan="5">'
echo '                <p>'$WPA_PASSPHRASE'</p>'
echo '              </td>'
echo '            </tr>'
#----------------------------------Country/Hidden SSID-------------------------------------------
pcp_toggle_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td class="'$COL'">'
echo '                <p>Country:</p>'
echo '              </td>'
echo '              <td class="'$COL'">'
echo '                <p>'$WPA_COUNTRY'</p>'
echo '              </td>'
echo '              <td class="'$COL'">'
echo '                <p></p>'
echo '              </td>'
echo '              <td class="'$COL'">'
echo '                <p></p>'
echo '              </td>'
echo '              <td class="'$COL'">'
echo '                <p>Hidden SSID:</p>'
echo '              </td>'
echo '              <td class="'$COL'">'
echo '                <p>'$(pcp_diag_wifi_hiddenssid)'</p>'
echo '              </td>'
echo '            </tr>'
#----------------------------------------------------------------------------------------
echo '          </table>'
echo '          <table class="bggrey percent100">'
#----------------------------------Uptime------------------------------------------------
if [ $(pcp_uptime_seconds) -lt 86400 ]; then
	pcp_green_tick "No reboot required."
else
	pcp_red_cross "Reboot recommended."
fi

pcp_toggle_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td class="'$COL'">'
echo '                <p>Uptime:</p>'
echo '              </td>'
echo '              <td colspan="2">'
echo '                <p>'$(pcp_uptime_days)'</p>'
echo '              </td>'
echo '              <td class="'$COL'">'
echo '                <p></p>'
echo '              </td>'
echo '              <td colspan="2">'
echo '                <p><span class="'$CLASS'">'$INDICATOR'</span>&nbsp;&nbsp;'$STATUS'</p>'
echo '              </td>'
echo '            </tr>'
#----------------------------------------------------------------------------------------
echo '          </table>'
echo '          <table class="bggrey percent100">'
#------------------------------------dmesg-----------------------------------------------
pcp_start_row_shade
pcp_toggle_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td>'
echo '                <p><b>dmesg:</b></p>'
echo '              </td>'
echo '            </tr>'
pcp_toggle_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td>'
echo '                <textarea class="inform" rows="12">'
                        pcp_diag_wifi_dmesg
echo '                </textarea>'
echo '              </td>'
echo '            </tr>'
#------------------------------------lsmod-----------------------------------------------
pcp_start_row_shade
pcp_toggle_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td>'
echo '                <p><b>Loaded modules:</b></p>'
echo '              </td>'
echo '            </tr>'
pcp_toggle_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td>'
echo '                <textarea class="inform" rows="6">'
                        pcp_diag_wifi_lsmod
echo '                </textarea>'
echo '              </td>'
echo '            </tr>'
#------------------------------------lsusb-----------------------------------------------
pcp_start_row_shade
pcp_toggle_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td>'
echo '                <p><b>lsusb results:</b></p>'
echo '              </td>'
echo '            </tr>'
pcp_toggle_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td>'
echo '                <textarea class="inform" rows="2">'
                        pcp_diag_wifi_lsusb
echo '                </textarea>'
echo '              </td>'
echo '            </tr>'
#------------------------------------wpa_supplicant.conf---------------------------------
pcp_start_row_shade
pcp_toggle_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td>'
echo '                <p><b>/etc/wpa_supplicant.conf:</b></p>'
echo '              </td>'
echo '            </tr>'
pcp_toggle_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td>'
echo '                <textarea class="inform" rows="14">'
                        pcp_diag_wifi_wpa_suplicant
echo '                </textarea>'
echo '              </td>'
echo '            </tr>'
#------------------------------------onboot.lst------------------------------------------
pcp_start_row_shade
pcp_toggle_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td>'
echo '                <p><b>'$ONBOOTLST':</b></p>'
echo '              </td>'
echo '            </tr>'
pcp_toggle_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td>'
echo '                <textarea class="inform" rows="10">'
                        pcp_diag_wifi_onbootlst
echo '                </textarea>'
echo '              </td>'
echo '            </tr>'
#------------------------------------wifi extensions installed---------------------------
pcp_start_row_shade
pcp_toggle_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td>'
echo '                <p><b>wifi extensions installed:</b></p>'
echo '              </td>'
echo '            </tr>'
pcp_toggle_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td>'
echo '                <textarea class="inform" rows="9">'
                        pcp_diag_wifi_extensions_installed
echo '                </textarea>'
echo '              </td>'
echo '            </tr>'
#------------------------------------iwconfig--------------------------------------------
pcp_start_row_shade
pcp_toggle_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td>'
echo '                <p><b>iwconfig results:</b></p>'
echo '              </td>'
echo '            </tr>'
pcp_toggle_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td>'
echo '                <textarea class="inform" rows="11">'
                        pcp_diag_wifi_iwconfig
echo '                </textarea>'
echo '              </td>'
echo '            </tr>'
#------------------------------------ifconfig--------------------------------------------
pcp_start_row_shade
pcp_toggle_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td>'
echo '                <p><b>ifconfig results:</b></p>'
echo '              </td>'
echo '            </tr>'
pcp_toggle_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td>'
echo '                <textarea class="inform" rows="9">'
                        pcp_diag_wifi_ifconfig
echo '                </textarea>'
echo '              </td>'
echo '            </tr>'
#------------------------------------iwlist----------------------------------------------
pcp_start_row_shade
pcp_toggle_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td>'
echo '                <p><b>iwlist results:</b></p>'
echo '              </td>'
echo '            </tr>'
pcp_toggle_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td>'
echo '                <textarea class="inform" rows="10">'
                        pcp_diag_wifi_iwlist
echo '                </textarea>'
echo '              </td>'
echo '            </tr>'
#----------------------------------------------------------------------------------------
echo '          </table>'
echo '        </fieldset>'
#----------------------------------------------------------------------------------------

#------------------------------------Available networks----------------------------------
echo '        <div class="row">'
echo '          <fieldset>'
echo '            <legend>Available wifi networks</legend>'
echo '            <table class="bggrey percent100">'
pcp_start_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td>'
echo '                  <textarea class="inform" rows="10">'
                          pcp_diag_wifi_available_networks
echo '                  </textarea>'
echo '                </td>'
echo '              </tr>'
echo '            </table>'
echo '          </fieldset>'
echo '        </div>'
#----------------------------------------------------------------------------------------

#------------------------------------Ping test-------------------------------------------
echo '        <div class="row">'
echo '          <fieldset>'
echo '            <legend>Ping tests</legend>'
echo '            <table class="bggrey percent100">'
#------------------------------------Ping LMS--------------------------------------------
pcp_start_row_shade
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td>'
echo '                  <p><b>ping LMS results:</b></p>'
echo '                </td>'
echo '              </tr>'
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td>'
echo '                  <textarea class="inform" rows="25">'
                          pcp_diag_wifi_ping_lms
echo '                  </textarea>'
echo '                </td>'
echo '              </tr>'
pcp_padding
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td>'
echo '                  <ul>'
echo '                    <li>You need to learn what is normal for your network.</li>'
echo '                    <li>Check the ping time is consistent and only a few ms.</li>'
echo '                    <li>Check for 0% packet loss.</li>'
echo '                  </ul>'
echo '                </td>'
echo '              </tr>'
#----------------------------------------------------------------------------------------
echo '            </table>'
echo '          </fieldset>'
echo '        </div>'
#----------------------------------------------------------------------------------------
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'

pcp_pastebin_button "wifi"

pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'