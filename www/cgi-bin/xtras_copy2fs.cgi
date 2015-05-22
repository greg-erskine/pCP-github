#!/bin/sh

# Version: 0.01 2015-05-22 GE
#   Original version.

. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "xtras copy2fs" "GE"

DEBUG=1

pcp_banner
pcp_running_string
pcp_xtras

pcp_httpd_query_string

#----------------------------------------------------------------------------------------
# COPY2FS SECTION
#----------------------------------------------------------------------------------------
case $COPY2FS in
	Yes)
		touch /mnt/mmcblk0p2/tce/copy2fs.flg
		;;
	No)
		rm -f /mnt/mmcblk0p2/tce/copy2fs.flg
		;;
	*)
		echo '<p class="error">$COPY2FS not set: '$COPY2FS'</p>'
	;;
esac

# Function to check the copy2fs-radio button setting
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
echo '                    <p>copy2fs</p>'
echo '                  </td>'
echo '                  <td class="column210">'
echo '                    <input class="small1" type="radio" name="COPY2FS" id="COPY2FS" value="Yes" '$COPY2FSyes'>Yes'
echo '                    <input class="small1" type="radio" name="COPY2FS" id="COPY2FS" value="No" '$COPY2FSno'>No'
echo '                  </td>'
echo '                  <td>'
echo '                    <p>Set copy2fs flag&nbsp;&nbsp;'
echo '                    <a class="moreless" id="'$ID'a" href=# onclick="return more('\'''$ID''\'')">more></a></p>'
echo '                    <div id="'$ID'" class="less">'
echo '                      <p>This sets the copy2fs flag so extensions are loaded into ram.</p>'
echo '                    </div>'
echo '                  </td>'
echo '                </tr>'
pcp_toggle_row_shade
echo '                <tr class="'$ROWSHADE'">'
echo '                  <td colspan="3">'
echo '                    <input type="submit" name="SUBMIT" value="Save">'
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
# Loop mounted extensions form
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Loop mounted extensions</legend>'
echo '          <table class="bggrey percent100">'
echo '            <tr class="odd">'
echo '              <td>'
                      pcp_textarea_inform "none" "df" 250
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
echo '</body>'
echo '</html>'