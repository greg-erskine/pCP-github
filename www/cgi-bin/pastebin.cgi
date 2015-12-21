#!/bin/sh

# Version: 0.01 2015-12-21 GE
#	Original version.

. pcp-functions
pcp_variables
. $CONFIGCFG
. pcp-pastebin-functions

pcp_html_head "pastebin" "GE"

pcp_banner
pcp_navigation
pcp_running_string

pcp_httpd_query_string
FILE=$($HTPPD -d $FILE)
[ $DEBUG = "1" ] && echo '<p class="debug">[ DEBUG ] File: '$FILE'</p>'

UPLOAD_FILE=/tmp/pcp_pastebin.txt

#----------------------------------------------------------------------------------------
# file actions
#----------------------------------------------------------------------------------------

case $SUBMIT in
	Upload)
		cp $FILE $UPLOAD_FILE
		case $FILE in
			*config.cfg)
				sed -i s/^PASSWORD=.*/PASSWORD=\"******\"/ $UPLOAD_FILE
				;;
		esac
		;;
	Accept)
		pcp_pastebin_paste $UPLOAD_FILE
		;;
	Reject)
		;;
esac

#========================================================================================
# xxxxx form
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Paste</legend>'
echo '          <table class="bggrey percent100">'

pcp_toggle_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td>'
echo '                <p><b>Pastebin etc etc.</b></p>'
echo '                <p>Note: Pastebin blah blah.</p>'
echo '              </td>'
echo '            </tr>'

pcp_start_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td>'
                      pcp_textarea_inform "none" "cat $UPLOAD_FILE" 200
echo '              </td>'
echo '            </tr>'

echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------

#========================================================================================
# Accept or reject form
#----------------------------------------------------------------------------------------
if [ $SUBMIT = "Upload" ]; then
	pcp_incr_id
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <form name="Accept_reject" action="pastebin.cgi" method="get">'
	echo '        <div class="row">'
	echo '          <fieldset>'
	echo '            <legend>Accept or reject</legend>'
	echo '            <table class="bggrey percent100">'
	pcp_start_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>Accept or reject</p>'
	echo '                </td>'
	echo '              </tr>'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td colspan="3">'
	echo '                  <input type="submit" name="SUBMIT" value="Accept">'
	echo '                  <input type="submit" name="SUBMIT" value="Reject">'
	echo '                  <input type="hidden" name="FILE" value="'$FILE'">'
	echo '                </td>'
	echo '              </tr>'
	echo '            </table>'
	echo '          </fieldset>'
	echo '        </div>'
	echo '      </form>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
fi

pcp_footer
pcp_copyright


echo '</body>'
echo '</html>'