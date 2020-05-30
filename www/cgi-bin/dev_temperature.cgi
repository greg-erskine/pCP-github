#!/bin/sh

# Version: 7.0.0 2020-05-30

# Title: Temperature monitor
# Description: Temperature using DS18B20

. pcp-functions

unset REBOOT_REQUIRED

pcp_html_head "Show Temperature" "GE"

pcp_navbar

ACTION="Initial"
pcp_httpd_query_string

FAIL_MSG="ok"
DEBUG=1

COLUMN4_1="col-sm-2"
COLUMN4_2="col-sm-3"
COLUMN4_3="col-sm-3"
COLUMN4_4="col-sm-4"

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
	pcp_message INFO "Installing packages for 1-wire." "text"
	pcp_message INFO "This can take a couple of minutes. Please wait..." "text"
	sudo -u tc pcp-load -r $PCP_REPO -wi w1-KERNEL.tcz

	pcp_mount_bootpart "text"
	pcp_message INFO "Adding w1-gpio overlay to config.txt..." "text"
	sed -i '/dtoverlay=w1-gpio/d' $CONFIGTXT
	sudo echo "dtoverlay=w1-gpio" >> $CONFIGTXT
	[ $? -eq 0 ] && echo "[ INFO ] dtoverlay=w1-gpio added." || FAIL_MSG="Can not add dtoverlay=w1-gpio."
	pcp_umount_bootpart "text"
	REBOOT_REQUIRED=TRUE
}

pcp_uninstall_w1() {
	pcp_message INFO "Removing packages for 1-wire." "text"
	sudo -u tc tce-audit builddb
	[ "$FAIL_MSG" = "ok" ] && sudo -u tc tce-audit delete w1-KERNEL.tcz

	pcp_mount_bootpart "text"
	pcp_message INFO "Removing w1-gpio overlay from config.txt..." "text"
	sed -i '/dtoverlay=w1-gpio/d' $CONFIGTXT
	[ $? -eq 0 ] && echo "[ INFO ] dtoverlay=w1-gpio removed." || FAIL_MSG="Can not remove dtoverlay=w1-gpio."
	pcp_umount_bootpart "text"l
	REBOOT_REQUIRED=TRUE
}

#========================================================================================
# Main
#----------------------------------------------------------------------------------------
pcp_border_begin
pcp_heading5 "1-wire temperature"

#----------------------------------Install/Uninstall Buttons-----------------------------
if [ "$ACTION" = "Initial" ]; then
	pcp_incr_id
	echo '          <form name="main" action="'$0'" method="get">'

	if ( ! df | grep w1- >/dev/null 2>&1 ); then
		echo '              <div class="row">'
		echo '                <div class="'$COLUMN4_1'">'
		echo '                  <input class="'$BUTTON'" type="submit" name="ACTION" value="Install">'
		echo '                </div>'
		echo '                <div class="col-11">'
		echo '                  <p>Install 1-wire&nbsp;&nbsp;'
		pcp_helpbadge
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
			echo '                <div class="'$COLUMN4_2'">'
			echo '                  <p>'$ROW'</p>'
			echo '                </div>'
			echo '                <div class="'$COLUMN4_3'">'
			echo '                  <p>'$(pcp_get_temperature "$(cat /sys/devices/w1_bus_master1/${W1_MASTER_SLAVE}/w1_slave)")'</p>'
			echo '                </div>'
			echo '              </div>'
			ROW=$((ROW+1))
		done

		pcp_incr_id
		echo '              <div class="row">'
		echo '                <div class="'$COLUMN4_1'">'
		echo '                  <input class="'$BUTTON'" type="submit" name="ACTION" value="Uninstall">'
		echo '                </div>'
		echo '                <div class="'$COLUMN4_2'">'
		echo '                  <p>Uninstall 1-wire&nbsp;&nbsp;'
		pcp_helpbadge
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
pcp_border_end

#---------------------------------------Install------------------------------------------
if [ "$ACTION" = "Install" ]; then
	pcp_infobox_begin
	[ "$FAIL_MSG" = "ok" ] && pcp_install_w1
	pcp_infobox_end
fi
#----------------------------------------------------------------------------------------

#---------------------------------------Uninstall----------------------------------------
if [ "$ACTION" = "Uninstall" ]; then
	pcp_infobox_begin
	[ "$FAIL_MSG" = "ok" ] && pcp_uninstall_w1
	pcp_infobox_end
