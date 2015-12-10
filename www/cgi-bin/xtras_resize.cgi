#!/bin/sh

# Version: 0.03 2015-11-27 GE
#	Added autoresize.

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
pcp_mode_lt_beta
pcp_running_script
pcp_httpd_query_string

case "$SUBMIT" in
	fdis*)
		OPT=1
		;;
	resi*)
		OPT=2
		;;
	auto)
		touch /home/tc/fdisk_required
		sudo filetool.sh -b
		sudo reboot
		;;
	*)
		OPT=0
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
	pcp_squeezelite_stop
	fdisk /dev/mmcblk0 <<EOF
p
d
$LAST_PARTITION_NUM
n
p
$LAST_PARTITION_NUM
$PARTITION_START

w
EOF

	echo '</textarea>'
	pcp_reboot_button
}

#========================================================================================
# resize2fs routine
#----------------------------------------------------------------------------------------
pcp_resize2fs() {
	pcp_squeezelite_stop
	echo '<textarea class="inform">'
	echo 'resize2fs can take a couple of minutes. Please wait...'
	sudo resize2fs /dev/mmcblk0p2
	echo 'Finished. Please reboot now...'
	echo '</textarea>'
	pcp_reboot_button
}

#========================================================================================
# auto resize partition
#----------------------------------------------------------------------------------------
if [ -f /home/tc/www/cgi-bin/autoresize.sh ]; then

	pcp_start_row_shade
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '        <legend>Auto resize partition</legend>'
	echo '          <table class="bggrey percent100">'
	echo '            <form name="auto" action="xtras_resize.cgi" method="get">'
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td>'
	echo '                  <p>Auto resizing the partition is an automatic process:</p>'
	echo '                  <ol>'
	echo '                    <li>fdisk, then auto reboot</li>'
	echo '                    <li>resize2fs, then auto reboot</li>'
	echo '                  </ol>'
	echo '                </td>'
	echo '              </tr>'
	echo '              <tr class="warning">'
	echo '                <td>'
	echo '                  <p style="color:white"><input type="submit" name="SUBMIT" value="auto" />&nbsp;&nbsp;auto resize partition</p>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'

fi

#========================================================================================
# fdisk and resize2fs buttons
#----------------------------------------------------------------------------------------
pcp_start_row_shade
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '        <legend>Manual resize partition</legend>'
echo '          <table class="bggrey percent100">'
echo '            <form name="increase" action="xtras_resize.cgi" method="get">'
echo '              <tr class="'$ROWSHADE'">'
echo '                <td>'
echo '                  <p>Resizing the partition is a 2 step process:</p>'
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
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td>'
                        [ $OPT == 1 ] && pcp_fdisk
echo '                </td>'
echo '              </tr>'
echo '              <tr class="warning">'
echo '                <td>'
echo '                  <p style="color:white"><input type="submit" name="SUBMIT" value="resize2fs" />&nbsp;&nbsp;resize2fs to expand partition to fit file system</p>'
echo '                </td>'
echo '              </tr>'
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
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
pcp_start_row_shade
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <form name="sd_information" method="get">'
echo '        <div class="row">'
echo '          <fieldset>'
echo '            <legend>Partition Information</legend>'
echo '            <table class="bggrey percent100">'
echo '              <tr class="'$ROWSHADE'">'
echo '                <td>'
                        pcp_textarea_inform "none" "df -h /dev/mmc*" 50
echo '                </td>'
echo '              </tr>'
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td>'
echo '                </td>'
echo '              </tr>'
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
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