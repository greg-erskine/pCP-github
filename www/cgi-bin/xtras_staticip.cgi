#!/bin/sh

# Version: 7.0.0 2020-05-23
<<<<<<< HEAD
=======

# Title: Static IP
# Description: Set a static IP. The preferred method is to use DHCP.
>>>>>>> origin/develop

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

pcp_navbar
pcp_httpd_query_string

VALIDNETWORKS=$(ls /sys/class/net | sed '/^lo/d')
FAIL=0
unset REBOOT_REQUIRED

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
	[ $DEBUG -eq 1 ] && pcp_message DEBUG "Writing /opt/bootlocal.sh..." "html"
	grep -v ${NETWORK}.sh /opt/bootlocal.sh >/opt/bootlocal.sh~
	sudo chmod u=rwx,go=rx /opt/bootlocal.sh~
	sudo mv /opt/bootlocal.sh~ /opt/bootlocal.sh
	sudo chown tc.staff /opt/bootlocal.sh
	[ "$1" = "add" ] && sed -i "4i /opt/${NETWORK}.sh" /opt/bootlocal.sh
	[ $DEBUG -eq 1 ] && pcp_message DEBUG "$(ls -al /opt/bootlocal.sh)" "html"
}

#========================================================================================
# Add/delete nodhcp boot code to /mnt/mmcblk0p1/cmdline.txt ($CMDLINETXT).
#----------------------------------------------------------------------------------------
pcp_nodhcp_bootcode() {
<<<<<<< HEAD
	[ $DEBUG -eq 1 ] && pcp_message DEBUG "Writing '$CMDLINETXT'..." "html"
=======
	[ $DEBUG -eq 1 ] && pcp_message DEBUG "Writing $CMDLINETXT..." "html"
>>>>>>> origin/develop
	pcp_mount_bootpart >/dev/null
	if mount | grep $VOLUME >/dev/null; then
		sed -i 's/nodhcp //g' $CMDLINETXT
		[ "$1" = "add" ] && sed -i 's/^/nodhcp /' $CMDLINETXT
		pcp_umount_bootpart >/dev/null
	else
		[ $DEBUG -eq 1 ] && pcp_messsage ERROR "$VOLUME not mounted" "html"
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

	case "$FIRST" in
		10)  CLASS=A ;;
		172) CLASS=B ;;
		192) CLASS=C ;;
	esac

	case "$CLASS" in
		A)	EXAMPLE1="10.0.0.123"
			EXAMPLE2="10.0.1.123"
			EXAMPLE3="255.0.0.0"
			EXAMPLE4="10.0.0.255"
			EXAMPLE5="10.0.1.255"
			EXAMPLE6="10.0.0.1"
			EXAMPLE7="10.0.1.1"
			EXAMPLE8="10.0.1.254"
			EXAMPLE9="8.8.8.8"
		;;
		B)	EXAMPLE1="172.16.0.123"
			EXAMPLE2="172.16.1.123"
			EXAMPLE3="255.255.0.0"
			EXAMPLE4="172.16.0.255"
			EXAMPLE5="172.16.1.255"
			EXAMPLE6="172.16.0.1"
			EXAMPLE7="172.16.1.1"
			EXAMPLE8="172.16.1.254"
			EXAMPLE9="8.8.8.8"
		;;
		C)	EXAMPLE1="192.168.0.123"
			EXAMPLE2="192.168.1.123"
			EXAMPLE3="255.255.255.0"
			EXAMPLE4="192.168.0.255"
			EXAMPLE5="192.168.1.255"
			EXAMPLE6="192.168.0.1"
			EXAMPLE7="192.168.1.1"
			EXAMPLE8="192.168.1.254"
			EXAMPLE9="8.8.8.8"
		;;
	esac
}

