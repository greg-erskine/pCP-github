#!/bin/sh

# Version: 7.0.0 2020-05-30

# Title: Temperature monitor
# Description: Temperature using DS18B20

. pcp-functions

unset REBOOT_REQUIRED

pcp_html_head "Show Temperature" "GE"

ACTION="Initial"
pcp_httpd_query_string

FAIL_MSG="ok"
DEBUG=1

#========================================================================================
# Refer: https://datasheets.maximintegrated.com/en/ds/DS18B20.pdf
#
#    DALLAS
#    DS18B20
#
#   1   2   3
#  GND DQ  VDD
#
# 4k7 resistor between DQ and VDD
#
#     RPi            DS18B20
# -----------       ---------
# pin 6 GND    -->  pin 1 GND
# pin 7 GPIO4  -->  pin 2 DQ   <---------|
# pin 1 3V3    -->  pin 3 VDD  <--|4k7|--|
#
#----------------------------------------------------------------------------------------
# Directory
# =========
# /sys/bus/w1/devices/28-xxxxxxxxxxxx/
# /sys/devices/w1_bus_master1/28-xxxxxxxxxxxx/w1_slave
#----------------------------------------------------------------------------------------
W1_MASTER_SLAVE_COUNT=$( cat /sys/devices/w1_bus_master1/w1_master_slave_count )
W1_MASTER_SLAVES=$( cat /sys/devices/w1_bus_master1/w1_master_slaves )

#========================================================================================
# w1_slave
# ========
# 61 01 4b 46 7f ff 0f 10 02 : crc=02 YES
# 61 01 4b 46 7f ff 0f 10 02 t=22062
#----------------------------------------------------------------------------------------
pcp_get_temperature() {
	W1_SLAVE=$1
	if ( echo $W1_SLAVE | grep "crc=.. YES" >/dev/null ); then
		echo $W1_SLAVE | awk -F"t=" '{printf "%4.3f&deg;C (%4.3f&deg;F)",$2/1000,(($2*9)/5000)+32}'
	else
		echo "[ ERROR ] CRC failure. "
	fi
}

#========================================================================================
# This routine writes temperature.sh
#----------------------------------------------------------------------------------------
TEMPERATURE_LOG="/var/log/pcp_temperature.log"
TEMPERATURE_SH="/tmp/pcp_temperature.sh"

pcp_write_termperature_sh() {
cat <<EOF > $TEMPERATURE_SH
#!/bin/sh

W1_MASTER_SLAVE_COUNT=\$( cat /sys/devices/w1_bus_master1/w1_master_slave_count )
W1_MASTER_SLAVES=\$( cat /sys/devices/w1_bus_master1/w1_master_slaves )

pcp_get_temperature() {
	W1_SLAVE=\$1
	if ( echo \$W1_SLAVE | grep "crc=.. YES" >/dev/null ); then
		STRING=\${STRING}\$(echo \$W1_SLAVE | awk -F"t=" '{printf " %4.3f", \$2/1000}')
	fi
}

while true
do
	STRING=\$(date | awk '{print \$4}' | awk -F: '{print \$1, \$2}' | sed 's/ /:/g')

	for W1_MASTER_SLAVE in \$W1_MASTER_SLAVES; do
		pcp_get_temperature "\$(cat /sys/devices/w1_bus_master1/\${W1_MASTER_SLAVE}/w1_slave)"
	done

	echo \$STRING
	sleep 60
done
EOF

	sudo chmod u=rwx,og=rx $TEMPERATURE_SH
}

case "$OPTION" in
	Start)
		pcp_write_termperature_sh
		killall $TEMPERATURE_SH
		$TEMPERATURE_SH >$TEMPERATURE_LOG &
	;;
	Stop)
		killall $TEMPERATURE_SH
	;;
	Clean)
		killall $TEMPERATURE_SH
		rm -f $TEMPERATURE_LOG
		rm -f $TEMPERATURE_SH
	;;
esac

#========================================================================================
# w1-KERNEL.tcz and w1-gpio install
#----------------------------------------------------------------------------------------
pcp_install_w1() {
	pcp_message INFO "Installing packages for 1-wire.'
	pcp_message INFO "This can take a couple of minutes. Please wait...'
	sudo -u tc pcp-load -r $PCP_REPO -wi w1-KERNEL.tcz

	pcp_mount_bootpart_nohtml
	pcp_message INFO "Adding w1-gpio overlay to config.txt...'
	sed -i '/dtoverlay=w1-gpio/d' $CONFIGTXT
	sudo echo "dtoverlay=w1-gpio" >> $CONFIGTXT
	[ $? -eq 0 ] && echo "[ INFO ] dtoverlay=w1-gpio added." || FAIL_MSG="Can not add dtoverlay=w1-gpio."
	pcp_umount_bootpart_nohtml
	REBOOT_REQUIRED=TRUE
}

