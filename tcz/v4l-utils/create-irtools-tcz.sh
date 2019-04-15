#!/bin/bash

V4L=v4l-utils
V4LVERSION=1.16.5
SRC=$V4L-$V4LVERSION
SRCTAR=${V4L}-${V4LVERSION}.tar.bz2
STARTDIR=`pwd`
LOG=$PWD/config.log
OUTPUT=$PWD/${V4L}-build
TOOLS=irtools
TCZ=pcp-$TOOLS.tcz
TCZINFO=$TCZ.info
 
# Build requires these extra packages in addition to the debian stretch 9.3+ build tools
# sudo apt-get install libudev-dev

## Start
echo "Most log mesages sent to $LOG... only 'errors' displayed here"
date > $LOG

## Build

if [ -d $OUTPUT ]; then
	echo "Removing old install..."
	sudo rm -rf $OUTPUT >> $LOG
fi

if [ -d $SRC ]; then
	echo "Removing old sources..."
	rm -rf $SRC >> $LOG
fi

mkdir -p $OUTPUT >> $LOG

if [ ! -f $SRCTAR ]; then
	wget -O $SRCTAR https://linuxtv.org/downloads/$V4L/$SRCTAR
fi

echo "Extracting source..."
if [ -f $SRCTAR ]; then
	bsdtar -xf $SRCTAR >> $LOG
else
	echo "Source download failed."
	exit
fi

cd $STARTDIR >> $LOG

echo "Compiling..."
./compile-irtools.sh $SRC $OUTPUT >> $LOG

echo "Creating $TCZs..."

find $OUTPUT/usr/local/bin -type f -exec strip --strip-unneeded {} \; >> $LOG

mkdir -p $OUTPUT/usr/local/etc/keytables
mkdir -p $OUTPUT/usr/local/share/pcp-$TOOLS/files
cp -p $SRC/COPYING $OUTPUT/usr/local/share/pcp-$TOOLS
echo "# table: slimdevices, type: nec" > $OUTPUT/usr/local/share/pcp-$TOOLS/files/slimdevices
awk -F, '{printf "%s\t%s\n",$1,$2}' keytable-jivelite-slimdevices.csv | sed -e 's/"//g' >> $OUTPUT/usr/local/share/pcp-$TOOLS/files/slimdevices
echo "# table: justboomir, type: rc-5" > $OUTPUT/usr/local/share/pcp-$TOOLS/files/justboomir
awk -F, '{printf "%s\t%s\n",$1,$2}' keytable-jivelite-justboomIR.csv | sed -e 's/"//g' >> $OUTPUT/usr/local/share/pcp-$TOOLS/files/justboomir

cd $OUTPUT >> $LOG

find * -not -type d > $STARTDIR/${TCZ}.list

cd $STARTDIR >> $LOG

if [ -f $TCZ ]; then
	rm $TCZ >> $LOG
fi

mksquashfs $OUTPUT $TCZ -all-root >> $LOG
md5sum `basename $TCZ` > ${TCZ}.md5.txt

echo "$TCZ contains"
unsquashfs -ll $TCZ

echo -e "Title:\t\t$TCZ" > $TCZINFO
echo -e "Description:\tLinux Kernel Media Subsystem IR Tools." >> $TCZINFO
echo -e "Version:\t$V4LVERSION" >> $TCZINFO
echo -e "Authors:\tGregor Jasny and others." >> $TCZINFO
echo -e "Original-site:\thttps://linuxtv.org/" >> $TCZINFO
echo -e "Copying-policy:\tGPLv2+ and GPLv2" >> $TCZINFO
echo -e "Size:\t\t$(ls -lk $TCZ | awk '{print $5}')k" >> $TCZINFO
echo -e "Extension_by:\tpiCorePlayer team: https://www.picoreplayer.org" >> $TCZINFO
echo -e "\t\tCompiled for piCore 10.x" >> $TCZINFO