fi
#----------------------------------------------------------------------------------------


#--------------------------------Start/Stop/Clean----------------------------------------
pcp_border_begin
pcp_heading5 "Temperature logging options"
echo '          <form name="actions" action="'$0'" method="get">'
echo '            <div class="row">'
echo '              <div class="'$COLUMN4_1'">'
echo '                <input class="'$BUTTON'" type="submit" name="OPTION" value="Start">'
echo '              </div>'
echo '              <div class="'$COLUMN4_1'">'
echo '                <input class="'$BUTTON'" type="submit" name="OPTION" value="Stop">'
echo '              </div>'
echo '              <div class="'$COLUMN4_1'">'
echo '                <input class="'$BUTTON'" type="submit" name="OPTION" value="Clean">'
echo '              </div>'
echo '            </div>'
echo '          </form>'
pcp_border_end
#----------------------------------------------------------------------------------------

#========================================================================================
# Debug
#----------------------------------------------------------------------------------------
if [ $DEBUG -eq 1 ]; then
	pcp_heading5 "Debug"
	#------------------------------------------------------------------------------------
	echo '            <div class="row">'
	echo '              <div class="col">'
	pcp_infobox_begin
	                        echo 'Looking for w1-gpio overlay...'
	                        pcp_mount_bootpart_nohtml >/dev/null 2>&1
	                        if ! cat $CONFIGTXT | grep dtoverlay=w1-gpio; then
	                          pcp_message ERROR "w1-gpio overlay not found." "text"
	                          FAIL_MSG="w1-gpio overlay not found."
	                        fi
	                        pcp_umount_bootpart_nohtml >/dev/null 2>&1
	pcp_infobox_end
	echo '              </div>'
	echo '            </div>'
	#------------------------------------------------------------------------------------
	echo '            <div class="row">'
	echo '              <div class="col">'
	pcp_infobox_begin
	                        echo 'Looking for wire in dmesg...'
	                        if ! dmesg | grep wire; then
	                          pcp_message ERROR "Nothing found in dmesg." "text"
	                          FAIL_MSG="Nothing found in dmesg."
	                        fi
	pcp_infobox_end
	echo '              </div>'
	echo '            </div>'
	#------------------------------------------------------------------------------------
	echo '            <div class="row">'
	echo '              <div class="col">'
	pcp_infobox_begin
	                        echo 'Looking for errors in dmesg...'
	                        if ! dmesg | grep w1_slave_driver; then
	                          pcp_message ERROR "Nothing found in dmesg." "text"
	                          FAIL_MSG="No errors found in dmesg."
	                        fi
	pcp_infobox_end
	echo '              </div>'
	echo '            </div>'
	#------------------------------------------------------------------------------------
	echo '            <div class="row">'
	echo '              <div class="col">'
	pcp_infobox_begin
	                        echo 'Looking for w1 modules...'
	                        if ! lsmod | grep w1; then
	                          pcp_message ERROR "No w1 modules found." "text"
	                          FAIL_MSG="No w1 modules found."
	                        fi
	pcp_infobox_end
	echo '              </div>'
	echo '            </div>'
	#------------------------------------------------------------------------------------
	echo '            <div class="row">'
	echo '              <div class="col">'
	pcp_infobox_begin
	                        echo 'Looking for devices...'
	                        if ! ls /sys/bus/w1/devices/; then
	                          pcp_message ERROR "No devices found." "text"
	                          FAIL_MSG="No devices found."
	                        fi
	pcp_infobox_end
	echo '              </div>'
	echo '            </div>'
	#------------------------------------------------------------------------------------
	echo '            <div class="row">'
	echo '              <div class="col">'
	pcp_infobox_begin
	                        gpio readall
	pcp_infobox_end
	echo '              </div>'
	echo '            </div>'
	#------------------------------------------------------------------------------------

fi

#========================================================================================
# Generate status message and finish html page
#----------------------------------------------------------------------------------------

pcp_heading5 "Status"
echo '            <div class="row">'
echo '              <div class="'$COLUMN4_1'">'
echo '                <p>'$FAIL_MSG'</p>'
echo '              </div>'
echo '            </div>'

pcp_html_end
[ $REBOOT_REQUIRED ] && pcp_reboot_required
exit
