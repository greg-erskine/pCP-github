#!/bin/sh

# Version: 6.0.0 2020-01-10

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
		echo '                <textarea class="inform" style="height:350px">'
		echo '[ INFO ] Updating pcp-base and any needed dependencies.'
		sudo -u tc pcp-update pcp-base.tcz
		CHK=$?
		if [ $CHK -eq 2 ]; then
			echo '[ INFO ] There is no update for pcp-base at this time.'
		elif [ $CHK -eq 1 ]; then
			echo '[ ERROR ] There was an error updating pcp-base, please try again later!'
		else
			REBOOT_REQUIRED=TRUE
		fi

		WWWVER=$(pcp_picoreplayer_version | awk -F'-' '{ print $1}')
		echo ''
		echo '[ INFO ] Updating pcp-www and any needed dependencies.'
		sudo -u tc pcp-update pcp-$WWWVER-www.tcz
		CHK=$?
		if [ $CHK -eq 2 ]; then
			echo '[ INFO ] There is no update for pcp-base at this time.'
		elif [ $CHK -eq 1 ]; then
			echo '[ ERROR ] There was an error updating pcp-base, please try again later!'
		else
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
if [ $REBOOT_REQUIRED ]; then
	echo '[ INFO ] A [Reboot] is required to complete the update.'
	pcp_reboot_required
fi
pcp_end