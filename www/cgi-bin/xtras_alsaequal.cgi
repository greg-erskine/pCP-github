#!/bin/sh

# Version: 0.01 2016-01-08 GE
#	Original version.

#========================================================================================
# Have a play with alsaequal
#----------------------------------------------------------------------------------------

DEBUG=1

. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "xtras alsaequal" "GE"

pcp_controls
pcp_banner
pcp_running_script
pcp_httpd_query_string

SET_EQUAL="sudo amixer -D equal cset numid="
BAND=1
FORMID=alsaequal

#========================================================================================
# Routines
#----------------------------------------------------------------------------------------

pcp_load_equaliser() {
	for VALUE in $EQSET
	do
		${SET_EQUAL}$BAND $VALUE >/dev/null 2>&1
		BAND=$(($BAND + 1))
	done

#      Here we need a method to refresh the pCP-webpage in this place. So that the new settings will be shown.       <----------------Do yo have an idea
}

ID1=3
echo 'ID er " $ID1 "$ID2" "$ID3" "$ID4"'
greg=$(sudo amixer -D equal contents | grep ": values" | awk -F"," '{print $2}')
#echo $greg

#=========================================================================================
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>ALSAEQUAL</legend>'
#----------------------------------------------------------------------------------------
pcp_incr_id
echo '          <table class="bggrey percent100">'
echo '            <form name="equal" action="'$0'" method="get">'
pcp_start_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td>'
echo '            <form name="adjust" action="'$0'" method="get">'
echo '</form>' #------------------new
echo '</form>' #------------------new
echo '<form id="$FORMID" action="xtras_alsaequal.cgi">' #------------------new
LB1="31 Hz Playback Volume"
LB2="63 Hz Playback Volume"
LB3="125 Hz Playback Volume"
LB4="250 Hz Playback Volume"
LB5="500 Hz Playback Volume"
LB6="1 kHz Playback Volume"
LB7="2 kHz Playback Volume"
LB8="4 kHz Playback Volume"
LB9="8 kHz Playback Volume"
LB10="16 kHz Playback Volume"

# Added this line because I don't have alsaequal loaded
#greg="66 66 66 66 66 66 66 66 66 66"

	i=1
	for VALUE in $greg
	do
		echo '                  <p><input class="large36" type="range" name="VALUE'$i'" value="'$VALUE'" min="0" max="100" id="ID'$i'" <label for="id">&nbsp;&nbsp;'$(eval "echo \$LB$i")'</label></p>'
	i=$((i + 1))
	done

	echo '                <p><b>10 band ALSA equalizer&nbsp;&nbsp;</b>'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <p>Use the sliders to achive the soundstage you want.</p>'
	echo '                  <p><b>Note:</b></p>'
	echo '                  <ul>'
	echo '                    <li>Changes are reflected immideately so you can hear the effects.</li>'
	echo '                    <li>Please use the refresh button after you have saved your settings.</li>'
	echo '                  </ul>'
	echo '                </div>'



echo '                </td>'
echo '              </tr>'
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'" >'
echo '                <td colspan=3>'

echo '                  <input type="submit" name="SUBMIT" value="Save">'

echo '                </td>'
echo '              </tr>'
echo '            </form>'
echo '          </table>'

#----------------------------------------------------------------------------------------
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'


EQSET=$(echo "$VALUE1" "$VALUE2" "$VALUE3" "$VALUE4" "$VALUE5" "$VALUE6" "$VALUE7" "$VALUE8" "$VALUE9" "$VALUE10")
[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] EQSET is: '$EQSET' </p>'
#echo $greg
[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] ID is: "$ID1" "$ID2" "$ID3" "$ID4" </p>'

pcp_load_equaliser
pcp_backup
pcp_refresh_button
pcp_refresh

pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'