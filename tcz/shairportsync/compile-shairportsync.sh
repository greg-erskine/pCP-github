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

./configure --with-alsa --with-tinysvcmdns --with-ssl=openssl --with-soxr --with-stdout --with-pipe --with-metadata --with-convolution

make

if [ -f shairport-sync ]; then
	rm shairport-sync
	# gcc -Wno-multichar -Wl,-rpath,/usr/local/lib -DSYSCONFDIR=\"/usr/local/etc\" -s -O2 -o shairport-sync shairport.o rtsp.o mdns.o mdns_external.o common.o rtp.o player.o alac.o audio.o mdns_tinysvcmdns.o tinysvcmdns.o audio_alsa.o audio_stdout.o audio_pipe.o -lasound /usr/lib/arm-linux-gnueabihf/libsoxr.a /usr/lib/gcc/arm-linux-gnueabihf/4.9/libgomp.a /usr/lib/arm-linux-gnueabihf/libssl.a /usr/lib/arm-linux-gnueabihf/libcrypto.a /usr/lib/arm-linux-gnueabihf/libconfig.a /usr/lib/arm-linux-gnueabihf/libpopt.a /usr/lib/arm-linux-gnueabihf/libdaemon.a -lm -lpthread -lrt -ldl -lz
	g++ -std=c++11 -Wl,-rpath,/usr/local/lib -s -O2 -o shairport-sync shairport.o rtsp.o mdns.o mdns_external.o common.o rtp.o player.o alac.o audio.o loudness.o mdns_tinysvcmdns.o tinysvcmdns.o audio_alsa.o audio_stdout.o audio_pipe.o FFTConvolver/AudioFFT.o FFTConvolver/FFTConvolver.o FFTConvolver/Utilities.o FFTConvolver/convolver.o /usr/lib/arm-linux-gnueabihf/libsndfile.a /usr/lib/arm-linux-gnueabihf/libFLAC.a /usr/lib/arm-linux-gnueabihf/libvorbisfile.a /usr/lib/arm-linux-gnueabihf/libvorbis.a /usr/lib/arm-linux-gnueabihf/libvorbisenc.a /usr/lib/arm-linux-gnueabihf/libogg.a -lasound /usr/lib/arm-linux-gnueabihf/libsoxr.a /usr/lib/gcc/arm-linux-gnueabihf/4.9/libgomp.a /usr/lib/arm-linux-gnueabihf/libssl.a /usr/lib/arm-linux-gnueabihf/libcrypto.a /usr/lib/arm-linux-gnueabihf/libconfig.a /usr/lib/arm-linux-gnueabihf/libpopt.a /usr/lib/arm-linux-gnueabihf/libdaemon.a -lm -lpthread -lrt -ldl
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
