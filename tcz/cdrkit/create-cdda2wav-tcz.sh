#!/bin/bash

CDRKIT=cdrkit
CDRKITVERSION=1.1.11
SRC=$CDRKIT-$CDRKITVERSION
SRCTAR=${CDRKIT}_${CDRKITVERSION}.orig.tar.gz
STARTDIR=`pwd`
LOG=$PWD/config.log
OUTPUT=$PWD/${CDRKIT}-build
TCZLIB=pcp-cdda2wav.tcz
TCZLIBINFO=pcp-cdda2wav.tcz.info
 
# Build requires these extra packages in addition to the debian jessie 8.3+ build tools
# sudo apt-get install squashfs-tools bsdtar cmake libcap-dev libbz2-dev

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
	wget -O $SRCTAR https://sourceforge.net/projects/wodim/files/$CDRKIT/$SRCTAR/download
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
./compile-cdda2wav.sh $SRC $OUTPUT >> $LOG

echo "Creating $TCZs..."

find $OUTPUT/usr/local/bin -type f -exec strip --strip-unneeded {} \; >> $LOG
cd $OUTPUT/usr/local/bin; ln -s icedax cdda2wav >> $LOG
sudo chown -Rh root:root $OUTPUT
sudo chmod u+s $OUTPUT/usr/local/bin/icedax

cd $STARTDIR >> $LOG

if [ -f $TCZLIB ]; then
	rm $TCZLIB >> $LOG
fi

echo -e "usr/local/lib\nusr/local/include\nusr/local/share\nusr/local/bin/genisoimage\nusr/local/bin/devdump\nusr/local/bin/isodebug\nusr/local/bin/isodump\nusr/local/bin/isoinfo\nusr/local/bin/isovfy\nusr/local/bin/cdda2mp3\nusr/local/bin/pitchplay\nusr/local/bin/readmult\nusr/local/bin/cdda2ogg\nusr/local/bin/readom\nusr/local/bin/dirsplit\nusr/local/sbin/netscsid\nusr/local/sbin" > $STARTDIR/onlybin
mksquashfs $OUTPUT $TCZLIB -ef $STARTDIR/onlybin >> $LOG
md5sum `basename $TCZLIB` > ${TCZLIB}.md5.txt
rm $STARTDIR/onlybin

echo "$TCZLIB contains"
unsquashfs -ll $TCZLIB

echo -e "Title:\t\t$TCZLIB" > $TCZLIBINFO
echo -e "Description:\tDigital CD audio extraction program." >> $TCZLIBINFO
echo -e "Version:\t$CDRKITVERSION" >> $TCZLIBINFO
echo -e "Author:\t\tMark Hobley" >> $TCZLIBINFO
echo -e "Original-site:\thttps://sourceforge.net/projects/wodim/" >> $TCZLIBINFO
echo -e "Copying-policy:\tGPL" >> $TCZLIBINFO
echo -e "Size:\t\t$(ls -lk $TCZLIB | awk '{print $5}')k" >> $TCZLIBINFO
echo -e "Extension_by:\tpiCorePlayer team: https://sites.google.com/site/picoreplayer" >> $TCZLIBINFO
echo -e "\t\tCompiled for piCore 8.x" >> $TCZLIBINFO

