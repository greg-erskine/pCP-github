#!/bin/sh

LIRC=lirc
LIRCVERSION=0.9.4d
SRC=${LIRC}-$LIRCVERSION
INPUTLIRC=inputlirc-23
STARTDIR=`pwd`
LOG=$STARTDIR/config.log
OUTPUT=$STARTDIR/${LIRC}-build
OUTPUTDEV=$STARTDIR/${LIRC}-build-dev
TCZ=pcp-${LIRC}.tcz
TCZINFO=pcp-${LIRC}.tcz.info
TCZDEV=pcp-${LIRC}-dev.tcz
TCZDEVINFO=pcp-${LIRC}-dev.tcz.info

# Build requires these extra packages in addition to the raspbian 9.3 build tools
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
mkdir -p $OUTPUT

echo "Untarring..."
bsdtar -xf $SRC.tar.bz2 >> $LOG 

echo "Removing udev development files..."
sudo apt-get -y purge libudev-dev

cd $SRC >> $LOG

make distclean >> $LOG
./autogen.sh

echo "Patching..."
patch -p1 -i $OUTPUT/../lirc-gpio-ir.patch || exit 1

echo "Configuring..."

CC="gcc -s" \
CXX="g++ -s -pipe -fno-exceptions -fno-rtti" \
LDFLAGS="-s -Wl,-rpath,/usr/local/lib" \
./configure \
--prefix=/usr/local \
--sysconfdir=/usr/local/etc \
--enable-static=yes \
--enable-shared=yes \
--without-x  >> $LOG

find . -name Makefile -type f -exec sed -i 's/-g -O2/-O2/g' {} \;
sed -i "s#/usr/local/var/run#/var/run#" paths.h || exit 1

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

cd $STARTDIR

if [ -d $INPUTLIRC ]; then
	rm -rf $INPUTLIRC
fi

bsdtar -xf $STARTDIR/$INPUTLIRC.tar.bz2
cd $INPUTLIRC
make >> $LOG
cp -p $STARTDIR/$INPUTLIRC/inputlircd $OUTPUT/usr/local/sbin

cd $OUTPUT/usr/local || exit 1


find lib -type f -name '*so*' -exec patchelf --set-rpath "/usr/local/lib" {} \;
find sbin -type f -exec patchelf --set-rpath "/usr/local/lib" {} \;
find bin -type f -exec patchelf --set-rpath "/usr/local/lib" {} \;

rm bin/irdb-get
rm bin/irtext2udp
rm bin/pronto2lirc
rm bin/lirc-config-tool
rm bin/lirc-make-devinput
rm bin/lirc-setup
rm sbin/lircd-setup
rm -rf lib/python3.5
rm -rf lib/pkgconfig

find lib -type f -name '*a' -exec rm {} \;

cd $OUTPUT >> $LOG

cp -p $STARTDIR/tce.newlirc $OUTPUT/usr/local/tce.installed/pcp-lirc
cp -p $STARTDIR/lircrc-squeezebox $OUTPUT/usr/local/share/lirc/files
cp -p $STARTDIR/lircd.conf $OUTPUT/usr/local/share/lirc/files/lircd-squeezebox
cp -p $STARTDIR/lirc_options.conf $OUTPUT/usr/local/share/lirc/files
#cp -p $STARTDIR/lircd-jivelite $OUTPUT/usr/local/share/lirc/files
#cp -p $STARTDIR/lircd-jivelite-RMTD116A $OUTPUT/usr/local/share/lirc/files
#cp -p $STARTDIR/lircd-jivelite-justboomIR $OUTPUT/usr/local/share/lirc/files
cp -p $STARTDIR/lircd-justboomIR $OUTPUT/usr/local/share/lirc/files
cp -p $STARTDIR/lircrc-justboomIR $OUTPUT/usr/local/share/lirc/files

mkdir -p $OUTPUTDEV/usr/local/lib
mkdir -p $OUTPUTDEV/usr/local/include
cp -pr $STARTDIR/$SRC/pkg/usr/local/include/* $OUTPUTDEV/usr/local/include
cp -pr $STARTDIR/$SRC/pkg/usr/local/lib/liblirc_client*a $OUTPUTDEV/usr/local/lib

find * -not -type d > $OUTPUT/../${TCZ}.list

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
echo -e "Version:\t$(grep ^VERSION $SRC/VERSION | awk -F[=\"] '{printf "%s",$3}')" >> $TCZINFO
echo -e "Author:\t\tAlec Leamas" >> $TCZINFO
echo -e "Original-site:\thttp://www.lirc.org" >> $TCZINFO
echo -e "Copying-policy:\tGPL" >> $TCZINFO
echo -e "Size:\t\t$(ls -lk $TCZ | awk '{print $5}')k" >> $TCZINFO
echo -e "Extension_by:\tpiCorePlayer team: https://www.picoreplayer.org" >> $TCZINFO
echo -e "Tags:\t\tIR remote control" >> $TCZINFO
echo -e "Comments:\tBinaries only" >> $TCZINFO
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

echo "Reinstalling udev development files.."
sudo apt-get -y install libudev-dev

