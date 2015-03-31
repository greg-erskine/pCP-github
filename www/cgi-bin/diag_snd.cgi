#!/bin/sh
# Sound diagnostics script

# Version: 0.02 2015-03-07 GE
#	Minor updates.

# version: 0.01 2014-10-22 GE
#	Original.

. pcp-functions
pcp_variables

# Local variables
START="====================> Start <===================="
END="=====================> End <====================="
LOG="/tmp/diagsnd.log"
(echo $0; date) > $LOG

pcp_html_head "Sound Diagnostics" "GE"

pcp_footer
pcp_banner
pcp_diagnostics
pcp_running_script
pcp_refresh_button
pcp_go_main_button

if [ $MODE -lt 5 ]; then
	echo '<p class="error">[ ERROR ] Wrong mode.</p>'
	echo '</body>'
	echo '</html>'
	exit 1
fi

#=========================================================================================
# Sound diagnostics
#-----------------------------------------------------------------------------------------
pcp_textarea "amixer cset numid=3" "sudo amixer cset numid=3" 80 log
pcp_textarea "Loaded sound modules" "lsmod | grep snd" 360 log
pcp_textarea "Current /proc/asound" "ls -al /proc/asound" 210 log
pcp_textarea "PLAYBACK Hardware Devices" "aplay -l" 240 log
pcp_textarea "Sound devices" "aplay -L" 100 log

pcp_textarea "Current card0 pcm0p sub0" "cat /proc/asound/card0/pcm0p/sub0/hw_params" 130 log
pcp_textarea "Current card0 pcm0p sub1" "cat /proc/asound/card0/pcm0p/sub1/hw_params" 130 log
pcp_textarea "Current card0 pcm1p sub0" "cat /proc/asound/card0/pcm1p/sub0/hw_params" 130 log

pcp_textarea "amixer" "amixer" 100 log
pcp_textarea "Play" "aplay -v -D hw:0,0 -f S16_LE -r 96000 -c 2 -t raw -d 1" 150 log
pcp_textarea "Current /etc/group" "cat /etc/group" 100 log
pcp_textarea "Current /etc/asound.conf" "cat /etc/asound.conf" 150 log
pcp_textarea "Current /var/lib/alsa/asound.state" "cat /var/lib/alsa/asound.state" 180 log
pcp_textarea "Squeezelite log" "cat /tmp/$LOGFILE" 250 log
pcp_textarea "Left speaker test" "speaker-test -t sine -f 480 -c 2 -s 1" 240 log
pcp_textarea "Right speaker test" "speaker-test -t sine -f 480 -c 2 -s 2" 240 log


echo '<br />'
echo '<br />'

pcp_footer
pcp_copyright
pcp_refresh_button

echo '</body>'
echo '</html>'