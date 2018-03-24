#!/bin/bash

# Turn off system LEDs
echo none > /sys/class/leds/led0/trigger
echo 0 > /sys/class/leds/led0/brightness

echo none > /sys/class/leds/led1/trigger
echo 0 > /sys/class/leds/led1/brightness

# Turn of network LEDs
echo 0 > /sys/class/smsc95xx_leds/eth_fdx
echo 0 > /sys/class/smsc95xx_leds/eth_lnk
echo 0 > /sys/class/smsc95xx_leds/eth_spd

