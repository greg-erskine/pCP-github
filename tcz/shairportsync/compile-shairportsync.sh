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

./configure --with-alsa --with-tinysvcmdns --with-ssl=openssl --with-soxr --with-stdout

make

if [ -f shairport-sync ]; then
	rm shairport-sync
	gcc -Wno-multichar -Wl,-rpath,/usr/local/lib -s -o shairport-sync shairport.o rtsp.o mdns.o mdns_external.o common.o rtp.o player.o alac.o audio.o  mdns_tinysvcmdns.o tinysvcmdns.o audio_alsa.o audio_stdout.o -lasound -lavahi-common -lavahi-client /usr/lib/arm-linux-gnueabihf/libsoxr.a /usr/lib/gcc/arm-linux-gnueabihf/4.6/libgomp.a /usr/lib/arm-linux-gnueabihf/libssl.a /usr/lib/arm-linux-gnueabihf/libcrypto.a /usr/lib/arm-linux-gnueabihf/libconfig.a /usr/lib/arm-linux-gnueabihf/libpopt.a -lm -lpthread -ldaemon -lrt -ldl -lz
fi
