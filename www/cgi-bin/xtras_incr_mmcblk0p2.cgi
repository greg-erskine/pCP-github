#!/bin/sh

# Version: 0.01 2014-12-21 GE
#   Original version.

. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "xtras increase mmcblk0p2" "GE"

pcp_banner
pcp_running_string
pcp_navigation

echo '<textarea rows="40">'

echo '$ fdisk -l /dev/mmcblk0'
fdisk -l /dev/mmcblk0
echo ''
echo ''

LAST_PARTITION_NUM=$(fdisk -l /dev/mmcblk0 | tail -n 1 | sed 's/  */ /g' | cut -d' ' -f 1 | cut -c14)
PARTITION_START=$(fdisk -l /dev/mmcblk0 | tail -n 1 | sed 's/  */ /g' | cut -d' ' -f 2 )

echo '$LAST_PARTITION_NUM: '$LAST_PARTITION_NUM
echo '$PARTITION_START: '$PARTITION_START

  fdisk /dev/mmcblk0 <<EOF
p
d
$LAST_PARTITION_NUM
n
p
$LAST_PARTITION_NUM
$PARTITION_START

p
EOF












echo '</textarea>'

pcp_footer
pcp_refresh_button
pcp_go_back_button

echo '</body>'
echo '</html>'