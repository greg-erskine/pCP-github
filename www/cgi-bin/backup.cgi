#!/bin/sh

# Version: 7.0.0 2020-05-12

. pcp-functions

pcp_html_head "Backup mydata" "SBP"

pcp_navbar

pcp_heading5 "Backing up configuration"

pcp_infobox_begin
pcp_backup "text"
pcp_infobox_end

pcp_redirect_button "Go to Main Page" "main.cgi" 10

pcp_html_end
