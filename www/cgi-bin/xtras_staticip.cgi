#!/bin/sh

# Version: 5.0.0 2019-04-06

#========================================================================================
# This script sets a static IP.
#----------------------------------------------------------------------------------------
# The steps below follow the de-facto Tiny Core method of setting static IP address
# that is recommended in a few Tiny Core forum threads.
#
#   1. Insert "nodhcp" bootcode in cmdline.txt
#   2. Create script ie. ethX.sh or wlanX.sh
#   3. Add /opt/ethX.sh to bootlocal.sh (Note: not done for wifi)
#   4. Backup
#
# Complications:
#   1. /proc/cmdline is only updated from /mnt/mmcblk0p1/cmdline.txt at boot time
#   2. /etc/init.d/settime.sh doesn't run if nodhcp bootcode is set.
#---------------------------------------------------------------------------------------+
# link-local addressing for IPv4 networks 169.254.0.0/16                                |
#------------------------------------+-------------+-----------------+------------------+
# IANA reserved private IPv4 ranges  | Start       | End             | No. of addresses |
#------------------------------------+-------------+-----------------+------------------+
# 24-bit block (/8 prefix, 1 × A)    | 10.0.0.0    | 10.255.255.255  | 16777216         |
# 20-bit block (/12 prefix, 16 × B)  | 172.16.0.0  | 172.31.255.255  | 1048576          |
# 16-bit block (/16 prefix, 256 × C) | 192.168.0.0 | 192.168.255.255 | 65536            |
#------------------------------------+-------------+-----------------+------------------+

. pcp-functions

pcp_html_head "xtras - Static IP" "GE"

pcp_banner
pcp_navigation
pcp_httpd_query_string

VALIDNETWORKS=$(ls /sys/class/net | sed '/^lo/d')

#========================================================================================
# Look for existing static IP script - if found, set $NETWORK to it
#----------------------------------------------------------------------------------------
if [ x"" = x"$NETWORK" ]; then
	for i in $VALIDNETWORKS; do
		[ -f "/opt/${i}.sh" ] && NETWORK="$i" && break
	done
fi

#========================================================================================
# If $NETWORK not set, set to default eth0 or wlan0
#----------------------------------------------------------------------------------------
if [ x"" = x"$NETWORK" ]; then
	for i in $VALIDNETWORKS; do
		NETWORK="$i"
		break
	done
fi

STATICIP="/opt/${NETWORK}.sh"

#========================================================================================
# Add/remove $STATICIP to line 3 of /opt/bootlocal.sh script.
#
# -rwxrwxr-x    1 tc       staff          197 Apr 24 10:18 bootlocal.sh
# -rwxr-xr-x    1 root     staff          284 Apr 19 22:39 bootsync.sh
#----------------------------------------------------------------------------------------
pcp_edit_bootlocal() {
	[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] Writing /opt/bootlocal.sh...</p>'
	grep -v ${NETWORK}.sh /opt/bootlocal.sh >/opt/bootlocal.sh~
	sudo chmod u=rwx,go=rx /opt/bootlocal.sh~
	sudo mv /opt/bootlocal.sh~ /opt/bootlocal.sh
	sudo chown tc.staff /opt/bootlocal.sh
	[ "$1" = "add" ] && sed -i "4i /opt/${NETWORK}.sh" /opt/bootlocal.sh
	[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] '$(ls -al /opt/bootlocal.sh)'</p>'
}

#========================================================================================
# Add/delete nodhcp boot code to /mnt/mmcblk0p1/cmdline.txt ($CMDLINETXT).
#----------------------------------------------------------------------------------------
pcp_nodhcp_bootcode() {
	[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] Writing '$CMDLINETXT'...</p>'
	pcp_mount_bootpart "nohtml" >/dev/null
	if mount | grep $VOLUME >/dev/null; then
		sed -i 's/nodhcp //g' $CMDLINETXT
		[ "$1" = "add" ] && sed -i 's/^/nodhcp /' $CMDLINETXT
		pcp_umount_bootpart "nohtml" >/dev/null
	else
		[ $DEBUG -eq 1 ] && echo '<p class="error">[ ERROR ] '$VOLUME' not mounted</p>'
	fi
}