pcp_uninstall_w1() {
	pcp_message INFO "Removing packages for 1-wire.'
	sudo -u tc tce-audit builddb
	[ "$FAIL_MSG" = "ok" ] && sudo -u tc tce-audit delete w1-KERNEL.tcz

	pcp_mount_bootpart_nohtml
	pcp_message INFO "Removing w1-gpio overlay from config.txt...'
	sed -i '/dtoverlay=w1-gpio/d' $CONFIGTXT
	[ $? -eq 0 ] && echo "[ INFO ] dtoverlay=w1-gpio removed." || FAIL_MSG="Can not remove dtoverlay=w1-gpio."
	pcp_umount_bootpart_nohtml
	REBOOT_REQUIRED=TRUE
}

#========================================================================================
# Main
#----------------------------------------------------------------------------------------
echo '  <div>'
echo '    <div>'
echo '      <div class="row">'
pcp_heading5 "1-wire temperature"

#----------------------------------Install/Uninstall Buttons-----------------------------
if [ "$ACTION" = "Initial" ]; then
	pcp_incr_id
	echo '          <form name="main" action="'$0'" method="get">'

	if ( ! df | grep w1- >/dev/null 2>&1 ); then
		echo '              <div class="row">'
		echo '                <div class="'$COLUMN4_1'">'
		echo '                  <input type="submit" name="ACTION" value="Install" />'
		echo '                </div>'
		echo '                <div>'
		echo '                  <p>Install 1-wire&nbsp;&nbsp;'
		echo '                    <a id="dt'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
		echo '                  </p>'
		echo '                  <div id="dt'$ID'" class="'$COLLAPSE'">'
		echo '                    <p>Install 1-wire from repository.</p>'
		echo '                  </div>'
		echo '                </div>'
		echo '              </div>'
	else
		echo '              <div class="row">'
		echo '                <div class="'$COLUMN4_1'">'
		echo '                  <p>Number of sensors: '$W1_MASTER_SLAVE_COUNT'</p>'
		echo '                </div>'
		echo '              </div>'

		ROW=1
		for W1_MASTER_SLAVE in $W1_MASTER_SLAVES; do
			echo '              <div class="row">'
			echo '                <div class="'$COLUMN4_1'">'
			echo '                  <p>'$ROW'</p>'
			echo '                </div>'
			echo '                <div>'
			echo '                  <p>'$(pcp_get_temperature "$(cat /sys/devices/w1_bus_master1/${W1_MASTER_SLAVE}/w1_slave)")'</p>'
			echo '                </div>'
			echo '              </div>'
			ROW=$((ROW+1))
		done

		pcp_incr_id
		echo '              <div class="row">'
		echo '                <div class="'$COLUMN4_1'">'
		echo '                  <input type="submit" name="ACTION" value="Uninstall">'
		echo '                </div>'
		echo '                <div>'
		echo '                  <p>Uninstall 1-wire&nbsp;&nbsp;'
		echo '                    <a id="dt'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
		echo '                  </p>'
		echo '                  <div id="dt'$ID'" class="'$COLLAPSE'">'
		echo '                    <p>Uninstall 1-wire from '$NAME'.</p>'
		echo '                  </div>'
		echo '                </div>'
		echo '              </div>'
	fi
	echo '          </form>'
fi
#----------------------------------------------------------------------------------------

#---------------------------------------Install------------------------------------------
if [ "$ACTION" = "Install" ]; then
	echo '                  <textarea class="inform" style="height:200px">'
	[ "$FAIL_MSG" = "ok" ] && pcp_install_w1
	echo '                  </textarea>'
fi
#----------------------------------------------------------------------------------------

#---------------------------------------Uninstall----------------------------------------
if [ "$ACTION" = "Uninstall" ]; then
	echo '                  <textarea class="inform" style="height:200px">'
	[ "$FAIL_MSG" = "ok" ] && pcp_uninstall_w1
	echo '                  </textarea>'
fi
#----------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------
echo '      </div>'
echo '    </div>'
echo '  </div>'
#----------------------------------------------------------------------------------------

