#!/bin/bash

WAV35=default-wav35skin
WAV35VERSION=1.0
SRC=DesktopJive
STARTDIR=`pwd`
LOG=$PWD/config.log
OUTPUT=$PWD/${WAV35}-build
TCZLIB=pcp-jivelite_${WAV35}.tcz
TCZLIBINFO=pcp-jivelite_${WAV35}.tcz.info
 
# Build requires these extra packages for debian jessie 8.3+
# sudo apt-get install squashfs-tools subversion

## Start
echo "Most log mesages sent to $LOG... only 'errors' displayed here"
date > $LOG

## Build

if [ -d $OUTPUT ]; then
	echo "Removing old install..."
	rm -rf $OUTPUT >> $LOG
fi

mkdir -p $OUTPUT/opt/jivelite/share/lua/5.1/applets >> $LOG
cd $OUTPUT/opt/jivelite/share/lua/5.1/applets >> $LOG

if [ ! -d $SRC ]; then
	svn export https://github.com/ralph-irving/jivelite.git/trunk/share/jive/applets/DesktopJive
	sed -i "s#HDSkin-VGA#Wav35Skin#" DesktopJive/DesktopJiveMeta.lua
	sed -i "s#loadPriority=1#loadPriority=0#" DesktopJive/loadPriority.lua
fi

echo "Extracting skin..."
if [ ! -d $SRC ]; then
	echo "Source export failed."
	exit
fi

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
echo -e "Description:\tSet Waveshare 3.5\" TFT LCD jivelite skin as default." >> $TCZLIBINFO
echo -e "Version:\t$WAV35VERSION" >> $TCZLIBINFO
echo -e "Author:\t\tRalph Irving" >> $TCZLIBINFO
echo -e "Original-site:\thttp://www.pughx2.com/" >> $TCZLIBINFO
echo -e "Copying-policy:\tGPLv3" >> $TCZLIBINFO
echo -e "Size:\t\t$(ls -lk $TCZLIB | awk '{print $5}')k" >> $TCZLIBINFO
echo -e "Extension_by:\tpiCorePlayer team: https://sites.google.com/site/picoreplayer" >> $TCZLIBINFO
echo -e "\t\tPackaged for piCore 8.x" >> $TCZLIBINFO
