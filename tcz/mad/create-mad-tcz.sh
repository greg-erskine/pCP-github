#!/bin/bash

MAD=libmad
MADVERSION=0.15.1b
SRC=$MAD-$MADVERSION
STARTDIR=`pwd`
LOG=$PWD/config.log
OUTPUT=$PWD/${MAD}-build
TCZLIB=pcp-${MAD}.tcz
TCZLIBINFO=pcp-${MAD}.tcz.info
 
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
	if [ ! -f $SRC-8.tar.gz ]; then
		echo "Should be including the repository."
		exit
	fi
	echo "Extracting source..."
	if [ -f $SRC-8.tar.gz ]; then
		bsdtar -xf $SRC-8.tar.gz >> $LOG
	else
		echo "Source download failed."
		exit
	fi
fi

echo "Compiling..."
./compile-mad.sh $SRC $OUTPUT >> $LOG

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

echo -e "usr/local/lib/libmad.la\nusr/local/include" > $STARTDIR/onlylib
mksquashfs $OUTPUT $TCZLIB -all-root -ef $STARTDIR/onlylib >> $LOG
md5sum `basename $TCZLIB` > ${TCZLIB}.md5.txt
rm $STARTDIR/onlylib

echo "$TCZLIB contains"
unsquashfs -ll $TCZLIB

echo -e "Title:\t\t$TCZLIB" > $TCZLIBINFO
echo -e "Description:\tMPEG Audio Decoder library." >> $TCZLIBINFO
echo -e "Version:\t$MADVERSION" >> $TCZLIBINFO
echo -e "Author:\t\tRobert Leslie" >> $TCZLIBINFO
echo -e "Original-site:\thttp://www.underbit.com/products/mad/" >> $TCZLIBINFO
echo -e "Copying-policy:\tGPL" >> $TCZLIBINFO
echo -e "Size:\t\t$(ls -lk $TCZLIB | awk '{print $5}')k" >> $TCZLIBINFO
echo -e "Extension_by:\tpiCorePlayer team: https://sites.google.com/site/picoreplayer" >> $TCZLIBINFO
echo -e "\t\tCompiled for piCore 8.x" >> $TCZLIBINFO

