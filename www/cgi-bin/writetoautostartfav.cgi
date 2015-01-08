#!/bin/sh

# Version: 0.01 2015-01-08 GE
#	Original.

. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "Write to Autostart favorite" "GE" "15" "tweaks.cgi"

pcp_banner
pcp_running_script
pcp_httpd_query_string

# Save the encoded parameter to the config file, with quotes
sudo sed -i "s/\(AUTOSTARTFAV=\).*/\1\"$AUTOSTARTFAV\"/" $CONFIGCFG
echo '<p class="info">[ INFO ] Autostart favorite is set to: '$AUTOSTARTFAV'</p>'

pcp_backup

if [ "$SUBMIT" == "Test" ]; then
	echo '<p class="info">[ INFO ] Submit: '$SUBMIT'</p>'
	pcp_auto_start_fav
fi

[ $DEBUG = 1 ] && pcp_show_config_cfg
pcp_go_back_button

echo '</body>'
echo '</html>'