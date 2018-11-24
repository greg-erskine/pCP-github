#!/bin/sh

# Version: 4.1.0 2018-09-19

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