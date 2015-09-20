#!/bin/sh
# Wifi diagnostics script

# Version: 0.03 2015-09-20 GE
#	Added evdev to exclude list.

# Version: 0.02 2015-09-08 GE
#	Updated.

# Version: 0.01 2015-08-20 GE
#	Original.

. pcp-rpi-functions
. pcp-functions
pcp_variables

pcp_html_head "Wifi Diagnostics" "GE"

pcp_banner
pcp_diagnostics
pcp_running_script

#========================================================================================
# Routine to display usb devices found during boot process. Some of the standard RPi usb
# devices are jumped to focus on wifi device. 
#----------------------------------------------------------------------------------------
pcp_wifi_diag_dmesg() {
	echo "dmesg" >>$LOG
	echo ========================================================================================= >>$LOG
	dmesg | sed -n '{
		/New USB device found, idVendor=1d6b/n
		/New USB device found, idVendor=0424/n
		/New USB device found, idVendor=/ {
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
	echo >>$LOG
}

#========================================================================================
# Routine to generate a list of wifi related modules. Some of the standard RPi modules
# have been filtered to foucs on wifi modules.
#----------------------------------------------------------------------------------------
pcp_wifi_diag_lsmod() {
	echo "lsmod" >>$LOG
	echo ========================================================================================= >>$LOG
	lsmod | grep -vE "^snd|^ctr|^ccm|^arc4|^uio|^i2c|^crc|^spi|^bcm2|^evdev" | tee -a $LOG
	echo >>$LOG
}

#========================================================================================
# lsusb routine - Check for usbutils.tcz and download and install
#----------------------------------------------------------------------------------------
pcp_install_lsusb() {
	echo '<textarea class="inform" rows="4">'
	which lsusb
	if [ $? = 0 ]; then
		echo 'usbutils.tcz already installed.'
	else
		if [ ! -f /mnt/mmcblk0p2/tce/optional/usbutils.tcz ]; then
			echo 'usbutils.tcz downloading... '
			sudo -u tc tce-load -w usbutils.tcz
			[ $? = 0 ] && echo 'Done.' || echo 'Error.'
		else
			echo 'usbutils.tcz downloaded.'
		fi
		echo 'usbutils.tcz installing... '
		sudo -u tc tce-load -i usbutils.tcz
		[ $? = 0 ] && echo 'Done.' || echo 'Error.'
	fi
	echo '</textarea>'
}

#========================================================================================
# Routine to report on usb devices. Some of the standard RPi usb devices have been
# filtered to focus on wifi usb devices.
#----------------------------------------------------------------------------------------
pcp_wifi_diag_lsusb() {
	echo "wifi usb report (lsusb)" >>$LOG
	echo ========================================================================================= >>$LOG
	lsusb | grep -vE "ID 0424|ID 1d6b" | tee -a $LOG
	echo >>$LOG
}

#========================================================================================
# Routine to report on the wifi interface using the wireless specific iwconfig tool.
#----------------------------------------------------------------------------------------
pcp_wifi_diag_iwconfig() {
	echo "iwconfig" >>$LOG
	echo ========================================================================================= >>$LOG
	iwconfig wlan0 | tee -a $LOG
	echo >>$LOG
}

#========================================================================================
# Routine to report on the wifi interface using the generic interface ifconfig tool. 
#----------------------------------------------------------------------------------------
pcp_wifi_diag_ifconfig() {
	echo "ifconfig" >>$LOG
	echo ========================================================================================= >>$LOG
	ifconfig wlan0 | tee -a $LOG
	echo >>$LOG
}

#========================================================================================
# Routine to get wireless statistics from specific nodes.
#----------------------------------------------------------------------------------------
pcp_wifi_diag_iwlist() {
	echo "iwlist" >>$LOG
	echo ========================================================================================= >>$LOG
	iwlist wlan0 scan | tee -a $LOG
	echo >>$LOG
}

#========================================================================================
# Routine to display wireless access points statistics in a nice format.
#----------------------------------------------------------------------------------------
available_networks() {
	#=========================================================================================
	# (c) Robert Shingledecker 2011-2012 v1.4
	# This routine has been based on code from the piCore script wifi.sh
	# /usr/local/bin/wifi.sh
	#-----------------------------------------------------------------------------------------
	unset WIFI2 && CNT=0
	echo -en "Scanning"
	until [ -n "$WIFI2" ]
	do
		[ $((CNT++)) -gt 5 ] && break || sleep 1
		echo -en "."
		WIFI2="$(iwconfig 2>/dev/null | awk '{if (NR==1)print $1}')"
	done
	if [ -z "$WIFI2" ]; then
		echo -en "\n\nNo wifi devices found!\n\n"
		echo -en "Possible error:\n\n"
		echo -en "1. USB wifi adapter missing - insert adapter.\n"
		echo -en "2. wifi drivers and firmware missing - reboot required."
		echo '</textarea>'
		echo '                </td>'
		echo '              </tr>'
		echo '            </table>'
		echo '          </fieldset>'
		echo '        </div>'
		echo '      </form>'
		echo '    </td>'
		echo '  </tr>'
		echo '</table>'
		pcp_refresh_button
		pcp_footer
		pcp_copyright
		echo '</body>'
		echo '</html>'
		exit
	fi
	ifconfig "$WIFI2" up 2>/dev/null
	(for i in `seq 5`
	do
		iwlist "$WIFI2" scanning
		[ "$?" == 0 ] && break
		sleep 1
	done ) | awk -v wifi=$WIFI2 '
	BEGIN {
		RS="\n"
		FS=":"
		i = 0
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
			split(q,c,"/")
			qual[i] = c[1] * 100 / c[2]
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
		print ""
		print "---------------------------------------------------------------------------------------------"
		print "       SSID                 Quality   Level       Channel      Encryption       Address"
		print "---------------------------------------------------------------------------------------------"
		for (l=1; l<15; l++) {
			++j
			#                     |NO. |SSID |Qual  |Level |Channel   |Encrypt   |Address      
			if ( j <= i ) printf "%2d. %-25s %3d    %7s    %2d %10s   %-3s %-4s  %18s\n", j, sid[j], qual[j], level[j], chan[j], freq[j], enc[j], type[j], addr[j]
		}
		print "---------------------------------------------------------------------------------------------"
	} ' | tee -a $LOG
}
#----------------------------------------------------------------------------------------

#========================================================================================
# Create the log file. Start with some basic information.
#----------------------------------------------------------------------------------------
MAC=$(echo $(pcp_wlan0_mac_address) | sed 's/://g')
LOG="/tmp/pcp_diagwifi_${MAC:6}.log"

echo Report $0 generated on $(date) >$LOG
cat /etc/motd >>$LOG
echo >>$LOG
echo ========================================================================================= >>$LOG
echo "Wifi:        "$WIFI >>$LOG
echo "SSID:        "$SSID >>$LOG
echo "Password:    "$PASSWORD >>$LOG
echo "Security:    "$ENCRYPTION >>$LOG
echo "MAC address: "$(pcp_wlan0_mac_address) >>$LOG
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
#----------------------------------------------------------------------------------------
pcp_start_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td class="column150">'
echo '                <p>Wifi:</p>'
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
echo '                <p>'$(pcp_wlan0_mac_address)'</p>'
echo '              </td>'
echo '            </tr>'
#----------------------------------------------------------------------------------------
pcp_toggle_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td class="column150">'
echo '                <p>SSID:</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>'$SSID'</p>'
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
echo '                <p>'$(pcp_wlan0_ip)'</p>'
echo '              </td>'
echo '            </tr>'
#----------------------------------------------------------------------------------------
pcp_toggle_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td class="column150">'
echo '                <p>Password:</p>'
echo '              </td>'
echo '              <td class="column150">'
echo '                <p>'$PASSWORD'</p>'
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
echo '                <p>'$ENCRYPTION'</p>'
echo '              </td>'
echo '            </tr>'
----------------------------------------------------------------------------------------
if [ $(pcp_uptime_seconds) -lt 86400 ]; then
	IMAGE="green.png"
	STATUS="No reboot required."
else
	IMAGE="red.png"
	STATUS="Reboot recommended."
fi

pcp_toggle_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td class="column300">'
echo '                <p>Your piCorePlayer has not been reboot for:</p>'
echo '              </td>'
echo '              <td class="column300">'
echo '                <p>'$(pcp_uptime_days)'</p>'
echo '              </td>'
echo '              <td class="column300">'
echo '                <p><img src="../images/'$IMAGE'" alt="'$STATUS'">&nbsp;&nbsp;'$STATUS'</p>'
echo '              </td>'
echo '            </tr>'
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
                        pcp_wifi_diag_dmesg
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
                        pcp_wifi_diag_lsmod
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
                      pcp_install_lsusb
echo '              </td>'
echo '            </tr>'
pcp_toggle_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td>'
echo '              </td>'
echo '            </tr>'
pcp_toggle_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td>'
echo '                <textarea class="inform" rows="2">'
                        pcp_wifi_diag_lsusb
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
                        pcp_wifi_diag_iwconfig
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
                        pcp_wifi_diag_ifconfig
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
                        pcp_wifi_diag_iwlist
echo '                </textarea>'
echo '              </td>'
echo '            </tr>'
#----------------------------------------------------------------------------------------
echo '          </table>'
echo '        </fieldset>'
#------------------------------------Available networks----------------------------------
echo '        <form name="wifi_networks" method="get">'
echo '          <div class="row">'
echo '            <fieldset>'
echo '              <legend>Available wifi networks</legend>'
echo '              <table class="bggrey percent100">'
pcp_start_row_shade
echo '                <tr class="'$ROWSHADE'">'
echo '                  <td>'
	                      pcp_textarea_inform "none" "available_networks" 110
echo '                  </td>'
echo '                </tr>'
echo '              </table>'
echo '            </fieldset>'
echo '          </div>'
echo '        </form>'
#----------------------------------------------------------------------------------------
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'

pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'
