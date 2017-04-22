#!/bin/sh

# Version: 3.20 2017-03-19
#	First Version. PH.

. pcp-functions
#. $CONFIGCFG

pcp_html_head "Updating pcp-base extension" "PH" "5" "main.cgi"

WGET="/bin/busybox wget"

pcp_banner
pcp_running_script
pcp_httpd_query_string
REBOOT_REQUIRED=0
RESULT=0

pcp_table_top "Update Extension"
#----------------------------------------------------------------------------------------
[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] ACTION='$ACTION'</p>'
case "${ACTION}" in
	Update)
		SPACE_REQUIRED=15
		pcp_sufficient_free_space $SPACE_REQUIRED
		if [ $? -eq 0 ]; then
		
			pcp_table_top "Updating pcp-base and any needed dependencies"
			echo '                <textarea class="inform" style="height:150px">'
			pcp-update pcp-base
			TEST=$?
			if [ $TEST -eq 2 ]; then
				echo '[ INFO ] There is no update for pcp-base at this time.'
				REBOOT_REQUIRED=0
			elif [ $TEST -eq 1 ]; then
				echo '[ ERROR ] There was an error updating pcp-base, please try again later'
				REBOOT_REQUIRED=0
			else 
				REBOOT_REQUIRED=1
			fi
			echo '                </textarea>'
			pcp_table_end
		fi
	;;
	*) echo '<p class="error">[ ERROR ] Option Error!'
	;;
esac

[ $REBOOT_REQUIRED -eq 1 ] && pcp_reboot_required

pcp_table_middle
pcp_go_back_button
pcp_table_end
pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'
