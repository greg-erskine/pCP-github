#!/bin/sh

# Version: 6.0.0 2019-07-19

. pcp-functions
. pcp-lms-functions

pcp_html_head "xtras_dosfsck" "GE"

pcp_banner
pcp_navigation
pcp_httpd_query_string

REBOOT_REQUIRED=false

#========================================================================================
# Check for dosfstools.tcz and download and install.
#----------------------------------------------------------------------------------------
pcp_check_dosfsck() {
	echo '<textarea class="inform" rows="6">'
	echo '[ INFO ] Requires dosfstools.tcz'
	which fsck.fat >/dev/null 2>&1
	if [ $? -eq 0 ]; then
		echo '[ INFO ] dosfstools.tcz already installed.'
	else
		if [ ! -f ${PACKAGEDIR}/dosfstools.tcz ]; then
			echo '[ INFO ] dosfstools.tcz downloading...'
			sudo -u tc pcp-load -r ${PCP_REPO} -w dosfstools.tcz
			[ $? -eq 0 ] && echo 'Done.' || echo 'Error.'
		else
			echo '[ INFO ] dosfstools.tcz downloaded.'
		fi
		echo '[ INFO ] dosfstools.tcz installing...'
		sudo -u tc tce-load -i dosfstools.tcz
		[ $? -eq 0 ] && echo 'Done.' || echo 'Error.'
	fi
	echo '</textarea>'
}

#========================================================================================
# Main.
#----------------------------------------------------------------------------------------
pcp_table_top "Check boot partition"
pcp_check_dosfsck
pcp_table_middle
echo '                <form name="fsck" action="'$0'" method="get">'
echo '                  <input type="submit"'
echo '                         name="ACTION"'
echo '                         value="dosfsck"'
echo '                  >&nbsp;&nbsp;Auto fix boot partition&nbsp;&nbsp;'
echo '                  <input type="submit"'
echo '                         name="ACTION"'
echo '                         value="Delete"'
echo '                  >&nbsp;&nbsp;Delete dosfstools.tcz extension (and dependencies)'
echo '                </form>'
#----------------------------------------------------------------------------------------
if [ "$ACTION" = "dosfsck" ]; then
	pcp_table_middle
	echo '                <textarea class="inform" rows="10">'
	                        fsck.fat -a $BOOTDEV
	echo '                </textarea>'
fi
#----------------------------------------------------------------------------------------
if [ "$ACTION" = "Delete" ]; then
	REBOOT_REQUIRED=true
	pcp_table_middle
	echo '                <textarea class="inform" rows="10">'
	                        sudo -u tc tce-audit builddb
	echo
	echo                    'After a reboot the following extensions will be permanently deleted:'
	echo
	                        sudo -u tc tce-audit delete dosfstools.tcz
	echo '                </textarea>'
fi
#----------------------------------------------------------------------------------------
pcp_table_end

#========================================================================================
# Partition information
#----------------------------------------------------------------------------------------
if [ "$ACTION" != "Delete" ]; then
	pcp_table_top "Boot partition information"
	pcp_textarea_inform "none" "fsck.fat -vrf ${BOOTDEV}" 300
	pcp_table_middle
	pcp_table_middle
	pcp_textarea_inform "none" "fsck -h" 25
	pcp_table_end
fi
#----------------------------------------------------------------------------------------

pcp_footer
pcp_copyright
pcp_remove_query_string

echo '</body>'
echo '</html>'

$REBOOT_REQUIRED
[ $? -eq 0 ] && pcp_reboot_required
exit