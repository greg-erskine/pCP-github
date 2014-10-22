#!/bin/sh
# Sound diagnostics script

# version: 0.01 2014-10-22 GE
#	Orignal.

. pcp-functions
pcp_variables

# Local variables
START="====================> Start <===================="
END="=====================> End <====================="
LOG="/tmp/diagsnd.log"
(echo $0; date) > $LOG

pcp_html_head "Sound Diagnostics" "GE"

if [ $MODE -lt 5 ]; then
	echo '</body>'
	echo '</html>'
	exit 1
fi

pcp_banner
pcp_navigation
pcp_refresh_button

#=========================================================================================
# Sound diagnostics
#-----------------------------------------------------------------------------------------
pcp_textarea "amixer cset numid=3" "sudo amixer cset numid=3" 80 log
pcp_textarea "Loaded sound modules" "lsmod | grep snd" 360 log
pcp_textarea "Current /proc/asound" "ls -al /proc/asound" 210 log
pcp_textarea "PLAYBACK Hardware Devices" "aplay -l" 240 log
pcp_textarea "Sound devices" "aplay -L" 100 log

pcp_textarea "Current pcm0p" "cat /proc/asound/card0/pcm0p/sub0/hw_params" 130 log
pcp_textarea "Current pcm0p" "cat /proc/asound/card0/pcm0p/sub1/hw_params" 130 log
pcp_textarea "Current pcm1p" "cat /proc/asound/card0/pcm1p/sub0/hw_params" 130 log

pcp_textarea "amixer" "amixer" 100 log
pcp_textarea "Play" "aplay -v -D hw:0,0 -f S16_LE -r 96000 -c 2 -t raw -d 1" 150 log
pcp_textarea "Current /etc/group" "cat /etc/group" 85 log
pcp_textarea "Current /etc/asound.conf" "cat /etc/asound.conf" 250 log
pcp_textarea "Current /var/lib/alsa/asound.state" "cat /var/lib/alsa/asound.state" 180 log
pcp_textarea "Left speaker test" "speaker-test -t sine -f 480 -c 2 -s 1" 240 log
pcp_textarea "Right speaker test" "speaker-test -t sine -f 480 -c 2 -s 2" 240 log

pcp_refresh_button
pcp_footer

echo '</body>'
echo '</html>'
