#!/bin/sh

# Version: 0.02 2015-05-01 GE
#   Continued development.

# Version: 0.01 2015-03-10 GE
#   Original version.

. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "xtras_asound_conf" "GE"

pcp_controls
pcp_banner
pcp_xtras
pcp_mode_lt_99
pcp_running_script

VOLUMELEFT=100
VOLUMERIGHT=100

#========================================================================================
# Write asound.conf - 0 = left, 1 = right
#----------------------------------------------------------------------------------------
pcp_write_asound_conf() {
	PCMTYPE=${HW}:${CARD},0
	echo '# '$OPTION' - Generated by piCorePlayer' >$ASOUNDCONF
	echo 'pcm.!default {'                         >>$ASOUNDCONF

	case $OPTION in
		default)
			echo '	type plug'                    >>$ASOUNDCONF
			echo '	slave.pcm "'$PCMTYPE'"'       >>$ASOUNDCONF
			;;
		stereo)
			echo '	type route'                   >>$ASOUNDCONF
			echo '	slave.pcm "'$PCMTYPE'"'       >>$ASOUNDCONF
			echo '	ttable {'                     >>$ASOUNDCONF
			echo '		0.0 '$VOLLEFT             >>$ASOUNDCONF
			echo '		1.1 '$VOLRIGHT            >>$ASOUNDCONF
			echo '	}'                            >>$ASOUNDCONF
			;;
		mono)
			echo '	type route'                   >>$ASOUNDCONF
			echo '	slave.pcm "'$PCMTYPE'"'       >>$ASOUNDCONF
			echo '	ttable {'                     >>$ASOUNDCONF
			echo '		0.1 '$VOLLEFT             >>$ASOUNDCONF
			echo '		0.0 '$VOLLEFT             >>$ASOUNDCONF
			echo '		1.0 '$VOLRIGHT            >>$ASOUNDCONF
			echo '		1.1 '$VOLRIGHT            >>$ASOUNDCONF
			echo '	}'                            >>$ASOUNDCONF
			;;
		swap)
			echo '	type route'                   >>$ASOUNDCONF
			echo '	slave.pcm "'$PCMTYPE'"'       >>$ASOUNDCONF
			echo '	ttable {'                     >>$ASOUNDCONF
			echo '		0.1 '$VOLLEFT             >>$ASOUNDCONF
			echo '		1.0 '$VOLRIGHT            >>$ASOUNDCONF
			echo '	}'                            >>$ASOUNDCONF
			;;
		left)
			echo '	type route'                   >>$ASOUNDCONF
			echo '	slave.pcm "'$PCMTYPE'"'       >>$ASOUNDCONF
			echo '	ttable {'                     >>$ASOUNDCONF
			echo '		0.0 '$VOLLEFT             >>$ASOUNDCONF
			echo '		1.1 0'                    >>$ASOUNDCONF
			echo '	}'                            >>$ASOUNDCONF
			;;
		right)
			echo '	type route'                   >>$ASOUNDCONF
			echo '	slave.pcm "'$PCMTYPE'"'       >>$ASOUNDCONF
			echo '	ttable {'                     >>$ASOUNDCONF
			echo '		0.0 0'                    >>$ASOUNDCONF
			echo '		1.1 '$VOLRIGHT            >>$ASOUNDCONF
			echo '	}'                            >>$ASOUNDCONF
			;;
	esac
	echo '}'                                      >>$ASOUNDCONF

pcp_backup >/dev/null 2>&1
}

pcp_httpd_query_string

VOLLEFT="0."$VOLUMELEFT
if [ $VOLUMELEFT -eq 0 ]; then
	VOLLEFT=0
elif [ $VOLUMELEFT -lt 10 ]; then
	VOLLEFT="0.0"$VOLUMELEFT
elif [ $VOLUMELEFT -ge 100 ]; then
	VOLLEFT=1
fi

VOLRIGHT="0."$VOLUMERIGHT
if [ $VOLUMERIGHT -eq 0 ]; then
	VOLRIGHT=0
elif [ $VOLUMERIGHT -lt 10 ]; then
	VOLRIGHT="0.0"$VOLUMERIGHT