#========================================================================================
# Read static IP script.
#----------------------------------------------------------------------------------------
pcp_read_script() {
	set -- `cat $STATICIP | grep ifconfig`
	IP=$3
	NETMASK=$5
	BROADCAST=$7
	set -- `cat $STATICIP | grep route`
	GATEWAY=$5
	set -- `cat $STATICIP | grep nameserver`
	NAMESERVER1=$4
	NAMESERVER2=$9
}

#========================================================================================
# Write static IP script.
#
# Note: Look into search gateway.
#----------------------------------------------------------------------------------------
pcp_write_script() {
	if ! [ x"" = x"$IP" ] || [ x"" = x"$NETMASK" ] || [ x"" = x"$BROADCAST" ] || [ x"" = x"$GATEWAY" ] || [ x"" = x"$NAMESERVER1" ]; then
		echo '#!/bin/sh' >$STATICIP
		echo '# Maintained by piCorePlayer' >>$STATICIP
		echo 'echo "[ INFO ] Running $0..."' >>$STATICIP
		echo 'NWOK=1' >>$STATICIP
		echo 'until [ -d /sys/class/net/'${NETWORK}' ]' >>$STATICIP
		echo 'do' >>$STATICIP
		echo '    if [ $((CNT++)) -gt '$NETWORK_WAIT' ]; then' >>$STATICIP
		echo '        echo -n "${RED}No Ethernet Adapter ['${NETWORK}'] Found!${NORMAL}"' >>$STATICIP
		echo '        NWOK=0' >>$STATICIP
		echo '        break' >>$STATICIP
		echo '    else' >>$STATICIP
		echo '        echo -n "."' >>$STATICIP
		echo '        sleep 0.5' >>$STATICIP
		echo '    fi' >>$STATICIP
		echo 'done' >>$STATICIP
		echo 'if [ $NWOK -eq 1 ]; then' >>$STATICIP
		echo '    ifconfig '$NETWORK' '$IP' netmask '$NETMASK' broadcast '$BROADCAST' up' >>$STATICIP
		echo '    route add default gw '$GATEWAY >>$STATICIP
#		echo '    echo search '$GATEWAY' > /etc/resolv.conf' >>$STATICIP
		echo '    sudo echo nameserver '$NAMESERVER1' > /etc/resolv.conf' >>$STATICIP
		[ x"" = x"$NAMESERVER2" ] || echo '    echo nameserver '$NAMESERVER2' >> /etc/resolv.conf' >>$STATICIP
		echo '    /etc/init.d/settime.sh &' >>$STATICIP
		echo 'fi' >>$STATICIP
		chmod ugo+x $STATICIP
	fi
}

#========================================================================================
# Work out default values.
#
# Note: NAMESERVER2 defaults to blank.
#----------------------------------------------------------------------------------------
pcp_which_class() {
	FIRST=$(echo $(pcp_lmsip) | awk -F. '{ print $1 }')
	THIRD=$(echo $(pcp_lmsip) | awk -F. '{ print $3 }')

	case $FIRST in
		10)  CLASS=A ;;
		172) CLASS=B ;;
		192) CLASS=C ;;
	esac

	case "$CLASS" in
		A)
			EXAMPLE1="10.0.0.123"
			EXAMPLE2="10.0.1.123"
			EXAMPLE3="255.0.0.0"
			EXAMPLE4="10.0.0.255"
			EXAMPLE5="10.0.1.255"
			EXAMPLE6="10.0.0.1"
			EXAMPLE7="10.0.1.1"
			EXAMPLE8="10.0.1.254"
		;;
		B)
			EXAMPLE1="172.16.0.123"
			EXAMPLE2="172.16.1.123"
			EXAMPLE3="255.255.0.0"
			EXAMPLE4="172.16.0.255"
			EXAMPLE5="172.16.1.255"
			EXAMPLE6="172.16.0.1"
			EXAMPLE7="172.16.1.1"
			EXAMPLE8="172.16.1.254"
		;;
		C)
			EXAMPLE1="192.168.0.123"
			EXAMPLE2="192.168.1.123"
			EXAMPLE3="255.255.255.0"
			EXAMPLE4="192.168.0.255"
			EXAMPLE5="192.168.1.255"
			EXAMPLE6="192.168.0.1"
			EXAMPLE7="192.168.1.1"
			EXAMPLE8="192.168.1.254"
		;;
	esac

	EXAMPLE9="8.8.8.8"
}

