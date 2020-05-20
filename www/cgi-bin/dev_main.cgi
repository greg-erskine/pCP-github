#!/bin/sh

# Version: 7.0.0 2020-05-20

. pcp-functions
. pcp-lms-functions

pcp_html_head "Development web pages" "GE"

pcp_controls
pcp_navbar
pcp_httpd_query_string

pcp_generate_listing "dev_*.cgi" "Developer web pages"

pcp_html_end
exit
