#!/bin/sh

# Version: 0.02 2015-06-02 GE
#	Minor updates.

# Version: 0.01 2015-02-17 GE
#   Original version.

. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "xtras_resize" "GE"

pcp_controls
pcp_banner
pcp_navigation
pcp_mode_lt_99
pcp_running_script
pcp_httpd_query_string

case "$SUBMIT" in
	fdis*)
		OPT=1
		;;
	resi*)
		OPT=2
		;;
esac

#========================================================================================
# fdisk routine
#----------------------------------------------------------------------------------------
pcp_fdisk() {
	echo '<textarea class="inform">'
	echo 'Please reboot now...'
	echo ''
	echo ''

	LAST_PARTITION_NUM=$(fdisk -l /dev/mmcblk0 | tail -n 1 | sed 's/  */ /g' | cut -d' ' -f 1 | cut -c14)
	PARTITION_START=$(fdisk -l /dev/mmcblk0 | tail -n 1 | sed 's/  */ /g' | cut -d' ' -f 2)

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

w
p
EOF

	echo '</textarea>'
	pcp_reboot_button
}

#========================================================================================
# resize2fs routine
#----------------------------------------------------------------------------------------
pcp_resize2fs() {
	echo '<textarea class="inform">'
	echo 'resize2fs can take a couple of minutes. Please wait...'
	sudo resize2fs /dev/mmcblk0p2
	echo 'Finished. Please reboot now...'
	echo '</textarea>'
	pcp_reboot_button
}

#========================================================================================
# fdisk and resize2fs buttons
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '        <legend>Resize partition</legend>'
echo '          <table class="bggrey percent100">'
echo '            <form name="increase" action="xtras_resize.cgi" method="get" id="increase">'
echo '              <tr class="even">'
echo '                <td>'
echo '                  <p>Resizing the partition is a 2 step process</p>'
echo '                  <ol>'
echo '                    <li>Step 1 - fdisk, then reboot</li>'
echo '                    <li>Step 2 - resize2fs, then reboot</li>'
echo '                  </ol>'
echo '                </td>'
echo '              </tr>'
echo '              <tr class="warning">'
echo '                <td>'
echo '                  <p style="color:white"><input type="submit" name="SUBMIT" value="fdisk" />&nbsp;&nbsp;fdisk to resize partition</p>'
echo '                </td>'
echo '              </tr>'
echo '              <tr class="even">'
echo '                <td>'
                        [ $OPT == 1 ] && pcp_fdisk
echo '                </td>'
echo '              </tr>'
echo '              <tr class="warning">'
echo '                <td>'
echo '                  <p style="color:white"><input type="submit" name="SUBMIT" value="resize2fs" />&nbsp;&nbsp;resize2fs to expand partition to fit file system</p>'
echo '                </td>'
echo '              </tr>'
echo '              <tr class="even">'
echo '                <td>'
                        [ $OPT == 2 ] && pcp_resize2fs
echo '                </td>'
echo '              </tr>'
echo '            </form>'
echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'

#========================================================================================
# Partition information
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <form name="sd_information" method="get">'
echo '        <div class="row">'
echo '          <fieldset>'
echo '            <legend>Partition Information</legend>'
echo '            <table class="bggrey percent100">'
echo '              <tr class="odd">'
echo '                <td>'
                        pcp_textarea_inform "none" "df -h /dev/mmc*" 50
echo '                </td>'
echo '              </tr>'
echo '              <tr class="odd">'
echo '                <td>'
                        pcp_textarea_inform "none" "fdisk -l" 120
echo '                </td>'
echo '              </tr>'
echo '            </table>'
echo '          </fieldset>'
echo '        </div>'
echo '      </form>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------

pcp_footer
pcp_copyright
[ $OPT -gt 0 ] && pcp_reboot_button

echo '</body>'
echo '</html>'