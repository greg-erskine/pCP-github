#!/bin/bash

if [ ! -d squeezelite ]; then
	exit 1
fi

cd squeezelite

BUILDOPTIONS="-DRESAMPLE -DFFMPEG -DVISEXPORT -DGPIO -DRPI -DIR -DUSE_SSL -DCUSTOM_VERSION=-pCP"

make OPTS="$BUILDOPTIONS -DDSD" clean || exit 2
make CFLAGS="-I./include" LDFLAGS="-s -L./lib" OPTS="$BUILDOPTIONS -DDSD" || exit 3

mv squeezelite squeezelite-dsd

make OPTS="$BUILDOPTIONS -DDSD" clean || exit 4
make CFLAGS="-I./include" LDFLAGS="-s -L./lib" OPTS="$BUILDOPTIONS" || exit 5

if [ -f find_servers ]; then
	rm find_servers
fi

gcc -O2 -s -o find_servers tools/find_servers.c

if [ -f alsacap ]; then
	rm alsacap
fi

gcc -O2 -s -lasound -o alsacap tools/alsacap.c
