#!/bin/sh

TS=libts
TSVERSION=kergoth
SRC=${TS}-$TSVERSION
LOG=$PWD/config.log
OUTPUT=$PWD/${TS}-build
TCZ=${TS}.tcz
TCZINFO=${TCZ}.info

# Build requires these extra packages in addition to the raspbian 7.6 build tools
# sudo apt-get install squashfs-tools bsdtar

## Start
echo "Most log mesages sent to $LOG... only 'errors' displayed here"
date > $LOG

## Build
echo "Cleaning up..."

if [ -d $OUTPUT ]; then
	sudo rm -rf $OUTPUT >> $LOG
fi

mkdir -p $OUTPUT

if [ ! -d $SRC ]; then
	git clone https://github.com/kergoth/tslib $SRC >> $LOG
	cd $SRC >> $LOG
fi

if [ -d $SRC ]; then
        cd $SRC
        if [ -d autom4te.cache ]; then
                rm -rf autom4te.cache
        fi
        patch -R -p1 -i $OUTPUT/../add-libts-kergoth-version.patch >> $LOG || exit 1
        patch -R -p1 -i $OUTPUT/../ts-calibrate-fix-edges.patch >> $LOG || exit 1
	
        git pull >> $LOG
fi

patch -p1 -i $OUTPUT/../add-libts-kergoth-version.patch >> $LOG || exit 1
patch -p1 -i $OUTPUT/../ts-calibrate-fix-edges.patch >> $LOG || exit 1

make distclean >> $LOG
./autogen-clean.sh
./autogen.sh

echo "Configuring..."
export CFLAGS="-s -O2"
export CPPFLAGS="${CFLAGS}"
export CXXFLAGS="${CFLAGS}"
export LDFLAGS="-s"

./configure --prefix=/usr/local --enable-shared=yes --enable-static=no >> $LOG

echo "Running make"
make >> $LOG
make DESTDIR=$OUTPUT install >> $LOG

cd $OUTPUT/usr/local

rm -rf include
rm -rf lib/pkgconfig
if [ -d share/man ]; then
	rm -rf share/man
fi
find lib -name '*\.la' -exec rm {} \;

if [ -d etc ]; then
	rm -rf etc
fi
mkdir etc
mkdir -p share/libts/files
cp -p $OUTPUT/../ts.conf share/libts/files >> $LOG
cp -p $OUTPUT/../pointercal share/libts/files >> $LOG

mkdir tce.installed >> $LOG
cp -p $OUTPUT/../tce.libts tce.installed/libts >> $LOG

sudo chown -Rh root:root $OUTPUT >> $LOG

sudo chown -R tc:staff tce.installed >> $LOG
sudo chmod 755 tce.installed/libts >> $LOG
sudo chown tc:staff share/libts/files/* >> $LOG
sudo chmod 664 share/libts/files/* >> $LOG

echo "Building tcz"
cd $OUTPUT >> $LOG

find * -not -type d > $OUTPUT/../${TCZ}.list

cd $OUTPUT/.. >> $LOG

if [ -f $TCZ ]; then
	rm $TCZ >> $LOG
fi

mksquashfs $OUTPUT $TCZ >> $LOG
md5sum `basename $TCZ` > ${TCZ}.md5.txt

echo "$TCZ contains"
unsquashfs -ll $TCZ

echo -e "Title:\t\t$TCZ" > $TCZINFO
echo -e "Description:\tC library for filtering touchscreen events" >> $TCZINFO
echo -e "Version:\t$(grep ^VERSION $SRC/Makefile | awk '{printf "%s", $3}')" >> $TCZINFO
echo -e "Commit:\t\t$(cd $SRC; git show | grep commit | awk '{print $2}')" >> $TCZINFO
echo -e "Author:\t\tMartin Kepplinger" >> $TCZINFO
echo -e "Original-site:\t$(grep url $SRC/.git/config | awk '{print $3}')" >> $TCZINFO
echo -e "Copying-policy:\tLGPLv2" >> $TCZINFO
echo -e "Size:\t\t$(ls -lk $TCZ | awk '{print $5}')k" >> $TCZINFO
echo -e "Extension_by:\tpiCorePlayer team: https://www.picoreplayer.org" >> $TCZINFO
echo -e "\t\tCompiled for piCore 9.x" >> $TCZINFO
