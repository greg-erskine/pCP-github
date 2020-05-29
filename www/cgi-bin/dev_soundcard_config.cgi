#!/bin/sh

# Version: 7.0.0 2020-05-17

# Title: Soundcard config files
# Description: Easy method for viewing the Soundcard configuration files

. pcp-functions
. pcp-soundcard-functions

pcp_html_head "Show Soundcard Config File" "GE"

pcp_navbar
pcp_httpd_query_string

PCPSOUNDCARDS=$(ls "${DACLOCATION}")

#========================================================================================
# Routines
#----------------------------------------------------------------------------------------
pcp_overlays_loaded() {
	pcp_mount_bootpart >/dev/null 2>&1
	OVERLAYS=$(cat ${VOLUME}/config.txt | grep ^dtoverlay | sed 's/dtoverlay=//')
	pcp_umount_bootpart >/dev/null 2>&1
}
pcp_overlays_loaded

#========================================================================================
# Selection form
#----------------------------------------------------------------------------------------
pcp_border_begin
pcp_heading5 "Select soundcard config file"
echo '  <form name="soundcard" action="'$0'" method="get">'
#----------------------------------------------------------------------------------------
echo '    <div class="row mx-1">'
echo '      <div class="input-group col-3">'
echo '        <select class="custom-select custom-select-sm" name="SELECTION">'

	            for CARD in $PCPSOUNDCARDS
	            do
	                [ "$SELECTION" = "$CARD" ] && SELECTED="selected" || SELECTED=""
	                echo '           <option value="'$CARD'" '$SELECTED'>'$(echo ${CARD/.conf/})'</option>'
	            done

echo '        </select>'
echo '      </div>'
pcp_incr_id
echo '      <div class="col-9">'
echo '        <p>Show soundcard config file&nbsp;&nbsp;'
echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
echo '        </p>'
echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
echo '          <p>The soundcard config files are located in '$DACLOCATION'</p>'
echo '        </div>'
echo '      </div>'
echo '    </div>'
echo '    <div class="row mx-1 mb-2">'
echo '      <div class="col-2">'
echo '        <input class="'$BUTTON'" type="submit" name="ACTION" value="Show">'
echo '      </div>'
echo '    </div>'
#----------------------------------------------------------------------------------------
echo '  </form>'
pcp_border_end
#----------------------------------------------------------------------------------------
pcp_hr
#------------------------------------Soundcard text--------------------------------------
pcp_soundcard_show() {
	pcp_heading5 "$(echo ${SELECTION/.conf/}) config file"
	LINES=$(wc -l ${DACLOCATION}/$SELECTION)
	pcp_textarea "none" 'cat ${DACLOCATION}/$SELECTION' $LINES
}
[ "$ACTION" = "Show" ] && pcp_soundcard_show
#----------------------------------------------------------------------------------------

#------------------------------------Loaded overlays-------------------------------------
pcp_heading5 "Loaded overlays"
pcp_textarea "none" "echo $OVERLAYS | sed 's/ /\n/g'" 2
#----------------------------------------------------------------------------------------

pcp_html_end
exit
