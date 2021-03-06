#!/bin/bash

FFMPEG=ffmpeg
FFMPEGVERSION=3.1.11
SRC=$FFMPEG-$FFMPEGVERSION
STARTDIR=`pwd`
LOG=$PWD/config.log
OUTPUT=$PWD/${FFMPEG}-build
TCZLIB=pcp-lib${FFMPEG}.tcz
TCZLIBINFO=pcp-lib${FFMPEG}.tcz.info
TCZDEV=pcp-lib${FFMPEG}-dev.tcz
TCZDEVINFO=pcp-lib${FFMPEG}-dev.tcz.info
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

if [ -f $STARTDIR/$SRC-headers.tar.gz ]; then
	rm $STARTDIR/$SRC-headers.tar.gz
fi

cd $STARTDIR >> $LOG

if [ -f $TCZ ]; then
	rm $TCZ >> $LOG
fi

echo -e "usr/local/lib\nusr/local/include\nusr/local/share" > $STARTDIR/onlybin
mksquashfs $OUTPUT $TCZ -all-root -ef $STARTDIR/onlybin >> $LOG
md5sum `basename $TCZ` > ${TCZ}.md5.txt
rm $STARTDIR/onlybin

echo "$TCZ contains"
unsquashfs -i $TCZ
cd squashfs-root
find * -not -type d > $STARTDIR/${TCZ}.list
cd ..
rm -rf squashfs-root

echo -e "Title:\t\t$TCZ" > $TCZINFO
echo -e "Description:\tMultimedia files command line conversion tools." >> $TCZINFO
echo -e "Version:\t$FFMPEGVERSION" >> $TCZINFO
echo -e "Author:\t\tFabrice Bellard" >> $TCZINFO
echo -e "Original-site:\thttp://ffmpeg.org/" >> $TCZINFO
echo -e "Copying-policy:\tGPL 2.1 or higher" >> $TCZINFO
echo -e "Size:\t\t$(ls -lk $TCZ | awk '{print $5}')k" >> $TCZINFO
echo -e "Extension_by:\tpiCorePlayer team: https://www.picoreplayer.org" >> $TCZINFO
echo -e "\t\tCompiled for piCore 10.x" >> $TCZINFO

if [ -f $TCZLIB ]; then
	rm $TCZLIB >> $LOG
fi

echo -e "usr/local/bin\nusr/local/lib/pkgconfig\nusr/local/include\nusr/local/share/ffmpeg/examples\n" > $STARTDIR/onlylib
cd $OUTPUT
ls -1 usr/local/lib/*\.a >> $STARTDIR/onlylib
cd ..
mksquashfs $OUTPUT $TCZLIB -all-root -ef $STARTDIR/onlylib >> $LOG
md5sum `basename $TCZLIB` > ${TCZLIB}.md5.txt
rm $STARTDIR/onlylib

echo "$TCZLIB contains"
unsquashfs -i $TCZLIB
cd squashfs-root
find * -not -type d > $STARTDIR/${TCZLIB}.list
cd ..
rm -rf squashfs-root

echo -e "Title:\t\t$TCZLIB" > $TCZLIBINFO
echo -e "Description:\tMultimedia files command line conversion tools shared libraries." >> $TCZLIBINFO
echo -e "Version:\t$FFMPEGVERSION" >> $TCZLIBINFO
echo -e "Author:\t\tFabrice Bellard" >> $TCZLIBINFO
echo -e "Original-site:\thttp://ffmpeg.org/" >> $TCZLIBINFO
echo -e "Copying-policy:\tGPL 2.1 or higher" >> $TCZLIBINFO
echo -e "Size:\t\t$(ls -lk $TCZLIB | awk '{print $5}')k" >> $TCZLIBINFO
echo -e "Extension_by:\tpiCorePlayer team: https://www.picoreplayer.org" >> $TCZLIBINFO
echo -e "\t\tCompiled for piCore 10.x" >> $TCZLIBINFO

if [ -f $TCZDEV ]; then
	rm $TCZDEV >> $LOG
fi

echo -e "usr/local/bin\nusr/local/share\n" > $STARTDIR/onlydev
cd $OUTPUT
ls -1 usr/local/lib/*\.so* >> $STARTDIR/onlydev
cd ..
mksquashfs $OUTPUT $TCZDEV -all-root -ef $STARTDIR/onlydev >> $LOG
md5sum `basename $TCZDEV` > ${TCZDEV}.md5.txt
rm $STARTDIR/onlydev

echo "$TCZDEV contains"
unsquashfs -i $TCZDEV
cd squashfs-root
find * -not -type d > $STARTDIR/${TCZDEV}.list
cd ..
rm -rf squashfs-root

echo -e "Title:\t\t$TCZDEV" > $TCZDEVINFO
echo -e "Description:\tMultimedia files command line conversion tools development files." >> $TCZDEVINFO
echo -e "Version:\t$FFMPEGVERSION" >> $TCZDEVINFO
echo -e "Author:\t\tFabrice Bellard" >> $TCZDEVINFO
echo -e "Original-site:\thttp://ffmpeg.org/" >> $TCZDEVINFO
echo -e "Copying-policy:\tGPL 2.1 or higher" >> $TCZDEVINFO
echo -e "Size:\t\t$(ls -lk $TCZLIB | awk '{print $5}')k" >> $TCZDEVINFO
echo -e "Extension_by:\tpiCorePlayer team: https://www.picoreplayer.org" >> $TCZDEVINFO
echo -e "\t\tCompiled for piCore 10.x" >> $TCZDEVINFO
