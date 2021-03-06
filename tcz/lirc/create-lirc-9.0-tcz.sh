#!/bin/sh

LIRC=lirc
LIRCVERSION=0.9.0
SRC=${LIRC}-$LIRCVERSION
STARTDIR=`pwd`
LOG=$STARTDIR/config.log
OUTPUT=$STARTDIR/${LIRC}-build
OUTPUTDEV=$STARTDIR/${LIRC}-build-dev
TCZ=pcp-${LIRC}.tcz
TCZINFO=pcp-${LIRC}.tcz.info
TCZDEV=pcp-${LIRC}-dev.tcz
TCZDEVINFO=pcp-${LIRC}-dev.tcz.info

# Build requires these extra packages in addition to the raspbian 8.3 build tools
#     sudo apt-get install squashfs-tools bsdtar
# Requires tc userid
#     sudo adduser --uid 1001 --gid 50 --shell /bin/sh tc

## Start
echo "Most log mesages sent to $LOG... only 'errors' displayed here"
date > $LOG

# Clean up
if [ -d $OUTPUT ]; then
        sudo rm -rf $OUTPUT >> $LOG
fi

if [ -d $OUTPUTDEV ]; then
        rm -rf $OUTPUTDEV >> $LOG
fi

if [ -d $SRC ]; then
        rm -rf $SRC >> $LOG
fi

## Build
echo "Untarring..."
bsdtar -xf $SRC.tar.bz2 >> $LOG 

echo "Configuring..."
cd $SRC >> $LOG

CC="gcc -march=armv6 -mfloat-abi=hard -mfpu=vfp -Os -pipe" \
CXX="g++ -march=armv6 -mfloat-abi=hard -mfpu=vfp -Os -pipe -fno-exceptions -fno-rtti" \
LDFLAGS="-s -Wl,-rpath,/usr/local/lib" \
./configure \
--prefix=/usr/local \
--sysconfdir=/usr/local/etc \
--with-driver=userspace \
--enable-sandboxed \
--with-transmitter \
--enable-static=yes \
--enable-shared=yes \
--without-x

find . -name Makefile -type f -exec sed -i 's/-O2 -g/-s/g' {} \;

echo "Running make"
make >> $LOG

if [ -d pkg ]; then
        rm -rf pkg
fi

make install DESTDIR=`pwd`/pkg >> $LOG

echo "Building tcz"
cd $STARTDIR >> $LOG

if [ -f $TCZ ]; then
        rm $TCZ >> $LOG
fi

if [ -f $TCZDEV ]; then
        rm $TCZDEV >> $LOG
fi

mkdir -p $OUTPUT/usr/local/etc/lirc >> $LOG
mkdir -p $OUTPUT/usr/local/share/lirc/files >> $LOG
mkdir -p $OUTPUT/usr/local/tce.installed >> $LOG

cd $STARTDIR/$SRC/pkg/usr/local >> $LOG

bsdtar -cf - bin sbin lib | (cd $OUTPUT/usr/local; bsdtar -xf -)

echo "Creating headers..."
cd $STARTDIR/$SRC/pkg/usr/local/include >> $LOG

if [ -f $STARTDIR/$SRC-headers.tar.gz ]; then
        rm $STARTDIR/$SRC-headers.tar.gz
fi

bsdtar -czf $STARTDIR/$SRC-headers.tar.gz *

cd $OUTPUT >> $LOG

cp -p $STARTDIR/tce.lirc $OUTPUT/usr/local/tce.installed/pcp-lirc
cp -p $STARTDIR/lircrc-squeezebox $OUTPUT/usr/local/share/lirc/files
cp -p $STARTDIR/lircd.conf $OUTPUT/usr/local/share/lirc/files
cp -p $STARTDIR/lircd-justboomIR  $OUTPUT/usr/local/share/lirc/files
cp -p $STARTDIR/lircrc-justboomIR $OUTPUT/usr/local/share/lirc/files

mkdir -p $OUTPUTDEV/usr/local/lib
mkdir -p $OUTPUTDEV/usr/local/include
cp -pr $STARTDIR/$SRC/pkg/usr/local/include/* $OUTPUTDEV/usr/local/include
mv $OUTPUT/usr/local/lib/liblirc_client.la $OUTPUTDEV/usr/local/lib
mv $OUTPUT/usr/local/lib/liblirc_client.a $OUTPUTDEV/usr/local/lib

sudo chown -Rh root:root usr >> $LOG
sudo chown tc:staff usr/local/etc/lirc >> $LOG
sudo chown tc:staff usr/local/tce.installed/pcp-lirc >> $LOG
sudo chown tc:staff usr/local/share/lirc/files/* >> $LOG
sudo chmod 664 usr/local/share/lirc/files/* >> $LOG

sudo chown root:root $OUTPUT

cd $OUTPUT >> $LOG
find * -not -type d > $STARTDIR/${TCZ}.list

cd $STARTDIR
mksquashfs $OUTPUT $TCZ >> $LOG
md5sum $TCZ > ${TCZ}.md5.txt

echo -e "Title:\t\t$TCZ" > $TCZINFO
echo -e "Description:\tLIRC package for remote control" >> $TCZINFO
echo -e "Version:\t$LIRCVERSION" >> $TCZINFO
echo -e "Author:\t\tAlec Leamas" >> $TCZINFO
echo -e "Original-site:\thttp://www.lirc.org" >> $TCZINFO
echo -e "Copying-policy:\tGPL" >> $TCZINFO
echo -e "Size:\t\t$(ls -lk $TCZ | awk '{print $5}')k" >> $TCZINFO
echo -e "Extension_by:\tpiCorePlayer team: https://www.picoreplayer.org" >> $TCZINFO
echo -e "Tags:\tIR remote control" >> $TCZINFO
echo -e "\t\tCompiled for piCore 10.x" >> $TCZINFO

cd $OUTPUTDEV >> $LOG
find * -not -type d > $STARTDIR/${TCZDEV}.list

cd $STARTDIR
mksquashfs $OUTPUTDEV $TCZDEV -all-root >> $LOG
md5sum $TCZDEV > ${TCZDEV}.md5.txt

echo -e "Title:\t\t$TCZDEV" > $TCZDEVINFO
echo -e "Description:\tLIRC remote control development files" >> $TCZDEVINFO
echo -e "Version:\t$LIRCVERSION" >> $TCZDEVINFO
echo -e "Author:\t\tAlec Leamas" >> $TCZDEVINFO
echo -e "Original-site:\thttp://www.lirc.org" >> $TCZDEVINFO
echo -e "Copying-policy:\tGPL" >> $TCZDEVINFO
echo -e "Size:\t\t$(ls -lk $TCZDEV | awk '{print $5}')k" >> $TCZDEVINFO
echo -e "Extension_by:\tpiCorePlayer team: https://www.picoreplayer.org" >> $TCZDEVINFO
echo -e "\t\tCompiled for piCore 10.x" >> $TCZDEVINFO
