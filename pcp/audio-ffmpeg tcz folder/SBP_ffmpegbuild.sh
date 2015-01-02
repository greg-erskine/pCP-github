#!/bin/sh

FFMPEG=ffmpeg
FFMPEGVERSION=2.5
SRC=${FFMPEG}
LOG=$PWD/config.log
OUTPUT=$PWD/${FFMPEG}-build
TCZ=audio-${FFMPEG}.tcz

# Build requires these extra packages in addition to the raspbian 7.6 build tools
# sudo apt-get install squashfs-tools bsdtar

## Start
echo "Most log mesages sent to $LOG... only 'errors' displayed here"
date > $LOG

# Clean up
if [ -d $OUTPUT ]; then
	rm -rf $OUTPUT >> $LOG
fi

if [ -d $SRC ]; then
	rm -rf $SRC >> $LOG
fi

## Build
#echo "Untarring..."
#sudo wget -O $SRC.tar.bz2 http://www.ffmpeg.org/releases/ffmpeg-snapshot.tar.bz2
#sudo tar -jxf $SRC.tar.bz2 >> $LOG

#Better method
echo "get source"
git clone --depth 1 git://git.videolan.org/ffmpeg



echo "Configuring..."
cd $SRC >> $LOG
./configure \
    --prefix=/usr/local \
    --disable-debug \
    --enable-static \
    --disable-avresample \
    --disable-dxva2 \
    --disable-fontconfig \
    --enable-gpl \
    --disable-libass \
    --disable-libbluray \
    --disable-libfreetype \
    --disable-libgsm \
    --disable-libmodplug \
    --disable-libmp3lame \
    --disable-libopencore_amrnb \
    --disable-libopencore_amrwb \
    --disable-libopenjpeg \
    --disable-libopus \
    --disable-libpulse \
    --disable-librtmp \
    --disable-libschroedinger \
    --disable-libspeex \
    --disable-libtheora \
    --disable-libv4l2 \
    --disable-libvorbis \
    --disable-libvpx \
    --disable-libx264 \
    --disable-libxvid \
    --enable-pic \
    --disable-postproc \
    --enable-runtime-cpudetect \
    --enable-shared \
    --disable-swresample \
    --disable-vdpau \
    --enable-version3 \
    --disable-x11grab \
    --disable-zlib \
    --enable-ffmpeg \
    --enable-ffplay \
    --enable-ffprobe \
    --enable-ffserver \
    --extra-ldflags=-Wl,-rpath,/usr/local/lib >> $LOG

echo "Running make"
make >> $LOG
make prefix=$OUTPUT/usr/local install

echo "Building tcz"
cd ../.. >> $LOG

if [ -f $TCZ ]; then
	rm $TCZ >> $LOG
fi

cd $OUTPUT/usr/local >> $LOG
rm -rf include >> $LOG
rm -rf bin >> $LOG
rm -rf share >> $LOG
cd lib >> $LOG
rm -rf pkgconfig >> $LOG
rm -f libavdevice\.* >> $LOG
rm -f libavfilter\.* >> $LOG
rm -f libswscale\.* >> $LOG
rm -f libavcodec.so.56 libavcodec.so libavcodec.a >> $LOG
mv libavcodec.so.56.* libavcodec.so.56 >> $LOG
strip libavcodec.so.56 >> $LOG
rm -f libavformat.so.56 libavformat.so libavformat.a >> $LOG
mv libavformat.so.56.* libavformat.so.56 >> $LOG
strip libavformat.so.56 >> $LOG
rm -f libavutil.so.54 libavutil.so libavutil.a >> $LOG
mv libavutil.so.54.* libavutil.so.54  >> $LOG
strip libavutil.so.54 >> $LOG
cd ../../../../ >> $LOG

# Not needed twice, included in libfaad.tcz. TODO create a separate libcofi.tcz
# cp -p /usr/lib/arm-linux-gnueabihf/libcofi_rpi.so $OUTPUT/usr/lib/ >> $LOG

mksquashfs $OUTPUT $TCZ -all-root >> $LOG
md5sum $TCZ > ${TCZ}.md5.txt

echo "$TCZ contains"
unsquashfs -ll $TCZ > $TCZ.tcz.lst


#Find file size to be used below
FILESIZE=$(stat -c%s "$TCZ")

###################################################
# Create info extension in temp dir                #
###################################################
echo "create info file"

echo "Title:          audio-ffmpeg.tcz
Description:    This small audio ffmpeg package contains codecs for wma and ALAC decoding via ffmpeg. 
                It is aimed at supporting high quality audio.
Version:        2.5
Author:         
Original-site:  https://www.ffmpeg.org/ 
Copying-policy: FFmpeg is licensed under the GNU Lesser General Public License (LGPL) version 2.1 or later. 
                However, FFmpeg incorporates several optional parts and optimizations that are covered by 
		  the GNU General Public License (GPL) version 2 or later. If those parts get used the GPL applies to all of FFmpeg.
Size:		  $FILESIZE b 
Extension_by:   SBP modified the build script provided by Ralph Irving (https://github.com/ralph-irving/tcz-libffmpeg)
Tags:	    	  audio-ffmpeg supports wma and ALAC decoding via ffmpeg library.
Comments:       Binaries only
                ----
                Compiled for piCore 6.x with
                ----
                PPI compatible
Change-log:     2015/2/1 First version, 2.5" > /tmp/audio-ffmpeg.info







