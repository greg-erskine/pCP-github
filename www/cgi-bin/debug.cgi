#!/bin/sh

# Version: 6.0.0 2019-10-29

#=========================================================================================
# This cgi script quickly turns on/off/sets $DEBUG, $TEST and $MODE in pcp.cfg from
# your web browser.
#
# Options:
#	$DEBUG   d=[0|1]
#	$TEST    t=[0-9]
#	$MODE    m=[0-100]
#	ALL      a=[0]
#
# Non-interactive examples: DOES NOT WORK!!! <==GE
#	Turn debug on:   http://192.168.1.xxx/cgi-bin/debug.cgi?d=1
#	Turn debug off:  http://192.168.1.xxx/cgi-bin/debug.cgi?d=0
#	Turn all off:    http://192.168.1.xxx/cgi-bin/debug.cgi?a=0
#
# Interactive mode example:
#	http://192.168.1.xxx/cgi-bin/debug.cgi
#-----------------------------------------------------------------------------------------

. pcp-functions

#========================================================================================
# Functions
#----------------------------------------------------------------------------------------
pcp_debug_save() {
	pcp_write_var_to_config DEBUG $d
	pcp_write_var_to_config TEST $t
	pcp_write_var_to_config MODE $m
	. $PCPCFG
}

pcp_debug_reset() {
	pcp_write_var_to_config DEBUG 0
	pcp_write_var_to_config TEST 0
	pcp_write_var_to_config MODE $MODE_PLAYER
	. $PCPCFG
}

pcp_debug_cli() {
	case "$QUERY_STRING" in
		d=[01])
			pcp_write_var_to_config DEBUG $d
		;;
		t=[0-9])
			pcp_write_var_to_config TEST $t
		;;
		m=100|m=[0-9][0-9]|m=[0-9])
			pcp_write_var_to_config MODE $m
		;;
		a=[0])
			pcp_debug_reset
		;;
		*)
			[ $DEBUG -eq 1 ] && echo '<p class="error">[ ERROR ] Invalid option: '$QUERY_STRING'</p>'
		;;
	esac
	. $PCPCFG
}

#========================================================================================
# Main
#----------------------------------------------------------------------------------------
pcp_html_head "Debug" "GE"
pcp_httpd_query_string

if [ x"" != x"$QUERY_STRING" ] && [ x"" = x"$ACTION" ]; then
	pcp_debug_cli
	echo '<body onload="javascript:location.href=document.referrer;">'
	exit 0
fi

case "$ACTION" in
	Save) pcp_debug_save ;;
	Res*) pcp_debug_reset ;;
esac

pcp_banner
pcp_navigation

#========================================================================================
# Debug info
#----------------------------------------------------------------------------------------
if [ $DEBUG -eq 1 ]; then
	pcp_table_top "Debug"
	pcp_debug_variables "html" QUERY_STRING DEBUG d MODE m TEST t ACTION
	pcp_table_end
fi

COLUMN1="column100"
COLUMN2="column150"
#========================================================================================
# Debug table
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <form name="debug" action="'$0'" method="get">'
echo '        <div class="row">'
echo '          <fieldset>'
echo '            <legend>Set debug options</legend>'
echo '            <table class="bggrey percent100">'
#--------------------------------------DEBUG---------------------------------------------
eval D${DEBUG}SELECTED=checked
pcp_start_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="'$COLUMN1'">'
echo '                  <p>DEBUG</p>'
echo '                </td>'
echo '                <td class="'$COLUMN2'">'
echo '                  <input id="rad1" type="radio" name="d" value="1" '$D1SELECTED'>'
echo '                  <label for="rad1">On&nbsp;</label>'
echo '                  <input id="rad2" type="radio" name="d" value="0" '$D0SELECTED'>'
echo '                  <label for="rad2">Off</label>'
echo '                </td>'
echo '                <td>'
echo '                  <p>Set DEBUG: [on|off].</p>'
echo '                </td>'
echo '              </tr>'
#--------------------------------------MODE----------------------------------------------
eval MODE${MODE}="selected"
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="'$COLUMN1'">'
echo '                  <p>MODE</p>'
echo '                </td>'
echo '                <td class="'$COLUMN2'">'
echo '                  <select class="large10" name="m">'
#echo '                    <option value="0" '$MODE0'>Initial</option>'
#echo '                    <option value="10" '$MODE10'>Basic</option>'
#echo '                    <option value="20" '$MODE20'>Normal</option>'
#echo '                    <option value="30" '$MODE30'>Advanced</option>'
echo '                    <option value="10" '$MODE10'>Player</option>'
echo '                    <option value="30" '$MODE30'>Player/Server</option>'
echo '                    <option value="40" '$MODE40'>Beta</option>'
echo '                    <option value="100" '$MODE100'>Developer</option>'
echo '                  </select>'
echo '                </td>'
echo '                <td>'
#echo '                  <p>Set MODE level: [Initial|Basic|Normal|Advanced|Beta|Developer].</p>'
echo '                  <p>Set MODE level: [Player|Server|Beta|Developer].</p>'
echo '                </td>'
echo '              </tr>'
#--------------------------------------TEST----------------------------------------------
eval TEST${TEST}="selected"
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="'$COLUMN1'">'
echo '                  <p>TEST</p>'
echo '                </td>'
echo '                <td class="'$COLUMN2'">'
echo '                  <select class="large10" name="t">'
echo '                    <option value="0" '$TEST0'>0</option>'
echo '                    <option value="1" '$TEST1'>1</option>'
echo '                    <option value="2" '$TEST2'>2</option>'
echo '                    <option value="3" '$TEST3'>3</option>'
echo '                    <option value="4" '$TEST4'>4</option>'
echo '                    <option value="5" '$TEST5'>5</option>'
echo '                    <option value="6" '$TEST6'>6</option>'
echo '                    <option value="7" '$TEST7'>7</option>'
echo '                    <option value="8" '$TEST8'>8</option>'
echo '                    <option value="9" '$TEST9'>9</option>'
echo '                  </select>'
echo '                </td>'
echo '                <td>'
echo '                  <p>Set TEST level: [0-9].</p>'
echo '                </td>'
echo '              </tr>'
#--------------------------------------BUTTONS-------------------------------------------
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td colspan=3>'
echo '                  <input type="submit" name="ACTION" value="Save">'
echo '                  <input type="submit" name="ACTION" value="Reset all">'
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
#----------------------------------------------------------------------------------------
pcp_footer
pcp_copyright
pcp_remove_query_string
echo '</body>'
echo '</html>'
exit