#!/bin/sh

# Version: 3.20 2017-03-08
#	Fixed pcp-xxx-functions issues. GE.

# Version: 3.10 2017-01-06
#	Enhanced formatting. GE.
#	Added pcp_squeezelite_status. GE.

# Version: 0.04 2016-02-02 GE
#	Added pcp_go_main_button.

# Version: 0.03 2016-01-07 SBP
#	Added shairport restart.

# Version: 0.02 2014-12-09 GE
#	HTML5 formatted.

# Version: 0.01 2014-06-24 GE
#	Original.

. pcp-functions

pcp_html_head "Restart Squeezelite" "SBP" "5" "main.cgi"

pcp_banner
pcp_running_script

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

pcp_table_end

[ $DEBUG -eq 1 ] && pcp_go_main_button

pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'