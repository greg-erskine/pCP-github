#!/bin/bash

KSH=ksh
KSHVERSION=93u-20120801-3.1
SRC=$KSH-$KSHVERSION
SRCTAR=${KSH}-${KSHVERSION}.tar.gz
STARTDIR=`pwd`
LOG=$PWD/config.log
OUTPUT=$PWD/${KSH}-build
TCZ=pcp-$KSH.tcz
TCZINFO=pcp-$KSH.tcz.info
 
# Build requires these extra packages in addition to the debian stretch 9.3+ build tools
# sudo apt-get install squashfs-tools bsdtar bison

## Start
echo "Most log mesages sent to $LOG... only 'errors' displayed here"
date > $LOG

## Build
if [ -d $OUTPUT ]; then
	echo "Removing old install..."
	sudo rm -rf $OUTPUT >> $LOG
fi

mkdir -p $OUTPUT/{bin,usr/local/share/pcp-$KSH} >> $LOG

if [ -d $SRC ]; then
	echo "Removing old sources..."
	rm -rf $SRC >> $LOG
fi

echo "Extracting source..."
if [ -f $SRCTAR ]; then
	bsdtar -xf $SRCTAR >> $LOG
else
	echo "Source file not found."
	exit
fi

cd $STARTDIR >> $LOG

echo "Compiling..."
./compile-ksh.sh $SRC $OUTPUT >> $LOG

echo "Creating $TCZs..."

cp -p $SRC/debian/copyright $OUTPUT/usr/local/share/pcp-$KSH/COPYING || exit 1
cp -p $SRC/arch/linux.arm/bin/ksh $OUTPUT/bin || exit 2

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
echo -e "Description:\tReal, AT&T version of the Korn shell." >> $TCZINFO
echo -e "Version:\t$KSHVERSION" >> $TCZINFO
echo -e "Author:\t\tDavid Korn <dgk@research.att.com>" >> $TCZINFO
echo -e "Original-site:\thttp://www.kornshell.com/" >> $TCZINFO
echo -e "Copying-policy:\tBSD-3-clause" >> $TCZINFO
echo -e "Size:\t\t$(ls -lk $TCZ | awk '{print $5}')k" >> $TCZINFO
echo -e "Extension_by:\tpiCorePlayer team: https://www.picoreplayer.org" >> $TCZINFO
echo -e "\t\tCompiled for piCore 10.x" >> $TCZINFO
