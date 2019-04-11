#!/bin/bash

if [ -z $2 ]; then
	echo "Usage $0 compilefolder installfolder"
	exit
fi

echo "Using $2 for DESTDIR"

cd $1

export CFLAGS="-march=armv6 -mfloat-abi=hard -mfpu=vfp -s"
export LDFLAGS="-Wl,-rpath,/usr/local/lib -s"

fakeroot debian/rules build
