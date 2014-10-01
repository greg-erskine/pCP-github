#!/bin/sh

sudo ifconfig wlan0 down
sleep 2
sudo ifconfig wlan0 up
sleep 2
exit