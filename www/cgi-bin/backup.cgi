#!/bin/sh

# Version: 3.10 2017-01-06
#	Updated formatting. GE.
#	Added backup log. GE.

# Version: 0.04 2014-12-09 GE
#	HTML5 formatted.

# Version: 0.03 2014-08-29 GE
#	Added pcp_go_main_button.

# Version: 0.02 2014-07-18 GE
#	Added pcp_running_script.

# Version: 0.01 2014-06-24 GE
#	Original.

. pcp-functions
pcp_variables

pcp_html_head "Backup mydata" "SBP" "10" "main.cgi"

pcp_banner
pcp_running_script

LOG="${LOGDIR}/pcp_backup.log"
pcp_log_header $0

pcp_table_top "Backup"
pcp_textarea_inform "none" 'pcp_backup "nohtml"' "100"
pcp_table_middle
pcp_go_main_button
pcp_table_end

pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'