#!/bin/sh

read -p "Write the version of piCorePlayer you want to make:" NUMBER
#NUMBER=write version number like 1.17b etc

#Copy the piCorePlayer.dep file to the correct location
sudo cp -f /home/tc/www/cgi-bin/piCorePlayer.dep /mnt/mmcblk0p2/tce/piCorePlayer.dep

#Update the piversion.cfg with the correct version number
sudo sed -i "s/\(PIVERS=\).*/\1\"piCorePlayer $NUMBER\"/" /usr/local/sbin/piversion.cfg

#TAR file:
sudo mount /dev/sda1
sudo mount /dev/mmcblk0p1
sudo mkdir /mnt/sda1/piCorePlayer"$NUMBER"
sudo tar -zcvf /mnt/sda1/piCorePlayer"$NUMBER"/piCorePlayer"$NUMBER"_boot.tar.gz /mnt/mmcblk0p1
sudo tar -zcvf /mnt/sda1/piCorePlayer"$NUMBER"/piCorePlayer"$NUMBER"_tce.tar.gz /mnt/mmcblk0p2/tce
sudo dd if=/dev/mmcblk0 of=/mnt/sda1/piCorePlayer"$NUMBER"/piCorePlayer"$NUMBER".img bs=1M count=65

echo "Version is: " piCorePlayer$NUMBER

cat /usr/local/sbin/piversion.cfg