pcp_set_defaults() {
	case "$CLASS" in
		A)
			[ x"" = x"$IP" ] && IP="10.0.0.123"
			[ x"" = x"$NETMASK" ] && NETMASK="255.0.0.0"
			[ x"" = x"$BROADCAST" ] && BROADCAST="10.0.0.255"
			[ x"" = x"$GATEWAY" ] && GATEWAY="10.0.0.1"
		;;
		B)
			[ x"" = x"$IP" ] && IP="172.16.0.123"
			[ x"" = x"$NETMASK" ] && NETMASK="255.255.0.0"
			[ x"" = x"$BROADCAST" ] && BROADCAST="172.16.0.255"
			[ x"" = x"$GATEWAY" ] && GATEWAY="172.16.0.1"
		;;
		C)
			[ x"" = x"$IP" ] && IP="192.168.$THIRD.123"
			[ x"" = x"$NETMASK" ] && NETMASK="255.255.255.0"
			[ x"" = x"$BROADCAST" ] && BROADCAST="192.168.$THIRD.255"
			[ x"" = x"$GATEWAY" ] && GATEWAY="192.168.$THIRD.1"
		;;
	esac

	[ x"" = x"$NAMESERVER1" ] && NAMESERVER1=$GATEWAY
}

pcp_clear_defaults() {
	IP=""
	NETMASK=""
	BROADCAST=""
	GATEWAY=""
	NAMESERVER1=""
	NAMESERVER2=""
}

#========================================================================================
# Display variables debug information.
#----------------------------------------------------------------------------------------
pcp_debug_info() {
	pcp_debug_variables "html" DHCP NETWORK VALIDNETWORKS STATICIP IP NETMASK BROADCAST\
		GATEWAY NAMESERVER1 NAMESERVER2 CLASS EXAMPLE1 EXAMPLE2 EXAMPLE3 EXAMPLE4\
		EXAMPLE5 EXAMPLE6 EXAMPLE7 EXAMPLE8 EXAMPLE9
}

#========================================================================================
# Network tabs.
#----------------------------------------------------------------------------------------
pcp_network_tabs() {
	echo '<!-- Start of pcp_network_tabs toolbar -->'
	echo '<p style="margin-top:8px;">'

	for i in $VALIDNETWORKS; do
		[ "$i" = "$NETWORK" ] && TAB_STYLE="tab7a" || TAB_STYLE="tab7"
		echo '  <a class="'$TAB_STYLE'" href="'$0'?NETWORK='$i'" title="'$i'">'$i'</a>'
	done

	echo '</p>'
	echo '<div class="tab7end" style="margin-bottom:10px;">pCP</div>'
	echo '<!-- End of pcp_network_tabs toolbar -->'
}

#========================================================================================
# Look for nodhcp boot code in /mnt/mmcblk0p1/cmdline.txt
#----------------------------------------------------------------------------------------
pcp_get_nodhcp() {
	pcp_mount_bootpart "nohtml" >/dev/null
	if mount | grep $VOLUME >/dev/null; then
		cat $CMDLINETXT | grep nodhcp >/dev/null
		case $? in
			0)
				[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] NODHCP boot code found in '$CMDLINETXT'.</p>'
				NODHCPYES="checked"
				DHCP="off"
			;;
			*)
				[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] NODHCP boot code not found in '$CMDLINETXT'.</p>'
				NODHCPNO="checked"
				DHCP="on"
			;;
		esac
		pcp_umount_bootpart "nohtml" >/dev/null
	else
		[ $DEBUG -eq 1 ] && echo '<p class="error">[ ERROR ] '$VOLUME' not mounted.</p>'
	fi
}

