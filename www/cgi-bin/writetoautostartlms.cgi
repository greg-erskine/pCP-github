#!/bin/sh

# Version: 0.02 2014-12-10 GE
#	Using pcp_html_head now.
#	HTML5 formatting.

# Version: 0.01 2014-09-09 GE
#	Original.

. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "Write to Autostart LMS" "SBP" "15" "tweaks.cgi"

pcp_banner
pcp_running_script
pcp_httpd_query_string

# Save the encoded parameter to the config file, with quotes
sudo sed -i "s/\(AUTOSTARTLMS=\).*/\1\"$AUTOSTARTLMS\"/" $CONFIGCFG
echo '<p class="info">[ INFO ] Autostart LMS is set to: '$AUTOSTARTLMS'</p>'

pcp_backup
[ $DEBUG = 1 ] && pcp_show_config_cfg
pcp_go_back_button

echo '</body>'
echo '</html>'