#!/bin/sh

# Version: 7.0.0 2020-05-26

# Title: SD Backup and Restore
# Description: Copies first 2 partitions to image file

. pcp-functions

pcp_html_head "SD Backup" "GE"

pcp_navbar
pcp_httpd_query_string

FDISK="/bin/busybox fdisk"
SDVALID=0

COLUMN2_1="col-2"
COLUMN2_2="col-10"

COLUMN3_1="col-2"
COLUMN3_2="col-4"
COLUMN3_3="col-6"

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
	pcp_debug_variables "html" ACTION BOOTDEV DEVICE NUM_OF_PARTITIONS \
		P1_NAME P2_NAME P3_NAME SDVALID \
		PART2_END BLOCK_SIZE COUNT TIMESTAMP IMG MOUNTDIR
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

case "$ACTION" in
	Save)
		pcp_infobox_begin
		pcp_message INFO "Saving image location..." "text"
		pcp_message INFO "Location - $MOUNTDIR/image/" "text"
		pcp_infobox_end
	;;
	Create)
		pcp_infobox_begin
		TIMESTAMP=$(date +%Y%m%d%H%M%S)
		IMG="pCP$(pcp_picoreplayer_version)-${COUNT}-${TIMESTAMP}.img"
		pcp_message INFO "Creating image..." "text"
		pcp_message INFO "Process will take a few minutes." "text"
		pcp_message INFO "Image:  $IMG" "text"
		pcp_message INFO "Location: $MOUNTDIR/image/" "text"
		dd if=/dev/mmcblk0 of=/${MOUNTDIR}/image/$IMG bs=1M count=$COUNT
		pcp_remove_query_string
		pcp_infobox_end
	;;
	Restore)
		pcp_infobox_begin
		pcp_message INFO "Restoring image..." "text"
		pcp_message WARN "Overwriting SD card..." "text"
		pcp_message INFO "Image: $IMG" "text"
		pcp_message INFO "Location: $MOUNTDIR/image/" "text"
		dd if=/${MOUNTDIR}/image/$IMG of=/dev/mmcblk0
		pcp_remove_query_string
		pcp_infobox_end
	;;
	*)
		pcp_infobox_begin
		pcp_message INFO "Initial..." "text"
		pcp_infobox_end
	;;
esac

#========================================================================================
# Image location - used for reading and writing images.
#----------------------------------------------------------------------------------------
pcp_border_begin
pcp_heading5 "Image location"
echo '  <form name="image_location" action="'$0'" method="get">'
#----------------------------------------------------------------------------------------
echo '    <div class="row mx-1">'
echo '      <div class="'$COLUMN3_1'">'
echo '        <p>Image location</p>'
echo '      </div>'
pcp_incr_id
echo '      <div class="'$COLUMN3_2'">'
echo '        <select class="custom-select custom-select-sm" name="MOUNTDIR">'

                ORIG_MOUNTDIR="$MOUNTDIR" 
                for DEST in mmcblk0p3 sda1 /tmp
                do
                    case $DEST in
                        mmc*|sd*) pcp_partition_test $DEST ;;
                        /tmp) MOUNTDIR=/tmp ;;
                    esac
                    if [ "$ORIG_MOUNTDIR" = "$MOUNTDIR" ]; then
                        SEL="selected"
                        CURRENT_MOUNTDIR="$MOUNTDIR"
                    else
                        SEL=""
                    fi
                    echo '          <option value="'$MOUNTDIR'" '$SEL'>'$MOUNTDIR'/image</option>'
                done

echo '        </select>'
echo '      </div>'
echo '      <div class="'$COLUMN3_3'">'
echo '        <p>Destination&nbsp;&nbsp;'
pcp_helpbadge
echo '        </p>'
echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
echo '          <p>Valid locations</p>'
echo '          <ul>'
echo '            <li><b>/tmp</b> - ram</li>'
echo '            <li><b>/dev/mmcblk0p3</b> - SD card</li>'
echo '            <li><b>/dev/sda1</b> - USB stick</li>'
echo '          </ul>'
echo '        </div>'
echo '      </div>'
echo '    </div>'
#--------------------------------------Buttons-------------------------------------------
echo '    <div class="row mx-1 mb-2">'
echo '      <div class="'$COLUMN2_1'">'
echo '        <input class="'$BUTTON'" type="submit" name="ACTION" value="Save">'
echo '      </div>'
echo '    </div>'
#----------------------------------------------------------------------------------------
echo '  </form>'
pcp_border_end
#----------------------------------------------------------------------------------------

