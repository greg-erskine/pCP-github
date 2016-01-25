#!/bin/sh

# Version: 0.04 2016-01-26 GE
#	Removed manual resize option.

# Version: 0.03 2015-11-27 GE
#	Added autoresize.

# Version: 0.02 2015-06-02 GE
#	Minor updates.

# Version: 0.01 2015-02-17 GE
#   Original version.

. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "xtras_resize" "GE" "30" "main.cgi"

pcp_controls
pcp_banner
pcp_navigation
pcp_mode_lt_beta
pcp_running_script
pcp_httpd_query_string

#========================================================================================
# Partition information
#----------------------------------------------------------------------------------------
pcp_start_row_shade
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <form name="sd_information" method="get">'
echo '        <div class="row">'
echo '          <fieldset>'
echo '            <legend>Partition Information</legend>'
echo '            <table class="bggrey percent100">'
echo '              <tr class="'$ROWSHADE'">'
echo '                <td>'
                        pcp_textarea_inform "none" "df -h /dev/mmc*" 50
echo '                </td>'
echo '              </tr>'
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td>'
echo '                </td>'
echo '              </tr>'
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td>'
                        pcp_textarea_inform "none" "fdisk -ul" 120
echo '                </td>'
echo '              </tr>'
echo '            </table>'
echo '          </fieldset>'
echo '        </div>'
echo '      </form>'
echo '    </td>'
echo '  </tr>'
echo '</table>'

#========================================================================================
# Resize or watiing tables
#----------------------------------------------------------------------------------------
if [ $SUBMIT = Resize ]; then
	pcp_start_row_shade
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '        <legend>Auto resize partition</legend>'
	echo '          <table class="bggrey percent100">'
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td>'
	echo '                <p>Resizing the partition is occuring, please wait...</p>'
	echo '                <p>This will take a couple of minutes and piCorePlayer will reboot a number of times.</p>'
	echo '                <p>Click [ Main Page ] after a few minutes.</p>'
	echo '              </td>'
	echo '            </tr>'
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
else
	if [ -f /home/tc/www/cgi-bin/autoresize.sh ]; then
		pcp_start_row_shade
		echo '<table class="bggrey">'
		echo '  <tr>'
		echo '    <td>'
		echo '      <div class="row">'
		echo '        <fieldset>'
		echo '        <legend>Auto resize partition</legend>'
		echo '          <table class="bggrey percent100">'
		echo '            <form name="auto" action="xtras_resize.cgi" method="get">'
		echo '              <tr class="'$ROWSHADE'">'
		echo '                <td>'
		echo '                  <p>Auto resizing the partition is an automatic process that will fully expand the partition:</p>'
		echo '                  <ol>'
		echo '                    <li>fdisk, then auto reboot</li>'
		echo '                    <li>resize2fs, then auto reboot</li>'
		echo '                  </ol>'
		echo '                </td>'
		echo '              </tr>'
		echo '              <tr class="warning">'
		echo '                <td>'
		echo '                  <p style="color:white">'
		echo '                    <input type="submit" name="SUBMIT" value="Resize" />&nbsp;&nbsp;Auto resize partition'
		echo '                  </p>'
		echo '                </td>'
		echo '              </tr>'
		echo '            </form>'
		echo '          </table>'
		echo '        </fieldset>'
		echo '      </div>'
		echo '    </td>'
		echo '  </tr>'
		echo '</table>'
	fi
fi

pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'

case $SUBMIT in
	Resize)
		touch /home/tc/fdisk_required
		pcp_backup
		sudo reboot
		;;
esac

exit