#!/bin/bash

MPG123=mpg123
MPG123VERSION=1.23.8
SRC=$MPG123-$MPG123VERSION
STARTDIR=`pwd`
LOG=$PWD/config.log
OUTPUT=$PWD/${MPG123}-build
TCZLIB=pcp-lib${MPG123}.tcz
TCZLIBINFO=pcp-lib${MPG123}.tcz.info
TCZ=pcp-${MPG123}.tcz
TCZINFO=pcp-${MPG123}.tcz.info
 
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
		wget https://www.mpg123.de/download/$SRC.tar.bz2
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
./compile-mpg123.sh $SRC $OUTPUT >> $LOG

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
echo -e "Description:\tMPEG 1.0/2.0/2.5 audio decoder command line tool." >> $TCZINFO
echo -e "Version:\t$MPG123VERSION" >> $TCZINFO
echo -e "Author:\t\tMichael Hipp" >> $TCZINFO
echo -e "Original-site:\thttps://www.mpg123.de/" >> $TCZINFO
echo -e "Copying-policy:\tGPLv2" >> $TCZINFO
echo -e "Size:\t\t$(ls -lk $TCZ | awk '{print $5}')k" >> $TCZINFO
echo -e "Extension_by:\tpiCorePlayer team: https://sites.google.com/site/picoreplayer" >> $TCZINFO
echo -e "\t\tCompiled for piCore 8.x" >> $TCZINFO

if [ -f $TCZLIB ]; then
	rm $TCZLIB >> $LOG
fi

echo -e "usr/local/bin\n\nusr/local/lib/libmpg123.la\nusr/local/lib/libout123.la\nusr/local/lib/pkgconfig\nusr/local/include\nusr/local/share" > $STARTDIR/onlylib
mksquashfs $OUTPUT $TCZLIB -all-root -ef $STARTDIR/onlylib >> $LOG
md5sum `basename $TCZLIB` > ${TCZLIB}.md5.txt
rm $STARTDIR/onlylib

echo "$TCZLIB contains"
unsquashfs -ll $TCZLIB

echo -e "Title:\t\t$TCZLIB" > $TCZLIBINFO
echo -e "Description:\tMPEG 1.0/2.0/2.5 audio decoder runtime library." >> $TCZLIBINFO
echo -e "Version:\t$MPG123VERSION" >> $TCZLIBINFO
echo -e "Author:\t\tMichael Hipp" >> $TCZLIBINFO
echo -e "Original-site:\thttps://www.mpg123.de/" >> $TCZLIBINFO
echo -e "Copying-policy:\tGPLv2" >> $TCZLIBINFO
echo -e "Size:\t\t$(ls -lk $TCZLIB | awk '{print $5}')k" >> $TCZLIBINFO
echo -e "Extension_by:\tpiCorePlayer team: https://sites.google.com/site/picoreplayer" >> $TCZLIBINFO
echo -e "\t\tCompiled for piCore 8.x" >> $TCZLIBINFO

