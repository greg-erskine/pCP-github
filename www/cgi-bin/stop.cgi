#!/bin/sh

# Version: 3.03 2016-10-19 GE
#	Enhanced formatting. GE.
#	Added pcp_squeezelite_status. GE.

# Version: 0.02 2014-12-09 GE
#	HTML5 formatted.

# Version: 0.01 2014-06-24 GE
#	Original.

. pcp-functions
pcp_variables

pcp_html_head "Stop Squeezelite" "SBP" "5" "main.cgi"

pcp_banner
pcp_running_script

pcp_table_top "Stopping Squeezelite"
pcp_squeezelite_stop
sleep 1
pcp_squeezelite_status "html"
pcp_table_end

pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'