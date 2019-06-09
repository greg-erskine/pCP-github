#!/bin/sh

# Version: 5.0.0 2019-04-24

# Title: Linux command line
# Description: Method for running Linux commands vi GUI.

. pcp-functions
. pcp-lms-functions

pcp_html_head "Command Line" "GE"

pcp_banner
pcp_running_script

pcp_httpd_query_string_no_decode
LINUXCMD=$(sudo $HTTPD -d $LINUXCMD)

#========================================================================================
# Start table
#----------------------------------------------------------------------------------------
pcp_incr_id
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <form name="setaudio" action="'$0'" method="get" id="setaudio">'
echo '        <div class="row">'
echo '          <fieldset>'
echo '            <legend>Linux command</legend>'
echo '            <table class="bggrey percent100">'
#----------------------------------------------------------------------------------------
pcp_incr_id
pcp_start_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="column150">'
echo '                  <p>Linux Command</p>'
echo '                </td>'
echo '                <td>'
echo '                  <input class="large60" type="text" name="LINUXCMD" value="'$LINUXCMD'">'
echo '                </td>'
echo '              </tr>'
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td>'
echo '                  <p>Enter a valid linux command and press [Execute]&nbsp;&nbsp;'
echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                  </p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <p>This page allows you to execute any valid linux command.</p>'
echo '                    <p>The output of the command will display in the Output window with the error code underneath.</p>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'
#----------------------------------------------------------------------------------------
pcp_incr_id
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td  class="column150">'
echo '                  <input type="submit" name="SUBMIT" value="Execute">'
echo '                </td>'
echo '              </tr>'
#----------------------------------------------------------------------------------------
echo '            </table>'
echo '          </fieldset>'
echo '        </div>'
echo '      </form>'
echo '    </td>'
echo '  </tr>'
echo '</table>'

#========================================================================================
# Run the linux command and display results.
#----------------------------------------------------------------------------------------
pcp_start_row_shade
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <form name="cmdline_output" method="get">'
echo '        <div class="row">'
echo '          <fieldset>'
echo '            <legend>Output</legend>'
echo '            <table class="bggrey percent100">'
echo '              <tr class="'$ROWSHADE'">'
echo '                <td>'

	TEMPFILE=$(mktemp)
	echo '<textarea class="inform" style="height:250px">'
	eval "$LINUXCMD" 2>&1 >$TEMPFILE
	RESULT=$?
	cat $TEMPFILE
	sudo rm -f $TEMPFILE
	echo '</textarea>'

echo '                </td>'
echo '              </tr>'
echo '            </table>'
echo '          </fieldset>'
echo '        </div>'
echo '      </form>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------Error code--------------------------------------------
pcp_start_row_shade
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <form name="result" method="get">'
echo '        <div class="row">'
echo '          <fieldset>'
echo '            <legend>Error code</legend>'
echo '            <table class="bggrey percent100">'
echo '              <tr class="'$ROWSHADE'">'
echo '                <td>'
	                    pcp_textarea_inform "none" "echo $RESULT" "20"
echo '                </td>'
echo '              </tr>'
echo '            </table>'
echo '          </fieldset>'
echo '        </div>'
echo '      </form>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------

pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'