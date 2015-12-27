#!/bin/sh

# Version: 0.01 2015-12-24 GE
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
# Submit actions
#----------------------------------------------------------------------------------------
case $SUBMIT in
	Upload)
		cp $FILE $UPLOAD_FILE
		case $FILE in
			*config.cfg)
				sed -i 1i"$(date)" $UPLOAD_FILE
				sed -i s/^PASSWORD=.*/PASSWORD=\"******\"/ $UPLOAD_FILE
				;;
		esac
		;;
	Accept)
		pcp_pastebin_paste $UPLOAD_FILE $REPORT
		;;
	Reject)
		echo "DELETED - paste text was NOT uploaded." >$UPLOAD_FILE
		;;
	*)
		echo "Invalid submit option." >$UPLOAD_FILE
		;;
esac

#========================================================================================
# Paste text form
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Paste text - '$REPORT'</legend>'
echo '          <table class="bggrey percent100">'
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
# Accept or reject paste text form
#----------------------------------------------------------------------------------------
if [ $SUBMIT = "Upload" ]; then
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <form name="Accept_reject" action="pastebin.cgi" method="get">'
	echo '        <div class="row">'
	echo '          <fieldset>'
	echo '            <legend>WARNING</legend>'
	echo '            <table class="bggrey percent100">'
	pcp_start_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td>'
	echo '                  <p>The window above contains the paste text that will be uploaded '
	echo '                     into pastebin. Please check you are happy with the content '
	echo '                     before you press [Accept].</p>'
	echo '                  <p>The paste text will be sent as a private paste, so it will not visable to the public. '
	echo '                     Also, the paste will expire in 24 hours.</p>'
	echo '                  <br />'
	echo '                  <p>Only press [Accept] if you AGREE to upload this paste text to pastebin.</p>'
	echo '                </td>'
	echo '              </tr>'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td colspan="3">'
	echo '                  <input type="submit" name="SUBMIT" value="Accept">'
	echo '                  <input type="submit" name="SUBMIT" value="Reject">'
	echo '                  <input type="hidden" name="FILE" value="'$FILE'">'
	echo '                  <input type="hidden" name="REPORT" value="'$REPORT'">'
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

#========================================================================================
# Results form
#----------------------------------------------------------------------------------------
if [ $SUBMIT = "Accept" ]; then
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <form name="Results" method="get">'
	echo '        <div class="row">'
	echo '          <fieldset>'
	echo '            <legend>Results</legend>'
	echo '            <table class="bggrey percent100">'
	pcp_start_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td>'
	echo '                  <p>url: '$PASTEBIN_URL'</p>'
	[ $MODE -ge $MODE_DEVELOPER ] &&
	echo '                  <a target="_blank" href="'$PASTEBIN_URL'">'$PASTEBIN_URL'</a>'
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