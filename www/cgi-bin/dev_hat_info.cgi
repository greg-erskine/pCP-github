#!/bin/sh

# Version: 4.0.1 2018-11-19

# Title: HAT information
# Description: Easy method for viewing the HAT information

. pcp-functions

pcp_html_head "View HAT Information" "GE"

pcp_banner
pcp_running_script
pcp_httpd_query_string

HATDIRECTORY="/proc/device-tree/hat/"
HATHEADINGS=$(ls $HATDIRECTORY)

LOG="${LOGDIR}/pcp_hat_info.log"
pcp_log_header $0
echo ====================================================================================== >>$LOG

#========================================================================================
# Routines
#----------------------------------------------------------------------------------------
pcp_overlays_loaded() {
	pcp_mount_bootpart nohtml >/dev/null 2>&1
	OVERLAYS=$(cat ${VOLUME}/config.txt | grep dtoverlay)
	pcp_umount_bootpart nohtml >/dev/null 2>&1
}
pcp_overlays_loaded

#========================================================================================
# Main HTML
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>HAT information</legend>'
echo '          <table class="bggrey percent100">'
#----------------------------------------------------------------------------------------
pcp_start_row_shade

for HEADING in $HATHEADINGS
do
	echo $HEADING': '$(cat ${HATDIRECTORY}${HEADING}) >>$LOG
	pcp_incr_id
	pcp_toggle_row_shade

	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150">'
	echo '                <p>'$HEADING'</p>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>'$(cat ${HATDIRECTORY}${HEADING})'</p>'
	echo '              </td>'
	echo '            </tr>'
done

echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------

#-------------------------------------------dmesg text area------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>dmesg | grep soc:sound</legend>'
echo '          <table class="bggrey percent100">'
echo '            <tr>'
echo '              <td>'
	                  pcp_textarea_inform "dmesg" 'dmesg | grep soc:sound' 50 log
echo '              </td>'
echo '            </tr>'
echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------

#------------------------------------------Overlays text area----------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Overlays in '${VOLUME}'/config.txt</legend>'
echo '          <table class="bggrey percent100">'
echo '            <tr>'
echo '              <td>'
	                  pcp_textarea_inform "Overlays" 'echo $OVERLAYS | sed "s/ /\n/g"' 50 log
echo '              </td>'
echo '            </tr>'
echo '          </table>'
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