#!/bin/sh
# Sound diagnostics script

# Version: 7.0.0 2020-05-06

. pcp-functions
. pcp-rpi-functions
. pcp-pastebin-functions

# Local variables
LOG="${LOGDIR}/pcp_sound.log"
pcp_log_header $0

pcp_html_head "Sound Diagnostics" "GE"

pcp_diagnostics

COLUMN1="col-12"
#=========================================================================================
# Sound diagnostics
#-----------------------------------------------------------------------------------------
pcp_heading5 "Sound diagnostics"

#pcp_textarea "Current /usr/local/tce.installed/alsa" "cat /usr/local/tce.installed/alsa" 10 log
#pcp_textarea "Current /usr/local/etc/udev/rules.d/90-alsa-restore.rules" "cat /usr/local/etc/udev/rules.d/90-alsa-restore.rules" 10 log
pcp_textarea "Current /var/lib/alsa/asound.state" "cat /var/lib/alsa/asound.state" 5 log
pcp_textarea "Current /usr/local/share/alsa/alsa.conf" "cat /usr/local/share/alsa/alsa.conf" 10 log

pcp_textarea "amixer cset numid=3" "sudo amixer cset numid=3" 10 log
pcp_textarea "Loaded sound modules" "lsmod | grep snd" 10 log
pcp_textarea "Current /proc/asound" "ls -al /proc/asound" 10 log
pcp_textarea "Sound devices" "aplay -L" 10 log
pcp_textarea "PLAYBACK Hardware Devices" "alsacap" 10 log
pcp_textarea "RECORDING Hardware Devices" "alsacap -R" 10 log

pcp_textarea "Current card0 pcm0p sub0" "cat /proc/asound/card0/pcm0p/sub0/hw_params" 10 log
pcp_textarea "Current card0 pcm0p sub1" "cat /proc/asound/card0/pcm0p/sub1/hw_params" 10 log
pcp_textarea "Current card1 pcm0p sub0" "cat /proc/asound/card1/pcm0p/sub0/hw_params" 10 log

pcp_textarea "amixer" "amixer" 10 log
pcp_textarea "Play" "aplay -v -D hw:0,0 -f S16_LE -r 96000 -c 2 -t raw -d 1" 10 log
pcp_textarea "Current /etc/group" "cat /etc/group" 10 log
pcp_textarea "Current /etc/asound.conf" "cat /etc/asound.conf" 10 log
pcp_textarea "Squeezelite log" "cat /var/log/pcp_squeezelite.log" 10 log

pcp_textarea "Left speaker test" "speaker-test -t sine -f 480 -c 2 -s 1" 10 log
pcp_textarea "Right speaker test" "speaker-test -t sine -f 480 -c 2 -s 2" 10 log

[ $MODE -ge $MODE_DEVELOPER ] && pcp_pastebin_button sound

pcp_html_end
