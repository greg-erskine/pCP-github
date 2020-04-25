#!/bin/sh

# Version: 6.0.0 2020-02-29

. pcp-functions
. pcp-lms-functions

pcp_html_head "IQAudIO Codec Card Settings" "PH"

pcp_picoreplayers_toolbar
pcp_controls
pcp_banner
pcp_navigation
pcp_httpd_query_string
pcp_remove_query_string

IQCODECCONF=/usr/local/etc/pcp/iqcodec.conf

#---------------------------Routines-----------------------------------------------------

set_iqcodec_conf() {
	echo "IQ_MODE=${IQ_MODE}" > $IQCODECCONF

	/usr/local/bin/iqcodec-config.sh
}

REBOOT_REQUIRED=0
case "$ACTION" in
	Setconfig)
		pcp_table_top "IQaudIO Codec configuration"
		echo '                <textarea class="inform" style="height:120px">'
		set_iqcodec_conf
		pcp_backup "text"
		echo '                </textarea>'
		pcp_table_end
	;;
esac

#========================================================================================
# Main table
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>IQAudIO Codec Card Configuration</legend>'
echo '          <table class="bggrey percent100">'

#------------------------------------------Configure ------------------------------------
[ -f /usr/local/etc/pcp/iqcodec.conf ] && . /usr/local/etc/pcp/iqcodec.conf
[ "$IQ_MODE" = "" ] && IQ_MODE="mode3"

pcp_incr_id
pcp_toggle_row_shade

COL1="column150 center"
COL2="column400"

#--------------------------------------Heading-------------------------------------------
echo '            <tr class="'$ROWSHADE'">'
echo '              <td class="'$COL1'">'
echo '                <p><b>Mode</b></p>'
echo '              </td>'
echo '              <td class="'$COL2'">'
echo '                <p><b>Description/Help</b></p>'
echo '              </td>'
echo '            </tr>'
#----------------------------------------------------------------------------------------

#--------------------------------------configure-----------------------------------------
pcp_iqcodec_configure() {
	MODE1=""
	MODE2=""
	MODE3=""
	MODE4=""
	case $IQ_MODE in
		mode1) MODE1yes="checked";;
		mode2) MODE2yes="checked";;
		mode3) MODE3yes="checked";;
		mode4) MODE4yes="checked";;
	esac

	echo '            <form name="configure" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL1'">'
	echo '                    <input id="rad1" type="radio" name="IQ_MODE" value="mode1" '$MODE1yes'>'
	echo '                    <label for="rad1">Mode 1:</label>'
	echo '                </td>'
	echo '                <td class="'$COL2'">'
	echo '                  <p>Record from Aux IN, Playback to Head Phone jack.</p>'
	echo '                </td>'
	echo '              </tr>'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL1'">'
	echo '                    <input id="rad2" type="radio" name="IQ_MODE" value="mode2" '$MODE2yes'>'
	echo '                    <label for="rad2">Mode 2:</label>'
	echo '                </td>'
	echo '                <td class="'$COL2'">'
	echo '                  <p>Record from Onboard Mic, Playback to Mono Speaker jack.</p>'
	echo '                </td>'
	echo '              </tr>'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL1'">'
	echo '                    <input id="rad3" type="radio" name="IQ_MODE" value="mode3" '$MODE3yes'>'
	echo '                    <label for="rad3">Mode 3:</label>'
	echo '                </td>'
	echo '                <td class="'$COL2'">'
	echo '                  <p>Playback to Head Phone jack.</p>'
	echo '                </td>'
	echo '              </tr>'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL1'">'
	echo '                    <input id="rad4" type="radio" name="IQ_MODE" value="mode4" '$MODE4yes'>'
	echo '                    <label for="rad4">Mode 4:</label>'
	echo '                </td>'
	echo '                <td class="'$COL2'">'
	echo '                  <p>Record from Stereo Mic, Playback to Head Phone jack.</p>'
	echo '                </td>'
	echo '              </tr>'
#--------------------------------------Submit button-------------------------------------
	pcp_incr_id
	pcp_toggle_row_shade
	echo '                <tr class="'$ROWSHADE'">'
	echo '                  <td class="column150 center">'
	echo '                    <button type="submit" name="ACTION" value="Setconfig" '$DISABLE'>Set Mode</button>'
	echo '                  </td>'
	echo '                  <td class="colspan=2">'
	echo '                    <p>Enable card mode by selecting above, then press the "Set Mode" button</p>'
	echo '                  </td>'
	echo '                </tr>'
	echo '              </form>'
}
[ $MODE -ge $MODE_PLAYER ] && pcp_iqcodec_configure
#----------------------------------------------------------------------------------------
echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------

pcp_footer
pcp_mode
pcp_copyright

echo '</body>'
echo '</html>'
