#!/bin/sh

# Version: 7.0.0 2020-05-24

# Title: Resize partition 2
# Description: Resize partition 2 and/or add partition 3

. pcp-functions

pcp_html_head "xtras_resize" "GE"

pcp_navbar
pcp_httpd_query_string

FDISK="/bin/busybox fdisk"
SDVALID=0

COLUMN3_1="col-sm-2"
COLUMN3_2="col-sm-3"
COLUMN3_3="col-sm-7"
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
	*mmcblk*)
		DEVICE=${BOOTDEV%%??}
		ROOTDEV="${DEVICE}p2"
		DATADEV="${DEVICE}p3"
		PHYSDEV="SD Card"
	;;
	*sd?*)
		DEVICE="${BOOTDEV%%?}"
		ROOTDEV="${DEVICE}2"
		DATADEV="${DEVICE}3"
		PHYSDEV="USB Device"
	;;
esac

SD_MAX_SIZE_BYTES=$($FDISK -l ${DEVICE} | grep ${DEVICE}: | sed 's/*//' | awk '{ print $5 }')
SD_MAX_SIZE_MB=$(pcp_convert_to_mb $SD_MAX_SIZE_BYTES)
SD_CARD_SIZE_GB=$(pcp_convert_to_sd_size $SD_MAX_SIZE_BYTES)

P1_ACTUAL_SIZE_MB=$(pcp_convert_to_mb $P1_ACTUAL_SIZE_BYTES)
P2_ACTUAL_SIZE_MB=$(pcp_convert_to_mb $P2_ACTUAL_SIZE_BYTES)
P2_MAX_SIZE_MB=$(($SD_MAX_SIZE_MB - $P1_ACTUAL_SIZE_MB))
AVAILABLE_SPACE_MB=$(($SD_MAX_SIZE_MB - ($P1_ACTUAL_SIZE_MB + $P2_ACTUAL_SIZE_MB)))

NUM_OF_PARTITIONS=$($FDISK -l $DEVICE | tail -n 1 | sed 's/  */ /g' | cut -d' ' -f 1 | awk '$0=$NF' FS=)
[ $NUM_OF_PARTITIONS -ne 2 ] && SDVALID=$((SDVALID + 1))

P1_NAME=$(tune2fs -l $BOOTDEV 2>/dev/null | tail -1 | grep PCP | awk -F"labelled '" '{print $2}' | sed "s/'//" )
[ "$P1_NAME" != "PCP_BOOT" ] && SDVALID=$((SDVALID + 1))
P2_NAME=$(tune2fs -l $ROOTDEV | grep "volume name" | awk -F":   " '{print $2}')
[ "$P2_NAME" = "<none>" ] && P2_NAME="&lt;none&gt;"
[ "$P2_NAME" != "PCP_ROOT" ] && SDVALID=$((SDVALID + 1))
P3_NAME=$(tune2fs -l $DATADEV | grep "volume name" | awk -F":   " '{print $2}')
[ $NUM_OF_PARTITIONS -eq 3 ] && [ "$P3_NAME" != "PCP_DATA" ] || [ "$P3_NAME" != "" ] && SDVALID=$((SDVALID + 1))

[ $AVAILABLE_SPACE_MB -le 100 ] && DISABLED000="disabled"
[ $P2_ACTUAL_SIZE_MB -ge 95 ] || [ $SD_MAX_SIZE_MB -le 100 ] && DISABLED100="disabled"
[ $P2_ACTUAL_SIZE_MB -ge 190 ] || [ $SD_MAX_SIZE_MB -le 200 ] && DISABLED200="disabled"
[ $P2_ACTUAL_SIZE_MB -ge 285 ] || [ $SD_MAX_SIZE_MB -le 300 ] && DISABLED300="disabled"
[ $P2_ACTUAL_SIZE_MB -ge 475 ] || [ $SD_MAX_SIZE_MB -le 500 ] && DISABLED500="disabled"
[ $P2_ACTUAL_SIZE_MB -ge 950 ] || [ $SD_MAX_SIZE_MB -le 1000 ] && DISABLED1000="disabled"
[ $P2_ACTUAL_SIZE_MB -ge 1900 ] || [ $SD_MAX_SIZE_MB -le 2000 ] && DISABLED2000="disabled"
#----------------------------------------------------------------------------------------

