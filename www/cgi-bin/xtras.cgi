#!/bin/sh

# Version: 3.20 2017-03-08
#	Fixed pcp-xxx-functions issues. GE.

# Version: 0.02 2015-07-04 GE
#	Removed pcp_picoreplayers and pcp_uptime_days.

# Version: 0.01 2015-04-30 GE
#	Original version.

. pcp-functions
. pcp-lms-functions
#. $CONFIGCFG

pcp_html_head "xtras" "GE"

pcp_banner
pcp_running_script
pcp_xtras

#========================================================================================
echo '<h1>Favorites toolbar</h1>'
#----------------------------------------------------------------------------------------
echo '<p><b>Note: </b>Your favorites should be appearing in the toolbar below.</p>'
pcp_favorites
#----------------------------------------------------------------------------------------

#========================================================================================
echo '<h1>Common buttons test</h1>'
#----------------------------------------------------------------------------------------
echo '<p><b>Note: </b>The commonly used buttons should appear below.</p>'
pcp_go_main_button
pcp_refresh_button
pcp_go_back_button
pcp_reboot_button
#----------------------------------------------------------------------------------------

pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'