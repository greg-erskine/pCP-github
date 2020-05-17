#!/bin/sh

# Version: 7.0.0 2020-05-17
# Title: copy2fs
# Description: Sets the copy2fs flag

. pcp-functions

pcp_html_head "xtras copy2fs" "GE"

pcp_xtras
pcp_httpd_query_string

REBOOT_REQUIRED=false

#----------------------------------------------------------------------------------------
# copy2fs actions
#----------------------------------------------------------------------------------------
case "$COPY2FS" in
	yes)
		touch ${TCEMNT}/tce/copy2fs.flg
		REBOOT_REQUIRED=true
	;;
	no)
		rm -f ${TCEMNT}/tce/copy2fs.flg
		REBOOT_REQUIRED=true
	;;
esac

#========================================================================================
pcp_heading5 "copy2fs"
#----------------------------------------------------------------------------------------
echo '  <form name="copy2fs" action="'$0'" method="get">'
#----------------------------------------------------------------------------------------
[ -f ${TCEMNT}/tce/copy2fs.flg ] && COPY2FSyes="checked" || COPY2FSno="checked"

pcp_incr_id
echo '    <div class="row">'
echo '      <div class="col-2">'
echo '        <p>copy2fs flag set</p>'
echo '      </div>'
echo '      <div class="col-2">'
echo '        <input id="rad1" type="radio" name="COPY2FS" value="yes" '$COPY2FSyes'>'
echo '        <label for="rad1">Yes</label>'
echo '        <input id="rad2" type="radio" name="COPY2FS" value="no" '$COPY2FSno'>'
echo '        <label for="rad2">No</label>'
echo '      </div>'
echo '      <div class="col-8">'
echo '        <p>Set the copy2fs flag&nbsp;&nbsp;'
echo '        <a class="moreless" id="dt'$ID'a" href=# onclick="return more('\'''$ID''\'')">more></a></p>'
echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
echo '          <p>This sets the copy2fs flag so, on the next reboot, all extensions are loaded into RAM.</p>'
echo '          <p>A reboot is required for the copy2fs flag to take effect.</p>'
echo '        </div>'
echo '      </div>'
echo '    </div>'
#----------------------------------------------------------------------------------------
echo '    <div class="row">'
echo '      <div class="col-2">'
echo '        <input class="'$BUTTON'"type="submit" name="SUBMIT" value="Save">'
echo '      </div>'
echo '    </div>'
#----------------------------------------------------------------------------------------
echo '  </form>'
#----------------------------------------------------------------------------------------

#========================================================================================
pcp_heading5 "Current mounted filesystems"
#----------------------------------------------------------------------------------------
pcp_textarea "none" "df" 20
#----------------------------------------------------------------------------------------
echo '  <div class="row">'
echo '    <div>'
echo '      <p><b>Example: copy2fs not set</b></p>'
echo '      <p>Note: There will be lots of loop mounted filesystems, one for each extension.</p>'
echo '    </div>'
echo '  </div>'
#----------------------------------------------------------------------------------------
echo '  <div class="row">'
echo '    <div>'
echo        '<textarea class="inform" style="height:160px">'
echo          'Filesystem           1K-blocks      Used Available Use% Mounted on'
echo          'tmpfs                   222492         0    222492   0% /dev/shm'
echo          '/dev/mmcblk0p2           36561     15244     18379  45% /mnt/mmcblk0p2'
echo          '/dev/loop0                 128       128         0 100% /tmp/tcloop/pcp'
echo          '/dev/loop1                 128       128         0 100% /tmp/tcloop/pcp-base'
echo          '/dev/loop2                 128       128         0 100% /tmp/tcloop/alsa'
echo          '/dev/loop3                1152      1152         0 100% /tmp/tcloop/alsa-utils'
echo          '/dev/loop4                 128       128         0 100% /tmp/tcloop/busybox-httpd'
echo          '     .                      .         .          .   .          .'
echo          '     .                      .         .          .   .          .'
echo        '</textarea>'
echo '    </div>'
echo '  </div>'
#----------------------------------------------------------------------------------------
echo '  <div class="row">'
echo '    <div>'
echo '      <p><b>Example: copy2fs set</b></p>'
echo '      <p>Note: There are no loop mounted filesystems.</p>'
echo '    </div>'
echo '  </div>'
#----------------------------------------------------------------------------------------
echo '  <div class="row">'
echo '    <div>'
echo        '<textarea class="inform" style="height:60px">'
echo          'Filesystem           1K-blocks      Used Available Use% Mounted on'
echo          'tmpfs                   222492         0    222492   0% /dev/shm'
echo          '/dev/mmcblk0p2           36561     15244     18379  45% /mnt/mmcblk0p2'
echo        '</textarea>'
echo '    </div>'
echo '  </div>'
#----------------------------------------------------------------------------------------

$REBOOT_REQUIRED
[ $? -eq 0 ] && pcp_reboot_required

pcp_html_end
exit
