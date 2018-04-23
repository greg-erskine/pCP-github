#!/bin/sh
# Wifi diagnostics script

# Version: 4.0.0 2018-04-21
#	Fixed pcp_pastebin_button. GE.

# Version: 3.5.0 2018-03-20
#	Added support for RPi3B+. GE.
#	lsusb is a standard command, no need for extension. GE.

# Version: 3.21 2017-05-20
#	Changed to allow booting from USB on RPi3. PH.

# Version: 3.20 2017-03-08
#	Fixed pcp-xxx-functions issues. GE.

# Version: 3.10 2017-01-06
#	Changed to using pcp_log_header. GE.
#	Changed to using pcp_green_tick, pcp_red_cross. GE.
#	Added wpa_supplicant.conf. GE.
#	Added wifi_wpadrv. GE.
#	Added ping tests. GE.

# Version: 0.01 2015-08-20
#	Original. GE.

. pcp-functions
. pcp-rpi-functions
. pcp-wifi-functions
. pcp-pastebin-functions

MAC=$(echo $(pcp_wlan0_mac_address) | sed 's/://g')
LOG="${LOGDIR}/pcp_diagwifi_${MAC:6}.log"

pcp_html_head "Wifi Diagnostics" "GE"

pcp_banner
pcp_diagnostics
pcp_running_script

#========================================================================================
# Routine to display USB wifi adapters found during boot process.
# Some of the standard RPi USB devices are jumped to focus on wifi device.
# Update: Routine also finds built-in wifi devices.
#----------------------------------------------------------------------------------------
pcp_diag_wifi_dmesg() {
	echo "dmesg" >>$LOG
	echo ========================================================================================= >>$LOG
	dmesg | sed -n '{
		/New USB device found, idVendor=1d6b/n
		/New USB device found, idVendor=0424/n
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
		/brcmfmac: brcmf_fw_map_chip_to_name:/n
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
	echo >>$LOG
}

#========================================================================================
# Routine to generate a list of wifi related modules. Some of the standard RPi modules
# have been filtered to focus on wifi modules.
#----------------------------------------------------------------------------------------
pcp_diag_wifi_lsmod() {
	echo "lsmod" >>$LOG
	echo ========================================================================================= >>$LOG
	lsmod | grep -vE "^snd|^ctr|^ccm|^arc4|^uio|^i2c|^crc|^spi|^bcm2|^evdev|^regmap|^squashfs|^zram|^zsmalloc|^lz4" | tee -a $LOG
	echo >>$LOG
}

