#!/bin/sh

# Version: 7.0.0 2020-05-26

# Title: dosfsck
# Description: Get rid of the dirty bits on your boot partition

. pcp-functions
. pcp-lms-functions

pcp_html_head "xtras_dosfsck" "GE"

pcp_navbar
pcp_httpd_query_string
pcp_remove_query_string

REBOOT_REQUIRED=false

#========================================================================================
# Check for dosfstools.tcz and download and install.
#----------------------------------------------------------------------------------------
pcp_check_dosfsck() {
	pcp_infobox_begin
	pcp_message INFO "Requires dosfstools.tcz" "text"
	which fsck.fat >/dev/null 2>&1
	if [ $? -eq 0 ]; then
		pcp_message INFO "dosfstools.tcz already installed." "text"
	else
		if [ ! -f ${PACKAGEDIR}/dosfstools.tcz ]; then
			pcp_message INFO "dosfstools.tcz downloading..." "text"
			sudo -u tc pcp-load -r ${PCP_REPO} -w dosfstools.tcz
			[ $? -eq 0 ] && echo 'Done.' || echo 'Error.'
		else
			pcp_message INFO "dosfstools.tcz downloaded." "text"
		fi
		pcp_message INFO "dosfstools.tcz installing..." "text"
		sudo -u tc tce-load -i dosfstools.tcz
		[ $? -eq 0 ] && echo 'Done.' || echo 'Error.'
	fi
	pcp_infobox_end
}

pcp_check_dosfsck
#========================================================================================
# Main.
#----------------------------------------------------------------------------------------
pcp_border_begin
echo '    <form name="fsck" action="'$0'" method="get">'
echo '      <div class="row my-2 mx-1">'
echo '        <div class="col-2">'
echo '          <input class="'$BUTTON'"'
echo '                 type="submit"'
echo '                 name="ACTION"'
echo '                 value="dosfsck"'
echo '          >'
echo '        </div>'
echo '        <div class="col-3">'
echo '          Auto fix boot partition'
echo '        </div>'
echo '        <div class="col-2">'
echo '          <input class="'$BUTTON'"'
echo '                 type="submit"'
echo '                 name="ACTION"'
echo '                 value="Delete"'
echo '          >'
echo '        </div>'
echo '        <div class="col">'
echo '          Delete dosfstools.tcz extension (and dependencies)'
echo '        </div>'
echo '      </div>'
echo '    </form>'
pcp_border_end
#----------------------------------------------------------------------------------------
if [ "$ACTION" = "dosfsck" ]; then
	pcp_heading5 "Fix file system (PCP_BOOT)"
	pcp_infobox_begin
	fsck.fat -a $BOOTDEV
	pcp_infobox_end
fi
#----------------------------------------------------------------------------------------
if [ "$ACTION" = "Delete" ]; then
	REBOOT_REQUIRED=true
	pcp_infobox_begin
	pcp_message INFO "Deleting dosfstools.tcz" "text"
	sudo -u tc tce-audit builddb
	echo
	pcp_message INFO "After a reboot the following extensions will be permanently deleted:" "text"
	sudo -u tc tce-audit delete dosfstools.tcz
	pcp_infobox_end
fi
#----------------------------------------------------------------------------------------

#========================================================================================
# Partition information
#----------------------------------------------------------------------------------------
if [ "$ACTION" != "Delete" ]; then
	pcp_heading5 "Check file system (PCP_BOOT)"
	pcp_infobox_begin
	fsck.fat -vrf ${BOOTDEV}
	pcp_infobox_end
	pcp_infobox_begin
	fsck -h
	pcp_infobox_end
fi
#----------------------------------------------------------------------------------------

pcp_html_end

$REBOOT_REQUIRED
[ $? -eq 0 ] && pcp_reboot_required
exit