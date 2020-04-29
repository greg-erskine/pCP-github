#!/bin/sh

# Version: 7.0.0 2020-04-26

. pcp-functions

pcp_html_head "Backup mydata" "SBP"

pcp_navbar

echo '<div>'
pcp_backup
echo '</div>'

pcp_redirect_button "Go to Main Page" "main.cgi" 10

pcp_html_end