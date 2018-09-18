#!/bin/sh
# Sound diagnostics script

# Version: 4.0.1 2018-09-19

. pcp-functions
. pcp-rpi-functions
. pcp-pastebin-functions

# Local variables
LOG="${LOGDIR}/pcp_sound.log"
pcp_log_header $0

pcp_html_head "Sound Diagnostics" "GE"

pcp_banner
pcp_diagnostics
pcp_running_script

#=========================================================================================
# Sound diagnostics
#-----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Sound diagnostics</legend>'
echo '          <table class="bggrey percent100">'
pcp_start_row_shade
pcp_toggle_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td>'

#                     pcp_textarea_inform "Current /usr/local/tce.installed/alsa" "cat /usr/local/tce.installed/alsa" 275 log
#                     pcp_textarea_inform "Current /usr/local/etc/udev/rules.d/90-alsa-restore.rules" "cat /usr/local/etc/udev/rules.d/90-alsa-restore.rules" 160 log
                      pcp_textarea_inform "Current /var/lib/alsa/asound.state" "cat /var/lib/alsa/asound.state" 180 log
                      pcp_textarea_inform "Current /usr/local/share/alsa/alsa.conf" "cat /usr/local/share/alsa/alsa.conf" 380 log

                      pcp_textarea_inform "amixer cset numid=3" "sudo amixer cset numid=3" 80 log
                      pcp_textarea_inform "Loaded sound modules" "lsmod | grep snd" 360 log
                      pcp_textarea_inform "Current /proc/asound" "ls -al /proc/asound" 210 log
                      pcp_textarea_inform "PLAYBACK Hardware Devices" "aplay -l" 240 log
                      pcp_textarea_inform "Sound devices" "aplay -L" 100 log

                      pcp_textarea_inform "Current card0 pcm0p sub0" "cat /proc/asound/card0/pcm0p/sub0/hw_params" 130 log
                      pcp_textarea_inform "Current card0 pcm0p sub1" "cat /proc/asound/card0/pcm0p/sub1/hw_params" 130 log
                      pcp_textarea_inform "Current card1 pcm0p sub0" "cat /proc/asound/card1/pcm0p/sub0/hw_params" 130 log

                      pcp_textarea_inform "amixer" "amixer" 100 log
                      pcp_textarea_inform "Play" "aplay -v -D hw:0,0 -f S16_LE -r 96000 -c 2 -t raw -d 1" 150 log
                      pcp_textarea_inform "Current /etc/group" "cat /etc/group" 100 log
                      pcp_textarea_inform "Current /etc/asound.conf" "cat /etc/asound.conf" 150 log
                      pcp_textarea_inform "Squeezelite log" "cat /var/log/pcp_squeezelite.log" 250 log

                      pcp_textarea_inform "Left speaker test" "speaker-test -t sine -f 480 -c 2 -s 1" 240 log
                      pcp_textarea_inform "Right speaker test" "speaker-test -t sine -f 480 -c 2 -s 2" 240 log

echo '              </td>'
echo '            </tr>'
echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'

[ $MODE -ge $MODE_DEVELOPER ] && pcp_pastebin_button sound

pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'