#========================================================================================
# Main.
#----------------------------------------------------------------------------------------
[ $DEBUG -eq 1 ] && pcp_table_top "Debug information"
pcp_which_class
[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] SUBMIT -> '$SUBMIT' option...</p>'

case "$SUBMIT" in
	Save)
		if [ "$DHCP" = "off" ]; then
			pcp_set_defaults
			pcp_write_script
			pcp_nodhcp_bootcode add
			[ "${NETWORK:0:3}" = "eth" ] && pcp_edit_bootlocal add
		else
			pcp_nodhcp_bootcode delete
			[ "${NETWORK:0:3}" = "eth" ] && pcp_edit_bootlocal delete
		fi
		pcp_backup >/dev/null
	;;
	Delete)
		rm -f $STATICIP
		pcp_clear_defaults
		pcp_backup >/dev/null
	;;
	Defaults)
		pcp_set_defaults
		pcp_write_script
		pcp_backup >/dev/null
	;;
	*)
		SUBMIT="Initial"
		pcp_get_nodhcp
	;;
esac

[ $DEBUG -eq 1 ] && pcp_debug_info
[ -f "/opt/${NETWORK}.sh" ] && pcp_read_script

pcp_get_nodhcp
[ $DEBUG -eq 1 ] && pcp_table_end

#========================================================================================
# Start table.
#----------------------------------------------------------------------------------------

#--------------------------------------Warning message-----------------------------------
echo '<table class="bgred">'
echo '  <tr class="warning">'
echo '    <td>'
echo '      <p style="color:white"><b>Warning:</b></p>'
echo '      <ul>'
echo '        <li style="color:white">The recommended method to set a static IP address is to map the MAC address to an IP address in your router.</li>'
echo '        <li style="color:white">You will need to re-install static IP after an insitu update.</li>'
echo '        <li style="color:white">You must get all the IP addresses and mask correct, or unusual network issues will occur.</li>'
echo '        <li style="color:white">All network interfaces must be DHCP or static IP, not mixed.</li>'
echo '        <li style="color:white">The network interface tabs will automatically show available network interfaces.</li>'
echo '      </ul>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------

pcp_network_tabs

COLUMN1="column150"
COLUMN2="column240"
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <form name="staticip" action="xtras_staticip.cgi" method="get" id="staticip">'
echo '        <div class="row">'
echo '          <fieldset>'
echo '            <legend>Set static IP for '$NETWORK'</legend>'
echo '            <table class="bggrey percent100">'
#--------------------------------------DHCP----------------------------------------------
pcp_incr_id
pcp_start_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="'$COLUMN1'">'
echo '                  <p class="row">DHCP/Static IP</p>'
echo '                </td>'
echo '                <td class="'$COLUMN2'">'
echo '                  <input class="small1" type="radio" id="DHCPon" name="DHCP" value="on" '$NODHCPNO'>DHCP&nbsp;&nbsp;'
echo '                  <input class="small1" type="radio" id="DHCPoff" name="DHCP" value="off" '$NODHCPYES'>Static IP'
echo '                </td>'
echo '                <td>'
echo '                  <p>Select DHCP or Static IP&nbsp;&nbsp;'
echo '                    <a class="moreless" id="'$ID'a" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                  </p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <p>&lt;DHCP|Static IP&gt;</p>'
echo '                    <p>Dynamic Host Configuration Protocol (DHCP)</p>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'
#----------------------------------------------------------------------------------------

