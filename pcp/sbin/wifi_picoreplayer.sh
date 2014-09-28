#!/bin/sh
echo "  "
echo "  "
echo "starting wifi script"
sudo ifconfig wlan0 down
sudo sleep 1
sudo ifconfig wlan0 up
sudo /usr/local/bin/wifi.sh -a 2>&1 > /tmp/wifi.log
