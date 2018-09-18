#!/bin/sh

# Version: 4.0.1 2018-09-19

. pcp-functions
. pcp-lms-functions

pcp_html_head "xtras_dosfsck" "GE"

pcp_banner
pcp_navigation
pcp_running_script
pcp_httpd_query_string

case "$SUBMIT" in
	dosfsck)
		OPTION="dosfsck"
	;;
	delete)
		OPTION="delete"
	;;
	*)
		OPTION="initial"
	;;
esac

#========================================================================================
# Check for dosfstools.tcz and download and install.
#========================================================================================
pcp_check_dosfsck() {
	echo '<textarea class="inform" rows="6">'
	echo 'Note: Requires dosfstools.tcz'
	which fsck.fat
	if [ $? -eq 0 ]; then
		echo 'dosfstools.tcz already installed.'
	else
		if [ ! -f ${PACKAGEDIR}/dosfstools.tcz ]; then
			echo 'dosfstools.tcz downloading... '
			sudo -u tc tce-load -w dosfstools.tcz
			[ $? -eq 0 ] && echo 'Done.' || echo 'Error.'
		else
			echo 'dosfstools.tcz downloaded.'
		fi
		echo 'dosfstools.tcz installing... '
		sudo -u tc tce-load -i dosfstools.tcz
		[ $? -eq 0 ] && echo 'Done.' || echo 'Error.'
	fi
	echo '</textarea>'
}

#========================================================================================
# Main.
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '        <legend>Check boot partition</legend>'
echo '          <table class="bggrey percent100">'
echo '            <tr class="even">'
echo '              <td>'
                      pcp_check_dosfsck
echo '              </td>'
echo '            </tr>'
echo '            <tr class="odd">'
echo '              <td>'
echo '                <form name="fsck" action="xtras_dosfsck.cgi" method="get">'
echo '                  <input type="submit" name="SUBMIT" value="dosfsck">&nbsp;&nbsp;Auto fix boot partition&nbsp;&nbsp;'
echo '                  <input type="submit" name="SUBMIT" value="delete">&nbsp;&nbsp;Delete dosfstools.tcz'
echo '                </form>'
echo '              </td>'
echo '            </tr>'
if [ "$OPTION" = "dosfsck" ]; then
	echo '            <tr class="even">'
	echo '              <td>'
	echo '                <textarea class="inform" rows="10">'
	                        fsck.fat -a $BOOTDEV
	echo '                </textarea>'
	echo '              </td>'
	echo '            </tr>'
fi
if [ "$OPTION" = "delete" ]; then
	echo '            <tr class="even">'
	echo '              <td>'
	echo '                <textarea class="inform" rows="10">'
	                        sudo -u tc tce-audit builddb
	echo
	echo                    'After a reboot the following extensions will be permanently deleted:'
	echo
	                        sudo -u tc tce-audit delete dosfstools.tcz
	echo '                </textarea>'
	echo '              </td>'
	echo '            </tr>'
fi
echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'

#========================================================================================
# Partition information
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Boot partition information</legend>'
echo '          <table class="bggrey percent100">'
echo '            <tr class="odd">'
echo '              <td>'
                      pcp_textarea_inform "none" "fsck.fat -vrf ${BOOTDEV}" 300
echo '              </td>'
echo '            </tr>'
echo '            <tr class="odd">'
echo '              <td>'
                      pcp_textarea_inform "none" "fsck -h" 25
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
pcp_remove_query_string

echo '</body>'
echo '</html>'