if [ "$DHCP" = "off" ]; then
	#--------------------------------------IP--------------------------------------------
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COLUMN1'">'
	echo '                  <p class="row">Static IP address</p>'
	echo '                </td>'
	echo '                <td class="'$COLUMN2'">'
	echo '                  <input class="large15"'
	echo '                         type="text"'
	echo '                         name="IP"'
	echo '                         value="'$IP'"'
	echo '                         title="xxx.xxx.xxx.xxx"'
	echo '                         pattern="\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(\:\d{1,5})?"'
	echo '                  >*'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p class="row">Set static IP address&nbsp;&nbsp;'
	echo '                    <a class="moreless" id="'$ID'a" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <ul>'
	echo '                      <li>Static IP must be unique and not clash with any other IP on your network.</li>'
	echo '                      <li>Static IP must not be in the range of IP addresses controlled by DHCP.</li>'
	echo '                    </ul>'
	echo '                    <p><b>Example: </b></p>'
	echo '                    <ul>'
	echo '                      <li>'$EXAMPLE1'</li>'
	echo '                      <li>'$EXAMPLE2'</li>'
	echo '                    </ul>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	#--------------------------------------NETMASK---------------------------------------
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COLUMN1'">'
	echo '                  <p class="row">Netmask</p>'
	echo '                </td>'
	echo '                <td class="'$COLUMN2'">'
	echo '                  <input class="large15"'
	echo '                         type="text"'
	echo '                         name="NETMASK"'
	echo '                         value="'$NETMASK'"'
	echo '                         title="xxx.xxx.xxx.xxx"'
	echo '                         pattern="\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(\:\d{1,5})?"'
	echo '                  >*'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p class="row">Set netmask address&nbsp;&nbsp;'
	echo '                    <a class="moreless" id="'$ID'a" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>The netmask must be the same on all your devices.</p>'
	echo '                    <p><b>Example: </b>'$EXAMPLE3'</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	#--------------------------------------BROADCAST-------------------------------------
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COLUMN1'">'
	echo '                  <p class="row">Broadcast</p>'
	echo '                </td>'
	echo '                <td class="'$COLUMN2'">'
	echo '                  <input class="large15"'
	echo '                         type="text"'
	echo '                         name="BROADCAST"'
	echo '                         value="'$BROADCAST'"'
	echo '                         title="xxx.xxx.xxx.xxx"'
	echo '                         pattern="\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(\:\d{1,5})?"'
	echo '                  >*'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p class="row">Set broadcast address&nbsp;&nbsp;'
	echo '                    <a class="moreless" id="'$ID'a" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>The broadcast address is fixed and can not be used for other purposes.</p>'
	echo '                    <p><b>Example:</b></p>'
	echo '                    <ul>'
	echo '                      <li>'$EXAMPLE4'</li>'
	echo '                      <li>'$EXAMPLE5'</li>'
	echo '                    </ul>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	#--------------------------------------GATEWAY---------------------------------------
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COLUMN1'">'
	echo '                  <p class="row">Default gateway</p>'
	echo '                </td>'
	echo '                <td class="'$COLUMN2'">'
	echo '                  <input class="large15"'
	echo '                         type="text"'
	echo '                         name="GATEWAY"'
	echo '                         value="'$GATEWAY'"'
	echo '                         title="xxx.xxx.xxx.xxx"'
	echo '                         pattern="\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(\:\d{1,5})?"'
	echo '                  >*'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p class="row">Set default gateway address&nbsp;&nbsp;'
	echo '                    <a class="moreless" id="'$ID'a" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>The gateway address is usually your modem IP address.</p>'
	echo '                    <p><b>Example:</b></p>'
	echo '                    <ul>'
	echo '                      <li>'$EXAMPLE6'</li>'
	echo '                      <li>'$EXAMPLE7'</li>'
	echo '                      <li>'$EXAMPLE8'</li>'
	echo '                    </ul>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	#--------------------------------------NAMESERVER1-----------------------------------
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COLUMN1'">'
	echo '                  <p class="row">Nameserver 1</p>'
	echo '                </td>'
	echo '                <td class="'$COLUMN2'">'
	echo '                  <input class="large15"'
	echo '                         type="text"'
	echo '                         name="NAMESERVER1"'
	echo '                         value="'$NAMESERVER1'"'
	echo '                         title="xxx.xxx.xxx.xxx"'
	echo '                         pattern="\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(\:\d{1,5})?"'
	echo '                  >*'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p class="row">Set nameserver 1 (DNS) address &nbsp;&nbsp;'
	echo '                    <a class="moreless" id="'$ID'a" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>The nameserver address is usually your modem IP address.</p>'
	echo '                    <p><b>Example:</b></p>'
	echo '                    <ul>'
	echo '                      <li>'$EXAMPLE6'</li>'
	echo '                      <li>'$EXAMPLE7'</li>'
	echo '                      <li>'$EXAMPLE8'</li>'
	echo '                      <li>'$EXAMPLE9'</li>'
	echo '                    </ul>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	#--------------------------------------NAMESERVER2-----------------------------------
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COLUMN1'">'
	echo '                  <p class="row">Nameserver 2</p>'
	echo '                </td>'
	echo '                <td class="'$COLUMN2'">'
	echo '                  <input class="large15"'
	echo '                         type="text"'
	echo '                         name="NAMESERVER2"'
	echo '                         value="'$NAMESERVER2'"'
	echo '                         title="xxx.xxx.xxx.xxx"'
	echo '                         pattern="\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(\:\d{1,5})?"'
	echo '                  >'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p class="row">Set nameserver 2 (DNS) address &nbsp;&nbsp;'
	echo '                    <a class="moreless" id="'$ID'a" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Alternative nameserver address, incase nameserver 1 is not available.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	#------------------------------------------------------------------------------------
