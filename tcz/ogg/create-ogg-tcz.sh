#!/bin/bash

OGG=libogg
OGGVERSION=1.3.3
SRC=$OGG-$OGGVERSION
STARTDIR=`pwd`
LOG=$PWD/config.log
OUTPUT=$PWD/${OGG}-build
TCZLIB=pcp-${OGG}.tcz
TCZLIBINFO=pcp-${OGG}.tcz.info
 
# Build requires these extra packages in addition to the debian jessie 8.3+ build tools
# sudo apt-get install squashfs-tools bsdtar xz-utils

## Start
echo "Most log mesages sent to $LOG... only 'errors' displayed here"
date > $LOG

## Build

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
		wget http://downloads.xiph.org/releases/ogg/$SRC.tar.xz
	fi
	echo "Extracting source..."
	if [ -f $SRC.tar.xz ]; then
		bsdtar -xf $SRC.tar.xz >> $LOG
	else
		echo "Source download failed."
		exit
	fi
fi

echo "Compiling..."
./compile-ogg.sh $SRC $OUTPUT >> $LOG

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


echo -e "usr/local/lib/pkgconfig\nusr/local/lib/libogg.la\nusr/local/include\nusr/local/share" > $STARTDIR/onlylib
mksquashfs $OUTPUT $TCZLIB -all-root -ef $STARTDIR/onlylib >> $LOG
md5sum `basename $TCZLIB` > ${TCZLIB}.md5.txt
rm $STARTDIR/onlylib

echo "$TCZLIB contains"
unsquashfs -ll $TCZLIB

echo -e "Title:\t\t$TCZLIB" > $TCZLIBINFO
echo -e "Description:\tOgg bitstream library." >> $TCZLIBINFO
echo -e "Version:\t$OGGVERSION" >> $TCZLIBINFO
echo -e "Commit:\t\tbc82844df068429d209e909da47b1f730b53b689" >> $TCZLIBINFO
echo -e "Author:\t\tXiph.Org Foundation" >> $TCZLIBINFO
echo -e "Original-site:\thttps://xiph.org/ogg/" >> $TCZLIBINFO
echo -e "Copying-policy:\tLesser GPL" >> $TCZLIBINFO
echo -e "Size:\t\t$(ls -lk $TCZLIB | awk '{print $5}')k" >> $TCZLIBINFO
echo -e "Extension_by:\tpiCorePlayer team: https://www.picoreplayer.org" >> $TCZLIBINFO
echo -e "\t\tCompiled for piCore 10.x" >> $TCZLIBINFO
