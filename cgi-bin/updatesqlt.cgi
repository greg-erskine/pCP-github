#!/bin/sh
. pcp-functions
pcp_variables

echo '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">'
echo '<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">'
echo ''
echo '<head>'
echo '  <meta http-equiv="Cache-Control" content="no-cache" />'
echo '  <meta http-equiv="Pragma" content="no-cache" />'
echo '  <meta http-equiv="Expires" content="0" />'
echo '  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
echo '  <meta http-equiv="Refresh" content="5; url=main.cgi">'
echo '  <title>pCP - Updating Squeezelite</title>'
echo '  <meta name="author" content="Steen" />'
echo '  <meta name="description" content="Updating Squeezelite" />'
echo '  <link rel="stylesheet" type="text/css" href="../css/piCorePlayer.css" />'
echo '</head>'
echo ''
echo '<body>'

pcp_banner
pcp_running_script
pcp_squeezelite_stop
pcp_httpd_query_string

[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Version: '$VERSION'</p>'

case $VERSION in
	Triode*)
		message="Updating Squeezelite to Triodes latest version..."
		download="http://squeezelite-downloads.googlecode.com/git/squeezelite-armv6hf"
		;;
	Ralphy*)
		message="Updating Squeezelite to Ralphys latest version which supports ALAC..."
		download="http://ralph_irving.users.sourceforge.net/pico/squeezelite-armv6hf"
		;;
esac

echo '<h2>[ INFO ] '$message'</h2>'
echo '<p class="info">[ INFO ] Current Squeezelite version: '$(pcp_squeezelite_version)'</p>'

# Remove Squeezelite from /tmp
if [ -e /tmp/squeezelite-armv6hf ]; then
	[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Removing /tmp/squeezelite-armv6hf...</p>'
	sudo rm -f /tmp/squeezelite-armv6hf*
fi

wget -P /tmp $download
result=$?
if [ $result -ne "0" ]; then
	echo '<p class="error">[ ERROR ] Download unsuccessful, try again later!'
else
	echo '<p class="ok">[ OK ] Download successful'
	sudo mv /mnt/mmcblk0p2/tce/squeezelite-armv6hf /tmp/squeezelite-armv6hf~
	sudo cp /tmp/squeezelite-armv6hf /mnt/mmcblk0p2/tce
	sudo chmod u+x /mnt/mmcblk0p2/tce/squeezelite-armv6hf
	#sudo rm -f /tmp/squeezelite-armv6hf~
	#sudo rm -f /tmp/squeezelite-armv6hf
fi

pcp_squeezelite_start

echo '<p class="info">[ INFO ] Upgraded Squeezelite version: '$(pcp_squeezelite_version)'</p>'

echo '</body>'
echo '</html>'
