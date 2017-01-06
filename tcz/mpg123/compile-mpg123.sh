#!/bin/bash

if [ -z $2 ]; then
	echo "Usage $0 compilefolder installfolder"
	exit
fi

echo "Using $2 for DESTDIR"

cd $1

export CFLAGS="-march=armv6 -mfloat-abi=hard -mfpu=vfp -s"
export LDFLAGS="-Wl,-rpath,/usr/local/lib -s"

./configure \
    --prefix=/usr/local \
    --enable-static=no \
    --with-optimization=4 \
    --with-audio=alsa

make -j 4 || return 1

make DESTDIR=$2 install
