#!/bin/bash

UCSPI=ucspi-tcp
UCSPIVERSION=0.88
SRC=$UCSPI-$UCSPIVERSION
SRCTAR=${UCSPI}-${UCSPIVERSION}.tar.gz
STARTDIR=`pwd`
LOG=$PWD/config.log
OUTPUT=$PWD/${UCSPI}-build
TCZ=pcp-$UCSPI.tcz
TCZINFO=$TCZ.info
 
# Build requires these extra packages in addition to the debian stretch 9.3+ build tools
# sudo apt-get install fakeroot

## Start
echo "Most log mesages sent to $LOG... only 'errors' displayed here"
date > $LOG

## Build

if [ -d $OUTPUT ]; then
	echo "Removing old install..."
	sudo rm -rf $OUTPUT >> $LOG
fi

mkdir -p $OUTPUT/{usr/local/bin,usr/local/share/pcp-$UCSPI} >> $LOG

if [ -d $SRC ]; then
	echo "Removing old sources..."
	rm -rf $SRC >> $LOG
fi

if [ ! -f $SRCTAR ]; then
	wget -O $SRCTAR http://cr.yp.to/$UCSPI/$UCSPI-$UCSPIVERSION.tar.gz
fi

echo "Extracting source..."
if [ -f $SRCTAR ]; then
	bsdtar -xf $SRCTAR >> $LOG
	cp -p $STARTDIR/conf-* $SRC
else
	echo "Source download failed."
	exit
fi

cd $STARTDIR >> $LOG

echo "Compiling..."
./compile-ucspi-tcp.sh $SRC $OUTPUT >> $LOG

echo "Creating $TCZs..."

cp -p $SRC/tcpserver $OUTPUT/usr/local/bin || exit 1
cp -p $SRC/debian/copyright $OUTPUT/usr/local/share/pcp-$UCSPI/COPYING || exit 1

find $OUTPUT/usr/local/bin -type f -exec strip --strip-unneeded {} \; >> $LOG

mkdir -p $OUTPUT/usr/local/bin

cd $OUTPUT >> $LOG

find * -not -type d > $STARTDIR/${TCZ}.list

cd $STARTDIR >> $LOG

if [ -f $TCZ ]; then
	rm $TCZ >> $LOG
fi

mksquashfs $OUTPUT $TCZ -all-root >> $LOG
md5sum `basename $TCZ` > ${TCZ}.md5.txt

echo "$TCZ contains"
unsquashfs -ll $TCZ

echo -e "Title:\t\t$TCZ" > $TCZINFO
echo -e "Description:\tCommand-line tool for building TCP server applications." >> $TCZINFO
echo -e "Version:\t$UCSPIVERSION" >> $TCZINFO
echo -e "Authors:\tD.J. Bernstein" >> $TCZINFO
echo -e "Original-site:\thttp://cr.yp.to/ucspi-tcp.html" >> $TCZINFO
echo -e "Copying-policy:\tPublic Domain" >> $TCZINFO
echo -e "Size:\t\t$(ls -lk $TCZ | awk '{print $5}')k" >> $TCZINFO
echo -e "Extension_by:\tpiCorePlayer team: https://www.picoreplayer.org" >> $TCZINFO
echo -e "\t\tCompiled for piCore 10.x" >> $TCZINFO