pcp_set_defaults() {
	case "$CLASS" in
		A)	[ x"" = x"$IP" ] && IP="10.0.0.123"
			[ x"" = x"$NETMASK" ] && NETMASK="255.0.0.0"
			[ x"" = x"$BROADCAST" ] && BROADCAST="10.0.0.255"
			[ x"" = x"$GATEWAY" ] && GATEWAY="10.0.0.1"
		;;
		B)	[ x"" = x"$IP" ] && IP="172.16.0.123"
			[ x"" = x"$NETMASK" ] && NETMASK="255.255.0.0"
			[ x"" = x"$BROADCAST" ] && BROADCAST="172.16.0.255"
			[ x"" = x"$GATEWAY" ] && GATEWAY="172.16.0.1"
		;;
		C)	[ x"" = x"$IP" ] && IP="192.168.$THIRD.123"
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
	echo '  <div>'
	echo '    <ul class="nav nav-tabs navbar-dark mt-1">'

	for i in $VALIDNETWORKS; do
		[ "$i" = "$NETWORK" ] && TAB_ACTIVE="active" || TAB_ACTIVE=""
		echo '      <li class="nav-item">'
		echo '        <a class="nav-link '$TAB_ACTIVE'" href="'$0'?NETWORK='$i'" title="'$i'">'$i'</a>'
		echo '      </li>'
	done

	echo '    </ul>'
	echo '  </div>'
	echo '<!-- End of pcp_network_tabs toolbar -->'
}

#========================================================================================
# Look for nodhcp boot code in /mnt/mmcblk0p1/cmdline.txt
#----------------------------------------------------------------------------------------
pcp_get_nodhcp() {
	pcp_mount_bootpart >/dev/null
	if mount | grep $VOLUME >/dev/null; then
		cat $CMDLINETXT | grep nodhcp >/dev/null
		case $? in
			0)
				[ $DEBUG -eq 1 ] && pcp_message DEBUG "NODHCP boot code found in $CMDLINETXT." "html"
				NODHCPYES="checked"
				DHCP="off"
			;;
			*)
				[ $DEBUG -eq 1 ] && pcp_message DEBUG "NODHCP boot code not found in $CMDLINETXT." "html"
				NODHCPNO="checked"
				DHCP="on"
			;;
		esac
		pcp_umount_bootpart >/dev/null
	else
		[ $DEBUG -eq 1 ] && pcp_message ERROR "$VOLUME not mounted." "html"
	fi
}

# && INDICATOR="" || INDICATOR="border-success"

#========================================================================================
# Validate Static IP settings
#----------------------------------------------------------------------------------------
pcp_validate_static_ip() {
	pcp_heading5 "Validating IP Settings"
	pcp_textarea_begin "" 5

	echo -n "[ INFO ] Checking IP unused: $IP..."
	CURIP=$(ifconfig $NETWORK | grep "inet addr" | cut -d':' -f2 | cut -d' ' -f1)
	if [ "$IP" = "$CURIP" ]; then
		echo "Matches Current [OK]"
		IP_IND="border-success"
	else
		ping -c 2 -W 5 $IP >/dev/null
		if [ $? -eq 1 ]; then
			echo "[OK]"
			IP_IND="border-success"
		else
			echo "IP address already in use. [ERROR]"
			FAIL=1
			IP_IND="border-danger"
		fi
	fi

	echo -n "[ INFO ] Checking Netmask..."
	echo "$NETMASK" | grep -E -q "^(255)\.(255|0)\.(255|0)\.0"
	if [ $? -eq 0 ]; then
		echo "[OK]"
		NETMASK_IND="border-success"
	else
		echo "Seems incorrect, check before rebooting. [ERROR]"
		NETMASK_IND="border-warning"
	fi

	echo -n "[ INFO ] Checking Broadcast..."
	TEST=$(echo "$GATEWAY" | awk -F'.' '{ print $1 "." $2 "." $3 ".255" }')
	if [ "$BROADCAST" = "$TEST" ]; then
		echo "[OK]"
		BROADCAST_IND="border-success"
	else
		echo "Seems incorrect, check before rebooting. [ERROR]"
		BROADCAST_IND="border-warning"
	fi

	echo -n "[ INFO ] Checking Gateway: $GATEWAY..."
	ping -c 2 -W 5 $GATEWAY >/dev/null
	if [ $? -eq 0 ]; then
		echo "[OK]"
		GATEWAY_IND="border-success"
	else
		echo "[ERROR]"
		FAIL=1
		GATEWAY_IND="border-danger"
	fi

	pcp_textarea_end
}

#========================================================================================
# Main.
#----------------------------------------------------------------------------------------
pcp_which_class
[ $DEBUG -eq 1 ] && pcp_debug_variables "html" SUBMIT

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
		if [ "$STATIC" != "firstrun" ]; then
			pcp_backup >/dev/null
			REBOOT_REQUIRED=TRUE
		fi
	;;
	Delete)
		rm -f $STATICIP
		[ "${NETWORK:0:3}" = "eth" ] && pcp_edit_bootlocal delete
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

