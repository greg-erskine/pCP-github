#!/bin/sh

# Version: 3.20 2017-04-16
#	Fixed pcp-xxx-functions issues. GE.
#  Changed reboot functions. PH.

# Version: 0.01 2015-08-28 GE
#	Original version.

. pcp-functions
#. $CONFIGCFG

pcp_html_head "xtras copy2fs" "GE"

pcp_banner
pcp_running_script
pcp_xtras

pcp_httpd_query_string

#----------------------------------------------------------------------------------------
# copy2fs actions
#----------------------------------------------------------------------------------------
case "$COPY2FS" in
	yes)
		touch /mnt/mmcblk0p2/tce/copy2fs.flg
	;;
	no)
		rm -f /mnt/mmcblk0p2/tce/copy2fs.flg
	;;
esac

[ -f /mnt/mmcblk0p2/tce/copy2fs.flg ] && COPY2FSyes="checked" || COPY2FSno="checked"

#========================================================================================
# copy2fs form
#----------------------------------------------------------------------------------------
pcp_incr_id
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <form name="copy2fs" action="xtras_copy2fs.cgi" method="get">'
echo '        <div class="row">'
echo '          <fieldset>'
echo '            <legend>copy2fs</legend>'
echo '            <table class="bggrey percent100">'
pcp_start_row_shade
echo '                <tr class="'$ROWSHADE'">'
echo '                  <td class="column150">'
echo '                    <p>copy2fs flag set</p>'
echo '                  </td>'
echo '                  <td class="column210">'
echo '                    <input class="small1" type="radio" name="COPY2FS" id="COPY2FS" value="yes" '$COPY2FSyes'>Yes'
echo '                    <input class="small1" type="radio" name="COPY2FS" id="COPY2FS" value="no" '$COPY2FSno'>No'
echo '                  </td>'
echo '                  <td>'
echo '                    <p>Set the copy2fs flag&nbsp;&nbsp;'
echo '                    <a class="moreless" id="'$ID'a" href=# onclick="return more('\'''$ID''\'')">more></a></p>'
echo '                    <div id="'$ID'" class="less">'
echo '                      <p>This sets the copy2fs flag so, on the next reboot, all extensions are loaded into RAM.</p>'
echo '                      <p>A reboot is required for the copy2fs flag to take effect.</p>'
echo '                    </div>'
echo '                  </td>'
echo '                </tr>'
pcp_toggle_row_shade
echo '                <tr class="'$ROWSHADE'">'
echo '                  <td colspan="3">'
echo '                    <input type="submit" name="SUBMIT" value="Save">'
echo '                    <input type="button" value="Reboot" onClick="javascript:pcp_confirm('\''Reboot '$NAME?''\'','\''reboot.cgi?RB=yes'\'')" />'
echo '                  </td>'
echo '                </tr>'
echo '            </table>'
echo '          </fieldset>'
echo '        </div>'
echo '      </form>'
echo '    </td>'
echo '  </tr>'
echo '</table>'

#========================================================================================
# Mounted filesystems form
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Mounted filesystems</legend>'
echo '          <table class="bggrey percent100">'
pcp_start_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td>'
                      pcp_textarea_inform "none" "df" 200
echo '              </td>'
echo '            </tr>'
pcp_toggle_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td>'
echo '                <p><b>Example showing copy2fs not set.</b></p>'
echo '                <p>Note: There will be lots of loop mounted filesystems, one for each extension.</p>'
echo '              </td>'
echo '            </tr>'
pcp_toggle_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td>'
echo                  '<textarea class="inform" style="height:160px">'
echo                    'Filesystem           1K-blocks      Used Available Use% Mounted on'
echo                    'tmpfs                   222492         0    222492   0% /dev/shm'
echo                    '/dev/mmcblk0p2           36561     15244     18379  45% /mnt/mmcblk0p2'
echo                    '/dev/loop0                 128       128         0 100% /tmp/tcloop/dropbear'
echo                    '/dev/loop1                 128       128         0 100% /tmp/tcloop/busybox-httpd'
echo                    '/dev/loop2                 256       256         0 100% /tmp/tcloop/libfaad'
echo                    '/dev/loop3                  12        12         0 100% /tmp/tcloop/libogg'
echo                    '/dev/loop4                 368       368         0 100% /tmp/tcloop/flac'
echo                    '     .                      .         .          .   .          .'
echo                    '     .                      .         .          .   .          .'
echo                  '</textarea>'
echo '              </td>'
echo '            </tr>'
pcp_toggle_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td>'
echo '                <p><b>Example showing copy2fs set.</b></p>'
echo '                <p>Note: There are no loop mounted filesystems.</p>'
echo '              </td>'
echo '            </tr>'
pcp_toggle_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td>'
echo                  '<textarea class="inform" style="height:60px">'
echo                    'Filesystem           1K-blocks      Used Available Use% Mounted on'
echo                    'tmpfs                   222492         0    222492   0% /dev/shm'
echo                    '/dev/mmcblk0p2           36561     15244     18379  45% /mnt/mmcblk0p2'
echo                  '</textarea>'
echo '              </td>'
echo '            </tr>'
echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------

pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'