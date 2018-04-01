#!/bin/sh

# Version: 3.5.1 2018-04-01
#	Added pcp_redirect_button. GE.
#	HTML5 cleanup. GE.

# Version: 3.20 2017-03-08
#	Fixed pcp-xxx-functions issues. GE.

# Version: 3.10 2017-01-06
#	Enhanced formatting. GE.
#	Added pcp_squeezelite_status. GE.

# Version: 0.01 2014-06-24 GE
#	Original. GE.

. pcp-functions

pcp_httpd_query_string
[ "$FROM_PAGE" = "" ] && FROM_PAGE="main.cgi"

pcp_html_head "Stop Squeezelite" "SBP"
pcp_banner
pcp_running_script

pcp_table_top "Stopping Squeezelite"
pcp_squeezelite_stop
sleep 1
pcp_squeezelite_status "html"
pcp_table_middle
pcp_redirect_button "Go to Main Page" "$FROM_PAGE" 5
pcp_table_end

pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'