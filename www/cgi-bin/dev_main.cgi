#!/bin/sh

# Version: 4.0.1 2018-09-19

. pcp-functions

pcp_html_head "Development pages" "GE"

pcp_banner
pcp_running_script
pcp_httpd_query_string

DEV_PAGES=$(ls /home/tc/www/cgi-bin/dev_*.cgi)

pcp_start_row_shade
pcp_toggle_row_shade

#========================================================================================
# Developer web pages
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Developer web pages</legend>'
echo '          <table class="bggrey percent100">'
#----------------------------------------------------------------------------------------
for PAGE in $DEV_PAGES
do
	PAGE=$(basename $PAGE)
	if [ "$PAGE" != "$0" ]; then
		pcp_toggle_row_shade
		echo '            <tr class="'$ROWSHADE'">'
		echo '              <td class="column300">'
		echo '                <p><a href="'$PAGE'">'${PAGE/.cgi/}'</a></p>'
		echo '              </td>'
		echo '            </tr>'
	fi
done
#----------------------------------------------------------------------------------------
echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------

pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'