#========================================================================================
# Routine to report on USB devices. Some of the standard RPi USB devices have been
# filtered to focus on wifi USB devices.
#----------------------------------------------------------------------------------------
pcp_diag_wifi_lsusb() {
	echo "wifi usb report (lsusb)" >>$LOG
	echo ========================================================================================= >>$LOG
	lsusb | grep -vE "ID 0424|ID 1d6b" | tee -a $LOG
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
# Routine to display wifi-wpadrv.
#----------------------------------------------------------------------------------------
pcp_diag_wifi_wpadrv() {
	echo "Wifi wpa driver (wifi-wpadrv)" >>$LOG
	echo ========================================================================================= >>$LOG
	cat /etc/sysconfig/wifi-wpadrv | tee -a $LOG
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
# Routines to ping localhost and LMS.
#----------------------------------------------------------------------------------------
pcp_diag_wifi_ping_local() {
	echo "Ping local test" >>$LOG
	echo ========================================================================================= >>$LOG
	ping -c6 127.0.0.1 | tee -a $LOG
	echo >>$LOG
}

pcp_diag_wifi_ping_lms() {
	echo "Ping LMS test" >>$LOG
	echo ========================================================================================= >>$LOG
	ping -c20 $(pcp_lmsip) | tee -a $LOG
	echo >>$LOG
}

#========================================================================================
# Routines to get pCP variables or display "None" if not set.
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

#========================================================================================
# Create the log file. Start with some basic information.
#----------------------------------------------------------------------------------------
pcp_wifi_read_wpa_supplicant

#WPA_SSID WPA_PASSWORD WPA_PW WPA_PSK WPA_PASSPHRASE KEY_MGMT WPA_ENCRYPTION WPA_HIDDENSSID

pcp_log_header $0
echo ========================================================================================= >>$LOG
echo "Wifi:        "$WIFI >>$LOG
echo "SSID:        "$WPA_SSID >>$LOG
echo "Password:    "$WPA_PASSWORD >>$LOG
echo "Passphrase:  "$WPA_PASSPHRASE >>$LOG
echo "Security:    "$WPA_ENCRYPTION >>$LOG
echo "MAC address: "$(pcp_diag_wifi_wlan0_mac_address) >>$LOG
echo "Uptime:      "$(pcp_uptime_days) >>$LOG
echo ========================================================================================= >>$LOG
echo >>$LOG

#========================================================================================
# Raspberry Pi
#----------------------------------------------------------------------------------------
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
echo '              <td class="column150">'
echo '                <p>Wifi</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>'$WIFI'</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p></p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p></p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>Wifi MAC:</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>'$(pcp_diag_wifi_wlan0_mac_address)'</p>'
echo '              </td>'
echo '            </tr>'
#----------------------------------SSID / Wifi IP----------------------------------------
pcp_toggle_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td class="column150">'
echo '                <p>SSID:</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>'$WPA_SSID'</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p></p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p></p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>Wifi IP:</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>'$(pcp_diag_wifi_wlan0_ip)'</p>'
echo '              </td>'
echo '            </tr>'
#----------------------------------Password / Security-----------------------------------
pcp_toggle_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td class="column150">'
echo '                <p>Password:</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>'$WPA_PASSWORD'</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p></p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p></p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>Security:</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>'$WPA_ENCRYPTION'</p>'
echo '              </td>'
echo '            </tr>'
#----------------------------------Passphrase--------------------------------------------
if [ $MODE -ge $MODE_DEVELOPER ]; then
	pcp_toggle_row_shade
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150">'
	echo '                <p>Passphrase:</p>'
	echo '              </td>'
	echo '              <td colspan="5">'
	echo '                <p>'$WPA_PASSPHRASE'</p>'
	echo '              </td>'
	echo '            </tr>'
fi
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
echo '              <td class="column150">'
echo '                <p>Uptime:</p>'
echo '              </td>'
echo '              <td class="column300">'
echo '                <p>'$(pcp_uptime_days)'</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p></p>'
echo '              </td>'
echo '              <td class="column300">'
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
echo '                <textarea class="inform" rows="6">'
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
echo '                <textarea class="inform" rows="3">'
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
echo '                <textarea class="inform" rows="10">'
                        pcp_diag_wifi_wpa_suplicant
echo '                </textarea>'
echo '              </td>'
echo '            </tr>'
#------------------------------------/etc/sysconfig/wifi-wpadrv--------------------------
pcp_start_row_shade
pcp_toggle_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td>'
echo '                <p><b>/etc/sysconfig/wifi-wpadrv:</b></p>'
echo '              </td>'
echo '            </tr>'
pcp_toggle_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td>'
echo '                <textarea class="inform" rows="2">'
                        pcp_diag_wifi_wpadrv
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
echo '                <textarea class="inform" rows="10">'
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
echo '                <textarea class="inform" rows="10">'
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
                        pcp_textarea_inform "none" "pcp_wifi_available_networks" 110
echo '                </td>'
echo '              </tr>'
echo '            </table>'
echo '          </fieldset>'
echo '        </div>'
#----------------------------------------------------------------------------------------

#------------------------------------Ping tests------------------------------------------
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
#----------------------------------------------------------------------------------------
echo '            </table>'
echo '          </fieldset>'
echo '        </div>'
#----------------------------------------------------------------------------------------
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'

[ $MODE -ge $MODE_DEVELOPER ] && pcp_pastebin_button "wifi"

pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'