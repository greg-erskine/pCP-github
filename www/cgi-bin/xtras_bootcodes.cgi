#!/bin/sh

# Version: 0.01 2015-02-15 GE
#   Original version.

. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "xtras_bootcodes" "GE"

pcp_controls
pcp_banner
pcp_xtras
pcp_running_script

echo '<p><b>Note: </b>At the moment this page simply displays the contents of cmdline.txt and cmdline.'
echo '   In the future, it is intended to be able to modify the contents of cmdline.txt.</p>'

pcp_mount_mmcblk0p1

#========================================================================================
# /mnt/mmcblkop1/cmdline.txt
#----------------------------------------------------------------------------------------
pcp_textarea "" "cat $CMDLINETXT" 50

echo '<h1>Bootcodes:</h1>'

cat $CMDLINETXT | awk '
	BEGIN {
		RS=" "
		FS="="
		i = 0
	}
	# main
	{
		bootcode[i]=$0
		i++
	}
	END {
		for (j=0; j<i; j++) {
			printf "%s. %s<br />\n",j+1,bootcode[j]
		}
	} '

pcp_umount_mmcblk0p1

#========================================================================================
# /proc/cmdline
#----------------------------------------------------------------------------------------
pcp_textarea "" "cat /proc/cmdline" 100

echo '<h1>Bootcodes:</h1>'

cat /proc/cmdline | sed 's/  / /g' | awk '
	BEGIN {
		RS=" "
		FS="="
		i = 0
	}
	# main
	{
		bootcode[i]=$0
		i++
	}
	END {
		for (j=0; j<i; j++) {
			printf "%s. %s<br />\n",j+1,bootcode[j]
		}
	} '

#----------------------------------------------------------------------------------------

echo '<br />'

pcp_footer

echo '</body>'
echo '</html>'