#!/bin/bash

if [ ! -d squeezelite ]; then
	exit 1
fi

cd squeezelite
make -f Makefile.pcp clean

patch -p0 -i scripts/squeezelite-ralphy-dsd.patch || exit 1

make -f Makefile.pcp OPTS="-DRESAMPLE -DFFMPEG -DVISEXPORT -DDSD -DGPIO -DRPI -DIR -I./include" || exit 2

mv squeezelite squeezelite-dsd

make -f Makefile.pcp clean

patch -p0 -R -i scripts/squeezelite-ralphy-dsd.patch || exit 3

make -f Makefile.pcp OPTS="-DRESAMPLE -DFFMPEG -DVISEXPORT -DGPIO -DRPI -DIR -I./include" || exit 4

if [ -f find_servers ]; then
	rm find_servers
fi

gcc -O2 -s -o find_servers tools/find_servers.c
