#!/bin/sh

# Version: 7.0.0 2020-05-26

. pcp-functions

pcp_httpd_query_string
[ "$FROM_PAGE" = "" ] && FROM_PAGE="main.cgi"

pcp_html_head "Stop Squeezelite" "SBP"

pcp_navbar

pcp_infobox_begin
pcp_squeezelite_stop "text"
sleep 2
pcp_squeezelite_status "text"
pcp_infobox_end

pcp_redirect_button "Go to Main Page" "$FROM_PAGE" 5

pcp_html_end
exit
