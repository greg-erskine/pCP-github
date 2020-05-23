#!/bin/sh

# Version: 7.0.0 2020-05-23

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
	pcp_message INFO "Requires dosfstools.tcz" "html"
	which fsck.fat >/dev/null 2>&1
	if [ $? -eq 0 ]; then
		pcp_message INFO "dosfstools.tcz already installed." "html"
	else
		if [ ! -f ${PACKAGEDIR}/dosfstools.tcz ]; then
			pcp_message INFO "dosfstools.tcz downloading..." "html"
			sudo -u tc pcp-load -r ${PCP_REPO} -w dosfstools.tcz
			[ $? -eq 0 ] && echo 'Done.' || echo 'Error.'
		else
			pcp_message INFO "dosfstools.tcz downloaded." "html"
		fi
		pcp_message INFO "dosfstools.tcz installing..." "html"
		sudo -u tc tce-load -i dosfstools.tcz
		[ $? -eq 0 ] && echo 'Done.' || echo 'Error.'
	fi
	pcp_infobox_end
}

#========================================================================================
# Main.
#----------------------------------------------------------------------------------------
pcp_check_dosfsck
echo '  <form name="fsck" action="'$0'" method="get">'
echo '    <div class="'$BORDER'">'
echo '      <div class="row my-2 mx-1">'
echo '        <div class="col-2">'
echo '          <input class="'$BUTTON'" type="submit"'
echo '                 name="ACTION"'
echo '                 value="dosfsck"'
echo '          >'
echo '        </div>'
echo '        <div class="col-3">'
echo '          Auto fix boot partition'
echo '        </div>'
echo '        <div class="col-2">'
echo '          <input class="'$BUTTON'" type="submit"'
echo '                 name="ACTION"'
echo '                 value="Delete"'
echo '          >'
echo '        </div>'
echo '        <div class="col">'
echo '          Delete dosfstools.tcz extension (and dependencies)'
echo '        </div>'
echo '      </div>'
echo '    </div>'
echo '  </form>'
#----------------------------------------------------------------------------------------
if [ "$ACTION" = "dosfsck" ]; then
	pcp_textarea_begin "" "8"
	fsck.fat -a $BOOTDEV
	pcp_textarea_end
fi
#----------------------------------------------------------------------------------------
if [ "$ACTION" = "Delete" ]; then
	REBOOT_REQUIRED=true
	pcp_textarea_begin "" "10"
	                        sudo -u tc tce-audit builddb
	echo
	echo                    'After a reboot the following extensions will be permanently deleted:'
	echo
	                        sudo -u tc tce-audit delete dosfstools.tcz
	pcp_textarea_end
fi
#----------------------------------------------------------------------------------------

#========================================================================================
# Partition information
#----------------------------------------------------------------------------------------
if [ "$ACTION" != "Delete" ]; then
	pcp_textarea "none" "fsck.fat -vrf ${BOOTDEV}" 22
	pcp_textarea "none" "fsck -h" 3
fi
#----------------------------------------------------------------------------------------

pcp_html_end

$REBOOT_REQUIRED
[ $? -eq 0 ] && pcp_reboot_required
exit