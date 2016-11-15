#!/bin/bash

if [ -z $2 ]; then
	echo "Usage $0 compilefolder installfolder"
	exit
fi

echo "Using $2 for DESTDIR"

cd $1

export CFLAGS="-march=armv6 -mfloat-abi=hard -mfpu=vfp -s"

./configure \
    --prefix=/usr/local \
    --disable-debug \
    --disable-static \
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
    --disable-libxcb \
    --disable-libxcb-shm \
    --disable-libxcb-xfixes \
    --disable-libxcb-shape \
    --disable-sdl \
    --disable-doc \
    --enable-pic \
    --disable-postproc \
    --enable-runtime-cpudetect \
    --enable-shared \
    --enable-swresample \
    --disable-vdpau \
    --enable-version3 \
    --disable-x11grab \
    --disable-iconv \
    --disable-xlib \
    --disable-zlib \
    --disable-bzlib \
    --extra-ldflags="-Wl,-rpath,/usr/local/lib -s"

make -j 4 || return 1

#make DESTDIR=$1 install-headers
#make DESTDIR=$1 install-libs
make DESTDIR=$2 install
