#!/bin/bash

LAME=lame
LAMEVERSION=3.99.5
SRC=$LAME-$LAMEVERSION
SRCTAR=${LAME}-${LAMEVERSION}.tar.gz
STARTDIR=`pwd`
LOG=$PWD/config.log
OUTPUT=$PWD/${LAME}-build
TCZ=pcp-$LAME.tcz
TCZINFO=pcp-$LAME.tcz.info
 
# Build requires these extra packages in addition to the debian jessie 8.3+ build tools
# sudo apt-get install squashfs-tools bsdtar nasm

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
	wget -O $SRCTAR https://sourceforge.net/projects/$LAME/files/$LAME/3.99/$SRCTAR/download
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
./compile-lame.sh $SRC $OUTPUT >> $LOG

echo "Creating $TCZs..."

find $OUTPUT/usr/local/bin -type f -exec strip --strip-unneeded {} \; >> $LOG

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
echo -e "Description:\tA high quality MP3 encoder." >> $TCZINFO
echo -e "Version:\t$LAMEVERSION" >> $TCZINFO
echo -e "Authors:\tRobert Hegemann, Alexander Leidinger, Rogerio Brito" >> $TCZINFO
echo -e "Original-site:\thttp://lame.sourceforge.net/" >> $TCZINFO
echo -e "Copying-policy:\tLGPLv2" >> $TCZINFO
echo -e "Size:\t\t$(ls -lk $TCZ | awk '{print $5}')k" >> $TCZINFO
echo -e "Extension_by:\tpiCorePlayer team: https://sites.google.com/site/picoreplayer" >> $TCZINFO
echo -e "\t\tCompiled for piCore 8.x" >> $TCZINFO