pcp_debug_variables "html" DISABLED000 DISABLED100 DISABLED200 DISABLED300 \
	DISABLED500 DISABLED1000 DISABLED2000 \
	SD_MAX_SIZE_BYTES SD_MAX_SIZE_MB SD_CARD_SIZE_GB NUM_OF_PARTITIONS \
	P1_ACTUAL_SIZE_BYTES P1_ACTUAL_SIZE_MB \
	P2_ACTUAL_SIZE_BYTES P2_ACTUAL_SIZE_MB P2_MAX_SIZE_MB AVAILABLE_SPACE_MB \
	P1_NAME P2_NAME P3_NAME SDVALID \
	DEVICE BOOTDEV ROOTDEV DATADEV PHYSDEV

pcp_log_header $0

#========================================================================================
#----------------------------------------------------------------------------------------
case "$SUBMIT" in
	Resize)
		#================================================================================
		# Resize partition 2 - PCP_ROOT
		#--------------------------------------------------------------------------------
		echo "SIZE=$SD_SIZE" > /home/tc/fdisk_part2_required
		[ x"$SD_SIZE" = x"" ] && NEW_SIZE=$P2_MAX_SIZE_MB || NEW_SIZE=$SD_SIZE

		pcp_textarea_begin "" 10
		pcp_message INFO "New $TCEDEV partition 2 size will be: $NEW_SIZE MB" "text"
		pcp_message INFO "Resizing the partition is occurring, please wait..." "text"
		pcp_message INFO "This will take a couple of minutes and piCorePlayer will reboot a number of times." "text"
		pcp_message INFO "The bigger the partition, the longer the process will take." "text"
		pcp_backup text
		pcp_message INFO "Click [Go to Main Page] or [Refresh] after a few minutes." "text"
		(sleep 1; sudo reboot) &
		pcp_textarea_end
		pcp_remove_query_string
		pcp_redirect_button "Go to Main Page" "main.cgi" 90
	;;
	Add)
		#================================================================================
		# Add partition 3 - PC_DATA
		#--------------------------------------------------------------------------------
		pcp_textarea_begin "" 10
		pcp_message INFO "Adding $DATADEV partition 3 is occurring, please wait..." "text"
		pcp_message INFO "This will take a couple of minutes and piCorePlayer will reboot a number of times." "text"
		touch /home/tc/fdisk_part3_required
		pcp_backup text
		pcp_message INFO "Click [Go to Resize Page] or [Refresh] after a few minutes." "text"
		(sleep 1; sudo reboot) &
		pcp_textarea_end
		pcp_remove_query_string
		pcp_redirect_button "Go to Resize Page" "$0" 100
	;;
	Create)
		#================================================================================
		# Create default directories on partition 3
		#--------------------------------------------------------------------------------
		pcp_textarea_begin
		pcp_message INFO "Creating default directories on partition 3..." "text"

		DIR=$(cat /etc/mtab | grep "$DATADEV" | awk '{print $2}')

		for i in music image config
		do
			if [ -d /$DIR/$i ]; then
				echo $DIR'/'$i' exists.'
			else
				echo 'Creating '$DIR'/'$i'.'
				sudo mkdir /$DIR/$i
				sudo chown tc:staff /$DIR/$i
			fi
		done

		pcp_textarea_end
		pcp_remove_query_string
		pcp_redirect_button "Go to Resize Page" "$0" 10
	;;
	*)
		#================================================================================
		#--------------------------------------------------------------------------------
		pcp_incr_id

		echo '  <div class="'$BORDER'">'
		pcp_heading5 "Resize partition 2 ($P2_NAME)"
		echo '    <form name="auto" action="'$0'" method="get">'
		#================================================================================
		# Resize partition 2 - PCP_ROOT
		#--------------------------------------------------------------------------------
		if [ $SDVALID -eq 0 ]; then
			if [ $AVAILABLE_SPACE_MB -gt 100 ]; then
				echo '      <div class="row mx-1">'
				echo '        <div class="input-group col-2">'
				echo '          <select class="custom-select custom-select-sm" name="SD_SIZE">'
				echo '            <option value="100" '"$DISABLED100"'>100 MB</option>'
				echo '            <option value="200" '"$DISABLED200"'>200 MB</option>'
				echo '            <option value="300" '"$DISABLED300"'>300 MB</option>'
				echo '            <option value="500" '"$DISABLED500"'>500 MB</option>'
				echo '            <option value="1000" '"$DISABLED1000"'>1000 MB</option>'
				echo '            <option value="2000" '"$DISABLED2000"'>2000 MB</option>'
				echo '            <option value="'$(($P2_MAX_SIZE_MB-100))'" '"$DISABLED000"'>Whole '$PHYSDEV'</option>'
				echo '          </select>'
				echo '        </div>'
				echo '        <div class="col-10">'
				echo '          <p>Select new partition size (currently '$P2_ACTUAL_SIZE_MB' MB)&nbsp;&nbsp;'
				pcp_helpbadge
				echo '          </p>'
				echo '          <div id="dt'$ID'" class="'$COLLAPSE'">'
				echo '            <p>You should only need to increase the size of the partition if you are adding'
				echo '               extra extensions such as Jivelite or LMS.</p>'
				echo '            <p>The resizing a partition process is done in 2 steps:</p>'
				echo '            <ol>'
				echo '              <li>fdisk and reboot</li>'
				echo '              <li>resize2fs and reboot</li>'
				echo '            </ol>'
				echo '          </div>'
				echo '        </div>'
				echo '      </div>'
			fi
			#--------------------------------------------------------------------------------
			if [ $AVAILABLE_SPACE_MB -gt 100 ]; then
				echo '      <div class="row mx-1 mb-2">'
				echo '        <div class="col-2">'
				echo '          <input class="'$BUTTON'" type="submit" name="SUBMIT" value="Resize">'
				echo '        </div>'
				echo '        <div class="col-10">'
				echo '           Click [Resize] to start the resize partition process.'
				echo '        </div>'
				echo '      </div>'
			else
				echo '      <div class="row mx-1">'
				echo '        <div class="col-12">'
				echo '          <p><b>WARNING:</b> Partition can not be expanded (only '$AVAILABLE_SPACE_MB' MB left).</p>'
				echo '        </div>'
				echo '      </div>'
			fi
		else
			echo '      <div class="row mx-1">'
			echo '        <div class="col-10">'
			echo '          <p><b>WARNING:</b> The resize partition 2 option has been disabled to prevent damage to your '$PHYSDEV'.</p>'
			echo '          <p>You have:</p>'
			echo '          <ul>'
			                  [ $NUM_OF_PARTITIONS -ne 2 ] &&
			echo '            <li>more than 2 partitions</li>'
			                  [ "$P1_NAME" != "PCP_BOOT" ] &&
			echo '            <li>partition 1 labelled "'$P1_NAME'" should be labelled "PCP_ROOT".</li>'
			                  [ "$P2_NAME" != "PCP_ROOT" ] &&
			echo '            <li>partition 2 labelled "'$P2_NAME'" should be labelled "PCP_BOOT".</li>'
			echo '          </ul>'
			echo '        </div>'
			echo '      </div>'
		fi
		#--------------------------------------------------------------------------------
		echo '    </form>'
		echo '  </div>'

		#================================================================================
		# Add partition 3 - PCP_DATA - BETA
		#--------------------------------------------------------------------------------
		if [ $MODE -ge $MODE_BETA ]; then
			pcp_incr_id
			echo '  <div class="'$BORDER' mb-3">'
			pcp_heading5 "Add partition 3 (PCP_DATA)"
			echo '    <form name="add" action="'$0'" method="get">'
			#----------------------------------------------------------------------------
			echo '      <div class="row mx-1">'
			echo '        <div class="col-12">'
			echo '          <p>It is NOT recommended adding partition 3 to your '$PHYSDEV'&nbsp;&nbsp;'
			pcp_helpbadge
			echo '          </p>'
			echo '          <div id="dt'$ID'" class="'$COLLAPSE'">'
			echo '            <ul>'
			echo '              <li>This operation will add an ext4 formatted partition 3, starting at the end of partition 2 and filling up the rest of the '$PHYSDEV'.</li>'
			echo '              <li>It is more reliable to store your data on a separate USB stick or HDD.</li>'
			echo '              <li>Once partition 3 is added, it will be very difficult to increase the size of partition 2.</li>'
			echo '              <li>Use [LMS] > <a href="lms.cgi#partmount">"Pick from the following detected USB disks to mount"</a> to mount partition.</li>'
			echo '            </ul>'
			echo '          </div>'
			echo '        </div>'
			echo '      </div>'

			if [ $AVAILABLE_SPACE_MB -lt 1000 ]; then
				ADD_ERROR=TRUE
				ADD_ERROR_MSG="Partition 3 can not be added insufficient free space (only $AVAILABLE_SPACE_MB MB left)."
			fi
			if [ $NUM_OF_PARTITIONS -gt 2 ]; then
				ADD_ERROR=TRUE
				ADD_ERROR_MSG="Partition 3 ($P3_NAME) already exists."
			fi

			echo '      <div class="row mx-1">'
			if ! [ $ADD_ERROR ]; then
				echo '        <div class="col-2 mb-2">'
				echo '          <input class="'$BUTTON'" type="submit" name="SUBMIT" value="Add">'
				echo '        </div>'
				echo '        <div class="col-10">'
				echo '          Click [Add] to add partition 3.'
				echo '        </div>'
			else
				echo '        <div class="col-12">'
				echo '          <p><b>WARNING:</b> '$ADD_ERROR_MSG'</p>'
				echo '        </div>'
			fi
			echo '      </div>'
			echo '    </form>'
