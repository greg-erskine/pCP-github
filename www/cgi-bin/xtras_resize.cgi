#!/bin/sh

# Version: 4.0.1 2018-10-22

. pcp-functions

pcp_html_head "xtras_resize" "GE"

pcp_banner
pcp_navigation
pcp_running_script
pcp_httpd_query_string

pcp_convert_to_sd_size() {
	LEN=$((${#1} - 9))
	echo $((${1:0:$LEN} + 1))
}

pcp_convert_to_mbytes() {
	echo $(($1 / 1024 / 1024))
}

FDISK="/bin/busybox fdisk"

#========================================================================================
# Logic determining actual size, maximum possible size
#----------------------------------------------------------------------------------------
P1_ACTUAL_SIZE_BYTES=$($FDISK -l $BOOTDEV | grep ${BOOTDEV}: | sed 's/*//' | awk '{ print $5 }')
P2_ACTUAL_SIZE_BYTES=$($FDISK -l $TCEDEV | grep ${TCEDEV}: | sed 's/*//' | awk '{ print $5 }')
case $BOOTDEV in
	*sd?*)
		SD_MAX_SIZE_BYTES=$($FDISK -l ${BOOTDEV%%?} | grep ${BOOTDEV%%?}: | sed 's/*//' | awk '{ print $5 }')
	;;
	*mmcblk*)
		SD_MAX_SIZE_BYTES=$($FDISK -l ${BOOTDEV%%??} | grep ${BOOTDEV%%??}: | sed 's/*//' | awk '{ print $5 }')
	;;
esac

SD_MAX_SIZE=$(pcp_convert_to_mbytes $SD_MAX_SIZE_BYTES)
SD_CARD_SIZE=$(pcp_convert_to_sd_size $SD_MAX_SIZE_BYTES)

P1_ACTUAL_SIZE=$(pcp_convert_to_mbytes $P1_ACTUAL_SIZE_BYTES)
P2_ACTUAL_SIZE=$(pcp_convert_to_mbytes $P2_ACTUAL_SIZE_BYTES)
P2_MAX_SIZE=$(($SD_MAX_SIZE - $P1_ACTUAL_SIZE))
AVAILABLE_SPACE=$(($SD_MAX_SIZE - ($P1_ACTUAL_SIZE + $P2_ACTUAL_SIZE)))

# Allow the correct values in dropdown list to be selectable
[ "$AVAILABLE_SPACE" -le 100 ] && DISABLED000=disabled
[ "$P2_ACTUAL_SIZE" -ge 95 ] || [ "$SD_MAX_SIZE" -le 100 ] && DISABLED100=disabled
[ "$P2_ACTUAL_SIZE" -ge 190 ] || [ "$SD_MAX_SIZE" -le 200 ] && DISABLED200=disabled
[ "$P2_ACTUAL_SIZE" -ge 285 ] || [ "$SD_MAX_SIZE" -le 300 ] && DISABLED300=disabled
[ "$P2_ACTUAL_SIZE" -ge 475 ] || [ "$SD_MAX_SIZE" -le 500 ] && DISABLED500=disabled
[ "$P2_ACTUAL_SIZE" -ge 950 ] || [ "$SD_MAX_SIZE" -le 1000 ] && DISABLED1000=disabled
[ "$P2_ACTUAL_SIZE" -ge 1900 ] || [ "$SD_MAX_SIZE" -le 2000 ] && DISABLED2000=disabled
#----------------------------------------------------------------------------------------

if [ $DEBUG -eq 1 ]; then
	echo '<!-- Start of debug info -->'
	pcp_debug_variables "html" DISABLED000 DISABLED100 DISABLED200 DISABLED300 DISABLED500 \
	DISABLED1000 DISABLED2000 P1_ACTUAL_SIZE_BYTES P1_ACTUAL_SIZE P2_ACTUAL_SIZE_BYTES \
	P2_ACTUAL_SIZE SD_MAX_SIZE_BYTES SD_MAX_SIZE P2_MAX_SIZE AVAILABLE_SPACE SD_CARD_SIZE
	echo '<!-- End of debug info -->'
fi

pcp_log_header $0

#========================================================================================
# Resize or waiting tables
#----------------------------------------------------------------------------------------
case "$SUBMIT" in
	Resize)
		echo "SIZE=$SD_SIZE" > /home/tc/partition_size.cfg
		[ "$SD_SIZE" = "" ] && NEW_SIZE=$P2_MAX_SIZE || NEW_SIZE=$SD_SIZE

		pcp_table_top "Resizing partition"
		echo '                <textarea class="inform" style="height:110px">'
		echo '[ INFO ] New '$TCEDEV' partition size will be: '$NEW_SIZE' MB'
		echo '[ INFO ] Resizing the partition is occuring, please wait...'
		echo '[ INFO ] This will take a couple of minutes and piCorePlayer will reboot a number of times.'
		echo '[ INFO ] The bigger the partition, the longer the process will take.'
		touch /home/tc/fdisk_required
		pcp_backup_nohtml
		echo '[ INFO ] Click Refresh or Reload after a few minutes.'
		(sleep 1; sudo reboot) &
		echo '                </textarea>'
		pcp_table_middle
		pcp_remove_query_string
		pcp_redirect_button "Go to Main Page" "main.cgi" 90
		pcp_table_end
	;;
	Reset)
		#================================================================================
		# For DEVELOPERS only - !!!BROKEN!!!
		# It is handy to be able to reset partition back to 50MB
		#--------------------------------------------------------------------------------
		SD_SIZE=200
		echo "SIZE=$SD_SIZE" > /home/tc/partition_size.cfg
		[ "$SD_SIZE" = "" ] && NEW_SIZE=$P2_MAX_SIZE || NEW_SIZE=$SD_SIZE

		pcp_table_top "Resetting partition"
		echo '                <textarea class="inform" style="height:110px">'
		echo '[ INFO ] New '$TCEDEV' partition size will be: '$NEW_SIZE' MB'
		echo '[ INFO ] Resetting the partition is occuring, please wait...'
		echo '[ INFO ] This will take a couple of minutes and piCorePlayer will reboot a number of times.'
		touch /home/tc/fdisk_required
		pcp_backup_nohtml
		echo '[ INFO ] Click Refresh or Reload after a few minutes.'
		(sleep 1; sudo reboot) &
		echo '                </textarea>'
		pcp_table_middle
		pcp_remove_query_string
		pcp_redirect_button "Go to Main Page" "main.cgi" 90
		pcp_table_end
	;;
	*)
		if [ -f /home/tc/www/cgi-bin/autoresize.sh ]; then
			pcp_start_row_shade
			pcp_incr_id
			echo '<table class="bggrey">'
			echo '  <tr>'
			echo '    <td>'
			echo '      <div class="row">'
			echo '        <fieldset>'
			echo '        <legend>Resize partition</legend>'
			echo '          <form name="auto" action="'$0'" method="get">'
			echo '            <table class="bggrey percent100">'
			if [ "$AVAILABLE_SPACE" -gt 100 ]; then
				echo '              <tr class="'$ROWSHADE'">'
				echo '                <td class="column210">'
				echo '                  <select class="large16" name="SD_SIZE">'
				echo '                    <option value="100" '"$DISABLED100"'>100 MB</option>'
				echo '                    <option value="200" '"$DISABLED200"'>200 MB</option>'
				echo '                    <option value="300" '"$DISABLED300"'>300 MB</option>'
				echo '                    <option value="500" '"$DISABLED500"'>500 MB</option>'
				echo '                    <option value="1000" '"$DISABLED1000"'>1000 MB</option>'
				echo '                    <option value="2000" '"$DISABLED2000"'>2000 MB</option>'
				echo '                    <option value="" '"$DISABLED000"'>Whole SD card</option>'
				echo '                  </select>'
				echo '                </td>'
				echo '                <td>'
				echo '                  <p>Select new partition size (currently '$P2_ACTUAL_SIZE' MB)&nbsp;&nbsp;'
				echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
				echo '                  </p>'
				echo '                  <div id="'$ID'" class="less">'
				echo '                    <p>You should only need to increase the size of the partition if you are adding'
				echo '                       extra extensions such as Jivelite or LMS.</p>'
				echo '                    <p>The resizing a partition process is done in 2 steps:</p>'
				echo '                    <ol>'
				echo '                      <li>fdisk and reboot</li>'
				echo '                      <li>resize2fs and reboot</li>'
				echo '                    </ol>'
				echo '                  </div>'
				echo '                </td>'
				echo '              </tr>'
			fi
			echo '              <tr class="warning">'
			echo '                <td colspan="2">'
			if [ "$AVAILABLE_SPACE" -gt 100 ]; then
				echo '                  <p style="color:white">'
				echo '                    <input type="submit" name="SUBMIT" value="Resize">&nbsp;&nbsp;Click [Resize] to start the resize partition process.'
				echo '                  </p>'
			else
				echo '                  <p style="color:white"><b>WARNING:</b> Partition is fully expanded (only '$AVAILABLE_SPACE' MB left).</p>'
			fi
			if [ $MODE -ge $MODE_DEVELOPER ]; then
				echo '                  <p style="color:white">'
				echo '                    <input type="submit" name="SUBMIT" value="Reset">&nbsp;&nbsp;!!!BROKEN!!! - Click [Reset] to resize partition to 50MB.'
				echo '                  </p>'
			fi
			echo '                </td>'
			echo '              </tr>'
			echo '            </table>'
			echo '          </form>'
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
			echo '            <legend>Current partition information</legend>'
			echo '            <table class="bggrey percent100">'
			echo '              <tr class="'$ROWSHADE'">'
			echo '                <td>'
			                        pcp_textarea_inform "none" "df -h ${TCEMNT} | tee -a $LOG" 40
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
			                        pcp_textarea_inform "none" "fdisk -ul | tee -a $LOG" 110
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
	;;
esac

pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'