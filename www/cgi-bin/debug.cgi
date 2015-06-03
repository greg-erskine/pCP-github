#!/bin/sh

#=========================================================================================
# This cgi script quickly turns on/off/sets $DEBUG, $TEST and $MODE in pcp-functions
# from your web browser.
#
# During testing, it is a pain to turn debugging on and off by editing pcp-functions
# in a text editor. Problem solved!
#
# Options:
#	$DEBUG   d=[0|1]
#	$TEST    t=[0-9]
#	$MODE    m=[0-99]
#	ALL      a=[0|1]
#
# Examples:
#	Turn debug on:   http://192.168.1.xxx/cgi-bin/debug.cgi?d=1
#	Turn debug off:  http://192.168.1.xxx/cgi-bin/debug.cgi?d=0
#	Turn all off:    http://192.168.1.xxx/cgi-bin/debug.cgi?a=0
#
#	Use the interactive mode.
#-----------------------------------------------------------------------------------------

# Version: 0.02 2015-06-03 GE
#	Added interaction mode.

# Version: 0.01 2014-10-24 GE
#	Original.

. pcp-lms-functions
. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "Debug" "GE"

pcp_controls
pcp_banner
pcp_navigation
pcp_running_script

pcp_httpd_query_string

#========================================================================================
# Routines
#----------------------------------------------------------------------------------------
pcp_debug_save() {
	sed -i "s/\(DEBUG=\).*/\1$d/" $pCPHOME/pcp-functions
	sed -i "s/\(TEST=\).*/\1$t/" $pCPHOME/pcp-functions
	sed -i "s/\(MODE=\).*/\1$m/" $pCPHOME/pcp-functions
} 

pcp_debug_reset() {
	sed -i "s/\(DEBUG=\).*/\10/" $pCPHOME/pcp-functions
	sed -i "s/\(TEST=\).*/\10/" $pCPHOME/pcp-functions
	sed -i "s/\(MODE=\).*/\10/" $pCPHOME/pcp-functions
}

pcp_debug_set() {
	sed -i "s/\(DEBUG=\).*/\11/" $pCPHOME/pcp-functions
	sed -i "s/\(TEST=\).*/\11/" $pCPHOME/pcp-functions
	sed -i "s/\(MODE=\).*/\11/" $pCPHOME/pcp-functions
}

#========================================================================================
# Command line mode
#----------------------------------------------------------------------------------------
if [ x"" != x"$QUERY_STRING" ]; then
	case $QUERY_STRING in
		d=[01])
			sed -i "s/\(DEBUG=\).*/\1$d/" $pCPHOME/pcp-functions
			;;
		t=[0-9])
			sed -i "s/\(TEST=\).*/\1$t/" $pCPHOME/pcp-functions
			;;
		m=[0-9]*) 
			sed -i "s/\(MODE=\).*/\1$m/" $pCPHOME/pcp-functions
			;;
		a=[01])
			sed -i "s/\(DEBUG=\).*/\1$a/" $pCPHOME/pcp-functions
			sed -i "s/\(TEST=\).*/\1$a/" $pCPHOME/pcp-functions
			sed -i "s/\(MODE=\).*/\1$a/" $pCPHOME/pcp-functions
			;;
		*)
			[ $DEBUG = 1 ] && echo '<p class="error">[ ERROR ] Invalid option: '$QUERY_STRING'</p>'
			;;
	esac
fi

#========================================================================================
# Respond to interactive Save, Set all and Reset all buttons
#----------------------------------------------------------------------------------------
case $SUBMIT in
	Save) pcp_debug_save ;;
	Set*) pcp_debug_set ;;
	Res*) pcp_debug_reset ;;
esac

sync
. pcp-functions

case $DEBUG in
	0) D0SELECTED=checked ;;
	1) D1SELECTED=checked ;;
esac

#========================================================================================
# Debug info
#----------------------------------------------------------------------------------------
if [ $DEBUG = 1 ]; then
	echo '<p class="debug">[ DEBUG ] DEBUG: '$DEBUG' d: '$d'<br />'
	echo '                 [ DEBUG ] TEST: '$TEST' t: '$t'<br />'
	echo '                 [ DEBUG ] MODE: '$MODE' m: '$m'</p>'
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
pcp_start_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="column150">'
echo '                  <p>DEBUG</p>'
echo '                </td>'
echo '                <td class="column210">'
echo '                  <input class="small1" type="radio" name="d" value="1" '$D1SELECTED'>On&nbsp;'
echo '                  <input class="small1" type="radio" name="d" value="0" '$D0SELECTED'>Off'
echo '                </td>'
echo '                <td>'
echo '                  <p>Set DEBUG on or off.</p>'
echo '                </td>'
echo '              </tr>'
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="column150">'
echo '                  <p>TEST</p>'
echo '                </td>'
echo '                <td class="column210">'
echo '                  <input type="number" name="t" value='$TEST' min="0" max="9">'
echo '                </td>'
echo '                <td>'
echo '                  <p>Set TEST level [0-9].</p>'
echo '                </td>'
echo '              </tr>'
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="column150">'
echo '                  <p>MODE</p>'
echo '                </td>'
echo '                <td class="column210">'
echo '                  <input type="number" name="m" value='$MODE' min="0" max="99">'
echo '                </td>'
echo '                <td>'
echo '                  <p>Set MODE level [1-99].</p>'
echo '                </td>'
echo '              </tr>'
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td colspan=3>'
echo '                  <input type="submit" name="SUBMIT" value="Save">'
echo '                  <input type="submit" name="SUBMIT" value="Set all">'
echo '                  <input type="submit" name="SUBMIT" value="Reset all">'
echo '                </td>'
echo '              </tr>'
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