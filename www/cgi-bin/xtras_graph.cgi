#!/bin/sh

# Version: 0.01 2015-02-21 GE
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
# Style sheet - move to piCorePlayer.css in the future
#----------------------------------------------------------------------------------------
echo '<style type="text/css">'
echo 'svg.graph {'
#echo '  height: 250px;'
#echo '  width: 300px;'
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
echo '  font-family: Courier;'
echo '  font-size: 8px;'
#echo '  kerning: 1;'
#echo '  text-anchor: middle;'
echo '}'
echo '.xlabels, .title {'
echo '  text-anchor: middle;'
echo '}'
echo '.ylabels {'
echo '  text-anchor: end;'
echo '}'
echo '.tics {'
echo '  stroke: black;'
echo '  stroke-width: 1;'
echo '}'
echo '</style>'
#----------------------------------------------------------------------------------------

TITLE="CPU Temperature"
MARGIN=20
LMARGIN=25
BMARGIN=25
XGAP=40
YGAP=40

YMAX=100
YMIN=0
YMAJOR=20
Y=$((($YMAX - $YMIN) / $YMAJOR))
YTIC=5
YSCALE=$(($YGAP / $YMAJOR))

XMAX=20
XMIN=0
XMAJOR=1
X=$((($XMAX - $XMIN) / $XMAJOR))
XTIC=5

echo '<svg version="1.1" class="graph"'
echo '  baseProfile="full"'
echo '  width="'$(($X * $XGAP + (2 * $MARGIN) + $LMARGIN))'" height="'$(($Y * $YGAP + $MARGIN + $MARGIN + $BMARGIN))'">'
echo '  xmlns="http://www.w3.org/2000/svg">'
echo ''
echo '  <rect width="100%" height="100%" fill="#eaeaea" />'
echo ''

#========================================================================================
# Vertical lines - X axis
#----------------------------------------------------------------------------------------
echo '<g class="grid x-grid" id="xGrid">'

for i in `seq 0 1 $X`
do
	GAP=$(($i * $XGAP))
	echo '  <line x1="'$(($GAP + $MARGIN + $LMARGIN))'" y1="'$MARGIN'" x2="'$(($GAP + $MARGIN + $LMARGIN))'" y2="'$(($Y * $YGAP + $MARGIN))'" />'
done

echo '</g>'

#========================================================================================
# Vertical tics - X axis
#----------------------------------------------------------------------------------------
echo '<g class="tics" id="xTic">'

for i in `seq 0 1 $X`
do
	GAP=$(($i * $XGAP))
	echo '  <line x1="'$(($GAP + $MARGIN + $LMARGIN))'" y1="'$(($Y * $YGAP + $MARGIN))'" x2="'$(($GAP + $MARGIN + $LMARGIN))'" y2="'$(($Y * $YGAP + $MARGIN + $YTIC))'" />'
done

echo '</g>'

#========================================================================================
# Vertical labels - X axis
#----------------------------------------------------------------------------------------
echo '<g class="labels xlabels" id="xLabels">'

for i in `seq 0 1 $X`
do
	GAP=$(($i * $XGAP))
	echo '  <text x="'$(($GAP + $MARGIN + $LMARGIN))'" y="'$(($Y * $YGAP + $MARGIN + $YTIC + 15))'" >'$i'</text>'
done

echo '</g>'

#========================================================================================
# Horizontal lines - Y axis
#----------------------------------------------------------------------------------------
echo '<g class="grid y-grid" id="yGrid">'

for i in `seq 0 1 $Y`
do
	GAP=$(($i * $YGAP))
	echo '  <line x1="'$(($MARGIN + $LMARGIN))'" y1="'$(($GAP + $MARGIN))'" x2="'$(($X * $XGAP + $MARGIN + $LMARGIN))'" y2="'$(($GAP + $MARGIN))'" />'
done

echo '</g>'

#========================================================================================
# Horizontal tics - Y axis
#----------------------------------------------------------------------------------------
echo '<g class="tics" id="yTic">'

for i in `seq 0 1 $Y`
do
	GAP=$(($i * $YGAP))
	echo '  <line x1="'$(($MARGIN - $XTIC + $LMARGIN))'" y1="'$(($GAP + $MARGIN))'" x2="'$(($MARGIN + $LMARGIN))'" y2="'$(($GAP + $MARGIN))'" />'
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
	echo '  <text x="'$(($MARGIN - $XTIC + $LMARGIN - 5))'" y="'$(($GAP + $MARGIN + 5))'">'$LABEL'</text>'
#	echo '  < x="'$(($GAP + $MARGIN))'" y="'$(($Y * $YGAP + $MARGIN + $YTIC + 15))'" >
done

echo '</g>'


#========================================================================================
# Place data dots
#----------------------------------------------------------------------------------------
echo '<g class="dots" data-setname="data" >'

DATA="100 90 80 70 60 50 40 30 20 10 0 10 20 30 40 55 60 70 80 90 100"

[ -f /home/tc/data.txt ] && DATA=$(cat /home/tc/data.txt | awk '{print $2}')

k=0

#for j in 0 20 50 75 48 49 48 100 100 

for j in $DATA

do
	GAP=$(($k * $XGAP))
	echo '  <circle cx="'$(($GAP + $MARGIN + $LMARGIN))'" cy="'$(((($YMAX - $j) * $YSCALE) + $MARGIN))'" data-value="'$j'" r="4" />'
	k=$(($k + 1))
done

echo '</g>'

#========================================================================================
# Place title
#----------------------------------------------------------------------------------------
#echo '<text x="'$(((($X * $XGAP) + (2 * $MARGIN)) / 2 ))'" y="'$((($Y * $YGAP) + $MARGIN + $MARGIN - 5))'" font-size="12" text-anchor="middle" fill="black">'$TITLE'</text>'

echo '<text class="title" x="'$((((($X * $XGAP) + (2 * $MARGIN)) / 2) + $LMARGIN))'" y="'$((($Y * $YGAP) + (2 * $MARGIN) + ($BMARGIN - 6)))'" >'$TITLE'</text>'

echo ''
echo '</svg>'


#----------------------------------------------------------------------------------------
pcp_footer
pcp_refresh_button

echo '</body>'
echo '</html>'