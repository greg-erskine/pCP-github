#!/bin/bash

FAAD=faad2
FAADVERSION=2.7
SRC=$FAAD-$FAADVERSION
STARTDIR=`pwd`
LOG=$PWD/config.log
OUTPUT=$PWD/${FAAD}-build
TCZLIB=pcp-lib${FAAD}.tcz
TCZLIBINFO=pcp-lib${FAAD}.tcz.info
TCZ=pcp-${FAAD}.tcz
TCZINFO=pcp-${FAAD}.tcz.info
 
# Build requires these extra packages in addition to the debian stretch 9.2+ build tools
# sudo apt-get install squashfs-tools bsdtar

## Start
echo "Most log mesages sent to $LOG... only 'errors' displayed here"
date > $LOG

## Build

if [ -d $OUTPUT ]; then
	echo "Removing old install..."
	rm -rf $OUTPUT >> $LOG
fi

mkdir -p $OUTPUT >> $LOG

if [ ! -d $SRC ]; then
        git clone https://github.com/ralph-irving/faad2.git $SRC
fi


cd $SRC
git pull

if [ ! -d autom4te.cache ]; then
	sh bootstrap
else
	make distclean
fi

cd $STARTDIR

echo "Compiling..."
./compile-faad.sh $SRC $OUTPUT >> $LOG

echo "Creating $TCZs..."
echo "Creating headers..."

if [ -f $STARTDIR/$SRC-headers.tar.gz ]; then
	rm $STARTDIR/$SRC-headers.tar.gz
fi

cd $OUTPUT/usr/local/include
bsdtar -czf $STARTDIR/$SRC-headers.tar.gz *

find $OUTPUT/usr/local/lib -type f -name '*so*' -exec strip --strip-unneeded {} \;

cd $STARTDIR >> $LOG

if [ -f $TCZ ]; then
	rm $TCZ >> $LOG
fi

echo -e "usr/local/lib\nusr/local/include\nusr/local/share" > $STARTDIR/onlybin
mksquashfs $OUTPUT $TCZ -all-root -ef $STARTDIR/onlybin >> $LOG
md5sum `basename $TCZ` > ${TCZ}.md5.txt
rm $STARTDIR/onlybin

echo "$TCZ contains"
unsquashfs -ll $TCZ

echo -e "Title:\t\t$TCZ" > $TCZINFO
echo -e "Description:\tMPEG-4 and MPEG-2 AAC decoder command line tool." >> $TCZINFO
echo -e "Version:\t$FAADVERSION" >> $TCZINFO
echo -e "Authors:\tM. Bakker,Alexander Kurpiers,Volker Fischer,Gian-Carlo Pascutto" >> $TCZINFO
echo -e "Commit:\t\t$(cd $SRC; git show | grep commit | awk '{print $2}')" >> $TCZINFO
echo -e "Source-site:\t$(grep url $SRC/.git/config | awk '{print $3}')" >> $TCZINFO
echo -e "Original-site:\thttp://www.audiocoding.com/faad2.html" >> $TCZINFO
echo -e "Copying-policy:\tGPLv2" >> $TCZINFO
echo -e "Size:\t\t$(ls -lk $TCZ | awk '{print $5}')k" >> $TCZINFO
echo -e "Extension_by:\tpiCorePlayer team: https://sites.google.com/site/picoreplayer" >> $TCZINFO
echo -e "\t\tCompiled for piCore 9.x" >> $TCZINFO

if [ -f $TCZLIB ]; then
	rm $TCZLIB >> $LOG
fi

echo -e "usr/local/bin\n\nusr/local/lib/libfaad.la\nusr/local/lib/libmp4ff.la\nusr/local/include\nusr/local/share" > $STARTDIR/onlylib
mksquashfs $OUTPUT $TCZLIB -all-root -ef $STARTDIR/onlylib >> $LOG
md5sum `basename $TCZLIB` > ${TCZLIB}.md5.txt
rm $STARTDIR/onlylib

echo "$TCZLIB contains"
unsquashfs -ll $TCZLIB

echo -e "Title:\t\t$TCZLIB" > $TCZLIBINFO
echo -e "Description:\tMPEG-4 and MPEG-2 AAC decoder runtime library." >> $TCZLIBINFO
echo -e "Version:\t$FAADVERSION" >> $TCZLIBINFO
echo -e "Authors:\tM. Bakker,Alexander Kurpiers,Volker Fischer,Gian-Carlo Pascutto" >> $TCZLIBINFO
echo -e "Commit:\t\t$(cd $SRC; git show | grep commit | awk '{print $2}')" >> $TCZLIBINFO
echo -e "Source-site:\t$(grep url $SRC/.git/config | awk '{print $3}')" >> $TCZLIBINFO
echo -e "Original-site:\thttp://www.audiocoding.com/faad2.html" >> $TCZLIBINFO
echo -e "Copying-policy:\tGPLv2" >> $TCZLIBINFO
echo -e "Size:\t\t$(ls -lk $TCZLIB | awk '{print $5}')k" >> $TCZLIBINFO
echo -e "Extension_by:\tpiCorePlayer team: https://sites.google.com/site/picoreplayer" >> $TCZLIBINFO
echo -e "\t\tCompiled for piCore 9.x" >> $TCZLIBINFO

