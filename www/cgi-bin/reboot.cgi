#!/bin/sh

# Version: 4.0.0 2018-04-17
#	Another attempt to fix reloading page does not reboot pCP again. SBP.

# Version: 3.20 2017-03-08
#	Fixed pcp-xxx-functions issues. GE.
#	Fix to reloading page does not reboot pCP again. PH.

# Version: 3.10 2017-01-06
#	Enhanced formatting. GE.

# Version: 0.01 2014-06-24
#	Original. GE.

. pcp-functions

pcp_html_head "Reboot Raspberry Pi" "SBP" "0" "main.cgi?ACTION=reboot"

#pcp_banner
#pcp_running_script
#
#	pcp_table_top "Rebooting"
#	echo "pCP is rebooting....."
#	pcp_table_middle
#	echo "pCP will automatically reload when available"
#	echo '<script>pcp_redirect("10","main.cgi")</script>'
#
#pcp_table_end
#
#pcp_footer
#pcp_copyright
#
echo '</body>'
echo '</html>'
exit
#
#pcp_reboot >/dev/null 2>&1 &
