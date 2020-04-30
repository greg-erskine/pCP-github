#!/bin/sh

# Version: 7.0.0 2020-04-30

. pcp-functions
. pcp-lms-functions

pcp_html_head "About" "SBP"

pcp_controls
pcp_navbar

#----------------------------------------------------------------------------------------
echo '    <div>'

echo '      <h4>Thank you for using piCorePlayer</h4>'

echo '      <p>piCorePlayer is built on a very small linux distro which is only about 12 MB,'
echo '         known as <a href="http://tinycorelinux.net/" target="_blank">Tiny Core Linux</a> '$EXTERNALLINK'. '
echo '         A special thanks to bmarkus from the <a href="http://forum.tinycorelinux.net/" target="_blank">microcore forum</a> '$EXTERNALLINK
echo '         for help building the piCore (a special version for the Raspberry Pi) and support. '
echo '         It boots very fast (often within 25 sec), and it is running entirely in RAM, therefore, '
echo '         you can simply pull the power without any risk of corruption of your SD card.</p>'

echo '      <p>In addition, piCorePlayer is using the fine Squeezelite player developed by Triode, which can be '
echo '         found <a href="https://github.com/ralph-irving/squeezelite" target="_blank">here</a> '$EXTERNALLINK'. Thanks to Ralphy for building '
echo '         a version of Squeezelite with wma and alac support and for providing the jivelite and Shairport packages. The patches applied '
echo '         to the kernel to improve DAC support and higher sample rates were developed by Clive Messer.</p>'

echo '      <p>Recently, Logitech Media Server LMS can be run on piCorePlayer. Thanks to Paul_123 and jgrulich from the piCore forum'
echo '         for building the LMS.tcz package.</p>'

echo '      <p>To use piCorePlayer you will need a Raspberry Pi computer. Read more about this '
echo '         <a href="http://www.raspberrypi.org/" target="_blank">small credit sized computer</a> '$EXTERNALLINK'. '
echo '         Raspberry Pi is a trademark of the Raspberry Pi Foundation.</p>'

echo '      <p>The web-GUI is powered by the small built-in Busybox webserver '
echo '         <a href="http://www.busybox.net/" target="_blank">HTTPD</a> '$EXTERNALLINK'.</p>'

echo '      <p>The official piCorePlayer web page can be found here '
echo '         <a href="https://www.picoreplayer.org" target="_blank">piCorePlayer web page</a> '$EXTERNALLINK'. '
echo '         A forum discussion can be found '
echo '         <a href="https://www.picoreplayer.org/announce.6.0.0" target="_blank">here</a> '$EXTERNALLINK'.</p>'
echo '    </div>'
echo '    <div class="text-center">'
echo '      <h5>Please donate if you like piCorePlayer</h5>'

echo '      <p><a href="https://www.paypal.com/cgi-bin/webscr?cmd=_donations&amp;business=U7JHY5WYHCNRU&amp;lc=GB&amp;currency_code=USD&amp;bn=PP%2dDonationsBF%3abtn_donateCC_LG%2egif%3aNonHosted" target="_blank">'
echo '         <img style="border:0px;" src="../images/donate.gif" alt="Donate"></a> '$EXTERNALLINK'</p>'
echo '    </div>'
echo '    <div>'
echo '      <p>//Paul, Ralphy, Steen and Greg</p>'

echo '    </div>'
#----------------------------------------------------------------------------------------

pcp_footer
pcp_copyright
echo '</div>'
echo '</body>'
echo '</html>'
exit
