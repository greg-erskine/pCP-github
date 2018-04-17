#!/bin/sh

# Version: 4.0.0 2018-04-17
#	Changed repo to new server. PH.

# Version 3.5.0 2018-02-28
#	wget will not over write, make sure package is not present. PH.

# Version 3.21 2017-05-28
#	Modifications for installing to bootdevice. i.e. USB boot. PH.

# Version 3.20 2017-03-25
#	Removed code that is not used until stage2. PH.
#	Change stage2 download to work with web based repo location. PH.

# Version 3.10 2016-12-26
#	Sourceforge repo changes. PH.

# Version 2.05 2016-06-17
#	Original version. SBP.
#	Split from insitu_update.cgi to download new updater before updates. SBP.

. pcp-functions

pcp_html_head "Update pCP" "GE"

pcp_banner
pcp_navigation
pcp_running_script
pcp_httpd_query_string

WGET="/bin/busybox wget -T 30"
FAIL_MSG="ok"

# As all the insitu update is done in one file, it may be better to define this here
UPD_PCP="/tmp/pcp_insitu_update"
#INSITU_DOWNLOAD=<----- defined in pcp-functions otherwise the beta testing does not work

#========================================================================================
# DEBUG info showing variables
#----------------------------------------------------------------------------------------
pcp_debug_info() {
	echo '<p class="debug">[ DEBUG ] QUERY_STRING: '$QUERY_STRING'<br />'
	echo '                 [ DEBUG ] ACTION: '$ACTION'<br />'
	echo '                 [ DEBUG ] VERSION: '$VERSION'<br />'
	echo '                 [ DEBUG ] UPD_PCP: '$UPD_PCP'<br />'
	echo '                 [ DEBUG ] INSITU_DOWNLOAD: '$INSITU_DOWNLOAD'<br />'
	echo '                 [ DEBUG ] SPACE_REQUIRED: '$SPACE_REQUIRED'</p>'
}

#========================================================================================
# Check we have Internet access - set FAIL_MSG if not accessible
#----------------------------------------------------------------------------------------
pcp_internet_indicator() {
	if [ $(pcp_internet_accessible) -eq 0 ]; then
		INTERNET_STATUS="Internet accessible."
	else
		INTERNET_STATUS="Internet not accessible!!"
		FAIL_MSG="Internet not accessible!!"
	fi
}

#========================================================================================
# Check we have repo access - set FAIL_MSG if not accessible
#----------------------------------------------------------------------------------------
pcp_repo_indicator() {
	if [ $(pcp_pcp_repo_accessible) -eq 0 ]; then
		REPO_STATUS="pCP repository accessible."
	else
		REPO_STATUS="pCP repository not accessible!!"
		FAIL_MSG="pCP repo not accessible!!"
	fi
}

#========================================================================================
# Download the new update script from repo - insitu_update_stage2.cgi
#----------------------------------------------------------------------------------------
pcp_get_newinstaller() {
	echo '[ INFO ] Step 2A. - Removing the old Update script...'
	sudo rm "${PCPHOME}/insitu_update_stage2.cgi"
	echo '[ INFO ] Step 2B. - Downloading the new Update script...'

	# The web storage does not allow for cgi downloads.
	PACKAGE="insitu_update_stage2.gz"
	[ -e ${PCPHOME}/${PACKAGE} ] && rm -f ${PCPHOME}/${PACKAGE}
	$WGET ${INSITU_DOWNLOAD}/${PACKAGE} -P ${PCPHOME} > /dev/null 2>&1
	if [ $? -eq 0 ]; then
		echo '[  OK  ] Successfully downloaded the new Update script.'
		gunzip ${PCPHOME}/${PACKAGE}
		if [ $? -eq 0 ]; then
			mv -f ${PCPHOME}/insitu_update_stage2 ${PCPHOME}/insitu_update_stage2.cgi
			sudo chmod u=rwx,g=rx,o= "${PCPHOME}/insitu_update_stage2.cgi"
			sudo dos2unix "${PCPHOME}/insitu_update_stage2.cgi"
			sudo chown tc:staff "${PCPHOME}/insitu_update_stage2.cgi"
		else
			echo '[ ERROR ] Downloaded pdate script is corrupted.'
			FAIL_MSG="Downloaded script is corrupted."
		fi
	else
		echo '[ ERROR ] Error downloading the Update script.'
		FAIL_MSG="Error downloading the Update script"
	fi
}

