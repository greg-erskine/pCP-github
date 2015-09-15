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
echo '<p class="info">[ INFO ] Host is now: '$HOST'</p>'
pcp_mount_mmcblk0p1
pcp_write_to_host
pcp_umount_mmcblk0p1
pcp_save_to_config
pcp_backup

[ $DEBUG = 1 ] && pcp_show_bootsync_sh
[ $DEBUG = 1 ] && pcp_show_config_cfg

pcp_go_back_button

echo '</body>'
echo '</html>'