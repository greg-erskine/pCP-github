#!/bin/sh

# Version: 5.0.0 2019-03-13

# Title: Quiet boot
# Description: Disables boot messages and startup script output

. pcp-functions

pcp_html_head "Security" "GE"

pcp_banner
pcp_running_script
pcp_httpd_query_string

#https://forums.slimdevices.com/showthread.php?109777-Starting-piCorePlayer-without-on-screen-console-messages-possible

#logo.nologo  <==== Raspberry Pi logo
#console=tty3 <==== Redirect to nowhere
#disable_splash=1 in config.txt <==== splash screen

#/opt/bootlocal.sh

#pCPstart------
#/home/tc/www/cgi-bin/pcp_startup.sh 2>&1 | tee -a /var/log/pcp_boot.log
#/home/tc/www/cgi-bin/pcp_startup.sh > /var/log/pcp_boot.log 2>&1
#pCPstop------

#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Quiet boot</legend>'
echo '          <table class="bggrey percent100">'
#----------------------------------------------------------------------------------------
echo '            <tr>'
echo '              <td>'
echo '                <p>logo.nologo in cmdline.txt <==== Raspberry Pi logo</p>'
echo '                <p>console=tty3  in cmdline.txt <==== Redirect to nowhere</p>'
echo '                <p>disable_splash=1 in config.txt <==== splash screen</p>'
echo '                <p>/opt/bootlocal.sh</p>'
echo '                <p>/home/tc/www/cgi-bin/pcp_startup.sh > /var/log/pcp_boot.log 2>&1</p>'
echo '                <p></p>'
echo '              </td>'
echo '            </tr>'
#----------------------------------------------------------------------------------------
echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------

pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'
exit
