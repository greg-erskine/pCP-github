#!/bin/bash

FFMPEG=ffmpeg
FFMPEGVERSION=3.1.7
SRC=$FFMPEG-$FFMPEGVERSION
STARTDIR=`pwd`
LOG=$PWD/config.log
OUTPUT=$PWD/${FFMPEG}-build
TCZLIB=pcp-lib${FFMPEG}.tcz
TCZLIBINFO=pcp-lib${FFMPEG}.tcz.info
TCZ=pcp-${FFMPEG}.tcz
TCZINFO=pcp-${FFMPEG}.tcz.info
 
# Build requires these extra packages in addition to the debian jessie 8.3+ build tools
# sudo apt-get install squashfs-tools bsdtar

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
	if [ ! -f $SRC.tar.bz2 ]; then
		wget http://ffmpeg.org/releases/$SRC.tar.bz2
	fi
	echo "Extracting source..."
	if [ -f $SRC.tar.bz2 ]; then
		bsdtar -xf $SRC.tar.bz2 >> $LOG
	else
		echo "Source download failed."
		exit
	fi
fi

echo "Compiling..."
./compile-ffmpeg.sh $SRC $OUTPUT >> $LOG

echo "Creating $TCZs..."
echo "Creating headers..."

if [ -f $STARTDIR/$SRC-headers.tar.gz ]; then
	rm $STARTDIR/$SRC-headers.tar.gz
fi

cd $OUTPUT/usr/local/include
bsdtar -czf $STARTDIR/$SRC-headers.tar.gz *
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
echo -e "Description:\tMultimedia files command line conversion tools." >> $TCZINFO
echo -e "Version:\t$FFMPEGVERSION" >> $TCZINFO
echo -e "Author:\t\tFabrice Bellard" >> $TCZINFO
echo -e "Original-site:\thttp://ffmpeg.org/" >> $TCZINFO
echo -e "Copying-policy:\tGPL 2.1 or higher" >> $TCZINFO
echo -e "Size:\t\t$(ls -lk $TCZ | awk '{print $5}')k" >> $TCZINFO
echo -e "Extension_by:\tpiCorePlayer team: https://sites.google.com/site/picoreplayer" >> $TCZINFO
echo -e "\t\tCompiled for piCore 8.x" >> $TCZINFO

if [ -f $TCZLIB ]; then
	rm $TCZLIB >> $LOG
fi

echo -e "usr/local/bin\nusr/local/lib/pkgconfig\nusr/local/include\nusr/local/share/ffmpeg/examples" > $STARTDIR/onlylib
mksquashfs $OUTPUT $TCZLIB -all-root -ef $STARTDIR/onlylib >> $LOG
md5sum `basename $TCZLIB` > ${TCZLIB}.md5.txt
rm $STARTDIR/onlylib

echo "$TCZLIB contains"
unsquashfs -ll $TCZLIB

echo -e "Title:\t\t$TCZLIB" > $TCZLIBINFO
echo -e "Description:\tMultimedia files command line conversion tools shared libraries." >> $TCZLIBINFO
echo -e "Version:\t$FFMPEGVERSION" >> $TCZLIBINFO
echo -e "Author:\t\tFabrice Bellard" >> $TCZLIBINFO
echo -e "Original-site:\thttp://ffmpeg.org/" >> $TCZLIBINFO
echo -e "Copying-policy:\tGPL 2.1 or higher" >> $TCZLIBINFO
echo -e "Size:\t\t$(ls -lk $TCZLIB | awk '{print $5}')k" >> $TCZLIBINFO
echo -e "Extension_by:\tpiCorePlayer team: https://sites.google.com/site/picoreplayer" >> $TCZLIBINFO
echo -e "\t\tCompiled for piCore 8.x" >> $TCZLIBINFO

