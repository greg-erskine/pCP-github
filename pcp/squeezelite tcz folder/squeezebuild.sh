#!/bin/sh
#
######################################################
# Build script for RPI                               #
#                                                    #
# See .info for details                              #
#                                                    #
# Januar 3, 2015                                 #
######################################################

######################################################
# Configure extension creation parameters            #
######################################################

WRKDIR=squeezelite
EXTNAM=squeezelite-armv6hf
TMPDIR=$PWD/squeezelite-armv6hf
EXECUTABLE=squeezelite-armv6hf



######################################################
# Prepare extension creation                         #
######################################################

# Remove dirs and files left from previous creation
echo " remove old traces after previous builds"
rm -r -f $WRKDIR

rm -r -f $TMPDIR
rm -r -f $TMPDIR-dev
rm -r -f $TMPDIR-doc

# Crete temporary directory
mkdir -p $TMPDIR/usr/local

######################################################
# Compile extension                                  #
######################################################

# Get the source in work directory
echo "get files from Github"
git clone https://code.google.com/p/squeezelite/

cd $WRKDIR

#Build with FFMPEG and Soxr (resample) support
OPTS="-DFFMPEG -DRESAMPLE" make -f Makefile 


#Copy squeezelite to correct place
cd ..
cp -f $PWD/$WRKDIR/squeezelite $TMPDIR/usr/local/squeezelite-armv6hf



###################################################
# Create base extension in temp dir               #
###################################################

cd $TMPDIR
cd ..
mksquashfs $TMPDIR $EXTNAM.tcz
cd $TMPDIR
find usr -not -type d > $EXTNAM.tcz.list
mv ../$EXTNAM.tcz .

# Create md5 file
md5sum $EXTNAM.tcz > $EXTNAM.tcz.md5.txt




###################################################
# Create dep extension in temp dir                #
###################################################
echo "create dep file"

echo "alsa.tcz
libasound.tcz
flac.tcz
libmad.tcz 
libvobis.tcz
faad2.tcz
libsoxr.tcz  
audio-ffmpeg.tcz" > $TMPDIR/squeezelite-armv6hf.tcz.dep

#Find file size to be used below
FILESIZE=$(stat -c%s "$EXECUTABLE.tcz")
###################################################
# Create info extension in temp dir                #
###################################################
echo "create info file"

echo "Title:          Squeezelite-armv6hf.tcz
Description:    Squeezelite is a small headless squeezebox emulator for linux using alsa audio output. 
                It is aimed at supporting high quality audio including usb dac based output at multiple sample rates 
                including 44.1/48/88.2/96/176.4/192k/352.8/384kHz. Squeezelite play pcm (wav/aiff) 
                plus flac, mp3, ogg and aac via libFLAC, libmad/libmpg123, libvorbisfile, libfaad respectively if they are present on your machine
Version:        1.7
Author:         Triode alias Adrian Smith
Original-site:  https://code.google.com/p/squeezelite
Copying-policy: Use (squeezelite-armv6hf -t) and see output or See LICENSE file in source
Size:		  $FILESIZE b
Extension_by:   SBP
Tags:	    	  Squeezelite supporting resampling via soxr. Wma and alac decoding via audio-ffmpeg library.
Comments:       Binaries only
                ----
                Compiled for piCore 6.x with  -DFFMPEG and -DRESAMPLE build options
                ----
                PPI compatible
Change-log:     2015/1/3 First version" > $TMPDIR/squeezelite-armv6hf.tcz.info











#################################################
# Clean up tmp directory                        #
#################################################
rm -r -f $PWD/$WRKDIR
rm -r -f $TMPDIR/usr



exit


