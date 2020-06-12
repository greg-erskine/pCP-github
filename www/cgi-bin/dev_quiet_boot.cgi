#!/bin/sh

# Version: 7.0.0 2020-06-12

# Title: Quiet boot
# Description: Disables boot messages and startup script output

. pcp-functions

pcp_html_head "Security" "GE"

pcp_httpd_query_string
pcp_navbar

#https://forums.slimdevices.com/showthread.php?109777-Starting-piCorePlayer-without-on-screen-console-messages-possible

#logo.nologo  <==== Raspberry Pi logo
#console=tty3 <==== Redirect to nowhere
#disable_splash=1 in config.txt <==== splash screen

#/opt/bootlocal.sh

#pCPstart------
#/usr/local/etc/init.d/pcp_startup.sh 2>&1 | tee -a /var/log/pcp_boot.log
#/usr/local/etc/init.d/pcp_startup.sh > /var/log/pcp_boot.log 2>&1
#pCPstop------

#----------------------------------------------------------------------------------------
pcp_heading5 "Quiet boot"
#----------------------------------------------------------------------------------------
pcp_border_begin
echo '    <div class="row mx-1">'
echo '      <ul>'
echo '        <li>logo.nologo in cmdline.txt <== Raspberry Pi logo</li>'
echo '        <li>console=tty3 in cmdline.txt <== Redirect to nowhere</li>'
echo '        <li>disable_splash=1 in config.txt <== splash screen</li>'
echo '        <li>/opt/bootlocal.sh</li>'
echo '        <li>/usr/local/etc/init.d/pcp_startup.sh > /var/log/pcp_boot.log 2>&1</li>'
echo '      </ul>'
echo '    </div>'
pcp_border_end
#----------------------------------------------------------------------------------------

pcp_html_end
exit
