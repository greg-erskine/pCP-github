#!/bin/sh
debug=1
image=$1

[ $debug = 1 ] && echo $image
[ $debug = 1 ] && fdisk -lu $image

offsetp1=$(fdisk -lu $image | awk '/FAT32/ { print $2 }')
offsetp2=$(fdisk -lu $image | awk '/Linux/ { print $2 }')

[ $debug = 1 ] && echo $offsetp1
[ $debug = 1 ] && echo $offsetp2

dd if=$image of=testp1.img bs=512 skip=$offsetp1
dd if=$image of=testp2.img bs=512 skip=$offsetp2

[ -d /mnt/testp1 ] || mkdir /mnt/testp1
[ -d /mnt/testp2 ] || mkdir /mnt/testp2

sudo mount -t auto -o loop testp1.img /mnt/testp1
sudo mount -t ext4 -o loop testp2.img /mnt/testp2

sudo diff -r /mnt/mmcblk0p1 /mnt/testp1 > reportp1.txt
sudo diff -r /mnt/mmcblk0p2 /mnt/testp2 > reportp2.txt

sudo umount /mnt/testp1
sudo umount /mnt/testp2

sudo rm -f testp*.img
sudo rm -r /mnt/testp*

