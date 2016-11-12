#!/bin/bash

FLAC=flac
FLACVERSION=1.3.1
SRC=$FLAC-$FLACVERSION
STARTDIR=`pwd`
LOG=$PWD/config.log
OUTPUT=$PWD/${FLAC}-build
OGGHEADERS=$STARTDIR/../ogg/libogg-1.3.2-headers.tar.gz	
TCZLIB=pcp-lib${FLAC}.tcz
TCZLIBINFO=pcp-lib${FLAC}.tcz.info
TCZ=pcp-${FLAC}.tcz
TCZINFO=pcp-${FLAC}.tcz.info
 
# Build requires these extra packages in addition to the debian jessie 8.3+ build tools
# sudo apt-get install squashfs-tools bsdtar xz-utils

## Start
echo "Most log mesages sent to $LOG... only 'errors' displayed here"
date > $LOG

## Build
if [ ! -f $OGGHEADERS ]; then
	echo "Need $OGGHEADERS to build $TCZLIB"
	exit 1
fi

if [ -d $OUTPUT ]; then
	echo "Removing old install..."
	rm -rf $OUTPUT >> $LOG
fi

mkdir -p $OUTPUT >> $LOG

if [ -f $SRC/config.log ]; then
	cd $SRC >> $LOG
	make clean >> $LOG
	cd $STARTDIR >> $LOG
else
	if [ ! -f $SRC.tar.xz ]; then
		wget http://downloads.xiph.org/releases/flac/$SRC.tar.xz
	fi
	echo "Extracting source..."
	if [ -f $SRC.tar.xz ]; then
		bsdtar -xf $SRC.tar.xz >> $LOG
		bsdtar -C $SRC/include -xf $OGGHEADERS
	else
		echo "Source download failed."
		exit
	fi
fi


echo "Compiling..."
./compile-flac.sh $SRC $OUTPUT >> $LOG

echo "Creating $TCZs..."
echo "Creating headers..."

if [ -f $STARTDIR/$SRC-headers.tar.gz ]; then
	rm $STARTDIR/$SRC-headers.tar.gz
fi

cd $OUTPUT/usr/local/include
bsdtar -czf $STARTDIR/$SRC-headers.tar.gz *

find $OUTPUT/usr/local/lib -type f -name '*so*' -exec strip --strip-unneeded {} \;

cd $STARTDIR >> $LOG

if [ -f $TCZ ]; then
	rm $TCZ >> $LOG
fi

echo -e "usr/local/lib\nusr/local/include\nusr/local/share" > $STARTDIR/onlybin
mksquashfs $OUTPUT $TCZ -all-root -ef $STARTDIR/onlybin >> $LOG
md5sum `basename $TCZ` > ${TCZ}.md5.txt
rm $STARTDIR/onlybin

echo "$TCZ contains"
unsquashfs -ll $TCZ

echo -e "Title:\t\t$TCZ" > $TCZINFO
echo -e "Description:\tFree Lossless Audio Codec - command line tools." >> $TCZINFO
echo -e "Version:\t$FLACVERSION" >> $TCZINFO
echo -e "Author:\t\tJosh Coalson, Xiph.Org Foundation" >> $TCZINFO
echo -e "Original-site:\thttps://xiph.org/flac/" >> $TCZINFO
echo -e "Copying-policy:\tLesser GPL" >> $TCZINFO
echo -e "Size:\t\t$(ls -lk $TCZ | awk '{print $5}')k" >> $TCZINFO
echo -e "Extension_by:\tpiCorePlayer team: https://sites.google.com/site/picoreplayer" >> $TCZINFO
echo -e "\t\tCompiled for piCore 8.x" >> $TCZINFO

if [ -f $TCZLIB ]; then
	rm $TCZLIB >> $LOG
fi

echo -e "usr/local/bin\nusr/local/lib/pkgconfig\nusr/local/lib/libFLAC.la\nusr/local/include\nusr/local/share" > $STARTDIR/onlylib
mksquashfs $OUTPUT $TCZLIB -all-root -ef $STARTDIR/onlylib >> $LOG
md5sum `basename $TCZLIB` > ${TCZLIB}.md5.txt
rm $STARTDIR/onlylib

echo "$TCZLIB contains"
unsquashfs -ll $TCZLIB

echo -e "Title:\t\t$TCZLIB" > $TCZLIBINFO
echo -e "Description:\tFree Lossless Audio Codec - runtime C library." >> $TCZLIBINFO
echo -e "Version:\t$FLACVERSION" >> $TCZLIBINFO
echo -e "Author:\t\tJosh Coalson, Xiph.Org Foundation" >> $TCZLIBINFO
echo -e "Original-site:\thttps://xiph.org/flac/" >> $TCZLIBINFO
echo -e "Copying-policy:\tLesser GPL" >> $TCZLIBINFO
echo -e "Size:\t\t$(ls -lk $TCZLIB | awk '{print $5}')k" >> $TCZLIBINFO
echo -e "Extension_by:\tpiCorePlayer team: https://sites.google.com/site/picoreplayer" >> $TCZLIBINFO
echo -e "\t\tCompiled for piCore 8.x" >> $TCZLIBINFO

