#!/bin/sh

# Version: 5.1.0 2019-06-17

# Title: SD Backup and Restore
# Description: Copies first 2 partitions to image file

. pcp-functions

pcp_html_head "SD Backup" "GE"

pcp_banner
[ $DEBUG -eq 1 ] && pcp_table_top "Debug"
pcp_running_script
pcp_httpd_query_string

FDISK="/bin/busybox fdisk"
SDVALID=0

#========================================================================================
# Routines
#----------------------------------------------------------------------------------------
pcp_tmp_test() {
	free -m
	free -m | grep Mem: | awk '{print $7}'
}

pcp_partition_test() {
	PARTITION=$1

	if mount | grep /dev/$PARTITION >/dev/null 2>&1; then
		MOUNTDIR=$(cat /etc/mtab | grep $PARTITION | awk '{print $2}')
		return 0
	else
		return 1
	fi
}

pcp_bebug_info() {
	echo '<!-- Start of debug info -->'
	pcp_debug_variables "html" ACTION BOOTDEV DEVICE NUM_OF_PARTITIONS \
		P1_NAME P2_NAME P3_NAME SDVALID \
		PART2_END BLOCK_SIZE COUNT TIMESTAMP IMG MOUNTDIR
	[ $DEBUG -eq 1 ] && pcp_table_end
	echo '<!-- End of debug info -->'
}

#========================================================================================
# Calculations
#----------------------------------------------------------------------------------------
case $BOOTDEV in
	*sd?*) DEVICE=${BOOTDEV%%?} ;;
	*mmcblk*) DEVICE=${BOOTDEV%%??} ;;
esac

NUM_OF_PARTITIONS=$($FDISK -l $DEVICE | tail -n 1 | sed 's/  */ /g' | cut -d' ' -f 1 | awk '$0=$NF' FS=)
[ $NUM_OF_PARTITIONS -ne 3 ] && SDVALID=$((SDVALID + 1))
P1_NAME=$(tune2fs -l /dev/mmcblk0p1 2>/dev/null | tail -1 | grep PCP | awk -F"labelled '" '{print $2}' | sed "s/'//" )
[ "$P1_NAME" != "PCP_BOOT" ] && SDVALID=$((SDVALID + 1))
P2_NAME=$(tune2fs -l /dev/mmcblk0p2 | grep "volume name" | awk -F":   " '{print $2}')
[ "$P2_NAME" = "<none>" ] && P2_NAME="&lt;none&gt;"
[ "$P2_NAME" != "PCP_ROOT" ] && SDVALID=$((SDVALID + 1))
P3_NAME=$(tune2fs -l /dev/mmcblk0p3 | grep "volume name" | awk -F":   " '{print $2}')
[ "$P3_NAME" != "PCP_DATA" ] && SDVALID=$((SDVALID + 1))

PART2_END=$(fdisk -l $DEVICE | grep mmcblk0p2 | sed 's/  */ /g' | cut -d' ' -f 5)
BLOCK_SIZE=$(fdisk -l $DEVICE | grep ^Units: | cut -d' ' -f 6)
COUNT=$((PART2_END * BLOCK_SIZE / 1024 / 1024))

pcp_bebug_info

pcp_table_top "Action"
case "$ACTION" in
	Save)
		pcp_message INFO "Saving image location..." html
		pcp_message INFO "Location - $MOUNTDIR/image/" html
	;;
	Create)
		TIMESTAMP=$(date +%Y%m%d%H%M%S)
		IMG="pCP$(pcp_picoreplayer_version)-${COUNT}-${TIMESTAMP}.img"
		pcp_message INFO "Creating image..." html
		pcp_message INFO "Image - $IMG" html
		pcp_message INFO "Location - $MOUNTDIR/image/" html
		dd if=/dev/mmcblk0 of=/${MOUNTDIR}/image/$IMG bs=1M count=$COUNT
		pcp_remove_query_string
	;;
	Restore)
		pcp_message INFO "Restoring image..." html
		pcp_message WARN "Overwriting SD card..." html
		pcp_message INFO "Image - $IMG" html
		pcp_message INFO "Location - $MOUNTDIR/image/" html
		dd if=/${MOUNTDIR}/image/$IMG of=/dev/mmcblk0
		pcp_remove_query_string
	;;
	*)
		pcp_message INFO "Initial..." html
	;;
esac
pcp_table_end

