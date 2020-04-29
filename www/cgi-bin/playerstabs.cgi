#!/bin/sh

# Version: 7.0.0 2020-04-29

# This generates player tab data in the background.

. pcp-functions
. pcp-lms-functions

TMP=$(mktemp)

pcp_lms_players squeezelite pCP>$TMP

printf "Content-type: text/html\n\n"
while read line
do
	TITLE=$(echo $line | awk -F, '{ print $1 }')
	URL=$(echo $line | awk -F, '{ print $2 }')
	[ "$NAME" = "$TITLE" ] && STATUS="active" || STATUS=""
	echo '<a class="dropdown-item '$STATUS'" href="http://'$URL'/cgi-bin/main.cgi" title="'$URL'">'${TITLE:0:20}'</a>'
done <$TMP
rm -r $TMP
