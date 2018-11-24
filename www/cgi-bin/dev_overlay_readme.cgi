#!/bin/sh

# Version: 4.1.0 2018-09-20

# Title: Overlays README
# Description: Easy method for viewing the README file in /mnt/mmcblk0p1/overlays

. pcp-functions

pcp_html_head "View Overlay Readme" "GE"

pcp_banner
pcp_running_script
pcp_httpd_query_string

TMPPATH="/tmp"
TEMPDIR="dbt"

#========================================================================================
# NOTE: Very inefficient ATM
#       Reads README and generates new files every time you hit [ Show ] button.
#----------------------------------------------------------------------------------------

#========================================================================================
# Routines
#----------------------------------------------------------------------------------------
pcp_overlay_cleanup() {
	rm -rf ${TMPPATH}/${TEMPDIR}
	mkdir ${TMPPATH}/${TEMPDIR}
}

pcp_overlays_loaded() {
	cat ${VOLUME}/config.txt  | grep ^dtoverlay | sed 's/dtoverlay=//' > ${TMPPATH}/${TEMPDIR}/LOADED_OVERLAYS
}

pcp_overlay_get_readme() {
	pcp_mount_bootpart_nohtml >/dev/null 2>&1
	cp ${VOLUME}/overlays/README ${TMPPATH}/${TEMPDIR}
	pcp_overlays_loaded
	pcp_umount_bootpart_nohtml >/dev/null 2>&1
}

pcp_overlay_split_readme() {
	cat ${TMPPATH}/${TEMPDIR}/README | awk -v temppath=${TMPPATH} -v tempdir=${TEMPDIR} '
		BEGIN {
			RS="Name:"
			FS="Name:"
			i=0
		}
		# main ()
		{
			name[i] = $1
			split($1,a,"\n")
			gsub("   ","",a[1])
			file[i]=a[1]
			i++
		}
		END {
			for (j=3; j<NR; j++) {
				filename = sprintf("%s/%s/%s.txt", temppath, tempdir, file[j]);
				print "Name:"name[j] > filename
			}
		} '
}

pcp_overlay_cleanup
pcp_overlay_get_readme
pcp_overlay_split_readme

PCPOVERLAYS=$(ls "${TMPPATH}/${TEMPDIR}" | grep txt)
#$(cat ${TMPPATH}/${TEMPDIR}/LOADED_OVERLAYS)

#========================================================================================
# Selection form
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Select overlay</legend>'
echo '          <form name="log" action="'$0'" method="get">'
echo '            <table class="bggrey percent100">'
#----------------------------------------------------------------------------------------
pcp_incr_id
pcp_start_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="column300">'
echo '                  <select class="large22" name="SELECTION">'

	                      for OVERLAY in $PCPOVERLAYS
	                      do
	                          [ "$SELECTION" = "$OVERLAY" ] && SELECTED="selected" || SELECTED=""

#	                          for LOADED in $(cat ${TMPPATH}/${TEMPDIR}/LOADED_OVERLAYS)
#	                          do
#	                              if ([ "${LOADED%,*}" = "$(echo ${OVERLAY/.txt/})" ] || [ "${LOADED}" = "$(echo ${OVERLAY/.txt/})" ]); then
#	                                  AS="***"
#	                                  break
#	                               else
#	                                  AS=""
#	                              fi
#	                          done

	                          echo '                    <option value="'$OVERLAY'" '$SELECTED'>'$(echo ${OVERLAY/.txt/})$AS'</option>'
	                      done

echo '                  </select>'
echo '                </td>'
echo '                <td>'
echo '                  <p>Overlays to show&nbsp;&nbsp;'
echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                  </p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <p>The overlays are located in /mnt/mmcblk0p1/overlays</p>'
#echo '                    <p>Overlays marked *** are currently loaded.</p>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td colspan="2">'
echo '                  <input type="submit" name="ACTION" value="Show">'
echo '                </td>'
echo '              </tr>'
echo '            </table>'
echo '          </form>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------

#------------------------------------------Overlay text area-----------------------------
pcp_overlay_show() {
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>'$(echo ${SELECTION/.txt/})' overlay</legend>'
	echo '          <table class="bggrey percent100">'
	echo '            <tr>'
	echo '              <td>'
	                      pcp_textarea_inform "none" 'cat ${TMPPATH}/${TEMPDIR}/$SELECTION' 250
	echo '              </td>'
	echo '            </tr>'
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
}
[ "$ACTION" = "Show" ] && pcp_overlay_show
#----------------------------------------------------------------------------------------

#------------------------------------------Overlay text area-----------------------------
pcp_overlay_loaded() {
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Loaded overlays</legend>'
	echo '          <table class="bggrey percent100">'
	echo '            <tr>'
	echo '              <td>'
	                      pcp_textarea_inform "none" 'cat ${TMPPATH}/${TEMPDIR}/LOADED_OVERLAYS' 50
	echo '              </td>'
	echo '            </tr>'
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
}
pcp_overlay_loaded
#----------------------------------------------------------------------------------------

pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'
