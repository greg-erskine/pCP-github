#!/bin/sh

# Version: 3.03 2016-10-13 GE
#	Enhanced formatting. GE.

# Version: 0.02 2014-12-09 GE
#	HTML5 formatted.

# Version: 0.01 2014-06-24 GE
#	Original.

. pcp-functions
pcp_variables

pcp_html_head "Shutdown Raspberry Pi" "SBP" "5" "main.cgi"

pcp_banner
pcp_running_script

pcp_table_top "Shutdowning piCorePlayer"
pcp_shutdown
pcp_table_end

pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'