#!/bin/sh

# Version: 3.20 2017-03-08
#	Fixed pcp-xxx-functions issues. GE.
#	Fix to reloading page does not reboot pCP again. PH.

# Version: 3.10 2017-01-06
#	Enhanced formatting. GE.

# Version: 0.03 2016-02-02 GE
#	Added pcp_go_main_button.

# Version: 0.02 2014-12-09 GE
#	HTML5 formatted.

# Version: 0.01 2014-06-24 GE
#	Original.

. pcp-functions

pcp_html_head "Reboot Raspberry Pi" "SBP" "5" "main.cgi"

pcp_banner
pcp_running_script
pcp_remove_query_string
pcp_httpd_query_string

case $RB in
	yes)
		pcp_table_top "Rebooting"
		pcp_reboot
		pcp_table_middle
	;;
	*)
		pcp_table_top "pCP has Rebooted"
		pcp_table_middle
	;;
esac

pcp_go_main_button
pcp_table_end

pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'