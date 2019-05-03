#!/bin/bash

SOX=sox
SOXVERSION=14.4.3
SRC=slimserver-vendor
STARTDIR=`pwd`
LOG=$PWD/config.log
OUTPUT=$PWD/${SOX}-build
TCZLIB=pcp-lib${SOX}.tcz
TCZLIBINFO=pcp-lib${SOX}.tcz.info
TCZ=pcp-${SOX}.tcz
TCZINFO=pcp-${SOX}.tcz.info
 
# Build requires these extra packages in addition to the debian stretch 9.2+ build tools
# sudo apt-get install squashfs-tools bsdtar

## Start
echo "Most log mesages sent to $LOG... only 'errors' displayed here"
date > $LOG

## Build

if [ -d $OUTPUT ]; then
	echo "Removing old install..."
	rm -rf $OUTPUT >> $LOG
fi

mkdir -p $OUTPUT/usr/local/bin >> $LOG
mkdir -p $OUTPUT/usr/local/share/pcp-$SOX >> $LOG

if [ ! -d $SRC ]; then
        git clone https://github.com/piCorePlayer/slimserver-vendor.git $SRC
fi

cd $SRC
git fetch -a
git pull
git checkout sox-lame || exit 1

cd $STARTDIR

if [ -x sox ]; then
	rm sox >> $LOG
fi

echo "Compiling..."
cp -p $STARTDIR/buildme-linux-armhf.sh $SRC/sox >> $LOG
cd $SRC/$SOX
./buildme-linux-armhf.sh

echo "Creating $TCZs..."

cp -p $SOX-$SOXVERSION/COPYING $OUTPUT/usr/local/share/pcp-$SOX/ || exit 1
cp -p $STARTDIR/sox $OUTPUT/usr/local/bin || exit 1

find $OUTPUT/usr/local/bin -type f -exec strip --strip-unneeded {} \;

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
echo -e "Description:\tSwiss army knife of sound processing." >> $TCZINFO
echo -e "Version:\t$SOXVERSION" >> $TCZINFO
echo -e "Authors:\tChris Bagwell, Rob Sykes, Pascal Giard" >> $TCZINFO
echo -e "Commit:\t\t$(cd $SRC; git show | grep commit | awk '{print $2}')" >> $TCZINFO
echo -e "Source-site:\t$(grep url $SRC/.git/config | awk '{print $3}')" >> $TCZINFO
echo -e "Original-site:\thttp://sox.sourceforge.net/" >> $TCZINFO
echo -e "Copying-policy:\tGPL and LGPL" >> $TCZINFO
echo -e "Size:\t\t$(ls -lk $TCZ | awk '{print $5}')k" >> $TCZINFO
echo -e "Extension_by:\tpiCorePlayer team: https://www.picoreplayer.org" >> $TCZINFO
echo -e "\t\tCompiled for piCore 10.x" >> $TCZINFO
