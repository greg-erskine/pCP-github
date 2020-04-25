#!/bin/sh

# Version: 4.0.0 2018-05-28

#========================================================================================
# This is an experiment to work out how to generate graphs using only:
# - shell
# - html5
# - svg
#
# Requires cputemp.sh to gather cpu temperature data
#----------------------------------------------------------------------------------------

. pcp-functions

CPU_TEMP_SH="/tmp/cputemp.sh"
CPU_TEMP_LOG="/var/log/pcp_cpu_temp.log"

pcp_html_head "xtras_graph" "GE"

pcp_banner
pcp_xtras
pcp_running_script
pcp_httpd_query_string

#========================================================================================
# This routine writes cputemp.sh
#----------------------------------------------------------------------------------------
pcp_write_cputemp_sh() {
cat <<EOF > $CPU_TEMP_SH
#!/bin/sh

. $WWWROOT/cgi-bin/pcp-functions
. $WWWROOT/cgi-bin/pcp-rpi-functions

while true
do
	TEMP=\$(pcp_rpi_thermal_temp degrees)
	TIME=\$(date | awk '{print \$4}' | awk -F: '{print \$1, \$2}' | sed 's/ /:/g')
	echo "\$TIME \$TEMP"
	sleep 60
done
EOF

	sudo chmod u=rwx,og=rx $CPU_TEMP_SH
}

case "$OPTION" in
	Start)
		pcp_write_cputemp_sh
		killall cputemp.sh
		$CPU_TEMP_SH >$CPU_TEMP_LOG &
	;;
	Stop)
		killall cputemp.sh
	;;
	Clean)
		killall cputemp.sh
		rm -f $CPU_TEMP_LOG
		rm -f $CPU_TEMP_SH
	;;
	Refresh)
		COUNTER=0
	;;
	Previous)
		COUNTER=$(($COUNTER - 10))
	;;
	Next)
		COUNTER=$(($COUNTER + 10))
		[ $COUNTER -ge 0 ] && COUNTER=0
	;;
esac

#========================================================================================
# Style sheet - move to piCorePlayer.css in the future
#----------------------------------------------------------------------------------------
echo '<style>'
echo 'svg.graph {'
#echo '  height: 250px;'
#echo '  width: 300px;'
echo '}'
echo '.grid {'
echo '  stroke: black;'
echo '  stroke-dasharray: 1px 2px;'
echo '  stroke-width: 1px;'
echo '}'
echo '.dots {'
echo '  stroke: red;'
echo '  fill: red;'
echo '  stroke-width: 1px;'
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
echo '  stroke-width: 1px;'
echo '}'
echo '.line {'
echo '  fill: none;'
echo '  stroke: red;'
echo '  stroke-width: 2px;'
echo '}'
echo '</style>'

#========================================================================================
# Set some graph parameters
#----------------------------------------------------------------------------------------
TITLE="CPU Temperature"
MARGIN=20
LMARGIN=25
BMARGIN=25
XGAP=40
YGAP=40

YMAX=100
YMIN=0
YMAJOR=10
Y=$((($YMAX - $YMIN) / $YMAJOR))
YTIC=5
YSCALE=$(($YGAP / $YMAJOR))

XMAX=20
XMIN=0
XMAJOR=1
X=$((($XMAX - $XMIN) / $XMAJOR))
XTIC=5

#========================================================================================
# Display graph within table
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>CPU Temperature Graph</legend>'
#echo '          <table class="bggrey percent100">'

echo '<svg version="1.1" class="graph"'
echo '  baseProfile="full"'
echo '  width="'$(($X * $XGAP + (2 * $MARGIN) + $LMARGIN))'" height="'$(($Y * $YGAP + $MARGIN + $MARGIN + $BMARGIN))'">'
#echo '  xmlns="http://www.w3.org/2000/svg">'
echo ''
echo '  <rect class="cputemp" />'
echo ''

#========================================================================================
# Get data from data.txt
#----------------------------------------------------------------------------------------
# Test data if data.txt doesn't exist

[ x"" = x"$COUNTER" ] && COUNTER=0

DATA1="06:25 06:26 06:27 06:28 06:29 06:30 06:31 06:32 06:33 06:34 06:35 06:36 06:37 06:38 06:39 06:40 06:41 06:42 06:43 06:44 06:45"
DATA2="100 90 80 70 60 50 40 30 20 10 0 10 20 30 40 55 60 70 80 90 100"

if [ -f $CPU_TEMP_LOG ]; then
	LINES=$(wc -l < $CPU_TEMP_LOG)
	BEGINRANGE=$(($LINES - $XMAX + $COUNTER))
	[ $BEGINRANGE -le 0 ] && BEGINRANGE=1
	ENDRANGE=$(($BEGINRANGE + $XMAX))
	DATA=$(cat $CPU_TEMP_LOG)
	DATA1=$(echo "$DATA" | sed -n ${BEGINRANGE},${ENDRANGE}p | awk '{print $1}')
	DATA2=$(echo "$DATA" | sed -n ${BEGINRANGE},${ENDRANGE}p | awk '{print $2}')
