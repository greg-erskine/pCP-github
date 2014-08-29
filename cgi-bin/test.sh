#!/bin/sh

CONFIG=/usr/local/sbin/config.cfg
#Read from config file.
. /$CONFIG

su "$USER" -c 'tce-load '-i' '/mnt/mmcblk0p2/tce/optional/firmware-ralinkwifi.tcz

#Logic that will skip loading wifi firmware if wifi is not used
if [ $WIFI = on ]; then
tce-load -i /mnt/mmcblk0p2/tce/optional/firmware-ralinkwifi.tcz
echo "first firmware"
tce-load -i /mnt/mmcblk0p2/tce/optional/firmware-rtlwifi.tcz
echo "second firmware"
tce-load -i /mnt/mmcblk0p2/tce/optional/firmware-atheros.tcz
echo "third firmware"
tce-load -i /mnt/mmcblk0p2/tce/optional/wifi.tcz
echo "wifi loaded"
else
exit
fi
