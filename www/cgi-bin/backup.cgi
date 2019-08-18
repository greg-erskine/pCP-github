#!/bin/sh

# Version: 6.0.0 2019-07-18

. pcp-functions

pcp_html_head "Backup mydata" "SBP"

pcp_banner

pcp_table_top "Backup"
pcp_backup
pcp_table_middle
pcp_redirect_button "Go to Main Page" "main.cgi" 10
pcp_table_end

pcp_html_end