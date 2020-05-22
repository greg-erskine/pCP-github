#!/bin/sh

# Version: 7.0.0 2020-05-22
# Title: asound.conf
# Description: BETA - Modify asound.conf

. pcp-functions

pcp_html_head "xtras_asound_conf" "GE"

pcp_controls
pcp_xtras

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
		[ $DEBUG -eq 1 ] && pcp_message DEBUG "Writing asound.conf..." "html"
		pcp_write_asound_conf
	;;
	*)
		[ $DEBUG -eq 1 ] && pcp_message DEBUG "Invalid option $SUBMIT..." "html"
	;;
esac

TYPE=$(cat $ASOUNDCONF)
[ $DEBUG -eq 1 ] && pcp_message DEBUG "Type ${TYPE:2:3}" "html"
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
echo '  <div>'
echo '    <div>'
echo '      <p><b>WARNING:</b> Beta software!! Does not work 100%,'
echo '      but it may be useful. Use at your own risk.</p>'
echo '    </div>'
echo '  </div>'
#========================================================================================

#----------------------------------------------------------------------------------------
echo '  <div class="'$BORDER'">'
echo '    <form name="asound" action="xtras_asoundrc.cgi" method="get" id="asound">'
pcp_heading5 "Generate asound.conf"
#--------------------------------------Warning-------------------------------------------
echo '      <div class="row mx-1">'
echo '        <div class="col-12">'
echo '          <p><b>Note:</b> Using an incompatible asound.conf may stop squeezelite from starting.</b></p>'
echo '        </div>'
echo '      </div>'
#--------------------------------------Default/Stereo/Mono/Swap/Left/Right---------------
echo '      <div class="row mx-1">'
echo '        <div class="col-3">'
echo '          <p>Stereo/Mono/Swap/L/R</p>'
echo '        </div>'
echo '        <div class="col-9">'
echo '          <input id="rad1" type="radio" name="OPTION" value="default" '$DEF'>'
echo '          <label for="rad1">Default&nbsp;&nbsp;</label>'
echo '          <input id="rad2" type="radio" name="OPTION" value="stereo" '$STE'>'
echo '          <label for="rad2">Stereo&nbsp;&nbsp;</label>'
echo '          <input id="rad3" type="radio" name="OPTION" value="mono" '$MON'>'
echo '          <label for="rad3">Mono&nbsp&nbsp;</label>'
echo '          <input id="rad4" type="radio" name="OPTION" value="swap" '$SWA'>'
echo '          <label for="rad4">Swap channels&nbsp;&nbsp;</label>'
echo '          <input id="rad5" type="radio" name="OPTION" value="left" '$LEF'>'
echo '          <label for="rad5">Left channel&nbsp;&nbsp;</label>'
echo '          <input id="rad6" type="radio" name="OPTION" value="right" '$RIG'>'
echo '          <label for="rad6">Right channel</label>'
echo '        </div>'
echo '      </div>'
#--------------------------------------Volume left---------------------------------------
echo '      <div class="row mx-1">'
echo '        <div class="col-3">'
echo '          <p>Left channel: '$VOLUMELEFT'</p>'
echo '        </div>'
echo '        <div class="form-group col-9">'
echo '          <input class="form-control form-control-sm" type="text" name="VOLUMELEFT" value="'$VOLUMELEFT'">&nbsp;Volume (0-100)'
echo '        </div>'
echo '      </div>'
#--------------------------------------Volume right---------------------------------------
echo '      <div class="row mx-1">'
echo '        <div class="col-3">'
echo '          <p>Right channel: '$VOLUMERIGHT'</p>'
echo '        </div>'
echo '        <div class="form-group col-9">'
echo '          <input class="form-control form-control-sm" id="vr" type="text" name="VOLUMERIGHT" value="'$VOLUMERIGHT'">'
echo '          <label class="input-group-text" for="vr">Volume (0-100)</label>'
echo '        </div>'
echo '      </div>'
#--------------------------------------Plug----------------------------------------------
echo '      <div class="row mx-1">'
echo '        <div class="col-3">'
echo '          <p>Plug: '$HW'</p>'
echo '        </div>'
echo '        <div class="col-9">'
echo '          <input id="radhw1" type="radio" name="HW" value="hw" '$HW0'>'
echo '          <label for="radhw1">hw&nbsp;&nbsp;</label>'
echo '          <input id="radhw2" type="radio" name="HW" value="plughw" '$HW1'>'
echo '          <label for="radhw2">plughw</label>'
echo '        </div>'
echo '      </div>'
#--------------------------------------Card----------------------------------------------
echo '      <div class="row mx-1">'
echo '        <div class="col-3">'
echo '          <p>Card: '$CARD'</p>'
echo '        </div>'
echo '        <div class="col-9">'
echo '          <input id="radcard1" type="radio" name="CARD" value="0" '$CARD0'>'
echo '          <label for="radcard1">0&nbsp;&nbsp;</label>'
echo '          <input id="radcard2" type="radio" name="CARD" value="1" '$CARD1'>'
echo '          <label for="radcard2">1</label>'
echo '        </div>'
echo '      </div>'
#--------------------------------------Write button--------------------------------------
echo '      <div class="row mx-1 mb-2">'
echo '        <div class="col-2">'
echo '          <input class="'$BUTTON'" type="submit" name="SUBMIT" value="Write">'
echo '        </div>'
echo '      </div>'
#----------------------------------------------------------------------------------------
echo '    </form>'
echo '  </div>'

#========================================================================================
# Current asound.conf
#----------------------------------------------------------------------------------------
pcp_textarea "Current $ASOUNDCONF" "cat $ASOUNDCONF" 15

echo '  <div class="'$BORDER'">'
pcp_heading5 "Current asound.conf"
#--------------------------------------Output settings-----------------------------------
echo '    <div class="row mx-1">'
echo '      <div class="col-2">'
echo '        <p>Output settings</p>'
echo '      </div>'
echo '      <div class="form-group col-3">'
echo '        <input class="form-control form-control-sm" type="text" name="OUTPUT" value="'$OUTPUT'" readonly>'
echo '      </div>'
echo '      <div class="col-7">'
echo '        <p>This field should be empty - use Squeezelite Settings page to remove Output setting.</p>'
echo '      </div>'
echo '    </div>'
#------------------------------------Squeezelite restart button--------------------------
echo '    <div class="row mx-1">'
echo '      <div class="col-2">'
echo '        <form name="Restart" action="restartsqlt.cgi" method="get">'
echo '          <input class="'$BUTTON'" type="submit" value="Restart">'
echo '        </form>'
echo '      </div>'
echo '      <div class="col-10">'
echo '        <p>Restart Squeezelite for new asound.conf to take effect.</p>'
echo '      </div>'
echo '    </div>'
#----------------------------------------------------------------------------------------
echo '  </div>'
#----------------------------------------------------------------------------------------

pcp_html_end
exit