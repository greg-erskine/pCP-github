#!/bin/sh

# Version: 7.0.0 2020-05-19

. pcp-functions
. pcp-lms-functions

pcp_html_head "About" "SBP"

pcp_controls
pcp_navbar

CARD="col my-3"

#echo '      <div class="card" style="width: 18rem;">'

#----------------------------------------------------------------------------------------
#echo '  <h4>Thank you for using piCorePlayer</h4>'

echo '  <div class="row row-cols-1 row-cols-md-3">'

echo '    <div class="'$CARD'">'
echo '      <div class="card">'
echo '        <div class="card-body">'
echo '          <h5 class="card-title">piCorePlayer</h5>'
echo '          <p class="card-text">piCorePlayer is built on a very small linux distro which is only about 12 MB,'
echo '             known as Tiny Core Linux.'
echo '             A special thanks to bmarkus from the Tiny Core/piCore forum'
echo '             for building piCore (a special version of Tiny Core for the Raspberry Pi) and support. '
echo '             It boots very fast (often within 25 sec), and it is running entirely in RAM, therefore, '
echo '             you can simply pull the power without any risk of corruption of your SD card.</p>'
echo '          <a href="http://tinycorelinux.net/" target="_blank" class="'$BUTTON'">Tiny Core Linux</a>'
echo '        </div>'
echo '      </div>'
echo '    </div>'

echo '    <div class="'$CARD'">'
echo '      <div class="card">'
echo '        <div class="card-body">'
echo '          <h5 class="card-title">Squeezelite</h5>'
echo '          <p class="card-text">In addition, piCorePlayer is using the fine Squeezelite player developed by Triode. Thanks to Ralphy for building '
echo '             a version of Squeezelite with wma and alac support and for providing the jivelite and Shairport packages. The patches applied '
echo '             to the kernel to improve DAC support and higher sample rates were developed by Clive Messer.</p>'
echo '          <a href="https://github.com/ralph-irving/squeezelite" target="_blank" class="'$BUTTON'">Squeezelite</a>'
echo '        </div>'
echo '      </div>'
echo '    </div>'

echo '    <div class="'$CARD'">'
echo '      <div class="card">'
echo '        <div class="card-body">'
echo '          <h5 class="card-title">Logitech Media Server LMS</h5>'
echo '          <p class="card-text">Recently, Logitech Media Server LMS can be run on piCorePlayer. Thanks to Paul_123 and jgrulich from the piCore forum'
echo '             for building the LMS.tcz package.</p>'
echo '          <a href="#" class="'$BUTTON'">Go somewhere</a>'
echo '        </div>'
echo '      </div>'
echo '    </div>'

echo '    <div class="'$CARD'">'
echo '      <div class="card">'
echo '        <div class="card-body">'
echo '          <h5 class="card-title">Raspberry Pi</h5>'
echo '          <p class="card-text">To use piCorePlayer you will need a Raspberry Pi computer. Read more about this '
echo '             small credit sized computer. '
echo '             Raspberry Pi is a trademark of the Raspberry Pi Foundation.</p>'
echo '          <a href="http://www.raspberrypi.org/" target="_blank" class="'$BUTTON'">Raspberry Pi</a>'
echo '        </div>'
echo '      </div>'
echo '    </div>'

echo '    <div class="'$CARD'">'
echo '      <div class="card">'
echo '        <div class="card-body">'
echo '          <h5 class="card-title">Busybox httpd webserver</h5>'
echo '          <p class="card-text">The web-GUI is powered by the small built-in Busybox webserver </p>'
echo '          <a href=href="http://www.busybox.net/" target="_blank" class="'$BUTTON'">Busybox httpd</a>'
echo '        </div>'
echo '      </div>'
echo '    </div>'

echo '    <div class="'$CARD'">'
echo '      <div class="card">'
echo '        <div class="card-body">'
echo '          <h5 class="card-title">official piCorePlayer web page</h5>'
echo '          <p>The official piCorePlayer web page can be found here '
echo '             <a href="https://www.picoreplayer.org" target="_blank">piCorePlayer web page</a> '$EXTERNALLINK'. '
echo '             A forum discussion can be found .</p>'
echo '          <a href="https://www.picoreplayer.org/announce.6.0.0" target="_blank" class="'$BUTTON'">official piCorePlayer web page</a>'
echo '        </div>'
echo '      </div>'
echo '    </div>'

echo '    <div class="'$CARD'">'
echo '      <div class="card">'
echo '        <div class="card-body">'
echo '          <h5 class="card-title">Thank you</h5>'
echo '          <p class="card-text">Thank you for using piCorePlayer.</p>'
echo '          <p class="card-text">//Paul, Ralphy, Steen and Greg</p>'
echo '        </div>'
echo '      </div>'
echo '    </div>'

echo '    <div class="'$CARD'">'
echo '      <div class="card">'
echo '        <div class="card-body text-center">'
echo '          <h5 class="card-title">Donations</h5>'
echo '          <p class="card-text">Please donate if you like piCorePlayer.</p>'
echo '          <p class="card-text"><a href="https://www.paypal.com/cgi-bin/webscr?cmd=_donations&amp;business=U7JHY5WYHCNRU&amp;lc=GB&amp;currency_code=USD&amp;bn=PP%2dDonationsBF%3abtn_donateCC_LG%2egif%3aNonHosted" target="_blank">'
echo '          <img style="border:0px;" src="../images/donate.gif" alt="Donate"></a> '$EXTERNALLINK'</p>'
echo '        </div>'
echo '      </div>'
echo '    </div>'

echo '  </div>'
#----------------------------------------------------------------------------------------

pcp_html_end
exit
