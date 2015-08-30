#!/bin/sh

# Version: 0.01 2015-08-30 GE
#   Original version.

. pcp-lms-functions
. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "Xtras Command Line" "GE"

pcp_banner
pcp_running_string
pcp_xtras

DEBUG=1

pcp_httpd_query_string
LINUXCMD=`sudo $HTPPD -d $LINUXCMD`

#========================================================================================
# Start table
#----------------------------------------------------------------------------------------
pcp_incr_id
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <form name="setaudio" action="xtras_cmdline.cgi" method="get" id="setaudio">'
echo '        <div class="row">'
echo '          <fieldset>'
echo '            <legend>Linux command</legend>'
echo '            <table class="bggrey percent100">'

#--------------------------------------Name of your player-------------------------------
pcp_incr_id
pcp_start_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="column150">'
echo '                  <p>Linux Command</p>'
echo '                </td>'
echo '                <td class="column210">'
echo '                  <input class="large15" type="text" name="LINUXCMD" value="'$LINUXCMD'">'
echo '                </td>'
echo '                <td>'
echo '                  <p>Enter a valid linux command and press execute&nbsp;&nbsp;'
echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                  </p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <p>More information goes here.</p>'
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
echo '            <legend>Command output</legend>'
echo '            <table class="bggrey percent100">'
echo '              <tr class="'$ROWSHADE'">'
echo '                <td>'



	TEMPFILE=$(mktemp)

	echo '<textarea class="inform" style="height:250px">'
	eval "$LINUXCMD" 2>&1 >$TEMPFILE
	echo $?
	cat $TEMPFILE
	sudo rm -f $TEMPFILE
	echo '</textarea>'




#	                    pcp_textarea_inform "none" "$LINUXCMD" "250"
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