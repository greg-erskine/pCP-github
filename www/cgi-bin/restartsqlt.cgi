#!/bin/sh

# Version: 0.3 2016-01-07 SBP
#	Added shairport restart.

# Version: 0.2 2014-12-09 GE
#	HTML5 formatted.

# Version: 0.1 2014-06-24 GE
#	Original.

. pcp-functions
pcp_variables

pcp_html_head "Restart Squeezelite" "SBP" "5" "main.cgi"

pcp_banner
pcp_running_script
pcp_squeezelite_stop
sleep 2
pcp_squeezelite_start

if [ $SHAIRPORT = yes ]; then
	pcp_shairport_stop
	sleep 2
	pcp_shairport_start
fi

echo '</body>'
echo '</html>'