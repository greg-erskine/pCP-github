#!/bin/sh

# Version: 0.01 2016-01-08 GE
#	Original version.

#========================================================================================
# Have a play with alsaequal
#----------------------------------------------------------------------------------------

DEBUG=1

. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "xtras alsaequal" "GE"

pcp_controls
pcp_banner
pcp_running_script
pcp_httpd_query_string

SET_EQUAL="sudo amixer -D equal cset numid="
BAND=1

#========================================================================================
# Routines
#----------------------------------------------------------------------------------------

RESET="66 66 66 66 66 66 66 66 66 66"
TREBLE="66 66 66 66 66 66 66 71 76 76"
BASS="76 76 71 66 66 66 66 66 66 66"

pcp_load_equaliser() {
	for VALUE in $RANGE
	do
		${SET_EQUAL}$BAND $VALUE >/dev/null 2>&1
		BAND=$(($BAND + 1))
	done
}

pcp_load_equaliser

#=========================================================================================
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>ALSAEQUAL</legend>'
#----------------------------------------------------------------------------------------
pcp_incr_id
echo '          <table class="bggrey percent100">'
echo '            <form name="equal" action="'$0'" method="get">'
pcp_start_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="column150">Preset</td>'
echo '                <td class="column210">'

echo '                  <select class="large16" name="RANGE">'
echo '                    <option value="'$RESET'" '$AEreset'>Reset</option>'
echo '                    <option value="'$TREBLE'" '$AEtreble'>Treble</option>'
echo '                    <option value="'$BASS'" '$AEbass'>Bass</option>'
echo '                  </select>'

echo '                </td>'
echo '              </tr>'
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'" >'
echo '                <td colspan=3>'
echo '                  <input type="submit" name="SUBMIT" value="Save">'
echo '                </td>'
echo '              </tr>'
echo '            </form>'
echo '          </table>'

#----------------------------------------------------------------------------------------
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'

#echo '                  <input class="large16" type="text" name="HOST" value="'$HOST'" maxlength="26" pattern="^[a-zA-Z0-9-]*$">'



pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'