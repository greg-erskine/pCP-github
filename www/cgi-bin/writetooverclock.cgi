#!/bin/sh

# Version: 0.03 2014-12-10 GE
#	Using pcp_html_head now.
#	HTML5 formatting.

# Version: 0.01 2014-06-24 SBP
#	Original.

. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "Write Overclock to Config" "SBP" "15" "tweaks.cgi"

pcp_banner
pcp_running_script
pcp_httpd_query_string

# Decode $OVERCLOCK using httpd, add quotes
OVERCLOCK=`sudo /usr/local/sbin/httpd -d \"$OVERCLOCK\"`
sudo sed -i "s/\(OVERCLOCK *=*\).*/\1$OVERCLOCK/" $CONFIGCFG

pcp_backup

# Call overclocking script
sudo ./overclock.sh

. $CONFIGCFG

echo '<p class="info">[ INFO ] Overclock is set to: '$OVERCLOCK'</p>'

[ $DEBUG = 1 ] && pcp_show_config_cfg

pcp_go_back_button

echo '</body>'
echo '</html>'