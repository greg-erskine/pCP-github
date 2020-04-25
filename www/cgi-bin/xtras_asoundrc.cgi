#!/bin/sh

# Version: 6.0.0 2019-12-29

. pcp-functions

pcp_html_head "xtras_asound_conf" "GE"

pcp_controls
pcp_banner
pcp_xtras
pcp_running_script

VOLUMELEFT=100
VOLUMERIGHT=100

#========================================================================================
# Write asound.conf - 0 = left, 1 = right
#----------------------------------------------------------------------------------------
pcp_write_asound_conf() {

	PCMTYPE=${HW}:${CARD},0
	sed -ir '/^pcm\.\!default/,/^\}/ { /^pcm\.\!default/n /^\}/ !{/.*/d}}' $ASOUNDCONF
	case "$OPTION" in
		default)
			sed -ir '/^pcm\.\!default/a\
   # '$OPTION'\
   type plug;\
   slave.pcm "'$PCMTYPE'";
   ' $ASOUNDCONF
		;;
		stereo)
			sed -ir '/^pcm\.\!default/a\
   # '$OPTION'\
   type route;\
   slave.pcm "'$PCMTYPE'";\
   ttable {\
      0.0 '$VOLLEFT';\
      1.1 '$VOLRIGHT';\
   }
   ' $ASOUNDCONF
		;;
		mono)
			sed -ir '/^pcm\.\!default/a\
   # '$OPTION'\
   type route;\
   slave.pcm "'$PCMTYPE'";\
   ttable {\
      0.1 '$VOLLEFT';\
      0.0 '$VOLLEFT';\
      1.0 '$VOLRIGHT';\
      1.1 '$VOLRIGHT';\
   }
   ' $ASOUNDCONF
		;;
		swap)
			sed -ir '/^pcm\.\!default/a\
   # '$OPTION'\
   type route;\
   slave.pcm "'$PCMTYPE'";\
   ttable {\
      0.1 '$VOLLEFT';\
      1.0 '$VOLRIGHT';\
   }
   ' $ASOUNDCONF
		;;
		left)
			sed -ir '/^pcm\.\!default/a\
   # '$OPTION'\
   type route;\
   slave.pcm "'$PCMTYPE'";\
   ttable {\
      0.0 '$VOLLEFT';\
      1.1 0;\
   }
   ' $ASOUNDCONF
		;;
		right)
			sed -ir '/^pcm\.\!default/a\
   # '$OPTION'\
   type route;\
   slave.pcm "'$PCMTYPE'";\
   ttable {\
      0.0 0;\
      1.1 '$VOLRIGHT';\
   }
   ' $ASOUNDCONF
		;;
	esac

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
		[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] Writing asound.conf...</p>'
		pcp_write_asound_conf
	;;
	*)
		[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] Invalid option '$SUBMIT'...</p>'
	;;
esac

TYPE=$(cat $ASOUNDCONF)
[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] Type '${TYPE:2:3}'</p>'
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
case "$HW" in
	hw) HW0="checked" ;;
	plughw) HW1="checked" ;;
esac

#########################################################################################
# Not sure if we will need this code in future. Leave here for time being.
#########################################################################################
#VOLUMELEFT=`grep "0\.[10]" $ASOUNDCONF | awk '{print $2}'`
#if [ $VOLUMELEFT = "1" ]; then
#	VOLUMELEFT=100
#elif [ $VOLUMELEFT = "0" ]; then
#	VOLUMELEFT=0
##elif [ "$VOLUMELEFT" = "" ]; then
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
##elif [ "$VOLUMERIGHT" = "" ]; then
##	VOLUMERIGHT=0
#else
#	if echo $VOLUMERIGHT | grep "0.0" >/dev/null 2>&1; then
#		VOLUMERIGHT=`echo $VOLUMERIGHT | awk -F"0.0" '{print $2}'`
#	else
#		VOLUMERIGHT=`echo $VOLUMERIGHT | awk -F"0." '{print $2}'`
#	fi
#fi

#========================================================================================
# WARNING message
#----------------------------------------------------------------------------------------
echo '<table class="bgred">'
echo '  <tr>'
echo '    <td>'
echo '      <p><b>WARNING:</b> Beta software!! Does not work 100%,'
echo '      but it may be useful. Use at your own risk.</p>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
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
pcp_start_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="warning" colspan="3">'
echo '                  <p><b>Note:</b> Using an incompatible asound.conf may stop squeezelite from starting.</b></p>'
echo '                </td>'
echo '              </tr>'
#--------------------------------------Default/Stereo/Mono/Swap/Left/Right---------------
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="column150">'
echo '                  <p class="row">Stereo/Mono/Swap/L/R</p>'
echo '                </td>'
echo '                <td class="column410">'
echo '                  <input id="rad1" type="radio" name="OPTION" value="default" '$DEF'>'
echo '                  <label for="rad1">Default&nbsp;</label>'
echo '                  <input id="rad2" type="radio" name="OPTION" value="stereo" '$STE'>'
echo '                  <label for="rad2">Stereo&nbsp;</label>'
echo '                  <input id="rad3" type="radio" name="OPTION" value="mono" '$MON'>'
echo '                  <label for="rad3">Mono&nbsp;</label>'
echo '                  <input id="rad4" type="radio" name="OPTION" value="swap" '$SWA'>'
echo '                  <label for="rad4">Swap channels&nbsp;</label>'
echo '                  <input id="rad5" type="radio" name="OPTION" value="left" '$LEF'>'
echo '                  <label for="rad5">Left channel&nbsp;</label>'
echo '                  <input id="rad6" type="radio" name="OPTION" value="right" '$RIG'>'
echo '                  <label for="rad6">Right channel</label>'
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
echo '                  <input id="radhw1" type="radio" name="HW" value="hw" '$HW0'>'
echo '                  <label for="radhw1">hw&nbsp;</label>'
echo '                  <input id="radhw2" type="radio" name="HW" value="plughw" '$HW1'>'
echo '                  <label for="radhw2">plughw&nbsp;</label>'
echo '                </td>'
echo '              </tr>'
#--------------------------------------Card----------------------------------------------
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="column150">'
echo '                  <p class="row">Card: '$CARD'</p>'
echo '                </td>'
echo '                <td class="column410">'
echo '                  <input id="radcard1" type="radio" name="CARD" value="0" '$CARD0'>'
echo '                  <label for="radcard1">0&nbsp;</label>'
echo '                  <input id="radcard2" type="radio" name="CARD" value="1" '$CARD1'>'
echo '                  <label for="radcard2">1&nbsp;</label>'
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
echo '  <tr>'
echo '    <td>'
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

#--------------------------------------Output settings-----------------------------------
echo '              <tr class="warning">'
echo '                <td class="column150">'
echo '                  <p>Output settings</p>'
echo '                </td>'
echo '                <td class="column210">'
echo '                  <input class="large15" type="text" name="OUTPUT" value="'$OUTPUT'" readonly>'
echo '                </td>'
echo '                <td>'
echo '                  <p>This field should be empty - use Squeezelite Settings page to remove Output setting.</p>'
echo '                </td>'
echo '              </tr>'
#------------------------------------Squeezelite restart button--------------------------
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="column150 center">'
echo '                  <form name="Restart" action="restartsqlt.cgi" method="get">'
echo '                    <input type="submit" value="Restart" />'
echo '                  </form>'
echo '                </td>'
echo '                <td colspan="2">'
echo '                  <p> Restart Squeezelite - necessary for new asound.conf to take effect.</p>'
echo '                </td>'
echo '              </tr>'
echo '            </table>'
echo '          </fieldset>'
echo '        </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------

pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'