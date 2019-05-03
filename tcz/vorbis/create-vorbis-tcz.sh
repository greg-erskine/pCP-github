#!/bin/bash

VORBIS=libvorbis
VORBISVERSION=1.3.6
SRC=$VORBIS-$VORBISVERSION
STARTDIR=`pwd`
LOG=$PWD/config.log
OUTPUT=$PWD/${VORBIS}-build
OGGHEADERS=$STARTDIR/../ogg/libogg-1.3.3-headers.tar.gz 
TCZLIB=pcp-${VORBIS}.tcz
TCZLIBINFO=pcp-${VORBIS}.tcz.info
 
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
		wget http://downloads.xiph.org/releases/vorbis/$SRC.tar.xz
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
./compile-vorbis.sh $SRC $OUTPUT >> $LOG

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

echo -e "usr/local/lib/pkgconfig\nusr/local/lib/libvorbisfile.la\nusr/local/lib/libvorbis.la\nusr/local/lib/libvorbisenc.la\nusr/local/lib/libvorbisenc.so\nusr/local/lib/libvorbisenc.so.2\nusr/local/lib/libvorbisenc.so.2.0.11\nusr/local/include\nusr/local/share" > $STARTDIR/onlylib
mksquashfs $OUTPUT $TCZLIB -all-root -ef $STARTDIR/onlylib >> $LOG
md5sum `basename $TCZLIB` > ${TCZLIB}.md5.txt
rm $STARTDIR/onlylib

echo "$TCZLIB contains"
unsquashfs -ll $TCZLIB

echo -e "Title:\t\t$TCZLIB" > $TCZLIBINFO
echo -e "Description:\tThe Vorbis General Audio Compression Codec decoder library." >> $TCZLIBINFO
echo -e "Version:\t$VORBISVERSION" >> $TCZLIBINFO
echo -e "Author:\t\tXiph.Org Foundation" >> $TCZLIBINFO
echo -e "Original-site:\thttps://xiph.org/vorbis/" >> $TCZLIBINFO
echo -e "Copying-policy:\tLesser GPL" >> $TCZLIBINFO
echo -e "Size:\t\t$(ls -lk $TCZLIB | awk '{print $5}')k" >> $TCZLIBINFO
echo -e "Extension_by:\tpiCorePlayer team: https://www.picoreplayer.org" >> $TCZLIBINFO
echo -e "\t\tCompiled for piCore 10.x" >> $TCZLIBINFO
