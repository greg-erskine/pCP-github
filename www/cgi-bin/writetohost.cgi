#!/bin/sh

# Version: 0.02 2014-12-10 GE
#	Using pcp_html_head now.
#	HTML5 formatting.

# Version: 0.01 2014-08-06 SBP
#   Original version.

. pcp-functions
pcp_variables

pcp_html_head "Write Hostname" "SBP" "15" "tweaks.cgi"

pcp_banner
pcp_running_script
pcp_httpd_query_string

# Decode Host name using httpd
HOST=`sudo $HTPPD -d \"$HOST\"`

# Update host name in config.cfg file
sudo sed -i "s/\(HOST *=*\).*/\1$HOST/" $CONFIGCFG
echo '<p class="info">[ INFO ] Your HOST name is set to: '$HOST'</p>'

# Update host name in bootsync.sh file
sudo sed -i '/sethostname/c\/usr/bin/sethostname '"$HOST" /opt/bootsync.sh

sudo hostname "$HOST"   # In order to change name immediately 

pcp_backup

[ $DEBUG = 1 ] && pcp_show_bootsync_sh
[ $DEBUG = 1 ] && pcp_show_config_cfg

pcp_go_back_button

echo '</body>'
echo '</html>'