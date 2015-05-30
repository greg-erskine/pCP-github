#!/bin/sh

# Version: 0.01 2015-02-25 GE
#   Original version.

. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "xtras_controls" "GE"

pcp_controls
pcp_banner
pcp_xtras
pcp_running_script

#========================================================================================
# Style sheet - move to piCorePlayer.css in the future
#----------------------------------------------------------------------------------------
echo '<style type="text/css">'

echo '.grid {'
echo '  stroke: black;'
echo '  stroke-dasharray: 1 2;'
echo '  stroke-width: 1;'
echo '}'

echo '</style>'
#----------------------------------------------------------------------------------------

#<a class="nav2" href="controls.cgi?COMMAND=random_tracks" title="Random">Random</a>'
#<a class="nav2" href="controls.cgi?COMMAND=volume_up" title="Volume Up">Volume Up ^</a>'
#<a class="nav2" href="controls.cgi?COMMAND=volume_down" title="Volume Down">Volume Down v</a>'
#<a class="nav2" href="controls.cgi?COMMAND=track_prev" title="Previous Track">&lt; Previous Track</a>'
#<a class="nav2" href="controls.cgi?COMMAND=track_next" title="Next Track">Next Track &gt;</a>'
#<a class="nav2" href="controls.cgi?COMMAND=play" title="Play">Play</a>'
#<a class="nav2" href="controls.cgi?COMMAND=stop" title="Stop">Stop</a>'


OFFSETX=100
OFFSETY=100
BUTTONWIDTH=25

echo '<svg version="1.1" class="button"'
echo '  baseProfile="full"'
echo '  width="100" height="0">'
echo '  xmlns="http://www.w3.org/2000/svg">'

echo '    <rect x="'$OFFSETX'" y="'$OFFSETY'" width="600" height="250" style="fill:grey" />'


BUTTON=2
echo '  <a xlink:href="controls.cgi?COMMAND=track_next" >'
echo '    <rect x="'$(($OFFSETX + ($BUTTONWIDTH * $BUTTON)))'" y="'$OFFSETY'" width="25" height="25" style="fill:red" />'
echo '  </a>'

BUTTON=1
echo '  <a xlink:href="controls.cgi?COMMAND=track_prev" >'
echo '    <rect x="'$(($OFFSETX + ($BUTTONWIDTH * $BUTTON)))'" y="'$OFFSETY'" width="25" height="25" fill="green" />'
echo '  </a>'

BUTTON=0
echo '  <a xlink:href="controls.cgi?COMMAND=play" >'
echo '    <rect x="'$(($OFFSETX + ($BUTTONWIDTH * $BUTTON)))'" y="'$OFFSETY'" width="25" height="25" fill="yellow" />'
echo '  </a>'



echo '</svg>'



#----------------------------------------------------------------------------------------
pcp_footer
pcp_refresh_button

echo '</body>'
echo '</html>'