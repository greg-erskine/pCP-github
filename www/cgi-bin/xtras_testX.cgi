#!/bin/sh

# Version: 7.0.0 2020-05-18
# Title: Squeezelite info
# Description: Display info of Squeezelite players

. pcp-functions
. pcp-lms-functions

pcp_html_head "xtras" "GE"

pcp_xtras

echo '<p>This page displays the Raspberry Pi diagnostics page for all Squeezelite players found on LMS.</p>'

TMP=$(mktemp)
pcp_lms_players squeezelite >$TMP
for i in $(cat $TMP | awk -F, '{ print $2 }')
do
	echo '<div>'
	pcp_heading5 "$i" hr
	echo '<iframe src="http://'$i'/cgi-bin/diag_rpi.cgi" width="1125" height="645" frameborder="0" scrolling="no"></iframe>'
#	echo '<iframe src="http://'$i'/cgi-bin/diag_rpi.cgi" frameborder="0" scrolling="no"></iframe>'
	echo '</div>'
done

pcp_html_end
exit
