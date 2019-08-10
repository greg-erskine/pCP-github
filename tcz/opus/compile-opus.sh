#!/bin/bash

if [ -z $2 ]; then
        echo "Usage $0 compilefolder installfolder"
        exit
fi

echo "Using $2 for DESTDIR"
echo "Using $3 for OPUSFILESRC"

OPUSFILESRC=${3}

cd $1

export CFLAGS="-march=armv6 -mfloat-abi=hard -mfpu=vfp -s -O2"
export CPPFLAGS="$CFLAGS"
export CXXFLAGS="$CFLAGS"
export LDFLAGS="-Wl,-rpath,/usr/local/lib -s" 

make clean
rm config.cache

./configure \
--prefix=/usr/local \
--enable-shared=yes \
--enable-static=yes \
--disable-extra-programs \
--disable-doc

make -j 2
make DESTDIR=$2 install || exit 1

echo "$OPUSFILESRC"

cd ../$OPUSFILESRC
make clean
rm config.cache

DEPS_CFLAGS="-I${2}/usr/local/include -I${2}/usr/local/include/opus" \
DEPS_LIBS="-L${2}/usr/local/lib -logg -lopus" \
./configure \
--prefix=/usr/local \
--enable-shared=yes \
--enable-static=yes \
--disable-http \
--disable-examples \
--disable-doc

make -j 2
make DESTDIR=$2 install || exit 1
