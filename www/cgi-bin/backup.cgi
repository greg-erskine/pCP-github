#!/bin/sh

# Version: 7.0.0 2020-05-09

. pcp-functions

pcp_html_head "Backup mydata" "SBP"

pcp_navbar

COLUMN1="col-3"

pcp_heading5 "Backing up configuration"

echo '<span class="monospace">'
echo '<div class="p-3" style="border:1px solid">'
pcp_backup
echo '</div>'
echo '</span>'

echo '<div class="mt-3">'
pcp_redirect_button "Go to Main Page" "main.cgi?CALLED_BY=Advanced" 10
echo '</div>'

pcp_html_end
