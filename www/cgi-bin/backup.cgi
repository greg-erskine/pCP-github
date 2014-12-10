#!/bin/sh

# Version: 0.04 2014-12-09 GE
#	HTML5 formatted.

# Version: 0.03 2014-08-29 GE
#	Added pcp_go_main_button.

# Version: 0.02 2014-07-18 GE
#	Added pcp_running_script.

# Version: 0.01 2014-06-24 GE
#	Original.

. pcp-functions
pcp_variables

pcp_html_head "Backup mydata" "SBP" "5" "main.cgi"
pcp_banner
pcp_running_script
pcp_backup
pcp_go_main_button

echo '</body>'
echo '</html>'