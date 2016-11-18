#!/bin/bash

if [ -z $2 ]; then
	echo "Usage $0 compilefolder installfolder"
	exit
fi

echo "Using $2 for DESTDIR"

cd $1

export CFLAGS="-march=armv6 -mfloat-abi=hard -mfpu=vfp -s"
export LDFLAGS="-Wl,-rpath,/usr/local/lib -s"

cmake -DCMAKE_BUILD_TYPE=Release -Wno-dev

make -j 4 || return 1

cd wodim

gcc -static CMakeFiles/wodim.dir/wodim.o CMakeFiles/wodim.dir/audiosize.o CMakeFiles/wodim.dir/auinfo.o CMakeFiles/wodim.dir/cdr_drv.o CMakeFiles/wodim.dir/cdtext.o CMakeFiles/wodim.dir/clone.o CMakeFiles/wodim.dir/crc16.o CMakeFiles/wodim.dir/cue.o CMakeFiles/wodim.dir/diskid.o CMakeFiles/wodim.dir/drv_7501.o CMakeFiles/wodim.dir/drv_jvc.o CMakeFiles/wodim.dir/drv_mmc.o CMakeFiles/wodim.dir/drv_philips.o CMakeFiles/wodim.dir/drv_simul.o CMakeFiles/wodim.dir/drv_sony.o CMakeFiles/wodim.dir/fifo.o CMakeFiles/wodim.dir/isosize.o CMakeFiles/wodim.dir/scsi_cdr_mmc4.o CMakeFiles/wodim.dir/scsi_mmc4.o CMakeFiles/wodim.dir/sector.o CMakeFiles/wodim.dir/subchan.o CMakeFiles/wodim.dir/wm_packet.o CMakeFiles/wodim.dir/wm_session.o CMakeFiles/wodim.dir/wm_track.o CMakeFiles/wodim.dir/xio.o -o wodim -L../librols -L../libusal -L../libedc -L../libusal -L../librols -L../wodim -L../libedc ../libusal/libusal.a ../librols/librols.a -lcap libwodimstuff.a ../libedc/libedc.a

cd ../

make DESTDIR=$2 install
