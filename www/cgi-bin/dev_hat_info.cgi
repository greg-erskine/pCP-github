#!/bin/sh

# Version: 7.0.0 2020-06-15

# Title: HAT information
# Description: Easy method for viewing the HAT information

. pcp-functions

pcp_html_head "View HAT Information" "GE"

pcp_httpd_query_string

pcp_navbar

HATDIRECTORY="/proc/device-tree/hat/"
HATHEADINGS=$(ls $HATDIRECTORY)

LOG="${LOGDIR}/pcp_hat_info.log"
pcp_log_header $0

echo ====================================================================================== >>$LOG

#========================================================================================
# Routines
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
pcp_border_begin
#----------------------------------------------------------------------------------------
for HEADING in $HATHEADINGS
do
	INFO=$(cat ${HATDIRECTORY}${HEADING})
	DATA=$DATA'"'$INFO'", '

	echo $HEADING': '$INFO >>$LOG
	echo '    <div class="row mx-1">'
	echo '      <div class="col-2">'$HEADING'</div>'
	echo '      <div class="col-10">'$INFO'</div>'
	echo '    </div>'
done

pcp_border_end

pcp_heading5 "DATA"
pcp_border_begin
echo '    <div class="row mx-1 my-2">'
echo '      <div class="col-12">'$DATA'</div>'
echo '    </div>'
pcp_border_end

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

"hat", "Digi+ Pro", "0x0000", "0x0000", "2154f80b-0f92-45e4-96db-c1643ec2b46b", "HiFiBerry",
"hat", "JustBoom Digi HAT v1.1", "0x0002", "0x0101", "20781897-663c-429a-938c-00000000041f", "JustBoom",
"hat", "HiFiBerry DAC+", "0x3141", "0x0001", "7d5bfef9-0298-4167-92d8-6f8bd776f4fc", "HiFiBerry (Modul 9 LLC)",