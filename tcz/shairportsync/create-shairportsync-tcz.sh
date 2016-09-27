#!/bin/bash

SPS=shairportsync
SRC=shairport-sync
LOG=$PWD/config.log
OUTPUT=$PWD/${SPS}-build
TCZ=pcp-${SPS}.tcz
TCZINFO=pcp-${SPS}.tcz.info
 
# Build requires these extra packages in addition to the debian jessie 8.3+ build tools
# sudo apt-get install squashfs-tools

## Start
echo "Most log mesages sent to $LOG... only 'errors' displayed here"
date > $LOG

## Build
echo "Cleaning up..."

if [ -d $OUTPUT ]; then
	rm -rf $OUTPUT >> $LOG
fi

mkdir -p $OUTPUT >> $LOG

echo "Compiling..."

./compile-shairportsync.sh >> $LOG

echo "Creating $TCZ..."
mkdir -p $OUTPUT/usr/local/sbin >> $LOG
cp -p $SRC/shairport-sync $OUTPUT/usr/local/sbin/shairport-sync >> $LOG

cd $OUTPUT/.. >> $LOG

if [ -f $TCZ ]; then
	rm $TCZ >> $LOG
fi

mksquashfs $OUTPUT $TCZ -all-root >> $LOG
md5sum `basename $TCZ` > ${TCZ}.md5.txt

echo "$TCZ contains"
unsquashfs -ll $TCZ

echo -e "Title:\t\t$TCZ" > $TCZINFO
echo -e "Description:\tAirPlay audio player" >> $TCZINFO
echo -e "Version:\t$($OUTPUT/usr/local/sbin/shairport-sync -V | awk -F- '{printf "%s", $1}')" >> $TCZINFO
echo -e "Commit:\t\t$(cd $SRC; git show | grep commit | awk '{print $2}')" >> $TCZINFO
echo -e "Author:\t\tMike Brady" >> $TCZINFO
echo -e "Original-site:\t$(grep url $SRC/.git/config | awk '{print $3}')" >> $TCZINFO
echo -e "Copying-policy:\tGPL" >> $TCZINFO
echo -e "Size:\t\t$(ls -lk $TCZ | awk '{print $5}')k" >> $TCZINFO
echo -e "Extension_by:\tpiCorePlayer team: https://sites.google.com/site/picoreplayer" >> $TCZINFO
echo -e "\t\tCompiled for piCore 8.x" >> $TCZINFO
echo -e "Change-log:\t$(cat README.md)" >> $TCZINFO
