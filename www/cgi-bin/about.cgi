#!/bin/sh

# Version: 0.04 2014-12-09 GE
#	Using pcp_html_head now.
#	HTML5 formatting.

# Version: 0.03 2014-09-04 GE
#	Adjusted size of textareas.

# Version: 0.02 2014-08-02 SBP
#	Updated information.

# Version: 0.01 2014-06-25 SBP
#	Original.

. pcp-functions
pcp_variables

# Local variables
START=""
END=""

pcp_html_head "Tweaks" "SBP"

pcp_controls
pcp_banner
pcp_navigation

echo '<table class="bgwhite">'
echo '  <tr>'
echo '    <td>'
echo '      <h1>Thank you for using piCorePlayer.</h1>'

echo '      <p>piCorePlayer is built on a very small linux distro which is only about 12 MB,'
echo '         known as <a href="http://tinycorelinux.net/">Tiny Core Linux</a>. '
echo '         A special thanks to bmarkus from the <a href="http://forum.tinycorelinux.net/">microcore forum</a> '
echo '         for help building the piCore (a special version for the Raspberry Pi) and support. '
echo '         It boots very fast (often within 15 sec), and it is running entirely in RAM, therefore, '
echo '         you can simply pull the power without any risk of corruption of your SD-card.</p>'

echo '      <p>In addition, piCorePlayer is using the fine Squeezelite player developed by Triode, which can be '
echo '         found <a href="https://code.google.com/p/squeezelite/">here</a>. Thanks to Ralphy for building '
echo '         a version of Squeezelite with wma and alac support.</p>'

echo '      <p>To use piCorePlayer you will need a Raspberry Pi computer. Read more about this '
echo '         <a href="http://www.raspberrypi.org/">small credit sized computer</a>. '
echo '         Raspberry Pi is a trademark of the Raspberry Pi Foundation.</p>'

echo '      <p>The web-GUI is powered by the small build-in Busybox webserver '
echo '         <a href="http://www.busybox.net/">HTTPD</a>.</p>'

echo '      <p>The official piCorePlayer web page can be found here '
echo '         <a href="https://sites.google.com/site/picoreplayer/home/news">piCorePlayer web page</a>. '
echo '         A forum discussion can be found '
echo '         <a href="http://forums.slimdevices.com/showthread.php?97803-piCoPlayer-Squeezelite-on-Microcore-linux-An-embedded-OS-in-RAM-with-Squeezelite">here</a>.</p>'

echo '      <h2>Please donate if you like piCorePlayer</h2>'

echo '      <p><a href="https://www.paypal.com/cgi-bin/webscr?cmd=_donations&amp;business=U7JHY5WYHCNRU&amp;'
echo 'lc=GB&amp;currency_code=USD&amp;bn=PP%2dDonationsBF%3abtn_donateCC_LG%2egif%3aNonHosted" target="_blank">'
echo '      <img border="0" src="../images/donate.gif" alt="Donate"/></a></p>'

echo '      <p>//Steen and Greg</p>'

echo '    </td>'
echo '  </tr>'
echo '</table>'

pcp_textarea "piCorePlayer version: $(pcp_picoreplayer_version)" "cat /usr/local/sbin/piversion.cfg" 50
pcp_textarea "Squeezelite version and license: $(pcp_squeezelite_version)" "/mnt/mmcblk0p2/tce/squeezelite-armv6hf -t" 260
pcp_show_config_cfg

pcp_footer

echo '</body>'
echo '</html>'