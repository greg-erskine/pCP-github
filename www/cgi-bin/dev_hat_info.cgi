#!/bin/sh

# Version: 7.0.0 2020-06-18

# Title: HAT information
# Description: Easy method for viewing the HAT information

. pcp-functions

pcp_html_head "View HAT Information" "GE"

pcp_httpd_query_string

pcp_navbar

HATDIRECTORY="/proc/device-tree/hat/"

LOG="${LOGDIR}/pcp_hat_info.log"
pcp_log_header $0

echo ====================================================================================== >>$LOG

#========================================================================================
# Functions
#----------------------------------------------------------------------------------------
pcp_overlays_loaded() {
	pcp_mount_bootpart >/dev/null 2>&1
	OVERLAYS=$(cat ${VOLUME}/config.txt | grep dtoverlay)
	pcp_umount_bootpart >/dev/null 2>&1
}

#========================================================================================
# Main HTML
#----------------------------------------------------------------------------------------
pcp_heading5 "HAT information"

if [ -d $HATDIRECTORY ]; then
	pcp_border_begin
	HATHEADINGS=$(ls $HATDIRECTORY)

	I=1
	for HEADING in $HATHEADINGS
	do
		INFO=$(cat ${HATDIRECTORY}${HEADING})
#		DATA=$DATA'"'$INFO'", '
		[ $I -eq 1 ] && DATA=${INFO} || DATA=${DATA}:${INFO}

		echo $HEADING': '$INFO >>$LOG
		echo '    <div class="row mx-1">'
		echo '      <div class="col-2">'$HEADING'</div>'
		echo '      <div class="col-10">'$INFO'</div>'
		echo '    </div>'
		I=$((I+1))
	done

	pcp_border_end
	#------------------------------------------------------------------------------------
	pcp_heading5 "DATA"
	pcp_border_begin
	echo '    <div class="row mx-1 my-2">'
	echo '      <div class="col-12">'$DATA'</div>'
	echo '    </div>'
	pcp_border_end

else
	pcp_infobox_begin
	pcp_message WARN "No HAT data available." "text"
	pcp_infobox_end
fi

#----------------------------------------------------------------------------------------
pcp_overlays_loaded
pcp_debug_variables "HTML" OVERLAYS HEADING DATA
#-----------------------------------dmesg text area--------------------------------------
pcp_heading5 "dmesg | grep soc:sound"
pcp_textarea "none" 'dmesg | grep soc:sound' 5 log
#----------------------------------Overlays text area------------------------------------
pcp_heading5 "Overlays in ${VOLUME}/config.txt"
pcp_textarea "none" 'echo $OVERLAYS | sed "s/ /\n/g"' 5 log
#----------------------------------------------------------------------------------------

pcp_html_end
exit
