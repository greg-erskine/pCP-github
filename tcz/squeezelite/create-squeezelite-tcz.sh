#!/bin/bash

SL=squeezelite
SRC=squeezelite
STARTDIR=`pwd`
LOG=$PWD/config.log
OUTPUT=$PWD/${SL}-build
TCZ=pcp-${SL}.tcz
TCZINFO=pcp-${SL}.tcz.info
PCPREPO=10.x/armv6
 
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

cd $SRC
git pull
cd $STARTDIR

echo "Extracting header files..."

if [ -d $SRC/include ]; then
	rm -rf $SRC/include
fi
mkdir -p $SRC/include

if [ -d $SRC/lib ]; then
	rm -rf $SRC/lib
fi
mkdir -p $SRC/lib

if [ -d $STARTDIR/squashfs-root ]; then
	rm -rf $STARTDIR/squashfs-root
fi

PKG=pcp-libffmpeg-dev.tcz
wget -q -O $STARTDIR/$PKG http://repo.picoreplayer.org/repo/$PCPREPO/tcz/$PKG
unsquashfs -n -d $STARTDIR/squashfs-root $STARTDIR/$PKG
cp -pr $STARTDIR/squashfs-root/usr/local/include/* $SRC/include
rm -rf $STARTDIR/squashfs-root
rm $STARTDIR/$PKG

PKG=pcp-libogg-dev.tcz
wget -q -O $STARTDIR/$PKG http://repo.picoreplayer.org/repo/$PCPREPO/tcz/$PKG
unsquashfs -n -d $STARTDIR/squashfs-root $STARTDIR/$PKG
cp -pr $STARTDIR/squashfs-root/usr/local/include/* $SRC/include
rm -rf $STARTDIR/squashfs-root
rm $STARTDIR/$PKG

PKG=pcp-libflac-dev.tcz
wget -q -O $STARTDIR/$PKG http://repo.picoreplayer.org/repo/$PCPREPO/tcz/$PKG
unsquashfs -n -d $STARTDIR/squashfs-root $STARTDIR/$PKG
cp -pr $STARTDIR/squashfs-root/usr/local/include/* $SRC/include
rm -rf $STARTDIR/squashfs-root
rm $STARTDIR/$PKG

PKG=pcp-libvorbis-dev.tcz
wget -q -O $STARTDIR/$PKG http://repo.picoreplayer.org/repo/$PCPREPO/tcz/$PKG
unsquashfs -n -d $STARTDIR/squashfs-root $STARTDIR/$PKG
cp -pr $STARTDIR/squashfs-root/usr/local/include/* $SRC/include
rm -rf $STARTDIR/squashfs-root
rm $STARTDIR/$PKG

PKG=pcp-libmad-dev.tcz
wget -q -O $STARTDIR/$PKG http://repo.picoreplayer.org/repo/$PCPREPO/tcz/$PKG
unsquashfs -n -d $STARTDIR/squashfs-root $STARTDIR/$PKG
cp -pr $STARTDIR/squashfs-root/usr/local/include/* $SRC/include
rm -rf $STARTDIR/squashfs-root
rm $STARTDIR/$PKG

PKG=pcp-libfaad2-dev.tcz
wget -q -O $STARTDIR/$PKG http://repo.picoreplayer.org/repo/$PCPREPO/tcz/$PKG
unsquashfs -n -d $STARTDIR/squashfs-root $STARTDIR/$PKG
cp -pr $STARTDIR/squashfs-root/usr/local/include/* $SRC/include
rm -rf $STARTDIR/squashfs-root
rm $STARTDIR/$PKG

PKG=pcp-libsoxr-dev.tcz
wget -q -O $STARTDIR/$PKG http://repo.picoreplayer.org/repo/$PCPREPO/tcz/$PKG
unsquashfs -n -d $STARTDIR/squashfs-root $STARTDIR/$PKG
cp -pr $STARTDIR/squashfs-root/usr/local/include/* $SRC/include
rm -rf $STARTDIR/squashfs-root
rm $STARTDIR/$PKG

PKG=pcp-libmpg123-dev.tcz
wget -q -O $STARTDIR/$PKG http://repo.picoreplayer.org/repo/$PCPREPO/tcz/$PKG
unsquashfs -n -d $STARTDIR/squashfs-root $STARTDIR/$PKG
cp -pr $STARTDIR/squashfs-root/usr/local/include/* $SRC/include
rm -rf $STARTDIR/squashfs-root
rm $STARTDIR/$PKG

PKG=pcp-lirc-dev.tcz
wget -q -O $STARTDIR/$PKG http://repo.picoreplayer.org/repo/$PCPREPO/tcz/$PKG
unsquashfs -n -d $STARTDIR/squashfs-root $STARTDIR/$PKG
cp -pr $STARTDIR/squashfs-root/usr/local/include/* $SRC/include
rm -rf $STARTDIR/squashfs-root
rm $STARTDIR/$PKG

PKG=pcp-lirc.tcz
wget -q -O $STARTDIR/$PKG http://repo.picoreplayer.org/repo/$PCPREPO/tcz/$PKG
unsquashfs -n -d $STARTDIR/squashfs-root $STARTDIR/$PKG
cp -pr $STARTDIR/squashfs-root/usr/local/lib/* $SRC/lib
rm -rf $STARTDIR/squashfs-root
rm $STARTDIR/$PKG

PKG=wiringpi-dev.tcz
wget -q -O $STARTDIR/$PKG http://repo.picoreplayer.org/repo/$PCPREPO/tcz/$PKG
unsquashfs -n -d $STARTDIR/squashfs-root $STARTDIR/$PKG
cp -pr $STARTDIR/squashfs-root/usr/local/include/* $SRC/include
rm -rf $STARTDIR/squashfs-root
rm $STARTDIR/$PKG

PKG=wiringpi.tcz
wget -q -O $STARTDIR/$PKG http://repo.picoreplayer.org/repo/$PCPREPO/tcz/$PKG
unsquashfs -n -d $STARTDIR/squashfs-root $STARTDIR/$PKG
if [ -f /usr/local/lib/libwiringPi.so ]; then
	cp -pr /usr/local/lib/libwiringPi\.so* $SRC/lib
else
	cp -pr $STARTDIR/squashfs-root/usr/local/lib/* $SRC/lib
fi
rm -rf $STARTDIR/squashfs-root
rm $STARTDIR/$PKG

PKG=openssl-dev.tcz
wget -q -O $STARTDIR/$PKG http://repo.picoreplayer.org/repo/$PCPREPO/tcz/$PKG
unsquashfs -n -d $STARTDIR/squashfs-root $STARTDIR/$PKG
cp -pr $STARTDIR/squashfs-root/usr/local/include/openssl $SRC/include
rm -rf $STARTDIR/squashfs-root
rm $STARTDIR/$PKG

PKG=openssl.tcz
wget -q -O $STARTDIR/$PKG http://repo.picoreplayer.org/repo/$PCPREPO/tcz/$PKG
unsquashfs -n -d $STARTDIR/squashfs-root $STARTDIR/$PKG
cp -pr $STARTDIR/squashfs-root/usr/local/lib/* $SRC/lib
rm -rf $STARTDIR/squashfs-root
rm $STARTDIR/$PKG

PKG=pcp-libopus-dev.tcz
wget -q -O $STARTDIR/$PKG http://repo.picoreplayer.org/repo/$PCPREPO/tcz/$PKG
unsquashfs -n -d $STARTDIR/squashfs-root $STARTDIR/$PKG
cp -pr $STARTDIR/squashfs-root/usr/local/include/opus $SRC/include
rm -rf $STARTDIR/squashfs-root
rm $STARTDIR/$PKG

PKG=pcp-libopus.tcz
wget -q -O $STARTDIR/$PKG http://repo.picoreplayer.org/repo/$PCPREPO/tcz/$PKG
unsquashfs -n -d $STARTDIR/squashfs-root $STARTDIR/$PKG
cp -pr $STARTDIR/squashfs-root/usr/local/lib/* $SRC/lib
rm -rf $STARTDIR/squashfs-root
rm $STARTDIR/$PKG

echo "Compiling..."

./compile-squeezelite.sh >> $LOG

echo "Creating $TCZ..."
mkdir -p $OUTPUT/usr/local/bin >> $LOG
cp -p $SRC/squeezelite $OUTPUT/usr/local/bin/ >> $LOG
cp -p $SRC/squeezelite-dsd $OUTPUT/usr/local/bin/ >> $LOG
cp -p $SRC/find_servers $OUTPUT/usr/local/bin/ >> $LOG
cp -p $SRC/alsacap $OUTPUT/usr/local/bin/ >> $LOG

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
echo -e "Authors:\tAdrian Smith, Ralph Irving, Others" >> $TCZINFO
echo -e "Original-site:\t$(grep url $SRC/.git/config | awk '{print $3}')" >> $TCZINFO
echo -e "Copying-policy:\tGPLv3" >> $TCZINFO
echo -e "Size:\t\t$(ls -lh $TCZ | awk '{print $5}')" >> $TCZINFO
echo -e "Extension_by:\tpiCorePlayer team: https://www.picoreplayer.org" >> $TCZINFO
echo -e "\t\tCompiled for piCore 10.x" >> $TCZINFO
