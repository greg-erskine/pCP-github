#!/bin/sh

# Version: 4.0.0 2018-10-06

. pcp-functions
. pcp-lms-functions

pcp_html_head "xtras" "GE"

pcp_banner
pcp_running_script
pcp_xtras

#========================================================================================
pcp_table_top "Favorites toolbar"
#echo '<h1>Favorites toolbar</h1>'
echo '<p><b>Note: </b>Your favorites should be appearing in the toolbar below.</p>'
pcp_table_end
pcp_lms_favorites
#----------------------------------------------------------------------------------------

#========================================================================================
pcp_table_top "Common buttons test"
#echo '<h1>Common buttons test</h1>'
echo '<p><b>Note: </b>The commonly used buttons should appear below.</p>'
pcp_go_main_button
pcp_refresh_button
pcp_go_back_button
pcp_reboot_button
pcp_table_end
#----------------------------------------------------------------------------------------

pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'