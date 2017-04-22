#!/bin/sh

# Version: 3.20 2017-03-08
#	Changed pcp_picoreplayers_toolbar and pcp_controls. GE.
#	Fixed pcp-xxx-functions issues. GE.

# Version: 0.02 2015-10-02 GE
#	Added pcp_lms_controls.

# Version: 0.01 2015-02-25 GE
#   Original version.

#========================================================================================
# This page shows the various types of LMS controls that are in development.
#   1. Controls toolbar at top
#   2. Emebded LMS page
#   3. SVG controls
#----------------------------------------------------------------------------------------

. pcp-functions
. pcp-lms-functions
#. $CONFIGCFG

pcp_html_head "xtras_controls" "GE"

pcp_picoreplayers_toolbar
pcp_controls
pcp_banner
pcp_xtras
pcp_mode_lt_developer
pcp_running_script

pcp_lms_controls

#----------------------------------------------------------------------------------------
pcp_footer
pcp_refresh_button

echo ' <embed width="15%" height="15%" src="../images/controls.svg" type="image/svg+xml" style="margin:0;"/>'

echo '<script>'

echo "window.open('http://${LMSIP}:9000/status_header.html?player=${MAC}', 'playerControl', 'width=400,height=150,status=no,menubar=no,location=no,resizable=yes');"

echo '</script>'

#http://'${LMSIP}':9000/status_header.html?player='${MAC}

echo '</body>'
echo '</html>'