#========================================================================================
# Generate warning message
#----------------------------------------------------------------------------------------
pcp_warning_message() {
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Warning</legend>'
	echo '          <table class="bggrey percent100">'
	echo '            <tr class="warning">'
	echo '              <td>'
	echo '                <p style="color:white"><b>Warning:</b> Assume an insitu update will overwrite ALL the data on your SD card.</p>'
	echo '                <ul>'
	echo '                  <li style="color:white">Any user modified or added files may be lost.</li>'
	echo '                  <li style="color:white">An insitu update requires about 50% free space.</li>'
	echo '                  <li style="color:white">Boot files config.txt and cmdline.txt will be overwritten.</li>'
	echo '                </ul>'
	echo '              </td>'
	echo '            </tr>'
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
}

#========================================================================================
# Generate status message and finish html page
#----------------------------------------------------------------------------------------
pcp_html_end() {
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Status</legend>'
	echo '          <table class="bggrey percent100">'
	pcp_start_row_shade
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td>'
	echo '                <p>'$FAIL_MSG'</p>'
	echo '              </td>'
	echo '            </tr>'
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
	pcp_footer
	pcp_copyright
	echo '</body>'
	echo '</html>'
	exit
}

#========================================================================================
# Main routine - this is done before any tables are generated
#----------------------------------------------------------------------------------------
case "$ACTION" in
	initial)
		STEP="Step 1 - Checking Network"
		pcp_warning_message
		pcp_internet_indicator
		[ "$FAIL_MSG" = "ok" ] || pcp_html_end
		pcp_repo_indicator
		[ "$FAIL_MSG" = "ok" ] || pcp_html_end
		;;
	download)
		STEP="Step 2 - Downloading files"
		pcp_warning_message
		;;
	*)
		STEP="Invalid ACTION"
		FAIL_MSG="Invalid ACTION: $ACTION"
		;;
esac

#========================================================================================
# First fieldset table
#----------------------------------------------------------------------------------------
pcp_incr_id
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>'$STEP'</legend>'
echo '          <table class="bggrey percent100">'
pcp_start_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td>'
echo '                  <textarea class="inform" style="height:130px">'
#----------------------------------------------------------------------------------------
if [ "$ACTION" = "initial" ]; then
	echo '[ INFO ] '$INTERNET_STATUS
	echo '[ INFO ] '$REPO_STATUS
	echo '[ INFO ] You are currently using piCorePlayer'$(pcp_picoreplayer_version)
fi
#----------------------------------------------------------------------------------------
if [ "$ACTION" = "download" ]; then
	echo '[ INFO ] You are downloading the Update script.'
	[ "$FAIL_MSG" = "ok" ] && pcp_get_newinstaller
fi
#----------------------------------------------------------------------------------------
echo '                  </textarea>'
echo '                </td>'
echo '              </tr>'
#----------------------------------------------------------------------------------------
if [ $DEBUG -eq 1 ]; then
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td>'
	                        pcp_debug_info
	echo '                </td>'
	echo '              </tr>'
fi
#----------------------------------------------------------------------------------------
echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'

#========================================================================================
# Initial
#----------------------------------------------------------------------------------------
if [ "$ACTION" = "initial" ] && [ "$FAIL_MSG" = "ok" ] ; then
	pcp_incr_id
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>piCorePlayer insitu update</legend>'
	echo '          <table class="bggrey percent100">'
	echo '            <form name="initial" action= "'$0'" method="get">'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="large18 center">'
	echo '                  <input class="large12" type="submit" value="Next >">'
	echo '                  <input type="hidden" name="ACTION" value="download">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Press the [ Next ] button to download new update script.</p>'
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
# Download
#----------------------------------------------------------------------------------------
if [ "$ACTION" = "download" ] && [ "$FAIL_MSG" = "ok" ] ; then
	pcp_incr_id
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>piCorePlayer insitu update</legend>'
	echo '          <table class="bggrey percent100">'
	echo '            <form name="download" action= "insitu_update_stage2.cgi">'
	pcp_start_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="large18 center">'
	echo '                  <input type="submit" value="Next" />'
	echo '                  <input type="hidden" name="ACTION" value="initial" />'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Press the [ Next ] button to start the update process.</p>'
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
pcp_html_end
