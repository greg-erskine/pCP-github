#!/bin/sh

# Version: 4.0.0 2018-04-17
#	Added pcp_redirect_button. GE.
#	HTML5 cleanup. GE.

# Version: 3.5.0 2018-02-04
#	Return to requested page. PH.

# Version: 3.20 2017-03-08
#	Fixed pcp-xxx-functions issues. GE.

# Version: 3.10 2017-01-06
#	Enhanced formatting. GE.
#	Added pcp_squeezelite_status. GE.

# Version: 0.01 2014-06-24
#	Original. GE.

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