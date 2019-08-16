#!/bin/sh

# Version: 6.0.0 2019-08-13

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
	[ "$NAME" = "$TITLE" ] && TAB_STYLE=tab7a || TAB_STYLE=tab7

	echo '<a class="'$TAB_STYLE'" href="http://'$URL'/cgi-bin/main.cgi" title="'$URL'">'${TITLE:0:20}'</a>'
done <$TMP
rm -r $TMP
