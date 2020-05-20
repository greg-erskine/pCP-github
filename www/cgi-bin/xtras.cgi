#!/bin/sh

# Version: 7.0.0 2020-05-20

. pcp-functions
. pcp-lms-functions

pcp_html_head "xtras" "GE"

pcp_controls
pcp_xtras
pcp_httpd_query_string

pcp_generate_listing "xtras_*.cgi" "Xtras web pages"

pcp_html_end
exit
