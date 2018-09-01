#!/bin/sh

# Version: 4.0.0 2018-06-15

. pcp-functions

pcp_html_head "Favorites" "GE"

#====================================Fix=================================================

[ $DEBUG -eq 1 ] && echo '<body>' || echo '<body onload="javascript:location.href=document.referrer;">'

#====================================Fix=================================================

[ $DEBUG -eq 1 ] && pcp_controls && pcp_banner && pcp_navigation && pcp_running_script

pcp_httpd_query_string

pcp_start_fav $STARTFAV

[ $DEBUG -eq 1 ] && pcp_footer

echo '</body>'
echo '</html>'