#========================================================================================
# Destination
#----------------------------------------------------------------------------------------
pcp_border_begin
pcp_heading5 "SD Card backup"
echo '  <form name="sd_backup" action="'$0'" method="get">'
#----------------------------------------------------------------------------------------
echo '    <div class="row mx-1">'
echo '      <div class="'$COLUMN2_1'">'
echo '        <p>Destination</p>'
echo '      </div>'
pcp_incr_id
echo '      <div class="'$COLUMN2_2'">'
echo '        <p>Destination&nbsp;&nbsp;'
pcp_helpbadge
echo '        </p>'
echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
echo '          <p>/tmp</p>'
echo '          <p>/dev/mmcblk0p3</p>'
echo '          <p>/dev/sda1</p>'
echo '        </div>'
echo '      </div>'
echo '    </div>'
#--------------------------------------Buttons-------------------------------------------
echo '    <div class="row mx-1 mb-2">'
echo '      <div class="'$COLUMN2_1'">'
echo '        <input class="'$BUTTON'" type="submit" name="ACTION" value="Create">'
echo '        <input type="hidden" name="MOUNTDIR" value="'$CURRENT_MOUNTDIR'">'
echo '      </div>'
echo '    </div>'
#----------------------------------------------------------------------------------------
echo '  </form>'
pcp_border_end
#----------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------
pcp_border_begin
pcp_heading5 "EXPERIMENTAL - SD Card restore"
echo '  <form name="sd_restore" action="'$0'" method="get">'
#----------------------------------------------------------------------------------------
echo '    <div class="row mx-1">'
echo '      <div class="'$COLUMN3_1'">'
echo '        <p>Restore</p>'
echo '      </div>'
pcp_incr_id
echo '      <div class="'$COLUMN3_2'">'
echo '        <select class="custom-select custom-select-sm" name="IMG">'

                IMAGES=$(ls ${CURRENT_MOUNTDIR}/image)
                for FILE in $IMAGES
                do
                    echo '                    <option value="'$FILE'" '$SEL'>'$FILE'</option>'
                done

echo '        </select>'
echo '      </div>'
echo '      <div class="'$COLUMN3_3'">'
echo '        <p>Source&nbsp;&nbsp;'
pcp_helpbadge
echo '        </p>'
echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
echo '          <p>/tmp</p>'
echo '          <p>/dev/mmcblk0p3</p>'
echo '          <p>/dev/sda1</p>'
echo '        </div>'
echo '      </div>'
echo '    </div>'
#--------------------------------------Buttons-------------------------------------------
echo '    <div class="row mx-1 mb-2">'
echo '      <div class="'$COLUMN2_1'">'
echo '        <input class="'$BUTTON'" type="submit" name="ACTION" value="Restore">'
echo '        <input type="hidden" name="MOUNTDIR" value="'$CURRENT_MOUNTDIR'">'
echo '      </div>'
echo '      <div class="'$COLUMN2_2'">'
echo '        <p>DESTROY your SD card</p>'
echo '      </div>'
echo '    </div>'
#----------------------------------------------------------------------------------------
echo '  </form>'
pcp_border_end
#----------------------------------------------------------------------------------------

#========================================================================================
# Partition information
#----------------------------------------------------------------------------------------
pcp_partition_info() {
	pcp_heading5 "Current mounted partition information" hr
	pcp_textarea "none" "df -h | grep -E \"Filesystem|mnt\" | tee -a $LOG" 4
	pcp_textarea "none" "$FDISK -ul | tee -a $LOG" 11
}
[ $DEBUG -eq 1 ] && pcp_partition_info
#----------------------------------------------------------------------------------------

pcp_html_end
exit