elif [ $VOLUMERIGHT -ge 100 ]; then
	VOLRIGHT=1
fi

case "$SUBMIT" in
	Write)
		[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Writing asound.conf...</p>'
		pcp_write_asound_conf
		;;
	*)
		[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Invalid option '$SUBMIT'...</p>'
		;;
esac

TYPE=$(cat $ASOUNDCONF)
[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Type '${TYPE:2:3}'</p>'
case ${TYPE:2:3} in
	def) DEF="checked" ;;
	ste) STE="checked" ;;
	mon) MON="checked" ;;
	swa) SWA="checked" ;;
	lef) LEF="checked" ;;
	rig) RIG="checked" ;;
	*)   DEF="checked" ;;
esac

CARD=`grep slave.pcm $ASOUNDCONF | awk -F: '{print $2}' | awk -F, '{print $1}'`
case $CARD in
	0) CARD0="checked" ;;
	1) CARD1="checked" ;;
esac

HW=`grep slave.pcm $ASOUNDCONF | awk -F: '{print $1}' | awk -F\" '{print $2}'`
case $HW in
	hw) HW0="checked" ;;
	plughw) HW1="checked" ;;
esac

#VOLUMELEFT=`grep "0\.[10]" $ASOUNDCONF | awk '{print $2}'`
#if [ $VOLUMELEFT = "1" ]; then
#	VOLUMELEFT=100
#elif [ $VOLUMELEFT = "0" ]; then
#	VOLUMELEFT=0
##elif [ "$VOLUMELEFT" == "" ]; then
##	VOLUMELEFT=0
#else
#	if echo $VOLUMELEFT | grep "0\.0" ; then
#		VOLUMELEFT=`echo $VOLUMELEFT | awk -F"0.0" '{print $2}'`
#	else
#		VOLUMELEFT=`echo $VOLUMELEFT | awk -F"0." '{print $2}'`
#	fi
#fi
#
#VOLUMERIGHT=`grep "1\.[10]" $ASOUNDCONF | awk '{print $2}'`
#if [ $VOLUMERIGHT = 1 ]; then
#	VOLUMERIGHT=100
#elif [ $VOLUMERIGHT = 0 ]; then
#	VOLUMERIGHT=0
##elif [ "$VOLUMERIGHT" == "" ]; then
##	VOLUMERIGHT=0
#else
#	if echo $VOLUMERIGHT | grep "0.0" >/dev/null 2>&1; then
#		VOLUMERIGHT=`echo $VOLUMERIGHT | awk -F"0.0" '{print $2}'`
#	else
#		VOLUMERIGHT=`echo $VOLUMERIGHT | awk -F"0." '{print $2}'`
#	fi
#fi

