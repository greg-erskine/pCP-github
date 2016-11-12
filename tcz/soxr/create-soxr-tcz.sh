#!/bin/bash

SOXR=soxr
SOXRVERSION=0.1.2
SRC=$SOXR-$SOXRVERSION-Source
STARTDIR=`pwd`
LOG=$PWD/config.log
OUTPUT=$PWD/${SOXR}-build
TCZLIB=pcp-lib${SOXR}.tcz
TCZLIBINFO=pcp-lib${SOXR}.tcz.info
 
# Build requires these extra packages in addition to the debian jessie 8.3+ build tools
# sudo apt-get install squashfs-tools bsdtar xz-utils cmake

## Start
echo "Most log mesages sent to $LOG... only 'errors' displayed here"
date > $LOG

## Build

if [ -d $OUTPUT ]; then
	echo "Removing old install..."
	rm -rf $OUTPUT >> $LOG
fi

if [ -d $SRC ]; then
	echo "Removing old sources..."
	rm -rf $SRC >> $LOG
fi

mkdir -p $OUTPUT >> $LOG

if [ ! -f $SRC.tar.xz ]; then
	wget -O $SRC.tar.xz https://sourceforge.net/projects/$SOXR/files/$SRC.tar.xz/download
fi

echo "Extracting source..."
if [ -f $SRC.tar.xz ]; then
	bsdtar -xf $SRC.tar.xz >> $LOG
else
	echo "Source download failed."
	exit
fi

cd $STARTDIR >> $LOG

echo "Compiling..."
./compile-soxr.sh $SRC $OUTPUT >> $LOG

echo "Creating $TCZs..."
echo "Creating headers..."

if [ -f $STARTDIR/$SRC-headers.tar.gz ]; then
	rm $STARTDIR/$SRC-headers.tar.gz
fi

cd $OUTPUT/usr/local/include
bsdtar -czf $STARTDIR/$SRC-headers.tar.gz *

find $OUTPUT/usr/local/lib -type f -name '*so*' -exec strip --strip-unneeded {} \;

cd $STARTDIR >> $LOG

if [ -f $TCZLIB ]; then
	rm $TCZLIB >> $LOG
fi

echo -e "usr/local/lib/pkgconfig\nusr/local/include\nusr/local/share" > $STARTDIR/onlylib
mksquashfs $OUTPUT $TCZLIB -all-root -ef $STARTDIR/onlylib >> $LOG
md5sum `basename $TCZLIB` > ${TCZLIB}.md5.txt
rm $STARTDIR/onlylib

echo "$TCZLIB contains"
unsquashfs -ll $TCZLIB

echo -e "Title:\t\t$TCZLIB" > $TCZLIBINFO
echo -e "Description:\tThe SoX Resampler library." >> $TCZLIBINFO
echo -e "Version:\t$SOXRVERSION" >> $TCZLIBINFO
echo -e "Author:\t\tRob Sykes" >> $TCZLIBINFO
echo -e "Original-site:\thttps://sourceforge.net/p/soxr/wiki/Home/" >> $TCZLIBINFO
echo -e "Copying-policy:\tLGPLv2" >> $TCZLIBINFO
echo -e "Size:\t\t$(ls -lk $TCZLIB | awk '{print $5}')k" >> $TCZLIBINFO
echo -e "Extension_by:\tpiCorePlayer team: https://sites.google.com/site/picoreplayer" >> $TCZLIBINFO
echo -e "\t\tCompiled for piCore 8.x" >> $TCZLIBINFO

