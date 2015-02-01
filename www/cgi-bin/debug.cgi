#!/bin/sh

#=========================================================================================
# This cgi script quickly turns on/off/sets $DEBUG, $TEST and $MODE in pcp-functions
# from your web browser.
#
# During testing, it is a pain to turn debugging on and off by editting pcp-functions
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
#-----------------------------------------------------------------------------------------

# Version: 0.01 2014-10-24 GE
#	Original.

. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "Debug" "GE"

pcp_footer
pcp_banner
pcp_diagnostics
pcp_running_script
pcp_refresh_button
pcp_go_main_button

pcp_httpd_query_string

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
			echo '<p class="error">[ ERROR ] Invalid option: '$QUERY_STRING'</p>'
			;;
	esac
fi

sync
. pcp-functions

echo '<p class="info">[ INFO ] DEBUG: '$DEBUG'<br />'
echo '                [ INFO ] TEST: '$TEST'<br />'
echo '                [ INFO ] MODE: '$MODE'</p>'

pcp_footer
pcp_refresh_button

echo '</body>'
echo '</html>'