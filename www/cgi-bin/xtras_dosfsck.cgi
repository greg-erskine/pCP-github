#!/bin/sh

# Version: 0.01 2014-12-27 GE
#   Original version.

. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "xtras_dosfsck" "GE"

pcp_controls
pcp_banner

pcp_navigation
pcp_running_script
pcp_httpd_query_string

case "$SUBMIT" in
	dosfsck)
		OPT=1
		;;
	xxxx*)
		OPT=2
		;;
esac

#========================================================================================
# Check for dosfstools.tcz and download and install
#========================================================================================
echo '<textarea class="inform">'
if [ ! -f /mnt/mmcblk0p2/tce/optional/dosfstools.tcz ]; then
	tce-load -w dosfstools.tcz
	echo 'dosfstools.tcz not loaded.'
else
	echo 'dosfstools.tcz loaded.'
fi
tce-load -i dosfstools.tcz
echo '</textarea>'

#========================================================================================
# dosfsck routine
#----------------------------------------------------------------------------------------
pcp_dosfsck() {
  echo '<textarea class="inform">'
  
  dosfsck -V /dev/mmcblk0p1
  
  echo '</textarea>'
}

#========================================================================================
# xxxx buttons
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '        <legend>Resize partition</legend>'
echo '          <table class="bggrey percent100">'
echo '            <form name="increase" action="xtras_dosfsck.cgi" method="get" id="increase">'
echo '              <tr class="even">'
echo '                <td>'
echo '                  <p>Checkomg the partition</p>'
echo '                </td>'
echo '              </tr>'
echo '              <tr class="odd">'
echo '                <td>'
echo '                  <input type="submit" name="SUBMIT" value="dosfsck" />&nbsp;&nbsp;check partition'
echo '                </td>'
echo '              </tr>'
echo '              <tr class="even">'
echo '                <td>'

[ $OPT == 1 ] && pcp_dosfsck

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

pcp_textarea_inform "none" "fsck -h" 50

echo '                </td>'
echo '              </tr>'
echo '              <tr class="odd">'
echo '                <td>'

pcp_textarea_inform "none" "dosfsck -V /dev/mmcblk0p1" 120

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

pcp_favorites
pcp_footer

echo '</body>'
echo '</html>'