#--------------------------------------Warning message-----------------------------------
<<<<<<< HEAD
echo '    <div>'
=======
echo '    <div class="alert alert-primary" role="alert">'
>>>>>>> origin/develop
echo '      <p><b>Warning:</b></p>'
echo '      <ul>'
echo '        <li>The recommended method to set a static IP address is to map the MAC address to an IP address in your router.</li>'
echo '        <li>You will need to re-install static IP after an insitu update.</li>'
echo '        <li>You must get all the IP addresses and mask correct, or unusual network issues will occur.</li>'
echo '        <li>All network interfaces must be DHCP or static IP, not mixed.</li>'
echo '        <li>The network interface tabs will automatically show available network interfaces.</li>'
echo '      </ul>'
echo '    </div>'
#----------------------------------------------------------------------------------------

<<<<<<< HEAD
pcp_network_tabs

COLUMN3_1="col-sm-2"
COLUMN3_2="col-sm-3"
COLUMN3_3="col-sm-7"

=======
COLUMN3_1="col-sm-2"
COLUMN3_2="col-sm-3"
COLUMN3_3="col-sm-7"
>>>>>>> origin/develop
#----------------------------------------------------------------------------------------
[ "$SUBMIT" = "Save" -a "$STATIC" != "firstrun" -a "$DHCP" = "off" ] && pcp_validate_static_ip
pcp_network_tabs

<<<<<<< HEAD
echo '  <div class="'$BORDER'">'
pcp_heading5 "Set static IP for $NETWORK"
echo '    <form name="staticip" action="'$0'" method="get" id="staticip">'

=======
echo '  <div class="'$BORDER' mb-2">'
pcp_heading5 "Set static IP for $NETWORK"
echo '    <form name="staticip" action="'$0'" method="get" id="staticip">'
>>>>>>> origin/develop
#-----------------------------------------DHCP-------------------------------------------
echo '        <div class="row mx-1">'
echo '          <div class="'$COLUMN3_1'">'
echo '            <p>DHCP/Static IP</p>'
echo '          </div>'
echo '          <div class="'$COLUMN3_2'">'
echo '            <input type="radio" id="DHCPon" name="DHCP" value="on" '$NODHCPNO'>'
echo '            <label for="DHCPon">DHCP&nbsp;&nbsp;</label>'
echo '            <input type="radio" id="DHCPoff" name="DHCP" value="off" '$NODHCPYES'>'
echo '            <label for="DHCPoff">Static IP</label>'
echo '          </div>'
pcp_incr_id
echo '          <div class="'$COLUMN3_3'">'
echo '            <p>Select DHCP or Static IP&nbsp;&nbsp;'
pcp_helpbadge
echo '            </p>'
echo '            <div id="dt'$ID'" class="'$COLLAPSE'">'
echo '              <p>&lt;DHCP|Static IP&gt;</p>'
echo '              <p>Dynamic Host Configuration Protocol (DHCP)</p>'
echo '            </div>'
echo '          </div>'
echo '        </div>'
#----------------------------------------------------------------------------------------

