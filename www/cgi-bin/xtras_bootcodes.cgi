#!/bin/sh

# Version: 0.01 2015-01-19 GE
#   Original version.

. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "xtras_bootcodes" "GE"

pcp_controls
pcp_banner
pcp_navigation
pcp_running_script

pcp_mount_mmcblk0p1

pcp_show_cmdline_txt

pcp_textarea "none" "cat $CMDLINETXT" 50

#========================================================================================
# 
#----------------------------------------------------------------------------------------

cat $CMDLINETXT | awk '

	BEGIN {
		RS=" "
		FS="="
		i = 0
	}
	#main
	{
		bootcode[i]=$0
		i++
	}
	END {
		for (j=0; j<i; j++) {
			printf "<br />Bootcode: %s\n",bootcode[j]
		}
	} '

#========================================================================================
# 
#----------------------------------------------------------------------------------------

pcp_umount_mmcblk0p1

pcp_footer

echo '</body>'
echo '</html>'