fi

#--------------------------------------BUTTONS-------------------------------------------
pcp_incr_id
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="column400">'
echo '                  <input type="submit" title="Save configuration to /opt/'${NETWORK}'.sh" name="SUBMIT" value="Save">'
echo '                  <input type="hidden" name="NETWORK" value="'$NETWORK'">'
[ "$DHCP" = "off" ] &&
echo '                  <input type="submit" title="Fill-in blanks with default values" name="SUBMIT" value="Defaults">'
[ -f "/opt/${NETWORK}.sh" ] &&
echo '                  <input type="submit" title="Delete /opt/'${NETWORK}'.sh" name="SUBMIT" value="Delete">'
echo '                </td>'
echo '                <td colspan="2">'
echo '                  <p>* required field</p>'
echo '                </td>'
echo '              </tr>'
#----------------------------------------------------------------------------------------
echo '            </table>'
echo '          </fieldset>'
echo '        </div>'
echo '      </form>'
echo '    </td>'
echo '  </tr>'
echo '</table>'

if [ $DEBUG -eq 1 ]; then
	#========================================================================================
	# Display current $STATICIP
	#----------------------------------------------------------------------------------------
	pcp_start_row_shade
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Current /opt/'${NETWORK}'.sh</legend>'
	echo '          <table class="bggrey percent100">'
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td>'
	                      pcp_textarea_inform "none" "cat /opt/'${NETWORK}'.sh" 100
	echo '              </td>'
	echo '            </tr>'
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
	#----------------------------------------------------------------------------------------

	#========================================================================================
	# Display current /etc/resolv.conf
	#----------------------------------------------------------------------------------------
	pcp_start_row_shade
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Current /etc/resolv.conf</legend>'
	echo '          <table class="bggrey percent100">'
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td>'
	                      pcp_textarea_inform "none" "cat /etc/resolv.conf" 25
	echo '              </td>'
	echo '            </tr>'
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
	#----------------------------------------------------------------------------------------

	#========================================================================================
	# Display current /mnt/mmcblk0p1/cmdline.txt
	#----------------------------------------------------------------------------------------
	pcp_start_row_shade
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Current '$CMDLINETXT'</legend>'
	echo '          <table class="bggrey percent100">'
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td>'
	                      pcp_mount_bootpart "nohtml" >/dev/null
	                      pcp_textarea_inform "none" "cat $CMDLINETXT" 25
	                      pcp_umount_bootpart "nohtml" >/dev/null
	echo '              </td>'
	echo '            </tr>'
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
	#----------------------------------------------------------------------------------------

	#========================================================================================
	# Display current /opt/bootlocal.sh
	#----------------------------------------------------------------------------------------
	pcp_start_row_shade
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Current /opt/bootlocal.sh</legend>'
	echo '          <table class="bggrey percent100">'
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td>'
	                      pcp_textarea_inform "none" "cat /opt/bootlocal.sh" 70
	echo '              </td>'
	echo '            </tr>'
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
	#----------------------------------------------------------------------------------------
fi

pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'
