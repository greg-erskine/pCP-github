#!/bin/sh

# Version: 7.0.0 2020-05-17

. pcp-functions
. pcp-lms-functions

pcp_html_head "xtras" "GE"

pcp_controls
pcp_xtras
pcp_httpd_query_string

XTRAS_PAGES=$(ls ${WWWROOT}/cgi-bin/xtras_*.cgi)

COLUMN1="col-12"
#========================================================================================
# Developer web pages
#----------------------------------------------------------------------------------------
pcp_heading5 "Xtras web pages"

echo '  <div class="row">'

for PAGE in $XTRAS_PAGES
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
