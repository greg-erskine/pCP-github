#!/bin/sh

# Version: 4.0.0 2018-05-18

. pcp-functions
. pcp-pastebin-functions
. pcp-rpi-functions

pcp_html_head "Pastebin" "GE"

pcp_banner
pcp_navigation
pcp_running_script
pcp_httpd_query_string

FILE=$($HTTPD -d $FILE)
UPLOAD_FILE="/tmp/pcp_pastebin.txt"

#========================================================================================
# Progress table
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Progress</legend>'
echo '          <table class="bggrey percent100">'
pcp_start_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td>'

pcp_debug_variables SUBMIT FILE UPLOAD_FILE REPORT

#----------------------------------------------------------------------------------------
# Submit actions
#----------------------------------------------------------------------------------------
case "$SUBMIT" in
	Upload)
		echo '<p class="info">[ INFO ] Prepare for uploading...</p>'
		cp "$FILE" "$UPLOAD_FILE"
		case $FILE in
			*config.cfg)
				sed -i 1i"$(date)" $UPLOAD_FILE
				sed -i s/^PASSWORD=.*/PASSWORD=\"******\"/ $UPLOAD_FILE
			;;
		esac
	;;
	Accept)
		echo '<p class="info">[ INFO ] Upload paste has been accepted.</p>'
		echo '<p class="info">[ INFO ] Encoding '$FILE'...</p>'

API_POST_CODE=$(/usr/bin/micropython -c '
#!/usr/bin/micropython
import uos as os
import sys
import ubinascii as binascii
import ure as re

infile = open("/tmp/pcp_pastebin.txt", "r")
p=re.compile("[-_.~a-zA-Z0-9]")

while True:
    ln = infile.read()
    outln=""
    if ln == "":
        break
    pos=0
    length=len(ln)-1
    while pos < length:
        c=ln[pos]
        m=p.match(c)
        if m:
            outln+=c
        else:
            c=binascii.hexlify(c)
            outln+="%"+str(c)[2:4]
        pos=pos+1
    print(outln)

infile.close
'
)

		pcp_pastebin_paste $UPLOAD_FILE $REPORT
	;;
	Reject)
		echo '<p class="info">[ INFO ] Rejected - paste was NOT uploaded.</p>'
		echo 'DELETED - paste was NOT uploaded.' >$UPLOAD_FILE
	;;
	*)
		echo '<p class="info">[ INFO ] Invalid submit option.</p>'
		echo 'Invalid submit option.' >$UPLOAD_FILE
	;;
esac

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
# Paste form.
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Paste - '$REPORT'</legend>'
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

if [ "$SUBMIT" = "Upload" ]; then
#========================================================================================
# Installing wget extension and dependencies.
#----------------------------------------------------------------------------------------
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Installing wget</legend>'
	echo '          <table class="bggrey percent100">'
	pcp_start_row_shade
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td>'
	                      pcp_install_wget
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
# Accept or reject paste form.
#----------------------------------------------------------------------------------------
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
	echo '                  <p>The Paste window above contains the paste that will be uploaded into Pastebin.</p>'
	echo '                  <p>Check you are happy with the contents BEFORE pressing the [ Accept ] button.</p>'
	echo '                  <p><b>Note:</b> The paste:</p>'
	echo '                  <ul>'
	echo '                     <li>will be sent as a private paste, so it will not visable to the public.</li>'
	echo '                     <li>will expire in 24 hours.</li>'
	echo '                  </ul>'
	echo '                  <p>Only press the [ Accept ] button if you AGREE to upload this paste to Pastebin.</p>'
	echo '                  <p>Please inform the pCP Team that you have uploaded a paste as we do not monitor Pastebin regularly.</p>'
	echo '                </td>'
	echo '              </tr>'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td>'
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
if [ "$SUBMIT" = "Accept" ]; then
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
	echo '                  <p>Please inform the pCP Team that you have uploaded a paste as we do not monitor Pastebin regularly.</p>'
	echo '                  <p>paste name: '$API_PASTE_NAME'</p>'
	echo '                  <p>url: '$PASTEBIN_URL'</p>'
	[ $MODE -ge $MODE_DEVELOPER ] && [ $TEST -eq 4 ] &&
	echo '                  <a target="_blank" href="'$PASTEBIN_URL'">'$PASTEBIN_URL'</a>'
	echo '                </td>'
	echo '              </tr>'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td>'
	                        pcp_redirect_button "Refresh Main Page" "main.cgi" 120
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