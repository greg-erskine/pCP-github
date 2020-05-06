#!/bin/sh

# Version: 7.0.0 2020-05-06

. pcp-functions

pcp_httpd_query_string
[ "$FROM_PAGE" = "" ] && FROM_PAGE="main.cgi"

pcp_html_head "Restart Squeezelite" "SBP"

pcp_navbar
pcp_remove_query_string

pcp_heading5 "Restarting Squeezelite"

echo '<div>'
pcp_squeezelite_stop "html"
sleep 2
pcp_squeezelite_start "html"
sleep 1
pcp_squeezelite_status "html"

if [ "$SHAIRPORT" = "yes" ]; then
	pcp_shairport_stop "html"
	sleep 2
	pcp_shairport_start "html"
fi
echo '</div>'

echo '<div class="mt-3">'
pcp_redirect_button "Go Back" "$FROM_PAGE" 5
echo '</div>'

pcp_html_end
