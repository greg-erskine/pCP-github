#!/bin/sh

# Version: 3.03 2016-10-01
#	Added selectable partition size from dropdown list. SBP.

# Version: 3.00 2016-07-08
#	Removed pcp_mode_lt_beta. GE. 

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
pcp_running_script
pcp_httpd_query_string

#========================================================================================
#Logic determining actual size, maximal possible size 
ACTUAL_SIZE=$(fdisk -l /dev/mmcblk0p2 | grep dev/mmcblk0p2: | awk '{ print $3 }')
MAX_SIZE=$(fdisk -l /dev/mmcblk0 | grep /dev/mmcblk0: | awk '{ print $3 }')


# Allow the correct values in dropdown list to be selectable
DISABLED100=""
DISABLED200=""
DISABLED300=""
DISABLED500=""
DISABLED1000=""
[ "$ACTUAL_SIZE" -ge 100 ] || [ "$MAX_SIZE" -le 100 ] && DISABLED100=disabled
[ "$ACTUAL_SIZE" -ge 200 ] || [ "$MAX_SIZE" -le 200 ] && DISABLED200=disabled
[ "$ACTUAL_SIZE" -ge 300 ] || [ "$MAX_SIZE" -le 300 ] && DISABLED300=disabled
[ "$ACTUAL_SIZE" -ge 500 ] || [ "$MAX_SIZE" -le 500 ] && DISABLED500=disabled
[ "$ACTUAL_SIZE" -ge 1000 ] || [ "$MAX_SIZE" -le 1000 ] && DISABLED1000=disabled


	if [ $DEBUG -eq 1 ]; then
		echo '<!-- Start of debug info -->'
		echo '<p class="debug">[ DEBUG ] $DISABLED100: '"$DISABLED100"'<br />'
		echo '<p class="debug">[ DEBUG ] $DISABLED200: '$DISABLED200'<br />'
		echo '<p class="debug">[ DEBUG ] $DISABLED300: '$DISABLED300'<br />'
		echo '<p class="debug">[ DEBUG ] $DISABLED500: '$DISABLED500'<br />'
		echo '<p class="debug">[ DEBUG ] $DISABLED1000: '$DISABLED1000'<br />'
		echo '                 [ DEBUG ] actual size: '$ACTUAL_SIZE'<br />'
		echo '                 [ DEBUG ] max size: '$MAX_SIZE'<br />'
		echo '<!-- End of debug info -->'
	fi
#----------------------------------------------------------------------------------------


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
if [ "$SUBMIT" = "Resize" ]; then
echo 'SIZE='$SD_SIZE > /home/tc/partition_size.cfg


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
	echo '                <p>New mmcblk0p2 partition size will be:  '$SD_SIZE' MB </p>'
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
	echo '                <td class="column210">'
	echo '                  <select class="large16" name="SD_SIZE">'
	echo '                    <option value="">Use the whole SD-card</option>'
	echo '                    <option value="100" '"$DISABLED100"'>Use 100 MB</option>'
	echo '                    <option value="200" '"$DISABLED200"'>Use 200 MB</option>'
	echo '                    <option value="300" '"$DISABLED300"'>Use 300 MB</option>'
	echo '                    <option value="500" '"$DISABLED500"'>Use 500 MB</option>'
	echo '                    <option value="1000" '"$DISABLED1000"'>Use 1000 MB</option>'
	echo '                  </select>'
	echo '                </td>'

		echo '                <td>'
		echo "                  <p>Chose a size from the list. You can choose a value between current size: <b>"$ACTUAL_SIZE" MB</b> and SD-card size: <b>"$MAX_SIZE" MB</b>.</p>"
		echo '                  <p>Auto resizing is an automatic process that will expand the mmcblk0p2 partition in 2 steps:</p>'
		echo '                  <ol>'
		echo '                    <li>fdisk, then auto reboot</li>'
		echo '                    <li>resize2fs, then auto reboot</li>'
		echo '                  </ol>'
		echo '                </td>'
		echo '              </tr>'
		echo '              <tr class="warning">'
		echo '                <td>'
		echo '                  <p style="color:white">'
		echo '                    <input type="submit" name="SUBMIT" value="Resize" />&nbsp;&nbsp;Start auto resize partition now.'
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

case "$SUBMIT" in
	Resize)
		touch /home/tc/fdisk_required
		pcp_backup
		sudo reboot
	;;
esac

exit