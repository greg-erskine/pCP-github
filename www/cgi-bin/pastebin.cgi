#!/bin/sh

# Version: 7.0.0 2020-05-31

. pcp-functions
. pcp-pastebin-functions
. pcp-rpi-functions

pcp_html_head "Pastebin" "GE"

pcp_navbar
pcp_httpd_query_string

FILE=$($HTTPD -d $FILE)
UPLOAD_FILE="/tmp/pcp_pastebin.txt"

COLUMN3_1="col-sm-2"
COLUMN3_2="col-sm-3"
COLUMN3_3="col-sm-7"

#========================================================================================
#
#----------------------------------------------------------------------------------------
pcp_border_begin
pcp_heading5 "Progress"
echo '      <div class="row mx-1 mb-2">'
echo '        <div class="col-12">'

pcp_debug_variables "html" SUBMIT FILE UPLOAD_FILE REPORT

#----------------------------------------------------------------------------------------
# Submit actions
#----------------------------------------------------------------------------------------
case "$SUBMIT" in
	Upload)
		pcp_message INFO "Prepare for uploading..." "text"
		cp "$FILE" "$UPLOAD_FILE"
		# Not really needed anymore <==GE
		case $FILE in
			*pcp.cfg)
				sed -i 1i"$(date)" $UPLOAD_FILE
				sed -i s/^PASSWORD=.*/PASSWORD=\"******\"/ $UPLOAD_FILE
			;;
		esac
	;;
	Accept)
		pcp_message INFO "Upload paste has been accepted." "text"
		pcp_message INFO "Encoding $FILE..." "text"

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
		pcp_message INFO "Rejected - paste was NOT uploaded." "text"
		echo 'DELETED - paste was NOT uploaded.' >$UPLOAD_FILE
	;;
	*)
		pcp_message INFO "Invalid submit option." "text"
		echo 'Invalid submit option.' >$UPLOAD_FILE
	;;
esac

echo '        </div>'
echo '      </div>'
pcp_border_end
#----------------------------------------------------------------------------------------

#========================================================================================
# Paste form.
#----------------------------------------------------------------------------------------
pcp_heading5 "Paste - $REPORT"
pcp_textarea "none" "cat $UPLOAD_FILE" 20
#----------------------------------------------------------------------------------------

if [ "$SUBMIT" = "Upload" ]; then
#========================================================================================
# Installing wget extension and dependencies.
#----------------------------------------------------------------------------------------
	pcp_heading5 "Installing wget"
	echo '      <div class="row">'
	echo '        <div class="col-12">'
	                pcp_install_wget
	echo '        </div>'
	echo '      </div>'
#----------------------------------------------------------------------------------------

#========================================================================================
# Accept or reject paste form.
#----------------------------------------------------------------------------------------
	echo '      <div class="alert alert-primary mt-3" role="alert">'
	echo '        <div class="col-12">'
	echo '          <b>WARNING:</b>'
	echo '          <p>The Paste window above contains the paste that will be uploaded into Pastebin.</p>'
	echo '          <p>Check you are happy with the contents BEFORE pressing the [ Accept ] button.</p>'
	echo '          <p><b>Note:</b> The paste:</p>'
	echo '          <ul>'
	echo '             <li>will be sent as a private paste, so it will not visable to the public.</li>'
	echo '             <li>will expire in 24 hours.</li>'
	echo '          </ul>'
	echo '          <p>Only press the [ Accept ] button if you AGREE to upload this paste to Pastebin.</p>'
	echo '          <p>Please inform the pCP Team that you have uploaded a paste as we do not monitor Pastebin regularly.</p>'
	echo '        </div>'
	echo '      </div>'


	echo '    <form name="Accept_reject" action="pastebin.cgi" method="get">'
	echo '      <div class="row mb-2">'
	echo '        <div class="'$COLUMN3_1'">'
	echo '          <input class="'$BUTTON'" type="submit" name="SUBMIT" value="Accept">'
	echo '        </div>'
	echo '        <div class="'$COLUMN3_1'">'
	echo '          <input class="'$BUTTON'" type="submit" name="SUBMIT" value="Reject">'
	echo '          <input type="hidden" name="FILE" value="'$FILE'">'
	echo '          <input type="hidden" name="REPORT" value="'$REPORT'">'
	echo '        </div>'
	echo '      </div>'
	echo '    </form>'
fi

#========================================================================================
# Results form
#----------------------------------------------------------------------------------------
if [ "$SUBMIT" = "Accept" ]; then
	pcp_heading5 "Results"
	pcp_border_begin
	echo '      <div class="row">'
	echo '        <div class="col-12">'
	echo '          <p>Please inform the pCP Team that you have uploaded a paste as we do not monitor Pastebin regularly.</p>'
	echo '          <p>paste name: '$API_PASTE_NAME'</p>'
	echo '          <p>url: '$PASTEBIN_URL'</p>'
	[ $MODE -ge $MODE_DEVELOPER ] && [ $TEST -eq 4 ] &&
	echo '          <a target="_blank" href="'$PASTEBIN_URL'">'$PASTEBIN_URL'</a>'
	echo '        </div>'
	echo '      </div>'
	pcp_border_end
	pcp_redirect_button "Refresh Main Page" "main.cgi" 1200
fi

pcp_html_end
exit
