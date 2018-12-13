#!/bin/sh

# Version: 4.2.0 2018-12-13

# Title: Temperature monitor
# Description: Temperature using DS18B20

. pcp-functions

unset REBOOT_REQUIRED

pcp_html_head "Show Temperature" "GE"

pcp_banner
pcp_running_script
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
# /sys/bus/w1/devices/28-00000xxxxxxx/
# /sys/devices/w1_bus_master1/28-00000xxxxxxx/w1_slave
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
		echo $W1_SLAVE | awk -F"t=" '{printf "%s&deg;C (%s&deg;F)",$2/1000,(($2*9)/5000)+32}'
	else
		echo "[ ERROR ] CRC failure. "
	fi
}

pcp_padding() {
	pcp_toggle_row_shade
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td>'
	echo '              </td>'
	echo '            </tr>'
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
		STRING=\${STRING}\$(echo \$W1_SLAVE | awk -F"t=" '{printf " %s", \$2/1000}')
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
	echo '[ INFO ] Installing packages for 1-wire.'
	echo '[ INFO ] This can take a couple of minutes. Please wait...'
	sudo -u tc pcp-load -r $PCP_REPO -wi w1-KERNEL.tcz

	pcp_mount_bootpart_nohtml
	echo '[ INFO ] Adding w1-gpio overlay to config.txt...'
	sed -i '/dtoverlay=w1-gpio/d' $CONFIGTXT
	sudo echo "dtoverlay=w1-gpio" >> $CONFIGTXT
	[ $? -eq 0 ] && echo "[ INFO ] dtoverlay=w1-gpio added." || FAIL_MSG="Can not add dtoverlay=w1-gpio."
	pcp_umount_bootpart_nohtml
	REBOOT_REQUIRED=TRUE
}

pcp_uninstall_w1() {
	echo '[ INFO ] Removing packages for 1-wire.'
	sudo -u tc tce-audit builddb
	[ "$FAIL_MSG" = "ok" ] && sudo -u tc tce-audit delete w1-KERNEL.tcz

	pcp_mount_bootpart_nohtml
	echo '[ INFO ] Removing w1-gpio overlay from config.txt...'
	sed -i '/dtoverlay=w1-gpio/d' $CONFIGTXT
	[ $? -eq 0 ] && echo "[ INFO ] dtoverlay=w1-gpio removed." || FAIL_MSG="Can not remove dtoverlay=w1-gpio."
	pcp_umount_bootpart_nohtml
	REBOOT_REQUIRED=TRUE
}

#========================================================================================
# Main
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>1-wire temperature</legend>'

#----------------------------------Install/Uninstall Buttons-----------------------------
if [ "$ACTION" = "Initial" ]; then
	pcp_incr_id
	pcp_start_row_shade
	echo '          <form name="main" action="'$0'" method="get">'
	echo '            <table class="bggrey percent100">'

	if ( ! df | grep w1- >/dev/null 2>&1 ); then
		echo '              <tr class="'$ROWSHADE'">'
		echo '                <td class="column150 center">'
		echo '                  <input type="submit" name="ACTION" value="Install" />'
		echo '                </td>'
		echo '                <td>'
		echo '                  <p>Install 1-wire&nbsp;&nbsp;'
		echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
		echo '                  </p>'
		echo '                  <div id="'$ID'" class="less">'
		echo '                    <p>Install 1-wire from repository.</p>'
		echo '                  </div>'
		echo '                </td>'
		echo '              </tr>'
	else
		echo '              <tr class="'$ROWSHADE'">'
		echo '                <td>'
		echo '                  <p>Number of sensors: '$W1_MASTER_SLAVE_COUNT'</p>'
		echo '                </td>'
		echo '              </tr>'

		ROW=1
		for W1_MASTER_SLAVE in $W1_MASTER_SLAVES; do
			pcp_toggle_row_shade
			echo '              <tr class="'$ROWSHADE'">'
			echo '                <td class="column50 center">'
			echo '                  <p>'$ROW'</p>'
			echo '                </td>'
			echo '                <td>'
			echo '                  <p>'$(pcp_get_temperature "$(cat /sys/devices/w1_bus_master1/${W1_MASTER_SLAVE}/w1_slave)")'</p>'
			echo '                </td>'
			echo '              </tr>'
			ROW=$((ROW+1))
		done

		pcp_incr_id
		pcp_toggle_row_shade
		echo '              <tr class="'$ROWSHADE'">'
		echo '                <td class="column150 center">'
		echo '                  <input type="submit" name="ACTION" value="Uninstall">'
		echo '                </td>'
		echo '                <td>'
		echo '                  <p>Uninstall 1-wire&nbsp;&nbsp;'
		echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
		echo '                  </p>'
		echo '                  <div id="'$ID'" class="less">'
		echo '                    <p>Uninstall 1-wire from '$NAME'.</p>'
		echo '                  </div>'
		echo '                </td>'
		echo '              </tr>'
	fi
	echo '            </table>'
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
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------