if [ "$DHCP" = "off" ]; then
	#--------------------------------------IP--------------------------------------------
	echo '        <div class="row mx-1">'
	echo '          <div class="'$COLUMN3_1'">'
	echo '            <p>Static IP address *</p>'
	echo '          </div>'
	echo '          <div class="form-group '$COLUMN3_2'">'
	echo '            <input class="form-control form-control-sm '$IP_IND'"'
	echo '                   type="text"'
	echo '                   name="IP"'
	echo '                   value="'$IP'"'
	echo '                   title="xxx.xxx.xxx.xxx"'
	echo '                   pattern="\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(\:\d{1,5})?"'
	echo '            >'
	echo '          </div>'
	pcp_incr_id
	echo '          <div class="'$COLUMN3_3'">'
	echo '            <p>Set static IP address&nbsp;&nbsp;'
	pcp_helpbadge
	echo '            </p>'
	echo '            <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '              <ul>'
	echo '                <li>Static IP must be unique and not clash with any other IP on your network.</li>'
	echo '                <li>Static IP must not be in the range of IP addresses controlled by DHCP.</li>'
	echo '              </ul>'
	echo '              <p><b>Example: </b></p>'
	echo '              <ul>'
	echo '                <li>'$EXAMPLE1'</li>'
	echo '                <li>'$EXAMPLE2'</li>'
	echo '              </ul>'
	echo '            </div>'
	echo '          </div>'
	echo '        </div>'
	#------------------------------------NETMASK-----------------------------------------
	echo '        <div class="row mx-1">'
	echo '          <div class="'$COLUMN3_1'">'
	echo '            <p>Netmask *</p>'
	echo '          </div>'
	echo '          <div class="form-group '$COLUMN3_2'">'
	echo '            <input class="form-control form-control-sm '$NETMASK_IND'"'
	echo '                   type="text"'
	echo '                   name="NETMASK"'
	echo '                   value="'$NETMASK'"'
	echo '                   title="xxx.xxx.xxx.xxx"'
	echo '                   pattern="\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(\:\d{1,5})?"'
	echo '            >'
	echo '          </div>'
	pcp_incr_id
	echo '          <div class="'$COLUMN3_3'">'
	echo '            <p>Set netmask address&nbsp;&nbsp;'
	pcp_helpbadge
	echo '            </p>'
	echo '            <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '              <p>The netmask must be the same on all your devices.</p>'
	echo '              <p><b>Example: </b>'$EXAMPLE3'</p>'
	echo '            </div>'
	echo '          </div>'
	echo '        </div>'
	#-----------------------------------BROADCAST----------------------------------------
	echo '        <div class="row mx-1">'
	echo '          <div class="'$COLUMN3_1'">'
	echo '            <p>Broadcast *</p>'
	echo '          </div>'
	echo '          <div class="form-group '$COLUMN3_2'">'
	echo '            <input class="form-control form-control-sm '$BROADCAST_IND'"'
	echo '                   type="text"'
	echo '                   name="BROADCAST"'
	echo '                   value="'$BROADCAST'"'
	echo '                   title="xxx.xxx.xxx.xxx"'
	echo '                   pattern="\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(\:\d{1,5})?"'
	echo '            >'
	echo '          </div>'
	pcp_incr_id
	echo '          <div class="'$COLUMN3_3'">'
	echo '            <p>Set broadcast address&nbsp;&nbsp;'
	pcp_helpbadge
	echo '            </p>'
	echo '            <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '              <p>The broadcast address is fixed and can not be used for other purposes.</p>'
	echo '              <p><b>Example:</b></p>'
	echo '              <ul>'
	echo '                <li>'$EXAMPLE4'</li>'
	echo '                <li>'$EXAMPLE5'</li>'
	echo '              </ul>'
	echo '            </div>'
	echo '          </div>'
	echo '        </div>'
	#------------------------------------GATEWAY-----------------------------------------
	echo '        <div class="row mx-1">'
	echo '          <div class="'$COLUMN3_1'">'
	echo '            <p>Default gateway *</p>'
	echo '          </div>'
	echo '          <div class="form-group '$COLUMN3_2'">'
	echo '            <input class="form-control form-control-sm '$GATEWAY_IND'"'
	echo '                   type="text"'
	echo '                   name="GATEWAY"'
	echo '                   value="'$GATEWAY'"'
	echo '                   title="xxx.xxx.xxx.xxx"'
	echo '                   pattern="\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(\:\d{1,5})?"'
	echo '            >'
	echo '          </div>'
	pcp_incr_id
	echo '          <div class="'$COLUMN3_3'">'
	echo '            <p>Set default gateway address&nbsp;&nbsp;'
	pcp_helpbadge
	echo '            </p>'
	echo '            <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '              <p>The gateway address is usually your modem IP address.</p>'
	echo '              <p><b>Example:</b></p>'
	echo '              <ul>'
	echo '                <li>'$EXAMPLE6'</li>'
	echo '                <li>'$EXAMPLE7'</li>'
	echo '                <li>'$EXAMPLE8'</li>'
	echo '              </ul>'
	echo '            </div>'
	echo '          </div>'
	echo '        </div>'
	#--------------------------------------NAMESERVER1-----------------------------------
	echo '        <div class="row mx-1">'
	echo '          <div class="'$COLUMN3_1'">'
	echo '            <p>Nameserver 1 *</p>'
	echo '          </div>'
	echo '          <div class="form-group '$COLUMN3_2'">'
	echo '            <input class="form-control form-control-sm"'
	echo '                   type="text"'
	echo '                   name="NAMESERVER1"'
	echo '                   value="'$NAMESERVER1'"'
	echo '                   title="xxx.xxx.xxx.xxx"'
	echo '                   pattern="\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(\:\d{1,5})?"'
	echo '            >'
	echo '          </div>'
	pcp_incr_id
	echo '          <div class="'$COLUMN3_3'">'
	echo '            <p>Set nameserver 1 (DNS) address &nbsp;&nbsp;'
	pcp_helpbadge
	echo '            </p>'
	echo '            <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '              <p>The nameserver address is usually your modem IP address.</p>'
	echo '              <p><b>Example:</b></p>'
	echo '              <ul>'
	echo '                <li>'$EXAMPLE6'</li>'
	echo '                <li>'$EXAMPLE7'</li>'
	echo '                <li>'$EXAMPLE8'</li>'
	echo '                <li>'$EXAMPLE9'</li>'
	echo '              </ul>'
	echo '            </div>'
	echo '          </div>'
	echo '        </div>'
	#--------------------------------------NAMESERVER2-----------------------------------
	echo '        <div class="row mx-1">'
	echo '          <div class="'$COLUMN3_1'">'
	echo '            <p>Nameserver 2</p>'
	echo '          </div>'
	echo '          <div class="form-group '$COLUMN3_2'">'
	echo '            <input class="form-control form-control-sm"'
	echo '                   type="text"'
	echo '                   name="NAMESERVER2"'
	echo '                   value="'$NAMESERVER2'"'
	echo '                   title="xxx.xxx.xxx.xxx"'
	echo '                   pattern="\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(\:\d{1,5})?"'
	echo '            >'
	echo '          </div>'
	pcp_incr_id
	echo '          <div class="'$COLUMN3_3'">'
	echo '            <p>Set nameserver 2 (DNS) address &nbsp;&nbsp;'
	pcp_helpbadge
	echo '            </p>'
	echo '            <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '              <p>Alternative nameserver address, incase nameserver 1 is not available.</p>'
	echo '            </div>'
	echo '          </div>'
	echo '        </div>'
	#------------------------------------------------------------------------------------
