#!/bin/sh

# Version: 7.0.0 2020-05-06

. pcp-functions

pcp_html_head "Backup mydata" "SBP"

pcp_navbar

pcp_heading5 "Backing up configuration"

echo '<div>'
pcp_backup
echo '</div>'

echo '<div class="mt-3">'
pcp_redirect_button "Go to Main Page" "main.cgi" 10
echo '</div>'

pcp_html_end
