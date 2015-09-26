#!/bin/sh

# Version: 0.01 2015-09-26 GE
#   Original version.

. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "xtras_controls" "GE"

pcp_controls
pcp_banner
pcp_xtras
pcp_mode_lt_developer
pcp_running_script

#========================================================================================
# SVG piCorePlayer simple controls
#----------------------------------------------------------------------------------------
echo '<embed width="15%" height="15%" src="../images/controls.svg" type="image/svg+xml" style="margin:0;"/>'

#echo '<p><img src="../images/controls.svg"></p>'

#----------------------------------------------------------------------------------------

pcp_footer
pcp_refresh_button

echo '</body>'
echo '</html>'