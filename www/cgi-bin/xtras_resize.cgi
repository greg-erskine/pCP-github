#!/bin/sh

# Version: 3.03 2016-10-04
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

#DEBUG=1

#========================================================================================
# Logic determining actual size, maximum possible size
#----------------------------------------------------------------------------------------
P1_ACTUAL_SIZE=$(fdisk -l /dev/mmcblk0p1 | grep dev/mmcblk0p1: | awk '{ print $3 }')
P2_ACTUAL_SIZE=$(fdisk -l /dev/mmcblk0p2 | grep dev/mmcblk0p2: | awk '{ print $3 }')
SD_MAX_SIZE=$(fdisk -l /dev/mmcblk0 | grep /dev/mmcblk0: | awk '{ print $3 }')

AVAILABLE_SPACE=$(($SD_MAX_SIZE - ($P1_ACTUAL_SIZE + $P2_ACTUAL_SIZE)))

# Allow the correct values in dropdown list to be selectable
[ "$AVAILABLE_SPACE" -le 100 ] && DISABLED000=disabled
[ "$P2_ACTUAL_SIZE" -ge 100 ] || [ "$SD_MAX_SIZE" -le 100 ] && DISABLED100=disabled
[ "$P2_ACTUAL_SIZE" -ge 200 ] || [ "$SD_MAX_SIZE" -le 200 ] && DISABLED200=disabled
[ "$P2_ACTUAL_SIZE" -ge 300 ] || [ "$SD_MAX_SIZE" -le 300 ] && DISABLED300=disabled
[ "$P2_ACTUAL_SIZE" -ge 500 ] || [ "$SD_MAX_SIZE" -le 500 ] && DISABLED500=disabled
[ "$P2_ACTUAL_SIZE" -ge 1000 ] || [ "$SD_MAX_SIZE" -le 1000 ] && DISABLED1000=disabled
#----------------------------------------------------------------------------------------

if [ $DEBUG -eq 1 ]; then
	echo '<!-- Start of debug info -->'
	echo '<p class="debug">[ DEBUG ] $DISABLED000:    '$DISABLED000'<br />'
	echo '                 [ DEBUG ] $DISABLED100:    '$DISABLED200'<br />'
	echo '                 [ DEBUG ] $DISABLED200:    '$DISABLED200'<br />'
	echo '                 [ DEBUG ] $DISABLED300:    '$DISABLED300'<br />'
	echo '                 [ DEBUG ] $DISABLED500:    '$DISABLED500'<br />'
	echo '                 [ DEBUG ] $DISABLED1000:   '$DISABLED1000'<br />'
	echo '                 [ DEBUG ] P1 actual size:  '$P1_ACTUAL_SIZE'<br />'
	echo '                 [ DEBUG ] P2 actual size:  '$P2_ACTUAL_SIZE'<br />'
	echo '                 [ DEBUG ] SD max size:     '$SD_MAX_SIZE'<br />'
	echo '                 [ DEBUG ] Available space: '$AVAILABLE_SPACE'</p>'
	echo '<!-- End of debug info -->'
fi

#========================================================================================
# Resize or watiing tables
#----------------------------------------------------------------------------------------
if [ "$SUBMIT" = "Resize" ]; then
	echo "SIZE=$SD_SIZE" > /home/tc/partition_size.cfg
	[ "$SD_SIZE" = "" ] && NEW_SIZE=$SD_MAX_SIZE || NEW_SIZE=$SD_SIZE

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
	echo '                <textarea class="inform" style="height:110px">'
	                        echo '[ INFO ] New mmcblk0p2 partition size will be: '$NEW_SIZE' MB'
	                        echo '[ INFO ] Resizing the partition is occuring, please wait...'
	                        echo '[ INFO ] This will take a couple of minutes and piCorePlayer will reboot a number of times.'
	                        touch /home/tc/fdisk_required
	                        pcp_backup_nohtml
	                        echo '[ INFO ] Click Refresh or Reload after a few minutes.'
	                        (sleep 1; sudo reboot) &
	echo '                </textarea>'
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
		pcp_incr_id
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
		echo '                    <option value="" '"$DISABLED000"'>Use the whole SD card</option>'
		echo '                    <option value="100" '"$DISABLED100"'>Use 100 MB</option>'
		echo '                    <option value="200" '"$DISABLED200"'>Use 200 MB</option>'
		echo '                    <option value="300" '"$DISABLED300"'>Use 300 MB</option>'
		echo '                    <option value="500" '"$DISABLED500"'>Use 500 MB</option>'
		echo '                    <option value="1000" '"$DISABLED1000"'>Use 1000 MB</option>'
		echo '                  </select>'
		echo '                </td>'
		echo '                <td>'
		echo '                  <p>Choose a size between the current partition size: <b>'$P2_ACTUAL_SIZE' MB</b> and the SD card size: <b>'$SD_MAX_SIZE' MB</b>&nbsp;&nbsp;'
		echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
		echo '                  </p>'
		echo '                  <div id="'$ID'" class="less">'
		echo '                    <p>Auto resizing is an automatic process that will expand the mmcblk0p2 partition in 2 steps:</p>'
		echo '                    <ol>'
		echo '                      <li>fdisk, then auto reboot</li>'
		echo '                      <li>resize2fs, then auto reboot</li>'
		echo '                    </ol>'
		echo '                  </div>'
		echo '                </td>'
		echo '              </tr>'
		echo '              <tr class="warning">'
		echo '                <td>'
		if [ "$AVAILABLE_SPACE" -gt 100 ]; then
			echo '                  <p style="color:white">'
			echo '                    <input type="submit" name="SUBMIT" value="Resize" />&nbsp;&nbsp;Click to start the auto resize partition process.'
			echo '                  </p>'
		else
			echo '                  <p style="color:white">NOTE: Not enough space available for expansion (only '$AVAILABLE_SPACE' MB).</p>'
		fi
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
	fi
fi

pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'