#========================================================================================
# Start table
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <form name="asound" action="xtras_asoundrc.cgi" method="get" id="asound">'
echo '        <div class="row">'
echo '          <fieldset>'
echo '            <legend>Generate asound.conf</legend>'
echo '            <table class="bggrey percent100">'
#--------------------------------------Warning-------------------------------------------
echo '              <tr class="warning">'
echo '                <td colspan="3">'
echo '                  <p style="color:white"><b>Note:</b> Using an incompatible asound.conf may stop squeezelite from starting.</b></p>'
echo '                </td>'
echo '              </tr>'
#--------------------------------------Default/Stereo/Mono/Swap/Left/Right---------------
pcp_start_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="column150">'
echo '                  <p class="row">Stereo/Mono/Swap/L/R</p>'
echo '                </td>'
echo '                <td class="column410">'
echo '                  <input class="small1" type="radio" name="OPTION" value="default" '$DEF'>Default&nbsp;'
echo '                  <input class="small1" type="radio" name="OPTION" value="stereo" '$STE'>Stereo&nbsp;'
echo '                  <input class="small1" type="radio" name="OPTION" value="mono" '$MON'>Mono&nbsp;'
echo '                  <input class="small1" type="radio" name="OPTION" value="swap" '$SWA'>Swap channels&nbsp;'
echo '                  <input class="small1" type="radio" name="OPTION" value="left" '$LEF'>Left channel&nbsp;'
echo '                  <input class="small1" type="radio" name="OPTION" value="right" '$RIG'>Right channel'
echo '                </td>'
echo '              </tr>'
#--------------------------------------Volume left---------------------------------------
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="column150">'
echo '                  <p class="row">Left channel: '$VOLUMELEFT'</p>'
echo '                </td>'
echo '                <td class="column210">'
echo '                  <input class="small2" type="text" name="VOLUMELEFT" value="'$VOLUMELEFT'">&nbsp;Volume (0-100)'
echo '                </td>'
echo '                <td colspan="2">'
echo '                  <p class="row"></p>'
echo '                </td>'
echo '              </tr>'
#--------------------------------------Volume right---------------------------------------
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="column150">'
echo '                  <p class="row">Right channel: '$VOLUMERIGHT'</p>'
echo '                </td>'
echo '                <td class="column210">'
echo '                  <input class="small2" type="text" name="VOLUMERIGHT" value="'$VOLUMERIGHT'">&nbsp;Volume (0-100)'
echo '                </td>'
echo '                <td class="column150">'
echo '                  <p class="row"></p>'
echo '                </td>'
echo '              </tr>'
#--------------------------------------Plug----------------------------------------------
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="column150">'
echo '                  <p class="row">Plug: '$HW'</p>'
echo '                </td>'
echo '                <td class="column410">'
echo '                  <input class="small1" type="radio" name="HW" value="hw" '$HW0'>hw&nbsp;'
echo '                  <input class="small1" type="radio" name="HW" value="plughw" '$HW1'>plughw&nbsp;'
echo '                </td>'
echo '              </tr>'
#--------------------------------------Card----------------------------------------------
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="column150">'
echo '                  <p class="row">Card: '$CARD'</p>'
echo '                </td>'
echo '                <td class="column410">'
echo '                  <input class="small1" type="radio" name="CARD" value="0" '$CARD0'>0&nbsp;'
echo '                  <input class="small1" type="radio" name="CARD" value="1" '$CARD1'>1&nbsp;'
echo '                </td>'
echo '              </tr>'
#--------------------------------------Write button--------------------------------------
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td colspan="3">'
echo '                  <input type="submit" name="SUBMIT" value="Write">'
echo '                </td>'
echo '              </tr>'
#----------------------------------------------------------------------------------------
echo '            </table>'
echo '          </fieldset>'
echo '        </div>'
echo '      </form>'
echo '    </td>'
echo '  </tr>'
echo '</table>'

#========================================================================================
# Current asound.conf
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
if [ $MODE = 99 ]; then
	echo '  <tr>'
	echo '    <td>'
	echo '      <form name="asound_conf" method="get">'
	echo '        <div class="row">'
	echo '          <fieldset>'
	echo '            <legend>Current asound.conf</legend>'
	echo '            <table class="bggrey percent100">'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td>'
	                        pcp_textarea_inform "none" "cat $ASOUNDCONF" 150
	echo '                </td>'
	echo '              </tr>'
	echo '            </table>'
	echo '          </fieldset>'
	echo '        </div>'
	echo '      </form>'
	echo '    </td>'
	echo '  </tr>'
fi
#--------------------------------------Output settings-----------------------------------
echo '  <tr class="warning">'
echo '    <td class="column150">'
echo '      <p style="color:white">Output settings</p>'
echo '    </td>'
echo '    <td class="column210">'
echo '      <input class="large15" type="text" name="OUTPUT" value="'$OUTPUT'" readonly>'
echo '    </td>'
echo '    <td>'
echo '      <p style="color:white">This field should be empty.</p>'
echo '    </td>'
echo '  </tr>'
#------------------------------------Squeezelite restart button--------------------------
pcp_toggle_row_shade
echo '  <tr class="'$ROWSHADE'">'
echo '    <td class="column150 center">'
echo '      <form name="Restart" action="restartsqlt.cgi" method="get">'
echo '        <input type="submit" value="Restart" />'
echo '      </form>'
echo '    </td>'
echo '    <td colspan="2">'
echo '      <p class="row">Restart Squeezelite - necessary for new asound.conf to take effect.</p>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------

pcp_footer
pcp_refresh_button

echo '</body>'
echo '</html>'