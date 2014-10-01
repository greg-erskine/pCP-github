#! /bin/sh
echo "  "
echo "  "
echo "update Squeezelite to newest version - first I will stop Squeezelite"
sleep 1
sudo /usr/local/etc/init.d/squeezelitehf stop

wget -P /tmp http://squeezelite.googlecode.com/files/squeezelite-armv6hf
if
test ! -f /tmp/squeezelite-armv6hf 
then echo "not downloaded, please try again later"
exit 
else

echo "Downloaded succesfully:"
sudo cp /mnt/mmcblk0p1/tce/squeezelite-armv6hf /tmp/squeezelite-armv6hf.old
sudo rm -f /mnt/mmcblk0p1/tce/squeezelite-armv6hf
sudo cp /tmp/squeezelite-armv6hf /mnt/mmcblk0p1/tce
sudo chmod u+x /mnt/mmcblk0p1/tce/squeezelite-armv6hf
sudo rm -f /tmp/squeezelite-armv6hf.old
sudo rm -f /tmp/squeezelite-armv6hf
    
sleep 1
echo "Squeezelite will be restarted with previous settings"
sudo /usr/local/etc/init.d/squeezelite_initd start
echo "  "
echo "  "
fi    
