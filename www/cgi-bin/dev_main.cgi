#!/bin/sh

# Version: 7.0.0 2020-05-04

. pcp-functions

pcp_html_head "Development pages" "GE"

pcp_controls
pcp_navbar
pcp_httpd_query_string

DEV_PAGES=$(ls ${WWWROOT}/cgi-bin/dev_*.cgi)

COLUMN1="col-12"
#========================================================================================
# Developer web pages
#----------------------------------------------------------------------------------------
pcp_heading5 "Developer web pages"

echo '  <div class="row">'

for PAGE in $DEV_PAGES
do
	pcp_get_page_info $PAGE
	[ "$TITLE" = "" ] && TITLE=$BASENAME
	if [ "$BASENAME" != "$0" ]; then
		echo '    <div class="col-3">'
		echo '      <a href="'$BASENAME'">'$TITLE'</a>'
		echo '    </div>'
		echo '    <div class="col-7">'
		echo '      '$DESCR
		echo '    </div>'
		echo '    <div class="col-2">'
		echo '      '$VERSION
		echo '    </div>'
	fi
done

echo '  </div>'
echo '  <br>'

pcp_html_end
exit
