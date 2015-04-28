#!/bin/sh

# Version: 0.01 2015-04-28 GE
#   Original version.

. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "xtras" "GE"

pcp_banner
pcp_running_string
pcp_xtras

#========================================================================================
echo '<h1>Common buttons test</h1>'
#----------------------------------------------------------------------------------------
echo '<p><b>Note: </b>The commonly used buttons should appear below.</p>'
pcp_go_main_button
pcp_refresh_button
pcp_go_back_button
pcp_reboot_button
#----------------------------------------------------------------------------------------

#========================================================================================
echo '<h1>Favorites toolbar</h1>'
#----------------------------------------------------------------------------------------
echo '<p><b>Note: </b>Your favorites should be appearing in the toolbar below.</p>'
pcp_favorites
#----------------------------------------------------------------------------------------

echo '<br />'

pcp_footer
echo '</body>'
echo '</html>'