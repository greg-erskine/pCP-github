#!/bin/sh

# Version: 7.0.0 2020-06-16

# Title: Overlays README
# Description: Easy method for viewing the README file in /mnt/mmcblk0p1/overlays

. pcp-functions

pcp_html_head "View the Overlay Readme" "GE"

pcp_navbar
pcp_httpd_query_string

TMPPATH="/tmp"
TEMPDIR="dbt"

#========================================================================================
# NOTE: Very inefficient ATM
#       Reads README and generates new files every time you hit [ Show ] button.
#----------------------------------------------------------------------------------------

#========================================================================================
# Functions
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

COLUMN1="col-4"
COLUMN2="col-8"
COLUMN3="col-2"

#========================================================================================
# Selection form
#----------------------------------------------------------------------------------------
pcp_border_begin
pcp_heading5 "Select overlay"
echo '    <form name="log" action="'$0'" method="get">'
echo '      <div class="row mx-1">'
echo '        <div class="input-group '$COLUMN1'">'
echo '          <select class="custom-select custom-select-sm" name="SELECTION">'

	              for OVERLAY in $PCPOVERLAYS
	              do
	                  [ "$SELECTION" = "$OVERLAY" ] && SELECTED="selected" || SELECTED=""
	                  echo '            <option value="'$OVERLAY'" '$SELECTED'>'$(echo ${OVERLAY/.txt/})$AS'</option>'
	              done

echo '          </select>'
echo '        </div>'
pcp_incr_id
echo '        <div class="'$COLUMN2'">'
echo '          <p>Select overlay to show&nbsp;&nbsp;'
pcp_helpbadge
echo '          </p>'
echo '          <div id="dt'$ID'" class="'$COLLAPSE'">'
echo '            <p>The overlays are located in /mnt/mmcblk0p1/overlays</p>'
echo '          </div>'
echo '        </div>'
echo '      </div>'
#----------------------------------------------------------------------------------------
echo '      <div class="row mx-1 mb-2">'
echo '        <div class="'$COLUMN3'">'
echo '          <input type="submit" class="'$BUTTON'" name="ACTION" value="Show">'
echo '        </div>'
echo '      </div>'
echo '    </form>'
pcp_border_end
#----------------------------------------------------------------------------------------
pcp_hr
#-----------------------------------Overlay text area------------------------------------
pcp_overlay_show() {
	pcp_textarea "${SELECTION/.txt/} overlay" 'cat ${TMPPATH}/${TEMPDIR}/$SELECTION' 8
}
[ "$ACTION" = "Show" ] && pcp_overlay_show
#----------------------------------------------------------------------------------------

#------------------------------------Overlays loaded-------------------------------------
pcp_overlay_loaded() {
	pcp_textarea "Loaded overlays" 'cat ${TMPPATH}/${TEMPDIR}/LOADED_OVERLAYS' 3
}
pcp_overlay_loaded
#----------------------------------------------------------------------------------------

pcp_html_end
exit
