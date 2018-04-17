#!/bin/sh

# Version: 4.0.0 2018-04-17
#	Changed order of pcp-pastebin-functions and pcp-rpi-functions. GE.
#	HTML5 update. GE.
#	Changed to micropython script for encoding. GE.

# Version: 3.20 2017-03-08
#	Fixed pcp-xxx-functions issues. GE.

# Version: 0.02 2016-05-09
#	Renamed variable HTPPD to HTTPD. GE.

# Version: 0.01 2016-02-05
#	Original version. GE.

. pcp-functions
. pcp-pastebin-functions
. pcp-rpi-functions

pcp_html_head "pastebin" "GE"

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

if [ $DEBUG -eq 1 ]; then
	echo '<p class="debug">[ DEBUG ] $SUMBMIT: '$SUBMIT'<br />'
	echo '                 [ DEBUG ] $LOG: '$LOG'<br />'
	echo '                 [ DEBUG ] $UPLOAD_FILE: '$UPLOAD_FILE'<br />'
	echo '                 [ DEBUG ] $FILE: '$FILE'</p>'
fi

pcp_check_binascii

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
		echo '<p class="info">[ INFO ] Upload has been accepted.</p>'
		echo '<p class="info">[ INFO ] Encoding '$FILE'...</p>'
API_POST_CODE=$(/usr/bin/micropython -c '
#!/usr/bin/micropython
import uos as os
import sys
import binascii
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
            c=binascii.b2a_hex(c)
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
		echo "DELETED - paste text was NOT uploaded." >$UPLOAD_FILE
	;;
	*)
		echo '<p class="info">[ INFO ] Invalid submit option.</p>'
		echo "Invalid submit option." >$UPLOAD_FILE
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
# Paste form
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

#========================================================================================
# Accept or reject paste form
#----------------------------------------------------------------------------------------
if [ "$SUBMIT" = "Upload" ]; then
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
	                        pcp_install_wget
	echo '                </td>'
	echo '              </tr>'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td>'
	echo '                  <p>The window above contains the paste that will be uploaded '
	echo '                     into pastebin. Check you are happy with the content '
	echo '                     before you press [Accept].</p>'
	echo '                  <p>The paste will be sent as a private paste, so it will not visable to the public. '
	echo '                     Also, the paste will expire in 24 hours.</p>'
	echo '                  <br />'
	echo '                  <p>Only press [Accept] if you AGREE to upload this paste to pastebin.</p>'
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
	echo '                  <p>paste name: '$API_PASTE_NAME'</p>'
	echo '                  <p>url: '$PASTEBIN_URL'</p>'
	[ $MODE -ge $MODE_DEVELOPER ] && [ $TEST -eq 4 ] &&
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