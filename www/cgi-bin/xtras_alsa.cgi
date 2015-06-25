#!/bin/sh

# Version: 0.01 2015-06-24 GE
#   Original version.

. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "xtras_alsa" "GE"

pcp_controls
pcp_banner
pcp_xtras
pcp_mode_lt_99
pcp_running_script





pcp_footer
pcp_refresh_button

echo '</body>'
echo '</html>'