#!/bin/sh

# Version: 4.1.0 2018-09-19

. pcp-functions

pcp_httpd_query_string
[ "$FROM_PAGE" = "" ] && FROM_PAGE="main.cgi"

pcp_html_head "Restart Squeezelite" "SBP"
pcp_banner
pcp_running_script
pcp_remove_query_string

pcp_table_top "Restarting Squeezelite"
pcp_squeezelite_stop
sleep 2
pcp_squeezelite_start
sleep 1
pcp_squeezelite_status "html"

if [ "$SHAIRPORT" = "yes" ]; then
	pcp_shairport_stop
	sleep 2
	pcp_shairport_start
fi

pcp_table_middle
pcp_redirect_button "Go to Main Page" "$FROM_PAGE" 5
pcp_table_end

pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'