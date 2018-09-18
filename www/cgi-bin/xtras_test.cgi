#!/bin/sh

# Version: 4.0.1 2018-09-19

. pcp-functions
. pcp-lms-functions

pcp_html_head "xtras" "GE"

pcp_banner
pcp_running_script
pcp_xtras

echo '<p>This page displays the Raspberry Pi diagnostics page for all Squeezelite players found on LMS.</p>'

TMP=$(mktemp)
pcp_lms_players squeezelite >$TMP
for i in $(cat $TMP | awk -F, '{ print $2 }')
do
	echo '<iframe src="http://'$i'/cgi-bin/diag_rpi.cgi" width="970" height="645" frameborder="0" scrolling="no"></iframe>'
done

pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'
exit

#========================================================================================
# Backup config file - DOES NOT WORK
#----------------------------------------------------------------------------------------
echo '<script type="text/javascript">'

echo '	var url="test.ext";'

echo 'function download1() {'
echo '	location.href=url;'
echo '}'

echo 'function download2() {'
echo "	window.open(url,'greg');"
echo '}'

echo 'function download3() {'
echo '	window.location.assign(url);'
echo '}'

echo '</script>'

echo '<br />'
echo '<p class="error">[ INFO ] These buttons do not work.</p>'
echo '<input type="button" value="download1" onClick="download1();">'
echo '<input type="button" value="download2" onClick="download2();">'
echo '<input type="button" value="download3" onClick="download3();">'
echo '<br />'
echo '<br />'

#========================================================================================
# Turn off Raspberry Pi activity led - DOES NOT WORK
#----------------------------------------------------------------------------------------
#sudo sh -c 'echo '"$GPIO"' > /sys/class/gpio/export'

echo '<textarea rows="20">'

cat /sys/class/leds/led0/brightness
#cat /sys/class/leds/led0/trigger

#echo "mmc0" > /sys/class/leds/led0/trigger
sudo sh -c 'echo "255" > /sys/class/leds/led0/brightness'

#echo "none" > /sys/class/leds/led0/trigger
#echo "0" > /sys/class/leds/led0/brightness

cat /sys/class/leds/led0/brightness
#cat /sys/class/leds/led0/trigger

echo ''

#========================================================================================
# Turn off rt2800 usb wifi adaptor led
#----------------------------------------------------------------------------------------
#/sys/devices/platform/bcm2708_usb/usb1/1-1/1-1.2/1-1.2:1.0/leds/rt2800usb-phy0::assoc

cat /sys/class/leds/rt2800usb-phy0::assoc/brightness

echo "0" > /sys/class/leds/rt2800usb-phy0::assoc/brightness
#echo "255" > /sys/class/leds/rt2800usb-phy0::assoc/brightness

cat /sys/class/leds/rt2800usb-phy0::assoc/brightness

echo ''
echo '</textarea>'

pcp_footer
pcp_refresh_button
pcp_go_back_button

pcp_reboot_button
pcp_go_main_button

echo '</body>'
echo '</html>'