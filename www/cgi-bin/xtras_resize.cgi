#!/bin/sh

# Version: 5.1.0 2019-06-05

. pcp-functions

pcp_html_head "xtras_resize" "GE"

pcp_banner
pcp_navigation

[ $DEBUG -eq 1 ] && pcp_table_top "Debug"
pcp_running_script
pcp_httpd_query_string

FDISK="/bin/busybox fdisk"
SDVALID=0
unset REBOOT_REQUIRED

#========================================================================================
# Local functions
#----------------------------------------------------------------------------------------
pcp_convert_to_sd_size() {
	LEN=$((${#1} - 9))
	echo $((${1:0:$LEN} + 1))
}

pcp_convert_to_mb() {
	echo $(($1 / 1024 / 1024))
}

#========================================================================================
# Logic determining actual size, maximum possible size
#----------------------------------------------------------------------------------------
P1_ACTUAL_SIZE_BYTES=$($FDISK -l $BOOTDEV | grep ${BOOTDEV}: | sed 's/*//' | awk '{ print $5 }')
P2_ACTUAL_SIZE_BYTES=$($FDISK -l $TCEDEV | grep ${TCEDEV}: | sed 's/*//' | awk '{ print $5 }')

case $BOOTDEV in
	*sd?*) DEVICE=${BOOTDEV%%?} ;;
	*mmcblk*) DEVICE=${BOOTDEV%%??} ;;
esac

SD_MAX_SIZE_BYTES=$($FDISK -l ${DEVICE} | grep ${DEVICE}: | sed 's/*//' | awk '{ print $5 }')
SD_MAX_SIZE_MB=$(pcp_convert_to_mb $SD_MAX_SIZE_BYTES)
SD_CARD_SIZE_GB=$(pcp_convert_to_sd_size $SD_MAX_SIZE_BYTES)

P1_ACTUAL_SIZE_MB=$(pcp_convert_to_mb $P1_ACTUAL_SIZE_BYTES)
P2_ACTUAL_SIZE_MB=$(pcp_convert_to_mb $P2_ACTUAL_SIZE_BYTES)
P2_MAX_SIZE_MB=$(($SD_MAX_SIZE_MB - $P1_ACTUAL_SIZE_MB))
AVAILABLE_SPACE_MB=$(($SD_MAX_SIZE_MB - ($P1_ACTUAL_SIZE_MB + $P2_ACTUAL_SIZE_MB)))

NUM_OF_PARTITIONS=$($FDISK -l $DEVICE | tail -n 1 | sed 's/  */ /g' | cut -d' ' -f 1 | awk '$0=$NF' FS=)
[ $NUM_OF_PARTITIONS -ne 2 ] && SDVALID=$(($SDVALID + 1))

P1_NAME=$(tune2fs -l /dev/mmcblk0p1 2>/dev/null | tail -1 | grep PCP | awk -F"labelled '" '{print $2}' | sed "s/'//" )
[ "$P1_NAME" != "PCP_BOOT" ] && SDVALID=$(($SDVALID + 1))
P2_NAME=$(tune2fs -l /dev/mmcblk0p2 | grep "volume name" | awk -F":   " '{print $2}')
[ "$P2_NAME" != "PCP_ROOT" ] && SDVALID=$(($SDVALID + 1))
P3_NAME=$(tune2fs -l /dev/mmcblk0p3 | grep "volume name" | awk -F":   " '{print $2}')
[ "$P3_NAME" != "PCP_DATA" } || [ "$P3_NAME" != "" ] && SDVALID=$(($SDVALID + 1))

# Allow the correct values in drop-down list to be selectable
[ $AVAILABLE_SPACE_MB -le 100 ] && DISABLED000="disabled"
[ $P2_ACTUAL_SIZE_MB -ge 95 ] || [ $SD_MAX_SIZE_MB -le 100 ] && DISABLED100="disabled"
[ $P2_ACTUAL_SIZE_MB -ge 190 ] || [ $SD_MAX_SIZE_MB -le 200 ] && DISABLED200="disabled"
[ $P2_ACTUAL_SIZE_MB -ge 285 ] || [ $SD_MAX_SIZE_MB -le 300 ] && DISABLED300="disabled"
[ $P2_ACTUAL_SIZE_MB -ge 475 ] || [ $SD_MAX_SIZE_MB -le 500 ] && DISABLED500="disabled"
[ $P2_ACTUAL_SIZE_MB -ge 950 ] || [ $SD_MAX_SIZE_MB -le 1000 ] && DISABLED1000="disabled"
[ $P2_ACTUAL_SIZE_MB -ge 1900 ] || [ $SD_MAX_SIZE_MB -le 2000 ] && DISABLED2000="disabled"
#----------------------------------------------------------------------------------------

if [ $DEBUG -eq 1 ]; then
	echo '<!-- Start of debug info -->'
#	pcp_table_top "Debug"
	pcp_debug_variables "html" DISABLED000 DISABLED100 DISABLED200 DISABLED300 \
		DISABLED500 DISABLED1000 DISABLED2000 \
		SD_MAX_SIZE_BYTES SD_MAX_SIZE_MB SD_CARD_SIZE_GB NUM_OF_PARTITIONS \
		P1_ACTUAL_SIZE_BYTES P1_ACTUAL_SIZE_MB \
		P2_ACTUAL_SIZE_BYTES P2_ACTUAL_SIZE_MB P2_MAX_SIZE_MB AVAILABLE_SPACE_MB \
		P1_NAME P2_NAME P3_NAME SDVALID
	pcp_table_end
	echo '<!-- End of debug info -->'
fi

pcp_log_header $0

#========================================================================================
# Resize partition 2 / add partition 3 tables
#----------------------------------------------------------------------------------------
case "$SUBMIT" in
	Resize)
		#================================================================================
		# Resize partition 2 - PCP_ROOT
		#--------------------------------------------------------------------------------
		echo "SIZE=$SD_SIZE" > /home/tc/fdisk_part2_required
		[ x"$SD_SIZE" = x"" ] && NEW_SIZE=$P2_MAX_SIZE_MB || NEW_SIZE=$SD_SIZE

		pcp_table_top "Resizing partition 2 - PCP_ROOT"
		echo '                <textarea class="inform" style="height:110px">'
		echo '[ INFO ] New '$TCEDEV' partition 2 size will be: '$NEW_SIZE' MB'
		echo '[ INFO ] Resizing the partition is occuring, please wait...'
		echo '[ INFO ] This will take a couple of minutes and piCorePlayer will reboot a number of times.'
		echo '[ INFO ] The bigger the partition, the longer the process will take.'
		pcp_backup_nohtml
		echo '[ INFO ] Click [Go to Main Page] or [Refresh] after a few minutes.'
		(sleep 1; sudo reboot) &
		echo '                </textarea>'
		pcp_table_middle
		pcp_remove_query_string
		pcp_redirect_button "Go to Main Page" "main.cgi" 90
		pcp_table_end
	;;
	Add)
		#================================================================================
		# Add partition 3 - PC_DATA
		#--------------------------------------------------------------------------------
		pcp_table_top "Adding partition 3  - PCP_DATA"
		echo '                <textarea class="inform" style="height:110px">'
		echo '[ INFO ] Adding partition 3 is occuring, please wait...'
		echo '[ INFO ] This will take a couple of minutes and piCorePlayer will reboot a number of times.'
		touch /home/tc/fdisk_part3_required
		pcp_backup_nohtml
		echo '[ INFO ] Click [Go to Main Page] or [Refresh] after a few minutes.'
		(sleep 1; sudo reboot) &
		echo '                </textarea>'
		pcp_table_middle
		pcp_remove_query_string
		pcp_redirect_button "Go to Main Page" "main.cgi" 90
		pcp_table_end
	;;
	*)
		#================================================================================
		# Main table
		#--------------------------------------------------------------------------------
		pcp_start_row_shade
		pcp_incr_id
		echo '<table class="bggrey">'
		echo '  <tr>'
		echo '    <td>'
		echo '      <div class="row">'
		echo '        <fieldset>'
		echo '        <legend>Resize partition 2 (PCP_ROOT)</legend>'
		echo '          <form name="auto" action="'$0'" method="get">'
		echo '            <table class="bggrey percent100">'
		#========================================================================================
		# Resize partition 2 - PCP_ROOT
		#----------------------------------------------------------------------------------------
		if [ $SDVALID -eq 0 ]; then
			if [ $AVAILABLE_SPACE_MB -gt 100 ]; then
				echo '              <tr class="'$ROWSHADE'">'
				echo '                <td class="column210">'
				echo '                  <select class="large16" name="SD_SIZE">'
				echo '                    <option value="100" '"$DISABLED100"'>100 MB</option>'
				echo '                    <option value="200" '"$DISABLED200"'>200 MB</option>'
				echo '                    <option value="300" '"$DISABLED300"'>300 MB</option>'
				echo '                    <option value="500" '"$DISABLED500"'>500 MB</option>'
				echo '                    <option value="1000" '"$DISABLED1000"'>1000 MB</option>'
				echo '                    <option value="2000" '"$DISABLED2000"'>2000 MB</option>'
				echo '                    <option value="'$(($P2_MAX_SIZE_MB-100))'" '"$DISABLED000"'>Whole SD card</option>'
				echo '                  </select>'
				echo '                </td>'
				echo '                <td>'
				echo '                  <p>Select new partition size (currently '$P2_ACTUAL_SIZE_MB' MB)&nbsp;&nbsp;'
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
			if [ $AVAILABLE_SPACE_MB -gt 100 ]; then
				echo '                  <p style="color:white">'
				echo '                    <input type="submit" name="SUBMIT" value="Resize">&nbsp;&nbsp;Click [Resize] to start the resize partition process.'
				echo '                  </p>'
			else
				echo '                  <p style="color:white"><b>WARNING:</b> Partition can not be expanded (only '$AVAILABLE_SPACE_MB' MB left).</p>'
			fi
			echo '                </td>'
			echo '              </tr>'
		else
			echo '              <tr  class="warning">'
			echo '                <td colspan="2">'
			echo '                  <p style="color:white"><b>WARNING:</b> The resize partition 2 option has been disabled to prevent damage to your SD card.</p>'
			echo '                  <p style="color:white">You may have:</p>'
			echo '                  <ul>'
			echo '                    <li style="color:white">more than 2 partitions, or</li>'
			echo '                    <li style="color:white">non-standard partition names.</li>'
			echo '                  </ul>'
			echo '                </td>'
			echo '              </tr>'
		fi
		#----------------------------------------------------------------------------------------
		echo '            </table>'
		echo '          </form>'
		echo '        </fieldset>'
		echo '      </div>'
		echo '    </td>'
		echo '  </tr>'
		echo '</table>'

		#========================================================================================
		# Add partition 3 - PCP_DATA - BETA
		#----------------------------------------------------------------------------------------
		if [ $MODE -ge $MODE_BETA ]; then
			pcp_start_row_shade
			pcp_incr_id
			echo '<table class="bggrey">'
			echo '  <tr>'
			echo '    <td>'
			echo '      <div class="row">'
			echo '        <fieldset>'
			echo '        <legend>Add partition 3 (PCP_DATA)</legend>'
			echo '          <form name="add" action="'$0'" method="get">'
			echo '            <table class="bggrey percent100">'
			echo '              <tr class="'$ROWSHADE'">'
			echo '                <td>'
			echo '                  <p>It is NOT recommended adding partition 3 to your SD card&nbsp;&nbsp;'
			echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
			echo '                  </p>'
			echo '                  <div id="'$ID'" class="less">'
			echo '                    <ul>'
			echo '                      <li>This operation will add an ext4 formatted partition 3, starting at the end of partition 2 and filling up the rest of the SD card.</li>'
			echo '                      <li>It is more reliable to store your data on a USB stick or HDD.</li>'
			echo '                      <li>Once partition 3 is added, it will be very difficult to increase the size of partition 2.</li>'
			echo '                      <li>Use [LMS] > "Pick from the following detected USB disks to mount" to mount partition.</li>'
			echo '                    </ul>'
			echo '                  </div>'
			echo '                </td>'
			echo '              </tr>'
			echo '              <tr class="'$ROWSHADE'">'
			echo '                <td class="warning">'
			if [ $AVAILABLE_SPACE_MB -lt 1000 ]; then
				ADD_ERROR=TRUE
				ADD_ERROR_MSG="Partition 3 can not be added insufficient free space (only $AVAILABLE_SPACE_MB MB left)."
			fi
			if [ $NUM_OF_PARTITIONS -gt 2 ]; then
				ADD_ERROR=TRUE
				ADD_ERROR_MSG="Partition 3 ($P3_NAME) already exists."
			fi
			if ! [ $ADD_ERROR ]; then
				echo '                  <p style="color:white">'
				echo '                    <input type="submit" name="SUBMIT" value="Add">&nbsp;&nbsp;Click [Add] to add partition 3.'
				echo '                  </p>'
			else
				echo '                  <p style="color:white"><b>WARNING:</b> '$ADD_ERROR_MSG'</p>'
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
		fi

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
		echo '            <legend>Current mounted partition information</legend>'
		echo '            <table class="bggrey percent100">'
		echo '              <tr class="'$ROWSHADE'">'
		echo '                <td>'
		                        pcp_textarea_inform "none" "df -h | grep -E \"Filesystem|mnt\" | tee -a $LOG" 40
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
		                        pcp_textarea_inform "none" "$FDISK -ul | tee -a $LOG" 110
		echo '                </td>'
		echo '              </tr>'
		echo '            </table>'
		echo '          </fieldset>'
		echo '        </div>'
		echo '      </form>'
		echo '    </td>'
		echo '  </tr>'
		echo '</table>'
	;;
esac
#----------------------------------------------------------------------------------------

#========================================================================================
# Debug information
#----------------------------------------------------------------------------------------
if [ $DEBUG -eq 1 ]; then
	pcp_table_top "/opt/bootsync.sh"
	echo '<!-- Start of debug info -->'
	pcp_textarea_inform "none" "cat /opt/bootsync.sh" "150"
	echo '<!-- End of debug info -->'
	pcp_table_end

	pcp_table_top "${TCEMNT}/tce/pcp_resize.log"
	echo '<!-- Start of debug info -->'
	pcp_textarea_inform "none" "cat ${TCEMNT}/tce/pcp_resize.log" "250"
	echo '<!-- End of debug info -->'
	pcp_table_end
fi
#----------------------------------------------------------------------------------------

pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'