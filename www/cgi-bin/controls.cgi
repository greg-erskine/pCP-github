#!/bin/sh

# Version: 0.06 2016-04-26 GE
#	Code tidyup.

# Version: 0.05 2014-12-11 GE
#	HTML5 formatting.

# Version: 0.04 2014-10-02 GE
#	Added variable $SERVER_IP_NO_PORT.

# Version: 0.03 2014-09-09 GE
#	Removed $LMSIP using $SERVER_IP instead.

# Version: 0.02 2014-07-18 GE
# 	Added support for wireless connection, pcp_controls_mac_address.

# Version: 0.01 2014-06-27 GE
#	Original.

. pcp-lms-functions
. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "Controls" "GE"

#====================================Fix=================================================
[ $DEBUG -eq 1 ] && echo '<body>' || echo '<body onload="javascript:location.href=document.referrer;">'
#========================================================================================

[ $DEBUG -eq 1 ] && pcp_controls && pcp_banner && pcp_navigation && pcp_running_script

pcp_httpd_query_string

case "$COMMAND" in
	random_tracks)
		pcp_lms_randomplay
	;;
	volume_up)
		pcp_lms_volume_up
	;;
	volume_down)
		pcp_lms_volume_down
	;;
	track_next)
		pcp_lms_next
	;;
	track_prev)
		pcp_lms_prev
	;;
	play)
		pcp_lms_play
	;;
	stop)
	    pcp_lms_stop
	;;
esac

[ $DEBUG -eq 1 ] && pcp_footer && pcp_copyright

echo '</body>'
echo '</html>'