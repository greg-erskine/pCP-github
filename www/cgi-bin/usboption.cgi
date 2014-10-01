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
echo '  <title>pCP - USB options</title>'
echo '  <meta name="author" content="Steen" />'
echo '  <meta name="description" content="USB options" />'
echo '  <link rel="stylesheet" type="text/css" href="../css/piCorePlayer.css" />'
echo '</head>'
echo ''
echo '<body>'

pcp_banner
pcp_running_script


if [ $TEST = 1 ]; then
	echo '<h2>[ TEST ] Select your USB-card from dropdown list test</h2> If your card is not listed correctly please copy and paste as described above'
	echo '<form name="usbdropdown" action= "writetoconfig.cgi" method="get">'
#	echo '<select name="AUDIO_OUTPUT">'
	echo '<select name="OUTPUT">'

	/mnt/mmcblk0p2/tce/squeezelite-armv6hf -l | awk '/^  / { print "<option value=\""$1"\">" $1"</option>" }'

	echo '<input type="submit" value="Save">'
	echo '</form>'
fi

echo '<h2>Available ALSA output devices</h2>'
echo '<p>(choose, copy and then insert it in the OUTPUT box on the previous page)</p>'
echo '<pre>'
/mnt/mmcblk0p2/tce/squeezelite-armv6hf -l
echo '</pre>'

if [ $TEST = 1 ]; then
	echo '<h2>[ TEST ] Results from aplay</h2>'
	echo '<textarea name="TextBox" cols="120" rows="15">'
    sudo aplay -L
    echo '</textarea>'
fi

pcp_go_back_button

echo '</body>'
echo '</html>'
