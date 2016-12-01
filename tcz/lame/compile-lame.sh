#!/bin/bash

if [ -z $2 ]; then
	echo "Usage $0 compilefolder installfolder"
	exit
fi

echo "Using $2 for DESTDIR"

cd $1

export CFLAGS="-march=armv6 -mfloat-abi=hard -mfpu=vfp -s"
export LDFLAGS="-Wl,-rpath,/usr/local/lib -s"

./configure --enable-shared=no --with-fileio=lame --enable-nasm --disable-gtktest

make -j 4 || return 1

cd frontend
rm lame
gcc -Wall -pipe -march=armv6 -mfloat-abi=hard -mfpu=vfp -s -Wl,-rpath -Wl,/usr/local/lib -s -o lame lame_main.o main.o brhist.o console.o get_audio.o lametime.o parse.o timestatus.o ../libmp3lame/.libs/libmp3lame.a /usr/lib/arm-linux-gnueabihf/libtinfo.a /usr/lib/arm-linux-gnueabihf/libncurses.a -lm

cd ../
make DESTDIR=$2 install