#			echo '  </div>'
		fi

		#================================================================================
		# Create default directories button if partition 3 mounted
		#--------------------------------------------------------------------------------
		if [ $MODE -ge $MODE_BETA ]; then
			if [ "$P3_NAME" = "PCP_DATA" ]; then
				echo '    <div class="row mx-1 mb-2">'
				if mount | grep "$DATADEV" >/dev/null 2>&1; then
					echo '      <div class="col-2 mb-2">'
					echo '        <form name="create" action="'$0'" method="get">'
					echo '          <input class="'$BUTTON'" type="submit" name="SUBMIT" value="Create">'
					echo '        </form>'
					echo '      </div>'
					echo '      <div class="col-10">'
					echo '        Click [Create] to create default directories on partition 3.'
					echo '      </div>'
				else
					echo '      <div class="col-12">'
					echo '        <p>'$MOUNTED'<b>WARNING:</b> Partition 3 not mounted.</p>'
					echo '        <p>Use [LMS] > <a href="lms.cgi#partmount">"Pick from the following detected USB disks to mount"</a> to mount partition.</p>'
					echo '      </div>'
				fi
				echo '    </div>'
			fi
			echo '  </div>'
		fi

		#================================================================================
		# Partition information
		#--------------------------------------------------------------------------------
		pcp_textarea "none" "df -h | grep -E \"Filesystem|mnt\" | tee -a $LOG" 4
		pcp_textarea "none" "$FDISK -ul | tee -a $LOG" 11
	;;
esac
#----------------------------------------------------------------------------------------

#========================================================================================
# Debug information
#----------------------------------------------------------------------------------------
if [ $DEBUG -eq 1 ]; then
	echo '<!-- Start of debug info -->'
	pcp_textarea "none" "cat /opt/bootsync.sh" "15"
	pcp_textarea "none" "cat ${TCEMNT}/tce/pcp_resize.log" "25"
	pcp_textarea "none" "tune2fs -l $BOOTDEV" "15"
	pcp_textarea "none" "tune2fs -l $ROOTDEV" "15"

	if [ $NUM_OF_PARTITIONS -gt 2 ]; then
		pcp_textarea "none" "tune2fs -l $DATADEV" "15"
	fi
	echo '<!-- End of debug info -->'
fi
#----------------------------------------------------------------------------------------

pcp_html_end
exit