#!/bin/bash

OPUS=opus
OPUSVERSION=1.3.1
SRC=$OPUS-$OPUSVERSION
SRCTAR=${OPUS}-${OPUSVERSION}.tar.gz
OPUSFILE=opusfile
OPUSFILEVERSION=0.11
OPUSFILESRC=${OPUSFILE}-${OPUSFILEVERSION}
OPUSFILETAR=$OPUSFILESRC.tar.gz
STARTDIR=`pwd`
LOG=$PWD/config.log
OUTPUT=$PWD/${OPUS}-build
OUTPUTDEV=$PWD/${OPUS}-build-dev
TCZ=pcp-lib${OPUS}.tcz
TCZINFO=pcp-lib${OPUS}.tcz.info
TCZDEV=pcp-lib${OPUS}-dev.tcz
TCZDEVINFO=pcp-lib${OPUS}-dev.tcz.info
PCPREPO=10.x/armv6
 
# Build requires these extra packages in addition to the debian stretch 9.3+ build tools
# sudo apt-get install squashfs-tools bsdtar bison

## Start
echo "Most log mesages sent to $LOG... only 'errors' displayed here"
date > $LOG

## Build
if [ -d $OUTPUT ]; then
	echo "Removing old install..."
	rm -rf $OUTPUT >> $LOG
fi

mkdir -p $OUTPUT/{usr/local/lib,usr/local/include,usr/local/share/pcp-$OPUS} >> $LOG

if [ -d $OUTPUTDEV ]; then
        rm -rf $OUTPUTDEV >> $LOG
fi

mkdir -p $OUTPUTDEV/usr/local/{lib,share/aclocal}

if [ -d $SRC ]; then
	echo "Removing old sources..."
	rm -rf $SRC >> $LOG
fi

if [ -d $OPUSFILESRC ]; then
	rm -rf $OPUSFILESRC >> $LOG
fi

echo "Extracting source..."
if [ ! -f $SRCTAR ]; then
	wget -q https://archive.mozilla.org/pub/opus/$SRCTAR >> $LOG
fi

bsdtar -xf $SRCTAR >> $LOG

if [ ! -f $OPUSFILETAR ]; then
	wget -q https://downloads.xiph.org/releases/opus/$OPUSFILETAR >> $LOG
fi

bsdtar -xf $OPUSFILETAR >> $LOG

PKG=pcp-libogg-dev.tcz
wget -q -O $STARTDIR/$PKG http://repo.picoreplayer.org/repo/$PCPREPO/tcz/$PKG
unsquashfs -n -d $STARTDIR/squashfs-root $STARTDIR/$PKG
cp -pr $STARTDIR/squashfs-root/usr/local/include/* $OUTPUT/usr/local/include
rm -rf $STARTDIR/squashfs-root
rm $STARTDIR/$PKG

PKG=pcp-libogg.tcz
wget -q -O $STARTDIR/$PKG http://repo.picoreplayer.org/repo/$PCPREPO/tcz/$PKG
unsquashfs -n -d $STARTDIR/squashfs-root $STARTDIR/$PKG
cp -pr $STARTDIR/squashfs-root/usr/local/lib/* $OUTPUT/usr/local/lib
rm -rf $STARTDIR/squashfs-root
rm $STARTDIR/$PKG

cd $STARTDIR >> $LOG

echo "Compiling..."
./compile-opus.sh $SRC $OUTPUT $OPUSFILESRC >> $LOG

echo "Creating $TCZs..."

mv $OUTPUT/usr/local/share/doc/opusfile/COPYING $OUTPUT/usr/local/share/pcp-$OPUS/ || exit 1
rm -rf $OUTPUT/usr/local/include/ogg
rm -rf $OUTPUT/usr/local/lib/libogg*
mv $OUTPUT/usr/local/include $OUTPUTDEV/usr/local
mv $OUTPUT/usr/local/lib/*a $OUTPUTDEV/usr/local/lib
mv $OUTPUT/usr/local/lib/pkgconfig $OUTPUTDEV/usr/local/lib
mv $OUTPUT/usr/local/share/aclocal $OUTPUTDEV/usr/local/share

rm -rf $OUTPUT/usr/local/share/doc

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
echo -e "Description:\tHigh-level API for basic manipulation of Ogg Opus audio streams." >> $TCZINFO
echo -e "Version:\t$OPUSVERSION" >> $TCZINFO
echo -e "Authors:\tTimothy B. Terriberry, Ralph Giles" >> $TCZDEVINFO
echo -e "Original-site:\thttp://opus-codec.org/" >> $TCZINFO
echo -e "Copying-policy:\tGPL" >> $TCZINFO
echo -e "Size:\t\t$(ls -lk $TCZ | awk '{print $5}')k" >> $TCZINFO
echo -e "Extension_by:\tpiCorePlayer team: https://www.picoreplayer.org" >> $TCZINFO
echo -e "\t\tCompiled for piCore 10.x" >> $TCZINFO

cd $OUTPUTDEV >> $LOG
find * -not -type d > $STARTDIR/${TCZDEV}.list

cd $STARTDIR

if [ -f $TCZDEV ]; then
	rm $TCZDEV >> $LOG
fi

mksquashfs $OUTPUTDEV $TCZDEV -all-root >> $LOG
md5sum $TCZDEV > ${TCZDEV}.md5.txt

echo "$TCZDEV contains"
unsquashfs -ll $TCZDEV

echo -e "Title:\t\t$TCZDEV" > $TCZDEVINFO
echo -e "Description:\tHigh-level API for basic manipulation of Ogg Opus audio streams development files." >> $TCZDEVINFO
echo -e "Version:\t$OPUSVERSION" >> $TCZDEVINFO
echo -e "Authors:\tTimothy B. Terriberry, Ralph Giles" >> $TCZDEVINFO
echo -e "Original-site:\thttp://opus-codec.org/" >> $TCZDEVINFO
echo -e "Copying-policy:\tGPL" >> $TCZDEVINFO
echo -e "Size:\t\t$(ls -lk $TCZDEV | awk '{print $5}')k" >> $TCZDEVINFO
echo -e "Extension_by:\tpiCorePlayer team: https://www.picoreplayer.org" >> $TCZDEVINFO
echo -e "\t\tCompiled for piCore 10.x" >> $TCZDEVINFO
