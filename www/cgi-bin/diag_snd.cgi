#!/bin/sh
# Sound diagnostics script

# Version: 0.09 2016-05-16 GE
#	Fixed card1 pcm0p sub0.
#	Changed name of log file.

# Version: 0.08 2016-03-28 GE
#	Changed log location to /var/log.

# Version: 0.07 2016-02-03 GE
#	Moved pcp_pastebin_button to Developer mode.

# Version: 0.06 2015-12-24 GE
#	Added Upload to pastebin feature.

# Version: 0.05 2015-07-04 GE
#	Minor updates.

# Version: 0.04 2015-05-13 GE
#	Added /usr/local/tce.installed/alsa,
#		  /usr/local/etc/udev/rules.d/90-alsa-restore.rules.
#		  /usr/local/share/alsa/alsa.conf

# Version: 0.03 2015-04-28 GE
#	Minor updates.

# Version: 0.02 2015-03-07 GE
#	Minor updates.

# version: 0.01 2014-10-22 GE
#	Original.

. pcp-functions
pcp_variables
. pcp-pastebin-functions

# Local variables
START="====================> Start <===================="
END="=====================> End <====================="
LOG="${LOGDIR}/pcp_sound.log"
(echo $0; date) > $LOG
cat /etc/motd >> $LOG

pcp_html_head "Sound Diagnostics" "GE"

pcp_banner
pcp_diagnostics
pcp_running_script

#=========================================================================================
# Sound diagnostics
#-----------------------------------------------------------------------------------------
pcp_textarea "Current /usr/local/tce.installed/alsa" "cat /usr/local/tce.installed/alsa" 275 log
pcp_textarea "Current /usr/local/etc/udev/rules.d/90-alsa-restore.rules" "cat /usr/local/etc/udev/rules.d/90-alsa-restore.rules" 160 log
pcp_textarea "Current /var/lib/alsa/asound.state" "cat /var/lib/alsa/asound.state" 180 log
pcp_textarea "Current /usr/local/share/alsa/alsa.conf" "cat /usr/local/share/alsa/alsa.conf" 380 log

pcp_textarea "amixer cset numid=3" "sudo amixer cset numid=3" 80 log
pcp_textarea "Loaded sound modules" "lsmod | grep snd" 360 log
pcp_textarea "Current /proc/asound" "ls -al /proc/asound" 210 log
pcp_textarea "PLAYBACK Hardware Devices" "aplay -l" 240 log
pcp_textarea "Sound devices" "aplay -L" 100 log

pcp_textarea "Current card0 pcm0p sub0" "cat /proc/asound/card0/pcm0p/sub0/hw_params" 130 log
pcp_textarea "Current card0 pcm0p sub1" "cat /proc/asound/card0/pcm0p/sub1/hw_params" 130 log
pcp_textarea "Current card1 pcm0p sub0" "cat /proc/asound/card1/pcm0p/sub0/hw_params" 130 log

pcp_textarea "amixer" "amixer" 100 log
pcp_textarea "Play" "aplay -v -D hw:0,0 -f S16_LE -r 96000 -c 2 -t raw -d 1" 150 log
pcp_textarea "Current /etc/group" "cat /etc/group" 100 log
pcp_textarea "Current /etc/asound.conf" "cat /etc/asound.conf" 150 log
pcp_textarea "Squeezelite log" "cat /var/log/pcp_squeezelite.log" 250 log

pcp_textarea "Left speaker test" "speaker-test -t sine -f 480 -c 2 -s 1" 240 log
pcp_textarea "Right speaker test" "speaker-test -t sine -f 480 -c 2 -s 2" 240 log

echo '<br />'
echo '<br />'

[ $MODE -ge $MODE_DEVELOPER ] && pcp_pastebin_button sound

pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'