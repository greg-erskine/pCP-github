#!/bin/bash

WAV35=wav35skin
WAV35VERSION=1.0
SRC=jivelite-wav.zip
STARTDIR=`pwd`
LOG=$PWD/config.log
OUTPUT=$PWD/${WAV35}-build
TCZLIB=pcp-jivelite_${WAV35}.tcz
TCZLIBINFO=pcp-jivelite_${WAV35}.tcz.info
 
# Build requires these extra packages for debian jessie 8.3+
# sudo apt-get install squashfs-tools unzip

## Start
echo "Most log mesages sent to $LOG... only 'errors' displayed here"
date > $LOG

## Build

if [ -d $OUTPUT ]; then
	echo "Removing old install..."
	rm -rf $OUTPUT >> $LOG
fi

mkdir -p $OUTPUT >> $LOG

if [ ! -f $SRC ]; then
	wget http://www.pughx2.com/assets/px2/files/$SRC
fi

echo "Extracting skin..."
if [ -f $SRC ]; then
	unzip -q -o -d $OUTPUT $SRC >> $LOG
else
	echo "Source download failed."
	exit
fi

mkdir -p $OUTPUT/opt/jivelite/share/jive/applets/SetupWallpaper/wallpaper
mv $OUTPUT/Jivelite/Wav35Skin $OUTPUT/opt/jivelite/share/jive/applets
find $OUTPUT/opt/jivelite/share/jive/applets -type f -name '*.db' -exec rm {} \;
mv $OUTPUT/Jivelite/SetupWallpaper/wallpaper/wav_* $OUTPUT/opt/jivelite/share/jive/applets/SetupWallpaper/wallpaper
mv $OUTPUT/opt/jivelite/share/jive/applets/Wav35Skin/images/UNOFFICIAL/VUMeter/vu_analog_25seq_?.png $STARTDIR || exit 1

rm -rf $OUTPUT/Jivelite

cd $OUTPUT/opt/jivelite/share/jive/applets/Wav35Skin
patch -p0 -i $STARTDIR/wav35skin-remove-nocturneWallpaper.patch || exit 2
cd $STARTDIR

echo "Creating $TCZs..."

cd $STARTDIR >> $LOG

if [ -f $TCZLIB ]; then
	rm $TCZLIB >> $LOG
fi

mksquashfs $OUTPUT $TCZLIB -all-root -no-progress >> $LOG
md5sum `basename $TCZLIB` > ${TCZLIB}.md5.txt

cd $OUTPUT
find * -not -type d > $STARTDIR/$TCZLIB.list
cd $STARTDIR

echo -e "Title:\t\t$TCZLIB" > $TCZLIBINFO
echo -e "Description:\tWaveshare 3.5\" TFT LCD Touch Screen jivelite skin." >> $TCZLIBINFO
echo -e "Version:\t$WAV35VERSION" >> $TCZLIBINFO
echo -e "Author:\t\tnowhinjing" >> $TCZLIBINFO
echo -e "Original-site:\thttp://www.pughx2.com/" >> $TCZLIBINFO
echo -e "Copying-policy:\tGPL" >> $TCZLIBINFO
echo -e "Size:\t\t$(ls -lk $TCZLIB | awk '{print $5}')k" >> $TCZLIBINFO
echo -e "Extension_by:\tpiCorePlayer team: https://sites.google.com/site/picoreplayer" >> $TCZLIBINFO
echo -e "\t\tPackaged for piCore 8.x" >> $TCZLIBINFO

. ./create-default-wav35skin-tcz.sh

. ./create-vumeters-wav35skin-tcz.sh
