#!/bin/sh

# Version: 7.0.0 2020-05-26

. pcp-functions

pcp_httpd_query_string
[ "$FROM_PAGE" = "" ] && FROM_PAGE="main.cgi"

pcp_html_head "Restart Squeezelite" "SBP"

pcp_navbar
pcp_remove_query_string

pcp_heading5 "Restarting Squeezelite"

pcp_infobox_begin
pcp_squeezelite_stop "text"
sleep 2
pcp_squeezelite_start "text"
sleep 1
pcp_squeezelite_status "text"

if [ "$SHAIRPORT" = "yes" ]; then
	pcp_shairport_stop "text"
	sleep 2
	pcp_shairport_start "text"
fi
pcp_infobox_end

pcp_redirect_button "Go Back" "$FROM_PAGE" 50

pcp_html_end
