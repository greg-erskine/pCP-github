#!/bin/sh

# Version: 0.01 2016-01-24 GE
#   Original version.

. pcp-functions
pcp_variables
. $CONFIGCFG

CARDS=$(cat /proc/asound/card*/id)

pcp_html_head "xtras_alsa" "GE"

pcp_controls
pcp_banner
pcp_navigation
pcp_running_script
pcp_httpd_query_string



#=========================================================================================
# 
#-----------------------------------------------------------------------------------------
pcp_view_asound_state() {
	if [ -f /var/lib/alsa/asound.state ]; then
		pcp_textarea_inform "Current /var/lib/alsa/asound.state" "cat /var/lib/alsa/asound.state" 180
	else
		pcp_textarea_inform "Current /var/lib/alsa/asound.state" "echo '[ WARN ] /var/lib/alsa/asound.state missing.'" 50
	fi
}

case $ACTION in
	Store)
		sudo alsactl store
		;;
	Restore)
		sudo alsactl restore
		;;
	Backup)
		pcp_backup
		;;
	Custom)
		echo
		;;
	View)
		echo
		;;
	Delete)
		sudo mv /var/lib/alsa/asound.state /var/lib/alsa/asound.state~
		;;
esac

#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>ALSA</legend>'
#----------------------------------------------------------------------------------------
pcp_incr_id
pcp_start_row_shade
echo '          <table class="bggrey percent100">'
echo '            <form name="xxxxxxxxxxxx" action="'$0'" method="get">'

pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td>'
echo '                  <textarea class="inform" style="height:200px">'

for VALUE in $CARDS
do
	echo CARD=$VALUE
	amixer -c $VALUE -- sget PCM
	echo
done

echo '                  </textarea>'
echo '                </td>'

pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td>'
echo '                  <input type="submit" name="ACTION" value="Store">'
echo '                  <input type="submit" name="ACTION" value="Restore">'
echo '                  <input type="submit" name="ACTION" value="Backup">'
echo '                  <input type="submit" name="ACTION" value="Custom">'
echo '                  <input type="submit" name="ACTION" value="View">'
echo '                  <input type="submit" name="ACTION" value="Delete">'
echo '                </td>'
echo '              </tr>'

if [ $ACTION = "View" ] || [ $ACTION = "Delete" ]; then

pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td>'
                        pcp_view_asound_state
                        #pcp_textarea_inform "Current /var/lib/alsa/asound.state" "cat /var/lib/alsa/asound.state" 180
echo '                </td>'
fi

echo '              </tr>'
echo '            </form>'
echo '          </table>'
#----------------------------------------------------------------------------------------
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------

pcp_footer
pcp_copyright
pcp_refresh_button

echo '</body>'
echo '</html>'