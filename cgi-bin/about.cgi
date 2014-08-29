#!/bin/sh
. pcp-functions
pcp_variables

echo '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN""http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">'
echo '<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">'
echo ''
echo '<head>'
echo '  <meta http-equiv="Cache-Control" content="no-cache" />'
echo '  <meta http-equiv="Pragma" content="no-cache" />'
echo '  <meta http-equiv="Expires" content="0" />'
echo '  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
echo '  <title>pCP - About</title>'
echo '  <meta name="author" content="Steen" />'
echo '  <meta name="description" content="About page" />'
echo '  <link rel="stylesheet" type="text/css" href="../css/piCorePlayer.css" />'
echo '</head>'
echo ''
echo '<body>'

pcp_controls
pcp_banner
pcp_navigation

echo '<table border="0" width="960">'
echo '  <tr>'
echo '    <td>'
echo '      <h2>Thank you for using piCorePlayer.</h2>'

echo '      <p>piCorePlayer is built on a very small linux distro which is only about 12 MB, known as <a href="http://tinycorelinux.net/">Tiny Core Linux</a>. A special thanks to bmarkus from the <a href="http://forum.tinycorelinux.net/">microcore forum</a> for help building the piCore (a special version for the Raspberry Pi) and 
support. It boots very fast (often within 15 sec), and it is running entirely in RAM, therefore, you can simply pull the power without any risk of corruption of your SD-card.</p>'
echo '      <p>In addition it is using the fine Squeezelite player developed by Triode, which can be found <a href="https://code.google.com/p/squeezelite/">here</a>. Thanks to Ralphy for building squeezelite with wma and 
alac support.</p>'
echo '      <p>To use piCorePlayer you will need a Raspberry Pi computer. Read more about <a href="http://www.raspberrypi.org/">this small credit sized computer</a>. Raspberry Pi is a trademark of the Raspberry Pi Foundation.</p>'
  
echo '      <p>The web-GUI is povered by the build-in small webserver in Busybox <a href="http://www.busybox.net/">HTTPD</a>.</p>'
echo '      <p>The official piCorePlayer web page can be found here <a href="https://sites.google.com/site/picoreplayer/home/news">piCorePlayer web page</a>. A discussion forum can be found here <a 
href="http://forums.slimdevices.com/showthread.php?97803-piCoPlayer-Squeezelite-on-Microcore-linux-An-embedded-OS-in-RAM-with-Squeezelite">here</a>.</p>'
echo '      <h3>Please donate if you like piCorePlayer</h3>'
echo '      <p><a href="https://www.paypal.com/cgi-bin/webscr?cmd=_donations&amp;business=U7JHY5WYHCNRU&amp;lc=GB&amp;currency_code=USD&amp;bn=PP%2dDonationsBF%3abtn_donateCC_LG%2egif%3aNonHosted" target="_blank"><img 
border="0" src="../images/donate.gif" alt="Donate"/></a></p>'
echo '      <p>//Steen and Greg</p>'
echo '      <p>****************************************************************************************</p>'



echo '      <h2>[ INFO ] List to show if /mnt/mmcblk0p2/tce/squeezelite-armv6hf is running</h2>'
echo '      <textarea name="TextBox" cols="120" rows="5">'
ps aux | grep 'squeezelite-'
echo '      </textarea>'


echo '      <h2>[ INFO ] piCorePlayer version: '$(pcp_picoreplayer_version)'</h2>'
echo '      <textarea name="TextBox" cols="120" rows="5">'
cat /usr/local/sbin/piversion.cfg
echo '      </textarea>'

echo '      <h2>[ INFO ] Squeezelite version and license: '$(pcp_squeezelite_version)'</h2>'
echo '      <textarea name="TextBox" cols="120" rows="15">'
/mnt/mmcblk0p2/tce/squeezelite-armv6hf -t
echo '      </textarea>'

pcp_show_config_cfg

echo '    </td>'
echo '  </tr>'
echo '</table>'

pcp_footer

echo '</body>'
echo '</html>'
