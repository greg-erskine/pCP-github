#!/bin/sh

# Version: 4.0.0 2018-04-17
#	Format cleanup. GE.

# Version: 3.5.0 2018-03-12
#	Added pcp_redirect_button. GE.

# Version: 3.20 2017-03-08
#	Fixed pcp-xxx-functions issues. GE.

# Version: 3.10 2017-01-06
#	Updated formatting. GE.
#	Added backup log. GE.

# Version: 0.01 2014-06-24
#	Original. GE.

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