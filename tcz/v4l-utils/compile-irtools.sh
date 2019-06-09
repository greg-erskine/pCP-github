#!/bin/bash

if [ -z $2 ]; then
	echo "Usage $0 compilefolder installfolder"
	exit
fi

echo "Using $2 for DESTDIR"

cd $1

export CFLAGS="-march=armv6 -mfloat-abi=hard -mfpu=vfp -s"
export LDFLAGS="-Wl,-rpath,/usr/local/lib -s"

./configure --enable-shared=no
make -C utils/ir-ctl
make -C utils/keytable

mkdir -p $2/usr/local/bin
cp -p utils/ir-ctl/ir-ctl $2/usr/local/bin
cp -p utils/keytable/ir-keytable $2/usr/local/bin