#========================================================================================
# Image location table
#----------------------------------------------------------------------------------------
COL1="column150"
COL2="column250"
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <form name="image_location" action="'$0'" method="get">'
echo '        <div class="row">'
echo '          <fieldset>'
echo '            <legend>Image location</legend>'
echo '            <table class="bggrey percent100">'
#----------------------------------------------------------------------------------------
pcp_incr_id
pcp_start_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="'$COL1'">'
echo '                  <p>Image location</p>'
echo '                </td>'
echo '                <td class="'$COL2'">'
echo '                  <select class="large16" name="MOUNTDIR">'

                          ORIG_MOUNTDIR=$MOUNTDIR 
                          for DEST in mmcblk0p3 sda1 /tmp
                          do
                              case $DEST in
                                  mmc*|sd*) pcp_partition_test $DEST ;;
                                  /tmp) MOUNTDIR=/tmp ;;
                              esac
                              if [ $ORIG_MOUNTDIR = $MOUNTDIR ]; then
                                  SEL="Selected"
                                  CURRENT_MOUNTDIR=$MOUNTDIR
                              else
                                  SEL=""
                              fi
                              echo '                    <option value="'$MOUNTDIR'" '$SEL'>'$MOUNTDIR'/image</option>'
                          done

echo '                  </select>'
echo '                </td>'
echo '                <td>'
echo '                  <p>Destination&nbsp;&nbsp;'
echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                  </p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <p>/tmp</p>'
echo '                    <p>/dev/mmcblk0p3</p>'
echo '                    <p>/dev/sda1</p>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'
#--------------------------------------Buttons-------------------------------------------
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td colspan="3">'
echo '                  <input type="submit" name="ACTION" value="Save">'
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

#========================================================================================
# SD card backup table
#----------------------------------------------------------------------------------------
#COL1="column100"
#COL2="column210"
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <form name="sd_backup" action="'$0'" method="get">'
echo '        <div class="row">'
echo '          <fieldset>'
echo '            <legend>SD Card backup</legend>'
echo '            <table class="bggrey percent100">'
#----------------------------------------------------------------------------------------
pcp_incr_id
pcp_start_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="'$COL1'">'
echo '                  <p>Destination</p>'
echo '                </td>'
echo '                <td class="'$COL2'">'

echo '                </td>'
echo '                <td>'
echo '                  <p>Destination&nbsp;&nbsp;'
echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                  </p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <p>/tmp</p>'
echo '                    <p>/dev/mmcblk0p3</p>'
echo '                    <p>/dev/sda1</p>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'
#--------------------------------------Buttons-------------------------------------------
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td colspan="3">'
echo '                  <input type="submit" name="ACTION" value="Create">&nbsp;&nbsp;'$IMG
echo '                  <input type="hidden" name="MOUNTDIR" value="'$CURRENT_MOUNTDIR'">'
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

#========================================================================================
# SD card restore table
#----------------------------------------------------------------------------------------
#COL1="column100"
#COL2="column210"
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <form name="sd_restore" action="'$0'" method="get">'
echo '        <div class="row">'
echo '          <fieldset>'
echo '            <legend>SD Card restore</legend>'
echo '            <table class="bggrey percent100">'
#----------------------------------------------------------------------------------------
pcp_incr_id
pcp_start_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="'$COL1'">'
echo '                  <p>Restore</p>'
echo '                </td>'
echo '                <td class="'$COL2'">'
echo '                  <select class="large25" name="IMG">'

                          IMAGES=$(ls ${CURRENT_MOUNTDIR}/image)
                          for FILE in $IMAGES
                          do
                              echo '                    <option value="'$FILE'" '$SEL'>'$FILE'</option>'
                          done

echo '                  </select>'
echo '                </td>'
echo '                <td>'
echo '                  <p>Source&nbsp;&nbsp;'
echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                  </p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <p>/tmp</p>'
echo '                    <p>/dev/mmcblk0p3</p>'
echo '                    <p>/dev/sda1</p>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'
#--------------------------------------Buttons-------------------------------------------
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td colspan="3">'
echo '                  <input type="submit" name="ACTION" value="Restore">'
echo '                  <input type="hidden" name="MOUNTDIR" value="'$CURRENT_MOUNTDIR'">'
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

#========================================================================================
# Partition information
#----------------------------------------------------------------------------------------
pcp_partition_info() {
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
}
[ $DEBUG -eq 1 ] && pcp_partition_info
#----------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------
pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'
exit