#!/bin/sh

# Version: 0.01 2014-12-18 GE
#   Original version.

. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "xtras" "GE"

pcp_banner
pcp_running_string
pcp_xtras
pcp_go_main_button





pcp_refresh_button
pcp_go_back_button
pcp_reboot_button

pcp_footer
echo '</body>'
echo '</html>'