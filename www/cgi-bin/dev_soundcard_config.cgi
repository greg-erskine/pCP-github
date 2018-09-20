#!/bin/sh

# Version: 4.0.1 2018-09-20

# Title: Soundcard config files
# Description: Easy method for viewing the Soundcard configuration files

. pcp-functions
. pcp-soundcard-functions

pcp_html_head "Show Soundcard Config File" "GE"

pcp_banner
pcp_running_script
pcp_httpd_query_string

PCPSOUNDCARDS=$(ls "${DACLOCATION}")

#========================================================================================
# Routines
#----------------------------------------------------------------------------------------
pcp_overlays_loaded() {
	pcp_mount_bootpart_nohtml >/dev/null 2>&1
	OVERLAYS=$(cat ${VOLUME}/config.txt | grep ^dtoverlay | sed 's/dtoverlay=//')
	pcp_umount_bootpart_nohtml >/dev/null 2>&1
}
pcp_overlays_loaded

#========================================================================================
# Selection form
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Select soundcard config file</legend>'
echo '          <form name="soundcard" action="'$0'" method="get">'
echo '            <table class="bggrey percent100">'
#----------------------------------------------------------------------------------------
pcp_incr_id
pcp_start_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="column300">'
echo '                  <select class="large22" name="SELECTION">'

	                      for CARD in $PCPSOUNDCARDS
	                      do
	                          [ "$SELECTION" = "$CARD" ] && SELECTED="selected" || SELECTED=""
	                          echo '                    <option value="'$CARD'" '$SELECTED'>'$(echo ${CARD/.conf/})'</option>'
	                      done

echo '                  </select>'
echo '                </td>'
echo '                <td>'
echo '                  <p>Show soundcard config file&nbsp;&nbsp;'
echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                  </p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <p>The soundcard config files are located in '$DACLOCATION'</p>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td colspan="2">'
echo '                  <input type="submit" name="ACTION" value="Show">'
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

#------------------------------------------Soundcard text area-----------------------------
pcp_soundcard_show() {
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>'$(echo ${SELECTION/.conf/})' config file</legend>'
	echo '          <table class="bggrey percent100">'
	echo '            <tr>'
	echo '              <td>'
	                      pcp_textarea_inform "none" 'cat ${DACLOCATION}/$SELECTION' 250
	echo '              </td>'
	echo '            </tr>'
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
}
[ "$ACTION" = "Show" ] && pcp_soundcard_show
#----------------------------------------------------------------------------------------

#------------------------------------------Loaded overlays text area---------------------
pcp_card_loaded() {
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Loaded Overlays</legend>'
	echo '          <table class="bggrey percent100">'
	echo '            <tr>'
	echo '              <td>'
	                      pcp_textarea_inform "none" "echo $OVERLAYS | sed 's/ /\n/g'" 50
	echo '              </td>'
	echo '            </tr>'
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
}
pcp_card_loaded
#----------------------------------------------------------------------------------------

pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'
