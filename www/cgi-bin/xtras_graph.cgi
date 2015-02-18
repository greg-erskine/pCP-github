#!/bin/sh

# Version: 0.01 2015-02-17 GE
#   Original version.

. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "xtras_graph" "GE"

pcp_controls
pcp_banner
pcp_navigation
pcp_running_script


echo '<svg version="1.1"'
echo '     baseProfile="full"'
echo '     width="300" height="250"'
echo '     xmlns="http://www.w3.org/2000/svg">'
echo ''
echo '  <rect width="100%" height="100%" fill="grey" />'
echo ''

# Vertical lines
for i in 1 2 3 4 5
do
	GAP=$(($i * 50))
	echo '<line x1="'$GAP'"  y1="0" x2="'$GAP'" y2="200" stroke="black" stroke-width="1"/>'
done

# Horizontal lines
for i in 1 2 3 4
do
	GAP=$(($i * 50))
	echo '<line x1="50" y1="'$GAP'" x2="250" y2="'$GAP'"  stroke="black" stroke-width="1"/>'
done

# Place data dots
echo '<circle cx="50"  cy="50" r="2" stroke="red" fill="red" stroke-width="1"/>'
echo '<circle cx="100"  cy="75" r="2" stroke="red" fill="red" stroke-width="1"/>'
echo '<circle cx="150" cy="150" r="2" stroke="red" fill="red" stroke-width="1"/>'
echo '<circle cx="200" cy="100" r="2" stroke="red" fill="red" stroke-width="1"/>'


echo '<text x="150" y="215" font-size="12" text-anchor="middle" fill="white">Temperature</text>'

echo ''
echo '</svg>'






pcp_footer
pcp_refresh_button

echo '</body>'
echo '</html>'