#--------------------------------Start/Stop/Clean----------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Temperature logging options</legend>'
echo '          <form name="actions" action="'$0'" method="get">'
echo '            <table class="bggrey percent100">'
echo '              <tr>'
echo '                <td>'
echo '                  <input type="submit" name="OPTION" value="Start">'
echo '                  <input type="submit" name="OPTION" value="Stop">'
echo '                  <input type="submit" name="OPTION" value="Clean">'
echo '                </td>'
echo '              </tr>'
echo '            </table>'
echo '          </form>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------

#========================================================================================
# Debug
#----------------------------------------------------------------------------------------
if [ $DEBUG = 1 ]; then
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Debug</legend>'
	echo '          <table class="bggrey percent100">'
	#------------------------------------------------------------------------------------
	pcp_start_row_shade
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td>'
	echo '                <textarea class="inform" style="height:25px">'
	                        echo 'Looking for w1-gpio overlay...'
	                        pcp_mount_bootpart_nohtml >/dev/null 2>&1
	                        if ! cat $CONFIGTXT | grep dtoverlay=w1-gpio; then
	                          echo '[ ERROR ] w1-gpio overlay not found.'
	                          FAIL_MSG="w1-gpio overlay not found."
	                        fi
	                        pcp_umount_bootpart_nohtml >/dev/null 2>&1
	echo '                </textarea>'
	echo '              </td>'
	echo '            </tr>'
	pcp_padding
	#------------------------------------------------------------------------------------
	pcp_start_row_shade
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td>'
	echo '                <textarea class="inform" style="height:70px">'
	                        echo 'Looking for wire in dmesg...'
	                        if ! dmesg | grep wire; then
	                          echo '[ ERROR ] Nothing found in dmesg.'
	                          FAIL_MSG="Nothing found in dmesg."
	                        fi
	echo '                </textarea>'
	echo '              </td>'
	echo '            </tr>'
	pcp_padding
	#------------------------------------------------------------------------------------
	pcp_start_row_shade
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td>'
	echo '                <textarea class="inform" style="height:50px">'
	                        echo 'Looking for w1 modules...'
	                        if ! lsmod | grep w1; then
	                          echo '[ ERROR ] No w1 modules found.'
	                          FAIL_MSG="No w1 modules found."
	                        fi
	echo '                </textarea>'
	echo '              </td>'
	echo '            </tr>'
	pcp_padding
	#------------------------------------------------------------------------------------
	pcp_start_row_shade
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td>'
	echo '                <textarea class="inform" style="height:50px">'
	                        echo 'Looking for devices...'
	                        if ! ls /sys/bus/w1/devices/; then
	                          echo '[ ERROR ] No devices found.'
	                          FAIL_MSG="No devices found."
	                        fi
	echo '                </textarea>'
	echo '              </td>'
	echo '            </tr>'
	pcp_padding
	#------------------------------------------------------------------------------------
	pcp_toggle_row_shade
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td>'
	echo '                <textarea class="inform" style="height:280px">'
	                        gpio readall
	echo '                </textarea>'
	echo '              </td>'
	echo '            </tr>'
	pcp_padding
	#------------------------------------------------------------------------------------
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
fi

#========================================================================================
# Generate status message and finish html page
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Status</legend>'
echo '          <table class="bggrey percent100">'
pcp_start_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td>'
echo '                <p>'$FAIL_MSG'</p>'
echo '              </td>'
echo '            </tr>'
echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'

pcp_footer
pcp_copyright
pcp_remove_query_string

echo '</body>'
echo '</html>'
[ $REBOOT_REQUIRED ] && pcp_reboot_required
exit
