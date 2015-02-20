#!/bin/sh

# Version: 0.01 2015-02-19 GE
#   Original version.

. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "xtras_graph" "GE"

pcp_controls
pcp_banner
pcp_navigation
pcp_running_script

#========================================================================================
# Style sheet
#----------------------------------------------------------------------------------------
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

echo '.dots {'
echo '  stroke: black;'
echo '  fill: red;'
echo '  stroke-width: 1;'
echo '}'

echo '.labels {'
#echo '  stroke: black;'
#echo '  stroke-width: 1;'
#echo '  font-family: Arial;'
#echo '  font-size: 8px;'
#echo '  kerning: 1;'
#echo '  text-anchor: middle;'
echo '}'



echo '.labels.xlabels {'
echo '  text-anchor: middle;'
echo '}'
echo ''
echo '.labels.ylabels {'
echo '  text-anchor: end;'
echo '}'


echo '.tics {'
echo '  stroke: black;'
echo '  stroke-width: 1;'
echo '}'

echo '</style>'



TITLE="CPU Temperature"
MARGIN=25
RMARGIN=50
BMARGIN=50
XGAP=40
YGAP=40

YMAX=100
YMIN=0
YMAJOR=20
Y=$((($YMAX - $YMIN) / $YMAJOR))
YTIC=5


XMAX=20
XMIN=0
XMAJOR=1
X=$((($XMAX - $XMIN) / $XMAJOR))
XTIC=5


echo '<svg version="1.1" class="graph"'
echo '     baseProfile="full"'
echo '     xmlns="http://www.w3.org/2000/svg">'
echo ''
echo '  <rect width="'$(($X * $XGAP + $MARGIN + $MARGIN))'" height="'$(($Y * $YGAP + $MARGIN + $MARGIN))'" fill="#eaeaea" />'
echo ''

#========================================================================================
# Vertical lines - X axis
#----------------------------------------------------------------------------------------
echo '<g class="grid x-grid" id="xGrid">'

for i in `seq 0 1 $X`
do
	GAP=$(($i * $XGAP))
	echo '  <line x1="'$(($GAP + $MARGIN))'" y1="'$MARGIN'" x2="'$(($GAP + $MARGIN))'" y2="'$(($Y * $YGAP + $MARGIN))'" />'
done

echo '</g>'

#========================================================================================
# Vertical tics - X axis
#----------------------------------------------------------------------------------------
echo '<g class="tics" id="xTic">'

for i in `seq 0 1 $X`
do
	GAP=$(($i * $XGAP))
	echo '  <line x1="'$(($GAP + $MARGIN))'" y1="'$(($Y * $YGAP + $MARGIN))'" x2="'$(($GAP + $MARGIN))'" y2="'$(($Y * $YGAP + $MARGIN + $YTIC))'" />'
done

echo '</g>'

#========================================================================================
# Vertical labels - X axis
#----------------------------------------------------------------------------------------
echo '<g class="labels xlabels" id="xLabels">'

for i in `seq 0 1 $X`
do
	GAP=$(($i * $XGAP))
	echo '  <text x="'$(($GAP + $MARGIN))'" y="'$(($Y * $YGAP + $MARGIN + $YTIC + 15))'" >'$i'</text>'
done

echo '</g>'

#========================================================================================
# Horizontal lines - Y axis
#----------------------------------------------------------------------------------------
echo '<g class="grid y-grid" id="yGrid">'

for i in `seq 0 1 $Y`
do
	GAP=$(($i * $YGAP))
	echo '  <line x1="'$MARGIN'" y1="'$(($GAP + $MARGIN))'" x2="'$(($X * $XGAP + $MARGIN))'" y2="'$(($GAP + $MARGIN))'" />'
done

echo '</g>'

#========================================================================================
# Horizontal tics - Y axis
#----------------------------------------------------------------------------------------
echo '<g class="tics" id="yTic">'

for i in `seq 0 1 $Y`
do
	GAP=$(($i * $YGAP))
	echo '  <line x1="'$(($MARGIN - $XTIC))'" y1="'$(($GAP + $MARGIN))'" x2="'$MARGIN'" y2="'$(($GAP + $MARGIN))'" />'
done

echo '</g>'

#========================================================================================
# Horizontal labels - Y axis
#----------------------------------------------------------------------------------------
echo '<g class="labels ylabels" id="yLabels">'

for i in `seq 0 1 $Y`
do
	LABEL=$(($YMAX - ($YMAJOR * $i)))
	GAP=$(($i * $YGAP))
	echo '  <text x="'$(($MARGIN - $XTIC))'" y="'$(($GAP + $MARGIN))'">'$LABEL'</text>'
#	echo '  < x="'$(($GAP + $MARGIN))'" y="'$(($Y * $YGAP + $MARGIN + $YTIC + 15))'" >
done

echo '</g>'


#========================================================================================
# Place data dots
#----------------------------------------------------------------------------------------
echo '<g class="dots">'
echo '  <circle cx="50"  cy="50"  r="4" />'
echo '  <circle cx="100" cy="75"  r="4" />'
echo '  <circle cx="150" cy="150" r="4" />'
echo '  <circle cx="200" cy="100" r="4" />'
echo '  <circle cx="250" cy="150" r="4" />'
echo '</g>'

#echo '<text x="'$(((($X * $XGAP) + (2 * $MARGIN)) / 2 ))'" y="'$((($Y * $YGAP) + $MARGIN + $MARGIN - 5))'" font-size="12" text-anchor="middle" fill="black">'$TITLE'</text>'
echo '<text x="'$(((($X * $XGAP) + (2 * $MARGIN)) / 2 ))'" y="'$((($Y * $YGAP) + $MARGIN + $MARGIN - 5))'" >'$TITLE'</text>'

echo ''
echo '</svg>'






pcp_footer
pcp_refresh_button

echo '</body>'
echo '</html>'