#--------------------------------Start/Stop/Clean----------------------------------------
echo '  <div>'
echo '    <div>'
echo '      <div class="row">'
pcp_heading5 "Temperature logging options"
echo '          <form name="actions" action="'$0'" method="get">'
echo '              <div>'
echo '                <div>'
echo '                  <input type="submit" name="OPTION" value="Start">'
echo '                  <input type="submit" name="OPTION" value="Stop">'
echo '                  <input type="submit" name="OPTION" value="Clean">'
echo '                </div>'
echo '              </div>'
echo '          </form>'
echo '      </div>'
echo '    </div>'
echo '  </div>'
#----------------------------------------------------------------------------------------

#========================================================================================
# Debug
#----------------------------------------------------------------------------------------
if [ $DEBUG -eq 1 ]; then
	echo '  <div>'
	echo '    <div>'
	echo '      <div class="row">'
	pcp_heading5 "Debug"
	#------------------------------------------------------------------------------------
	echo '            <div class="row">'
	echo '              <div>'
	echo '                <textarea class="inform" style="height:25px">'
	                        echo 'Looking for w1-gpio overlay...'
	                        pcp_mount_bootpart_nohtml >/dev/null 2>&1
	                        if ! cat $CONFIGTXT | grep dtoverlay=w1-gpio; then
	                          pcp_message ERROR "w1-gpio overlay not found.'
	                          FAIL_MSG="w1-gpio overlay not found."
	                        fi
	                        pcp_umount_bootpart_nohtml >/dev/null 2>&1
	echo '                </textarea>'
	echo '              </div>'
	echo '            </div>'
	#------------------------------------------------------------------------------------
	echo '            <div class="row">'
	echo '              <div>'
	echo '                <textarea class="inform" style="height:70px">'
	                        echo 'Looking for wire in dmesg...'
	                        if ! dmesg | grep wire; then
	                          pcp_message ERROR "Nothing found in dmesg.'
	                          FAIL_MSG="Nothing found in dmesg."
	                        fi
	echo '                </textarea>'
	echo '              </div>'
	echo '            </div>'
	#------------------------------------------------------------------------------------
	echo '            <div class="row">'
	echo '              <div>'
	echo '                <textarea class="inform" style="height:70px">'
	                        echo 'Looking for errors in dmesg...'
	                        if ! dmesg | grep w1_slave_driver; then
	                          pcp_message ERROR "Nothing found in dmesg.'
	                          FAIL_MSG="No errors found in dmesg."
	                        fi
	echo '                </textarea>'
	echo '              </div>'
	echo '            </div>'
	#------------------------------------------------------------------------------------
	echo '            <div class="row">'
	echo '              <div>'
	echo '                <textarea class="inform" style="height:50px">'
	                        echo 'Looking for w1 modules...'
	                        if ! lsmod | grep w1; then
	                          pcp_message ERROR "No w1 modules found.'
	                          FAIL_MSG="No w1 modules found."
	                        fi
	echo '                </textarea>'
	echo '              </div>'
	echo '            </div>'
	#------------------------------------------------------------------------------------
	echo '            <div class="row">'
	echo '              <div>'
	echo '                <textarea class="inform" style="height:50px">'
	                        echo 'Looking for devices...'
	                        if ! ls /sys/bus/w1/devices/; then
	                          pcp_message ERROR "No devices found.'
	                          FAIL_MSG="No devices found."
	                        fi
	echo '                </textarea>'
	echo '              </div>'
	echo '            </div>'
	#------------------------------------------------------------------------------------
	echo '            <div class="row">'
	echo '              <div>'
	echo '                <textarea class="inform" style="height:280px">'
	                        gpio readall
	echo '                </textarea>'
	echo '              </div>'
	echo '            </div>'
	#------------------------------------------------------------------------------------
	echo '      </div>'
	echo '    </div>'
	echo '  </div>'
fi

#========================================================================================
# Generate status message and finish html page
#----------------------------------------------------------------------------------------
echo '  <div>'
echo '    <div>'
echo '      <div class="row">'
pcp_heading5 "Status"
echo '            <div class="row">'
echo '              <div>'
echo '                <p>'$FAIL_MSG'</p>'
echo '              </div>'
echo '            </div>'
echo '      </div>'
echo '    </div>'
echo '  </div>'

pcp_footer
pcp_copyright
pcp_remove_query_string

echo '</body>'
echo '</html>'
[ $REBOOT_REQUIRED ] && pcp_reboot_required
exit
