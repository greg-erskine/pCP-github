#!/bin/sh

# Version: 7.0.0 2020-05-15

# Title: Linux command line
# Description: Method for running Linux commands vi GUI.

. pcp-functions
. pcp-lms-functions

pcp_html_head "Command Line" "GE"

pcp_controls
pcp_navbar

pcp_httpd_query_string_no_decode

LINUXCMD=$(sudo $HTTPD -d $LINUXCMD)

#========================================================================================
pcp_heading5 "Linux command"
#----------------------------------------------------------------------------------------
echo '  <form name="setaudio" action="'$0'" method="get" id="setaudio">'
#----------------------------------------------------------------------------------------
echo '    <div class="row">'
echo '      <div class="col-2">'
echo '        <p>Linux command</p>'
echo '      </div>'
echo '      <div class="col-4">'
echo '        <input class="form-control form-control-sm" type="text" name="LINUXCMD" value="'$LINUXCMD'">'
echo '      </div>'
pcp_incr_id
echo '      <div class="col-6">'
echo '        <p>Enter a valid linux command and press [Execute]&nbsp;&nbsp;'
echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
echo '        </p>'
echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
echo '          <p>This page allows you to execute any valid linux command.</p>'
echo '          <p>The output of the command will display in the Output window with the error code underneath.</p>'
echo '        </div>'
echo '      </div>'
echo '    </div>'
#----------------------------------------------------------------------------------------
echo '    <div class="row">'
echo '      <div class="col-2">'
echo '        <input class="'$BUTTON'" type="submit" name="SUBMIT" value="Execute">'
echo '      </div>'
echo '    </div>'
#----------------------------------------------------------------------------------------
echo '  </form>'

#========================================================================================
# Run the linux command and display results.
#----------------------------------------------------------------------------------------
pcp_heading5 "Output" hr

TEMPFILE=$(mktemp)
eval "$LINUXCMD" 2>&1 >$TEMPFILE
RESULT=$?
pcp_textarea "none" "cat $TEMPFILE" "20"
sudo rm -f $TEMPFILE

#----------------------------------Error code--------------------------------------------
pcp_heading5 "Error code" hr

pcp_textarea "none" "echo $RESULT" "1"
#----------------------------------------------------------------------------------------

pcp_html_end