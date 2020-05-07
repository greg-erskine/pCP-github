#!/bin/sh

# Version: 7.0.0 2020-05-07

. pcp-functions

pcp_html_head "Updating pcp-base extension" "PH"

WGET="/bin/busybox wget"

pcp_navbar
pcp_httpd_query_string

unset REBOOT_REQUIRED

#========================================================================================
# Routines.
#----------------------------------------------------------------------------------------
pcp_end() {
	pcp_html_end
	exit
}

#----------------------------------------------------------------------------------------
pcp_debug_variables "html" ACTION

case "${ACTION}" in
	Update)
		pcp_heading5 "Update pcp-base extension"
		SPACE_REQUIRED=15
		echo '                <textarea class="col-12 text-monospace" rows="22">'
		pcp_sufficient_free_space $SPACE_REQUIRED "text"
		if [ $? -eq 0 ]; then
			pcp_message INFO "Updating pcp-base and any needed dependencies." "text"
			sudo -u tc pcp-update pcp-base.tcz
			CHK=$?
			if [ $CHK -eq 2 ]; then
				pcp_message INFO "There is no update for pcp-base at this time." "text"
			elif [ $CHK -eq 1 ]; then
				pcp_message ERROR "There was an error updating pcp-base, please try again later!" "text"
			else
				REBOOT_REQUIRED=TRUE
			fi

			WWWVER=$(pcp_picoreplayer_version | awk -F'-' '{ print $1}')
			echo ''
			pcp_message INFO "Updating pcp-www and any needed dependencies." "text"
			sudo -u tc pcp-update pcp-$WWWVER-www.tcz
			CHK=$?
			if [ $CHK -eq 2 ]; then
				pcp_message INFO "There is no update for pcp-base at this time." "text"
			elif [ $CHK -eq 1 ]; then
				pcp_message ERROR "There was an error updating pcp-base, please try again later!" "text"
			else
				REBOOT_REQUIRED=TRUE
			fi
		fi

		echo '                </textarea>'
	;;
	*)
		pcp_message ERROR "[ ERROR ] Option Error!" "text"
	;;
esac

echo '<div class="mt-3">'
pcp_redirect_button "Go to Main Page" "main.cgi?CALLED_BY=Updates" 10
echo '</div>'

if [ $REBOOT_REQUIRED ]; then
	pcp_message INFO "A [Reboot] is required to complete the update." "text"
	pcp_reboot_required
fi
pcp_end