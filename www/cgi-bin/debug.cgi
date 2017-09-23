#!/bin/sh

# Version: 3.22 2017-07-21
#	Updated TEST mode. GE.

# Version: 3.20 2017-03-08
#	Moved variables $DEBUG, $TEST and $MODE to config.cfg. GE.
#	Fixed pcp-xxx-functions issues. GE.

# Version: 0.04 2015-08-16
#	Revised sed to match a tab in front of DEBUG, TEST and MODE. GE.

# Version: 0.03 2015-07-01
#	Made to work in non-interactive mode. GE.

# Version: 0.02 2015-06-04
#	Added interaction mode. GE.
#	Renamed $pCPHOME to $PCPHOME. GE.

# Version: 0.01 2014-10-24
#	Original. GE.

#=========================================================================================
# This cgi script quickly turns on/off/sets $DEBUG, $TEST and $MODE in config.cfg from
# your web browser.
#
# Options:
#	$DEBUG   d=[0|1]
#	$TEST    t=[0-9]
#	$MODE    m=[0-100]
#	ALL      a=[0]
#
# Non-interactive examples:
#	Turn debug on:   http://192.168.1.xxx/cgi-bin/debug.cgi?d=1
#	Turn debug off:  http://192.168.1.xxx/cgi-bin/debug.cgi?d=0
#	Turn all off:    http://192.168.1.xxx/cgi-bin/debug.cgi?a=0
#
# Interactive mode example:
#	http://192.168.1.xxx/cgi-bin/debug.cgi
#-----------------------------------------------------------------------------------------

. pcp-functions
. pcp-lms-functions

pcp_httpd_query_string

#========================================================================================
# Routines
#----------------------------------------------------------------------------------------
pcp_debug_save() {
	pcp_write_var_to_config DEBUG $d
	pcp_write_var_to_config TEST $t
	pcp_write_var_to_config MODE $m
}

pcp_debug_reset() {
	pcp_write_var_to_config DEBUG 0
	pcp_write_var_to_config TEST 0
	pcp_write_var_to_config MODE $MODE_INITIAL
}

#========================================================================================
# Command line mode
#----------------------------------------------------------------------------------------
pcp_debug_cli() {
	if [ x"" != x"$QUERY_STRING" ]; then
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
	fi
}

#========================================================================================
# Respond to interactive [Save] and [Reset all] buttons.
#----------------------------------------------------------------------------------------
case "$SUBMIT" in
	Save) pcp_debug_save ;;
	Res*) pcp_debug_reset ;;
esac

sync
. pcp-functions

pcp_html_head "Debug" "GE"

# Non-interactive (Command line) mode and exit
if [ x"" != x"$QUERY_STRING" ] && [ x"" = x"$SUBMIT" ]; then
	echo '<body onload="javascript:location.href=document.referrer;">'
	pcp_debug_cli
	exit 0
fi

# Interactive (Web page) mode
pcp_controls
pcp_banner
pcp_navigation
pcp_running_script

#========================================================================================
# Debug info
#----------------------------------------------------------------------------------------
if [ $DEBUG -eq 1 ]; then
	echo '<p class="debug">[ DEBUG ] DEBUG: '$DEBUG'<br />'
	echo '                 [ DEBUG ] d: '$d'<br />'
	echo '                 [ DEBUG ] MODE: '$MODE'<br />'
	echo '                 [ DEBUG ] m: '$m'<br />'
	echo '                 [ DEBUG ] TEST: '$TEST'<br />'
	echo '                 [ DEBUG ] t: '$t'<br />'
	echo '                 [ DEBUG ] SUBMIT: '$SUBMIT'</p>'
fi

#========================================================================================
# Main
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <form name="debug" action="debug.cgi" method="get">'
echo '        <div class="row">'
echo '          <fieldset>'
echo '            <legend>Set debug options</legend>'
echo '            <table class="bggrey percent100">'
#--------------------------------------DEBUG---------------------------------------------
case "$DEBUG" in
	0) D0SELECTED=checked ;;
	1) D1SELECTED=checked ;;
esac

pcp_start_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="column100">'
echo '                  <p>DEBUG</p>'
echo '                </td>'
echo '                <td class="column150">'
echo '                  <input class="small1" type="radio" name="d" value="1" '$D1SELECTED'>On&nbsp;'
echo '                  <input class="small1" type="radio" name="d" value="0" '$D0SELECTED'>Off'
echo '                </td>'
echo '                <td>'
echo '                  <p>Set DEBUG: [on|off].</p>'
echo '                </td>'
echo '              </tr>'
#--------------------------------------MODE----------------------------------------------
case "$MODE" in
	0) MODEinitial="selected" ;;
	10) MODEbasic="selected" ;;
	20) MODEnormal="selected" ;;
	30) MODEdvanced="selected" ;;
	40) MODEbeta="selected" ;;
	100) MODEdeveloper="selected" ;;
esac

pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="column100">'
echo '                  <p>MODE</p>'
echo '                </td>'
echo '                <td class="column150">'
echo '                  <select class="large10" name="m">'
echo '                    <option value="0" '$MODEinitial'>Initial</option>'
echo '                    <option value="10" '$MODEbasic'>Basic</option>'
echo '                    <option value="20" '$MODEnormal'>Normal</option>'
echo '                    <option value="30" '$MODEdvanced'>Advanced</option>'
echo '                    <option value="40" '$MODEbeta'>Beta</option>'
echo '                    <option value="100" '$MODEdeveloper'>Developer</option>'
echo '                  </select>'
echo '                </td>'
echo '                <td>'
echo '                  <p>Set MODE level: [Initial|Basic|Normal|Advanced|Beta|Developer].</p>'
echo '                </td>'
echo '              </tr>'
#--------------------------------------TEST----------------------------------------------
case "$TEST" in
	0) TEST0="selected" ;;
	1) TEST1="selected" ;;
	2) TEST2="selected" ;;
	3) TEST3="selected" ;;
	4) TEST4="selected" ;;
	5) TEST5="selected" ;;
	6) TEST6="selected" ;;
	7) TEST7="selected" ;;
	8) TEST8="selected" ;;
	9) TEST9="selected" ;;
esac

pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="column100">'
echo '                  <p>TEST</p>'
echo '                </td>'
echo '                <td class="column150">'
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
echo '                  <input type="submit" name="SUBMIT" value="Save">'
echo '                  <input type="submit" name="SUBMIT" value="Reset all">'
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

pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'