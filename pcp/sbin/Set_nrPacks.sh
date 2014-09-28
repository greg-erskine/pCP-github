#!/bin/sh
#Script for changing nrpacks on the fly


NRPACKS=$(cat /sys/module/snd_usb_audio/parameters/nrpacks)
echo "Current number of nrpacks="$NRPACKS


read -p "
- to keep current nrpacks press ENTER.  
- to change nrpacks use a value between 1 and 20:" t1
if [ -n "$t1" ]
then
  NRPACKS="$t1"
else
  NRPACKS=$NRPACKS
sudo modprobe -r snd-usb-audio
sudo modprobe snd-usb-audio nrpacks=$NRPACKS
  fi