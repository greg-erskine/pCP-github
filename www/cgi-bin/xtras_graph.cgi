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


echo '<style type="text/css">'
echo 'svg.graph {'
echo '  height: 250px;'
echo '  width: 300px;'
echo '}'
echo '.grid {'
echo '  stroke: black;'
echo '  stroke-dasharray: 1 2;'
echo '  stroke-width: 1;'
echo '}'
echo '</style>'



TITLE="CPU Temperature"
MARGIN=25
VMIN=0
VMAX=100
VMAJOR=10
XMIN=0
XMAX=20
XMAJOR=1
GAP=50


echo '<svg version="1.1" class="graph"'
echo '     baseProfile="full"'
echo '     xmlns="http://www.w3.org/2000/svg">'
echo ''
echo '  <rect width="100%" height="100%" fill="#eaeaea" />'
echo ''

# Vertical lines

echo '<g class="grid x-grid" id="xGrid">'

for i in 1 2 3 4 5
do
	GAP=$(($i * 50))
	echo '  <line x1="'$GAP'" y1="0" x2="'$GAP'" y2="200" />'
done

echo '</g>'


# Horizontal lines

echo '<g class="grid y-grid" id="yGrid">'

for i in 1 2 3 4
do
	GAP=$(($i * 50))
	echo '<line x1="50" y1="'$GAP'" x2="250" y2="'$GAP'" />'
done

echo '</g>'



# Place data dots
echo '<circle cx="50"  cy="50" r="4" stroke="red" fill="red" stroke-width="1"/>'
echo '<circle cx="100" cy="75" r="4" stroke="red" fill="red" stroke-width="1"/>'
echo '<circle cx="150" cy="150" r="4" stroke="red" fill="red" stroke-width="1"/>'
echo '<circle cx="200" cy="100" r="4" stroke="red" fill="red" stroke-width="1"/>'
echo '<circle cx="250" cy="150" r="4" stroke="red" fill="red" stroke-width="1"/>'


echo '<text x="150" y="215" font-size="12" text-anchor="middle" fill="black">'$TITLE'</text>'

echo ''
echo '</svg>'






pcp_footer
pcp_refresh_button

echo '</body>'
echo '</html>'