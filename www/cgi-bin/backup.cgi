#!/bin/sh

# Version: 4.0.1 2018-09-19

. pcp-functions

pcp_html_head "Backup mydata" "SBP"

pcp_banner
pcp_running_script

LOG="${LOGDIR}/pcp_backup.log"
pcp_log_header $0

pcp_table_top "Backup"
pcp_backup
pcp_table_middle
pcp_redirect_button "Go to Main Page" "main.cgi" 10
pcp_table_end

pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'