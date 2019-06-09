#!/bin/bash

STREAM=streamer
STREAMVERSION=1.00
SRC=$STREAM-$STREAMVERSION
SRCTAR=${STREAM}-${STREAMVERSION}.tar.gz
STARTDIR=`pwd`
LOG=$PWD/config.log
OUTPUT=$PWD/${STREAM}-build
TCZ=pcp-$STREAM.tcz
TCZINFO=$TCZ.info
 
## Start
echo "Most log mesages sent to $LOG... only 'errors' displayed here"
date > $LOG

## Build

if [ -d $OUTPUT ]; then
	echo "Removing old install..."
	sudo rm -rf $OUTPUT >> $LOG
fi

mkdir -p $OUTPUT/usr/local/{bin,share/pcp-$STREAM,etc/init.d} >> $LOG

cd $STARTDIR >> $LOG

echo "Creating $TCZs..."

cp -p $STARTDIR/tcpserver $OUTPUT/usr/local/bin || exit 1
cp -p $STARTDIR/pcp-stream.sh $OUTPUT/usr/local/bin || exit 1
cp -p $STARTDIR/streamer $OUTPUT/usr/local/etc/init.d || exit 1
cp -p $STARTDIR/COPYING $OUTPUT/usr/local/share/pcp-$STREAM || exit 1

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
echo -e "Description:\tStream audio from sound card line-in." >> $TCZINFO
echo -e "\t\tIncludes ucspi-tcp 0.88 tcpserver command line utility." >> $TCZINFO
echo -e "Original-site:  http://cr.yp.to/ucspi-tcp.html" >> $TCZINFO
echo -e "Version:\t$STREAMVERSION" >> $TCZINFO
echo -e "Authors:\tRalph Irving" >> $TCZINFO
echo -e "Copying-policy:\tPublic Domain" >> $TCZINFO
echo -e "Size:\t\t$(ls -lk $TCZ | awk '{print $5}')k" >> $TCZINFO
echo -e "Extension_by:\tpiCorePlayer team: https://www.picoreplayer.org" >> $TCZINFO
echo -e "\t\tCompiled for piCore 10.x" >> $TCZINFO
