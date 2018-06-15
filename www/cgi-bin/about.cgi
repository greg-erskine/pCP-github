#!/bin/sh

# Version: 4.0.0 2018-06-15

. pcp-functions
. pcp-rpi-functions
. pcp-lms-functions
. pcp-pastebin-functions

LOG=$PCPCFG

pcp_html_head "About" "SBP"

pcp_picoreplayers_toolbar
pcp_controls
pcp_banner
pcp_navigation

#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <table class="bggrey percent100">'
echo '            <tr>'
echo '              <td>'
echo '                <h1>Thank you for using piCorePlayer</h1>'
echo '                <p>piCorePlayer is built on a very small linux distro which is only about 12 MB,'
echo '                   known as <a href="http://tinycorelinux.net/" target="_blank">Tiny Core Linux</a> '$EXTERNALLINK'. '
echo '                   A special thanks to bmarkus from the <a href="http://forum.tinycorelinux.net/" target="_blank">microcore forum</a> '$EXTERNALLINK
echo '                   for help building the piCore (a special version for the Raspberry Pi) and support. '
echo '                   It boots very fast (often within 15 sec), and it is running entirely in RAM, therefore, '
echo '                   you can simply pull the power without any risk of corruption of your SD card.</p>'
echo '                <p>In addition, piCorePlayer is using the fine Squeezelite player developed by Triode, which can be '
echo '                   found <a href="https://github.com/ralph-irving/squeezelite" target="_blank">here</a> '$EXTERNALLINK'. Thanks to Ralphy for building '
echo '                   a version of Squeezelite with wma and alac support and for providing the jivelite and Shairport packages. The patches applied '
echo '                   to the kernel to improve DAC support and higher sample rates were developed by Clive Messer.</p>'
echo '                <p>Recently, Logitech Media Server LMS can be run on piCorePlayer. Thanks to Paul_123 and jgrulich from the piCore forum'
echo '                   for building the LMS.tcz package.</p>'
echo '                <p>To use piCorePlayer you will need a Raspberry Pi computer. Read more about this '
echo '                   <a href="http://www.raspberrypi.org/" target="_blank">small credit sized computer</a> '$EXTERNALLINK'. '
echo '                   Raspberry Pi is a trademark of the Raspberry Pi Foundation.</p>'
echo '                <p>The web-GUI is powered by the small built-in Busybox webserver '
echo '                   <a href="http://www.busybox.net/" target="_blank">HTTPD</a> '$EXTERNALLINK'.</p>'
echo '                <p>The official piCorePlayer web page can be found here '
echo '                   <a href="https://www.picoreplayer.org" target="_blank">piCorePlayer web page</a> '$EXTERNALLINK'. '
echo '                   A forum discussion can be found '
echo '                   <a href="http://forums.slimdevices.com/showthread.php?105997-Announce-piCorePlayer-3-00" target="_blank">here</a> '$EXTERNALLINK'.</p>'
echo '                <h2>Please donate if you like piCorePlayer</h2>'
echo '                <p class="center"><a href="https://www.paypal.com/cgi-bin/webscr?cmd=_donations&amp;business=U7JHY5WYHCNRU&amp;lc=GB&amp;currency_code=USD&amp;bn=PP%2dDonationsBF%3abtn_donateCC_LG%2egif%3aNonHosted" target="_blank">'
echo '                   <img style="border:0px;" src="../images/donate.gif" alt="Donate"></a> '$EXTERNALLINK'</p>'
echo '                <p>//Paul, Ralphy, Steen and Greg</p>'
echo '              </td>'
echo '            </tr>'
echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------
if [ $MODE -ge $MODE_BASIC ]; then
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Versions</legend>'
	echo '          <table class="bggrey percent100">'
	echo '            <tr>'
	echo '              <td>'
	                      pcp_textarea_inform "none" "cat ${PCPVERSIONCFG}" 30
	echo '              </td>'
	echo '            </tr>'
	echo '            <tr class="padding">'
	echo '              <td></td>'
	echo '            </tr>'
	echo '            <tr>'
	echo '              <td>'
	                      pcp_textarea_inform "none" "${SQLT_BIN} -t" 240
	echo '              </td>'
	echo '            </tr>'
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
fi
#----------------------------------------------------------------------------------------
if [ $MODE -ge $MODE_ADVANCED ]; then
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Current configuration</legend>'
	echo '          <table class="bggrey percent100">'
	echo '            <tr>'
	echo '              <td>'
	                      pcp_textarea_inform "$PCPCFG" 'cat $PCPCFG \
	                      | sed -e "s/\(PASSWORD=\).*/\1\"********\"/"\
	                      | sed -e "s/\(NETMOUNT1PASS=\).*/\1\"*******\"/" ' 560
	echo '              </td>'
	echo '            </tr>'
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
fi
#----------------------------------------------------------------------------------------

[ $MODE -ge $MODE_BETA ] && pcp_pastebin_button config.cfg

pcp_footer
[ $MODE -ge $MODE_ADVANCED ] && pcp_mode
pcp_copyright

echo '</body>'
echo '</html>'