fi

#--------------------------------------BUTTONS-------------------------------------------
echo '        <div class="row mx-1 mb-2">'
echo '          <div class="'$COLUMN3_1'">'
echo '            <input class="'$BUTTON'" type="submit" title="Save configuration to /opt/'${NETWORK}'.sh" name="SUBMIT" value="Save">'
echo '            <input type="hidden" name="NETWORK" value="'$NETWORK'">'
echo '          </div>'

if [ "$DHCP" = "off" ]; then
	echo '          <div class="'$COLUMN3_1'">'
	echo '            <input class="'$BUTTON'" type="submit" title="Fill-in blanks with default values" name="SUBMIT" value="Defaults">'
	echo '          </div>'
else
	echo '          <input type="hidden" name="STATIC" value="firstrun">'
fi

if [ -f "/opt/${NETWORK}.sh" ]; then
	echo '          <div class="'$COLUMN3_1'">'
	echo '            <input class="'$BUTTON'" type="submit" title="Delete /opt/'${NETWORK}'.sh" name="SUBMIT" value="Delete">'
	echo '          </div>'
fi

if [ "$DHCP" = "off" ]; then
	echo '          <div class="'$COLUMN3_2'">'
	echo '            <p>* required field</p>'
	echo '          </div>'
fi

echo '        </div>'
#----------------------------------------------------------------------------------------
echo '      </div>'
echo '    </form>'
echo '  </div>'

#========================================================================================
if [ $DEBUG -eq 1 ]; then
	pcp_hr
	pcp_textarea "" "cat /opt/${NETWORK}.sh" 10
<<<<<<< HEAD

	pcp_textarea "" "cat /etc/resolv.conf" 5

	pcp_mount_bootpart >/dev/null
	pcp_textarea "" "cat $CMDLINETXT" 5
	pcp_umount_bootpart >/dev/null

=======
	pcp_textarea "" "cat /etc/resolv.conf" 5
	pcp_mount_bootpart >/dev/null
	pcp_textarea "" "cat $CMDLINETXT" 5
	pcp_umount_bootpart >/dev/null
>>>>>>> origin/develop
	pcp_textarea "" "cat /opt/bootlocal.sh" 10

fi
#----------------------------------------------------------------------------------------

[ $REBOOT_REQUIRED -a $FAIL -eq 0 ] && pcp_reboot_required

pcp_html_end
