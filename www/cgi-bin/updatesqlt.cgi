#!/bin/sh
. pcp-functions
pcp_variables

# Version: 0.03 2015-12-09 GE
#	Remove Triode's version.
#	Update Ralphy's version.

# Version: 0.02 2014-12-09 GE
#	HTML5 formatted.

# Version: 0.01 2014-06-24 GE
#	Original.

pcp_html_head "Updating Squeezelite" "SBP" "5" "main.cgi"

pcp_banner
pcp_running_script
pcp_squeezelite_stop
pcp_httpd_query_string

[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Version: '$VERSION'</p>'

case $VERSION in
	Small*)
		message="Updating Squeezelite to Ralphy small version..."
		download="http://ralph_irving.users.sourceforge.net/pico/squeezelite-armv6hf-noffmpeg"
		;;
	Large*)
		message="Updating Squeezelite to Ralphy large version (will take a few minutes)..."
		download="http://ralph_irving.users.sourceforge.net/pico/squeezelite-armv6hf-ffmpeg"
		;;
esac

echo '<p>[ INFO ] '${message}'</p>'
echo '<p class="info">[ INFO ] Current Squeezelite version: '$(pcp_squeezelite_version)'</p>'

# Remove Squeezelite from /tmp
if [ -e /tmp/squeezelite-armv6hf ]; then
	[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Removing /tmp/squeezelite-armv6hf...</p>'
	sudo rm -f /tmp/squeezelite-armv6hf*
fi

wget -O /tmp/squeezelite-armv6hf $download
result=$?
if [ $result -ne "0" ]; then
	echo '<p class="error">[ ERROR ] Download unsuccessful, try again later!'
else
	echo '<p class="ok">[ OK ] Download successful'
	sudo mv /mnt/mmcblk0p2/tce/squeezelite-armv6hf /tmp/squeezelite-armv6hf~
	sudo cp /tmp/squeezelite-armv6hf /mnt/mmcblk0p2/tce
	sudo chmod u+x /mnt/mmcblk0p2/tce/squeezelite-armv6hf
fi

[ $DEBUG = 1 ] && (echo '<p class="ok">[ OK ] '; ls -al /mnt/mmcblk0p2/tce/squeezelite-armv6hf)

pcp_squeezelite_start

echo '<p class="info">[ INFO ] Upgraded Squeezelite version: '$(pcp_squeezelite_version)'</p>'

echo '</body>'
echo '</html>'