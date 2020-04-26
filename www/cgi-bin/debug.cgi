#!/bin/sh

# Version: 7.0.0 2020-10-26

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
	
	echo '<div>'
#	pcp_table_top "Debug"
	pcp_debug_variables "html" QUERY_STRING DEBUG d MODE m TEST t ACTION
#	pcp_table_end
	echo '</div>'
fi

#========================================================================================
# Debug table
#----------------------------------------------------------------------------------------
echo '<div>'
echo '  <h4 class="mt-12">Set debug options</h4>'
echo '  <form name="debug" action="'$0'" method="get">'
echo '    <fieldset>'
#--------------------------------------DEBUG---------------------------------------------
eval D${DEBUG}SELECTED=checked

echo '    <div class="form-group row mt-12">'

echo '        <div class="col-2">DEBUG</div>'
echo '        <div class="col-3">'
echo '          <input id="rad1" type="radio" name="d" value="1" '$D1SELECTED'>'
echo '          <label for="rad1">On&nbsp;</label>'
echo '          <input id="rad2" type="radio" name="d" value="0" '$D0SELECTED'>'
echo '          <label for="rad2">Off</label>'
echo '        </div>'
echo '        <div class="col-7">Set DEBUG: [on|off].</div>'

echo '    </div>'
#--------------------------------------MODE----------------------------------------------
eval MODE${MODE}="selected"

echo '    <div class="form-group row">'

echo '        <div class="col-sm-2">MODE</div>'
echo '        <div class="col-sm-3">'
echo '          <select class="btn btn-primary" name="m">'
echo '            <option value="10" '$MODE10'>Player</option>'
echo '            <option value="30" '$MODE30'>Player/Server</option>'
echo '            <option value="40" '$MODE40'>Beta</option>'
echo '            <option value="100" '$MODE100'>Developer</option>'
echo '          </select>'
echo '        </div>'
echo '        <div class="col-sm-7">Set MODE level: [Player|Server|Beta|Developer].</div>'

echo '    </div>'
#--------------------------------------TEST----------------------------------------------
eval TEST${TEST}="selected"

echo '    <div class="form-group row">'

echo '        <div class="col-2">TEST</div>'
echo '        <div class="col-3">'
echo '          <select class="btn btn-primary" name="t">'
echo '            <option value="0" '$TEST0'>0</option>'
echo '            <option value="1" '$TEST1'>1</option>'
echo '            <option value="2" '$TEST2'>2</option>'
echo '            <option value="3" '$TEST3'>3</option>'
echo '            <option value="4" '$TEST4'>4</option>'
echo '            <option value="5" '$TEST5'>5</option>'
echo '            <option value="6" '$TEST6'>6</option>'
echo '            <option value="7" '$TEST7'>7</option>'
echo '            <option value="8" '$TEST8'>8</option>'
echo '            <option value="9" '$TEST9'>9</option>'
echo '          </select>'
echo '        </div>'
echo '        <div class="col-7">Set TEST level: [0-9].</div>'

echo '    </div>'
#--------------------------------------BUTTONS-------------------------------------------
echo '    <div class="form-group row">'
echo '      <div class="col-sm-12 offset-sm-2">'
echo '        <button type="submit" class="btn btn-primary" name="ACTION" value="Save">Save</button>'
echo '        <button type="submit" class="btn btn-primary" name="ACTION" value="Reset">Reset all</button>'
echo '      </div>'
echo '    </div>'

#----------------------------------------------------------------------------------------
echo '    </fieldset>'
echo '  </form>'
#----------------------------------------------------------------------------------------
pcp_footer
pcp_copyright
pcp_remove_query_string

echo '</div>'
echo '</body>'
echo '</html>'
exit