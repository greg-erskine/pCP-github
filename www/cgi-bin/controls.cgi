#!/bin/sh

# Version: 4.0.1 2018-09-19

. pcp-functions
. pcp-lms-functions

pcp_html_head "Controls" "GE" "" "" "nobody"

[ $DEBUG -eq 1 ] && echo '<body>' || echo '<body onload="javascript:location.href=document.referrer;">'
[ $DEBUG -eq 1 ] && pcp_controls && pcp_banner && pcp_navigation && pcp_running_script

pcp_httpd_query_string

case "$COMMAND" in
	random_tracks)
		pcp_lms_randomplay &
	;;
	volume_up)
		pcp_lms_volume_up &
	;;
	volume_down)
		pcp_lms_volume_down &
	;;
	track_next)
		pcp_lms_next &
	;;
	track_prev)
		pcp_lms_prev &
	;;
	play)
		pcp_lms_play &
	;;
	stop)
	    pcp_lms_stop &
	;;
esac

[ $DEBUG -eq 1 ] && pcp_footer && pcp_copyright

echo '</body>'
echo '</html>'