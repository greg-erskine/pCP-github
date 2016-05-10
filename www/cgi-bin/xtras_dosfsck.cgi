#!/bin/sh

# Version: 0.02 2015-06-02 GE
#	Minor updates.

# Version: 0.01 2015-02-17 GE
#   Original version.

. pcp-lms-functions
. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "xtras_dosfsck" "GE"

pcp_controls
pcp_banner
pcp_navigation
pcp_mode_lt_beta
pcp_running_script
pcp_httpd_query_string

case "$SUBMIT" in
	dosfsck)
		OPT=1
	;;
	delete)
		OPT=2
	;;
	*)
		OPT=0
	;;
esac

#========================================================================================
# Check for dosfstools.tcz and download and install
#========================================================================================
pcp_check_dosfsck() {
	echo '<textarea class="inform" rows="6">'
	echo 'Note: Requires dosfstools.tcz'
	which dosfsck
	if [ $? -eq 0 ]; then
		echo 'dosfstools.tcz already installed.'
	else
		if [ ! -f /mnt/mmcblk0p2/tce/optional/dosfstools.tcz ]; then
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
# Delete dosfstools.tcz
#========================================================================================
if [ $OPT -eq 1 ]; then
	rm -f /mnt/mmcblk0p2/tce/optional/dosfstools.*
fi

#========================================================================================
# dosfsck routine
#----------------------------------------------------------------------------------------
pcp_dosfsck() {
	echo '<textarea class="inform" rows="10">'
	dosfsck -a /dev/mmcblk0p1
	echo '</textarea>'
}

#========================================================================================
# Main
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '        <legend>Check boot partition</legend>'
echo '          <table class="bggrey percent100">'
echo '            <form name="increase" action="xtras_dosfsck.cgi" method="get" id="increase">'
echo '              <tr class="even">'
echo '                <td>'
                        pcp_check_dosfsck
echo '                </td>'
echo '              </tr>'
echo '              <tr class="warning">'
echo '                <td>'
echo '                  <p style="color:white">'
echo '                    <input type="submit" name="SUBMIT" value="dosfsck" />&nbsp;&nbsp;Auto fix boot partition&nbsp;&nbsp;'
echo '                    <input type="submit" name="SUBMIT" value="delete" />&nbsp;&nbsp;Delete dosfstools.tcz'
echo '                  </p>'
echo '                </td>'
echo '              </tr>'
echo '              <tr class="even">'
echo '                <td>'
                        [ $OPT -eq 1 ] && pcp_dosfsck
echo '                </td>'
echo '              </tr>'
echo '            </form>'
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
echo '      <form name="sd_information" method="get">'
echo '        <div class="row">'
echo '          <fieldset>'
echo '            <legend>Boot partition information</legend>'
echo '            <table class="bggrey percent100">'
echo '              <tr class="odd">'
echo '                <td>'
                        pcp_textarea_inform "none" "dosfsck -vrf  /dev/mmcblk0p1" 300
echo '                </td>'
echo '              </tr>'
echo '              <tr class="odd">'
echo '                <td>'
                        pcp_textarea_inform "none" "fsck -h" 25
echo '                </td>'
echo '              </tr>'
echo '            </table>'
echo '          </fieldset>'
echo '        </div>'
echo '      </form>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------

pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'