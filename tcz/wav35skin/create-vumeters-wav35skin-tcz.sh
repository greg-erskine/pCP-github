#!/bin/bash
# VU_Meter_Kolossos_Oval-wav35skin.tcz (ks)

if [ -f VU_Meter_Kolossos_Oval-wav35skin.tcz ]; then
	rm VU_Meter_Kolossos_Oval-wav35skin.tcz
fi

# VU_Meter_Logitech_Black-wav35skin.tcz (b)

if [ -f VU_Meter_Logitech_Black-wav35skin.tcz ]; then
        rm VU_Meter_Logitech_Black-wav35skin.tcz
fi

# VU_Meter_Logitech_White-wav35skin.tcz (w)

if [ -f VU_Meter_Logitech_White-wav35skin.tcz ]; then
        rm VU_Meter_Logitech_White-wav35skin.tcz
fi

if [ -d wav35skin-build ]; then
        rm -rf wav35skin-build
else
        exit
fi

mkdir -p wav35skin-build/opt/jivelite/share/jive/applets/Wav35Skin/images/UNOFFICIAL/VUMeter
mv $STARTDIR/vu_analog_25seq_w.png \
        wav35skin-build/opt/jivelite/share/jive/applets/Wav35Skin/images/UNOFFICIAL/VUMeter/vu_analog_25seq_b.png

mksquashfs wav35skin-build VU_Meter_Logitech_White-wav35skin.tcz -all-root -no-progress
md5sum VU_Meter_Logitech_White-wav35skin.tcz > VU_Meter_Logitech_White-wav35skin.tcz.md5.txt
cd wav35skin-build
find * -not -type d > ../VU_Meter_Logitech_White-wav35skin.tcz.list
cd ..

if [ -d wav35skin-build ]; then
        rm -rf wav35skin-build
else
        exit
fi

mkdir -p wav35skin-build/opt/jivelite/share/jive/applets/Wav35Skin/images/UNOFFICIAL/VUMeter
mv $STARTDIR/vu_analog_25seq_b.png \
        wav35skin-build/opt/jivelite/share/jive/applets/Wav35Skin/images/UNOFFICIAL/VUMeter/

mksquashfs wav35skin-build VU_Meter_Logitech_Black-wav35skin.tcz -all-root -no-progress
md5sum VU_Meter_Logitech_Black-wav35skin.tcz > VU_Meter_Logitech_Black-wav35skin.tcz.md5.txt
cd wav35skin-build
find * -not -type d > ../VU_Meter_Logitech_Black-wav35skin.tcz.list
cd ..

if [ -d wav35skin-build ]; then
        rm -rf wav35skin-build
else
        exit
fi

mkdir -p wav35skin-build/opt/jivelite/share/jive/applets/Wav35Skin/images/UNOFFICIAL/VUMeter
cp -p vu_analog_25seq_ks.png \
        wav35skin-build/opt/jivelite/share/jive/applets/Wav35Skin/images/UNOFFICIAL/VUMeter/vu_analog_25seq_b.png

mksquashfs wav35skin-build VU_Meter_Kolossos_Oval-wav35skin.tcz -all-root -no-progress
md5sum VU_Meter_Kolossos_Oval-wav35skin.tcz > VU_Meter_Kolossos_Oval-wav35skin.tcz.md5.txt
cd wav35skin-build
find * -not -type d > ../VU_Meter_Kolossos_Oval-wav35skin.tcz.list
cd ..

