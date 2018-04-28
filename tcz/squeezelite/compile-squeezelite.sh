#!/bin/bash

if [ ! -d squeezelite ]; then
	exit 1
fi

cd squeezelite
make "OPTS=-DDSD -DRESAMPLE -DVISEXPORT -DIR -DRPI -DLINKALL" clean
make "OPTS=-DDSD -DRESAMPLE -DVISEXPORT -DIR -DRPI -DLINKALL"


make OPTS="-DRESAMPLE -DFFMPEG -DVISEXPORT -DDSD -DGPIO -DRPI -DIR -I./include" clean || exit 2
make OPTS="-DRESAMPLE -DFFMPEG -DVISEXPORT -DDSD -DGPIO -DRPI -DIR -I./include" || exit 3

mv squeezelite squeezelite-dsd
patchelf --set-rpath /usr/local/lib squeezelite-dsd

make OPTS="-DRESAMPLE -DFFMPEG -DVISEXPORT -DGPIO -DRPI -DIR -I./include" clean || exit 4
make OPTS="-DRESAMPLE -DFFMPEG -DVISEXPORT -DGPIO -DRPI -DIR -I./include" || exit 5
patchelf --set-rpath /usr/local/lib squeezelite

if [ -f find_servers ]; then
	rm find_servers
fi

gcc -O2 -s -o find_servers tools/find_servers.c