fi

#========================================================================================
# Vertical lines - X axis
#----------------------------------------------------------------------------------------
echo '<g class="grid x-grid cputemp" id="xGrid">'

for i in `seq 0 1 $X`
do
	GAP=$(($i * $XGAP))
	echo '  <line x1="'$(($GAP + $MARGIN + $LMARGIN))'" y1="'$MARGIN'" x2="'$(($GAP + $MARGIN + $LMARGIN))'" y2="'$(($Y * $YGAP + $MARGIN))'" />'
done

echo '</g>'

#========================================================================================
# Vertical tics - X axis
#----------------------------------------------------------------------------------------
echo '<g class="tics cputemp" id="xTic">'

for i in `seq 0 1 $X`
do
	GAP=$(($i * $XGAP))
	echo '  <line x1="'$(($GAP + $MARGIN + $LMARGIN))'" y1="'$(($Y * $YGAP + $MARGIN))'" x2="'$(($GAP + $MARGIN + $LMARGIN))'" y2="'$(($Y * $YGAP + $MARGIN + $YTIC))'" />'
done

echo '</g>'

#========================================================================================
# Vertical labels - X axis
#----------------------------------------------------------------------------------------
echo '<g class="labels xlabels cputemp" id="xLabels">'

k=0
for i in $DATA1
do
	GAP=$(($k * $XGAP))
	echo '  <text class="cputemp_text" x="'$(($GAP + $MARGIN + $LMARGIN))'" y="'$(($Y * $YGAP + $MARGIN + $YTIC + 15))'" >'$i'</text>'
	k=$(($k + 1))
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
	echo '  <text class="cputemp_text" x="'$(($MARGIN - $XTIC + $LMARGIN - 5))'" y="'$(($GAP + $MARGIN + 5))'">'$LABEL'</text>'
done

echo '</g>'

#========================================================================================
# Place data dots
#----------------------------------------------------------------------------------------
k=0
echo '<g class="dots" data-setname="data-dots">'
for j in $DATA2
do
	GAP=$(($k * $XGAP))
	echo '  <circle cx="'$(($GAP + $MARGIN + $LMARGIN))'" cy="'$(((($YMAX - $j) * $YSCALE) + $MARGIN))'" data-value="'$j'" r="3" />'
	k=$(($k + 1))
done
echo '</g>'

k=0
echo '<g>'
echo -n '<polyline class="line" points="'
for j in $DATA2
do
	GAP=$(($k * $XGAP))
	echo -n ' '$(($GAP + $MARGIN + $LMARGIN))','$(((($YMAX - $j) * $YSCALE) + $MARGIN))''
	k=$(($k + 1))
done
echo ' " />'
echo '</g>'

#========================================================================================
# Place title
#----------------------------------------------------------------------------------------
#echo '<text x="'$(((($X * $XGAP) + (2 * $MARGIN)) / 2 ))'" y="'$((($Y * $YGAP) + $MARGIN + $MARGIN - 5))'" font-size="12" text-anchor="middle" fill="black">'$TITLE'</text>'

echo '<text class="title cputemp_text" x="'$((((($X * $XGAP) + (2 * $MARGIN)) / 2) + $LMARGIN))'" y="'$((($Y * $YGAP) + (2 * $MARGIN) + ($BMARGIN - 6)))'" >'$TITLE'</text>'

echo ''
echo '</svg>'

#----------------------------------------------------------------------------------------
#echo '          </table>'

echo '          <table class="bggrey percent100">'
echo '            <tr>'
echo '              <td>'
echo '                <form name="actions" action="'$0'" method="get">'
echo '                  <input type="submit" name="OPTION" value="Previous">'
echo '                  <input type="submit" name="OPTION" value="Next">'
echo '                  <input type="hidden" name="COUNTER" value="'$COUNTER'">'
echo '                </form>'
echo '              </td>'
echo '              <td>'
echo '                <p>Lines: '$LINES' Begin: '$BEGINRANGE' End: '$ENDRANGE' Counter: '$COUNTER'</p>'
echo '              </td>'
echo '            </tr>'
echo '            <tr>'
echo '              <td colspan="2">'
                      pcp_redirect_button "Refresh" "$0" 30
echo '              </td>'
echo '            </tr>'
echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'

#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Logging options</legend>'
echo '          <form name="actions" action="'$0'" method="get">'
echo '            <table class="bggrey percent100">'
echo '              <tr>'
echo '                <td>'
echo '                  <input type="submit" name="OPTION" value="Start">'
echo '                  <input type="submit" name="OPTION" value="Stop">'
echo '                  <input type="submit" name="OPTION" value="Clean">'
echo '                </td>'
echo '              </tr>'
echo '            </table>'
echo '          </form>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'

#----------------------------------------------------------------------------------------
pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'