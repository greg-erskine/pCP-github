#!/bin/sh

# Version: 4.0.0 2018-04-17
#	Added pcp_redirect_button. GE.

# Version: 3.20 2017-03-19
#	First Version. PH.

. pcp-functions

pcp_html_head "Updating pcp-base extension" "PH"

WGET="/bin/busybox wget"

pcp_banner
pcp_running_script
pcp_httpd_query_string

unset REBOOT_REQUIRED

#========================================================================================
# Routines.
#----------------------------------------------------------------------------------------
pcp_end() {
	echo '</body>'
	echo '</html>'
	exit
}

#----------------------------------------------------------------------------------------
[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] ACTION='$ACTION'</p>'
case "${ACTION}" in
	Update)
		pcp_table_top "Update pcp-base extension"
		SPACE_REQUIRED=15
		pcp_sufficient_free_space $SPACE_REQUIRED
		[ $? -eq 0 ] || pcp_end
		echo '                <textarea class="inform" style="height:150px">'
		echo '[ INFO ] Updating pcp-base and any needed dependencies.'
#		pcp-update pcp-base >/dev/null 2>&1
		pcp-update pcp-base
		CHK=$?
		if [ $CHK -eq 2 ]; then
			echo '[ INFO ] There is no update for pcp-base at this time.'
			unset REBOOT_REQUIRED
		elif [ $CHK -eq 1 ]; then
			echo '[ ERROR ] There was an error updating pcp-base, please try again later!'
			unset REBOOT_REQUIRED
		else
			echo '[ INFO ] A [Reboot] is required to complete the update.'
			REBOOT_REQUIRED=TRUE
		fi
		echo '                </textarea>'
	;;
	*)
		echo '<p class="error">[ ERROR ] Option Error!'
	;;
esac

pcp_table_middle
pcp_redirect_button "Go to Main Page" "main.cgi" 10
pcp_table_end
pcp_footer
pcp_copyright
[ $REBOOT_REQUIRED ] && pcp_reboot_required
pcp_end