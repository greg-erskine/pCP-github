#!/bin/bash

SL=squeezelite
SRC=squeezelite
STARTDIR=`pwd`
LOG=$PWD/config.log
OUTPUT=$PWD/${SL}-build
TCZ=pcp-${SL}.tcz
TCZINFO=pcp-${SL}.tcz.info
 
# Build requires these extra packages in addition to the debian jessie 8.3+ build tools
# sudo apt-get install squashfs-tools

## Start
echo "Most log mesages sent to $LOG... only 'errors' displayed here"
date > $LOG

## Build
echo "Cleaning up..."

if [ -d $OUTPUT ]; then
	rm -rf $OUTPUT >> $LOG
fi

mkdir -p $OUTPUT >> $LOG

if [ ! -d $SRC ]; then
        git clone https://github.com/ralph-irving/squeezelite.git
fi


if [ ! -f $SRC/Makefile.pcp ]; then
	bsdtar -cf - Makefile.pcp | (cd $SRC ; bsdtar -xf -)
fi

cd $SRC
git pull
cd $STARTDIR

echo "Extracting header files..."

if [ -d $SRC/include ]; then
	rm -rf $SRC/include
fi
mkdir -p $SRC/include

bsdtar -C$SRC/include -xf $STARTDIR/../ffmpeg/ffmpeg-3.1.10-headers.tar.gz
bsdtar -C$SRC/include -xf $STARTDIR/../flac/flac-1.3.2-headers.tar.gz
bsdtar -C$SRC/include -xf $STARTDIR/../ogg/libogg-1.3.2-headers.tar.gz
bsdtar -C$SRC/include -xf $STARTDIR/../vorbis/libvorbis-1.3.5-headers.tar.gz
bsdtar -C$SRC/include -xf $STARTDIR/../mad/libmad-0.15.1b-headers.tar.gz
bsdtar -C$SRC/include -xf $STARTDIR/../faad/faad2-2.7-headers.tar.gz
bsdtar -C$SRC/include -xf $STARTDIR/../soxr/soxr-0.1.2-Source-headers.tar.gz
bsdtar -C$SRC/include -xf $STARTDIR/../mpg123/mpg123-1.23.8-headers.tar.gz
bsdtar -C$SRC/include -xf $STARTDIR/../lirc/lirc-0.9.0-headers.tar.gz

if [ -d $STARTDIR/squashfs-root ]; then
	rm -rf $STARTDIR/squashfs-root
fi

wget -q -O - http://picoreplayer.sourceforge.net/tcz_repo/8.x/armv6/tcz/wiringpi-dev.tcz > $STARTDIR/wiringpi-dev.tcz
unsquashfs -n -d $STARTDIR/squashfs-root $STARTDIR/wiringpi-dev.tcz
cp -p $STARTDIR/squashfs-root/usr/local/include/wiringPi.h $SRC/include

if [ -d $SRC/lib ]; then
	rm -rf $SRC/lib
fi
mkdir -p $SRC/lib

if [ -d $STARTDIR/squashfs-root ]; then
	rm -rf $STARTDIR/squashfs-root
fi

wget -q -O - http://picoreplayer.sourceforge.net/tcz_repo/8.x/armv6/tcz/wiringpi.tcz > $STARTDIR/wiringpi.tcz
unsquashfs -n -d $STARTDIR/squashfs-root wiringpi.tcz

cp -p $STARTDIR/squashfs-root/usr/local/lib/libwiringPi.so $SRC/lib
cp -p $STARTDIR/../lirc/liblirc_client.a $SRC/lib

echo "Compiling..."

./compile-squeezelite.sh >> $LOG

echo "Creating $TCZ..."
mkdir -p $OUTPUT/usr/local/bin >> $LOG
cp -p $SRC/squeezelite $OUTPUT/usr/local/bin/ >> $LOG
cp -p $SRC/find_servers $OUTPUT/usr/local/bin/ >> $LOG

mkdir -p $OUTPUT/usr/local/etc/init.d >> $LOG
cp -p $STARTDIR/squeezelite.init.d $OUTPUT/usr/local/etc/init.d/squeezelite >> $LOG
chmod 755 $OUTPUT/usr/local/etc/init.d/squeezelite >> $LOG

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
echo -e "Description:\tLightweight headless squeezebox player." >> $TCZINFO
echo -e "Version:\t$($OUTPUT/usr/local/bin/squeezelite -? | grep ^Squeezelite\ v | awk -F'[v,]' '{printf "%s", $2}')" >> $TCZINFO
echo -e "Commit:\t\t$(cd $SRC; git show | grep commit | awk '{print $2}')" >> $TCZINFO
echo -e "Authors:\tAdrian Smith, Ralph Irving" >> $TCZINFO
echo -e "Original-site:\t$(grep url $SRC/.git/config | awk '{print $3}')" >> $TCZINFO
echo -e "Copying-policy:\tGPLv3" >> $TCZINFO
echo -e "Size:\t\t$(ls -lk $TCZ | awk '{print $5}')k" >> $TCZINFO
echo -e "Extension_by:\tpiCorePlayer team: https://sites.google.com/site/picoreplayer" >> $TCZINFO
echo -e "\t\tCompiled for piCore 8.x" >> $TCZINFO
echo -e "Change-log:\t$(cat README.md)" >> $TCZINFO

