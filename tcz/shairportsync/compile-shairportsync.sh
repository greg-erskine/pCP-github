#!/bin/bash

if [ ! -d shairport-sync ]; then
	git clone https://github.com/mikebrady/shairport-sync.git
	cd shairport-sync
	autoreconf -i -f
fi

if [ -d shairport-sync ]; then
	cd shairport-sync
	git pull
	make clean
fi

aclocal -I .                   && \
autoheader                     && \
libtoolize --automake --copy   && \
automake --add-missing --copy  && \
autoconf || exit 1

./configure --with-alsa --with-tinysvcmdns --with-ssl=openssl --with-soxr --with-stdout --with-pipe --with-metadata || exit 2

make

if [ -f shairport-sync ]; then
	rm shairport-sync
	gcc -Wl,-rpath,/usr/local/lib -s -O2 -o shairport-sync shairport.o rtsp.o mdns.o mdns_external.o common.o rtp.o player.o alac.o audio.o loudness.o mdns_tinysvcmdns.o tinysvcmdns.o audio_alsa.o audio_stdout.o audio_pipe.o -lasound /usr/lib/arm-linux-gnueabihf/libsoxr.a /usr/lib/gcc/arm-linux-gnueabihf/4.9/libgomp.a /usr/lib/arm-linux-gnueabihf/libssl.a /usr/lib/arm-linux-gnueabihf/libcrypto.a /usr/lib/arm-linux-gnueabihf/libconfig.a /usr/lib/arm-linux-gnueabihf/libpopt.a /usr/lib/arm-linux-gnueabihf/libdaemon.a -lm -lpthread -lrt -ldl -lz
fi

if [ ! -d shairport-sync-metadata-reader ]; then
	git clone https://github.com/mikebrady/shairport-sync-metadata-reader
	cd shairport-sync-metadata-reader
	autoreconf -i -f
fi

if [ -d shairport-sync-metadata-reader ]; then
	cd shairport-sync-metadata-reader
	git pull
	make clean
fi

./configure

make
strip shairport-sync-metadata-reader
