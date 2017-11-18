#!/bin/sh

ifconfig | grep -q Bcast
if [ $? -ne 0 ]; then
  echo "Entering Wifi Ad-Hoc mode...."
  echo "Loading Wifi, if needed"
  sudo -u tc tce-load -i firmware-rpi3-wireless.tcz
  sudo -u tc tce-load -i wifi.tcz
  echo ""
  pkill udhcpd

  [ ! -d /var/lib/misc ] && mkdir /var/lib/misc
  touch /var/lib/misc/udhcpd.lease

  cat << EOF > /etc/udhcpd.conf
interface wlan0
start 10.10.10.2
end 10.10.10.10
opt subnet 255.255.255.0
opt dns 10.10.10.1
opt router 10.10.10.1
EOF
  echo "Bringing up wlan0 interface"
  ifconfig wlan0 down
  iwconfig wlan0 mode ad-hoc
  iwconfig wlan0 key 1234567ABC
  iwconfig wlan0 channel 6 essid pCP
  ifconfig wlan0 10.10.10.1 netmask 255.255.255.0 up 

  echo "Starting DHCP server"
  udhcpd

  DONE=0
  until [ $DONE -ne 0 ]; do
    if [ "$(iwgetid -r)" != "pCP" ]; then
	echo "New SSID Connected"
	DONE=1
    fi
    ifconfig eth0 | grep -q Bcast
    if [ $? -eq 0 ]; then
    	echo "eth0 is now up"
    	DONE=1
    fi
    sleep 5
  done
  pkill udhcpd
  echo "Exiting"
fi
