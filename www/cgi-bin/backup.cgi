#!/bin/sh

# Version: 7.0.0 2020-04-26

. pcp-functions

pcp_html_head "Backup mydata" "SBP"

pcp_banner

#pcp_table_top "Backup"
echo '<div>'
pcp_backup
#pcp_table_middle
echo '</div>'
echo '<div>'
pcp_redirect_button "Go to Main Page" "main.cgi" 10
#pcp_table_end
echo '</div>'

pcp_html_end