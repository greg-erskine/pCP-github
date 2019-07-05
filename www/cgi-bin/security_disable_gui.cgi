#!/bin/sh

# Version: 5.1.0 2019-06-08

#========================================================================================
# Disable web GUI
#----------------------------------------------------------------------------------------
STOP_HTTPD_SH="/tmp/stop_httpd.sh"

case $ACTION in
	Save\ GUI)
		pcp_save_to_config
		pcp_backup >/dev/null 2>&1
		REBOOT_REQUIRED=TRUE
	;;
	Abort\ GUI)
		sudo killall $STOP_HTTPD_SH
		REBOOT_REQUIRED=TRUE
	;;
	*)
		pcp_security_ssh
	;;
esac

COLUMN1="column210"
COLUMN2="column210"
#---------------------------------------web GUI------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <form id="GUI_Disable" name="GUI_Disable" action="'$0'" method="get">'
echo '        <div class="row">'
echo '          <fieldset>'
echo '            <legend>Disable web GUI</legend>'
echo '            <table class="bggrey percent100">'
#----------------------------------------------------------------------------------------
pcp_start_row_shade
pcp_incr_id
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="'$COLUMN1'">'
echo '                  <p>Disable web GUI</p>'
echo '                </td>'
echo '                <td class="'$COLUMN2'">'
echo '                  <input class="large6"'
echo '                         type="text"'
echo '                         name="GUI_DISABLE"'
echo '                         value="'$GUI_DISABLE'"'
echo '                         pattern="\d*"'
echo '                         title="Use numbers."'
echo '                  > seconds'
echo '                </td>'
echo '                <td>'
echo '                  <p>Set disable web GUI time&nbsp;&nbsp;'
echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                  </p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <p>&lt;xx seconds&gt;</p>'
echo '                    <p><b>Default: </b>0 = enable web GUI</p>'
echo '                    <p>1 = never start web GUI</p>'
echo '                    <p>&gt;20 = minimum value</p>'
echo '                    <p>This sets the time, in seconds, between piCorePlayer booting and the web GUI being disabled.</p>'
echo '                    <p>This increases security because it gives limited access window to the web GUI.</p>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'
#----------------------------------------------------------------------------------------
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td colspan="3">'
echo '                  <button type="submit" name="ACTION" value="Save GUI">Save</button>'
	                    [ -f $STOP_HTTPD_SH ] &&
echo '                  <button type="submit" name="ACTION" value="Abort GUI">Abort</button>'
echo '                  <input type="hidden" name="CALLED_BY" value="Disable GUI">'
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
#----------------------------------------------------------------------------------------
