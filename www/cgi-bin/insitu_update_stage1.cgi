#!/bin/sh

# Version: 6.0.0 2010-08-16

. pcp-functions

pcp_html_head "Update pCP" "GE"

pcp_banner
pcp_navigation
pcp_running_script
pcp_httpd_query_string

WGET_IUS1="/bin/busybox wget -T 30"
FAIL_MSG="ok"

# As all the insitu update is done in one file, it may be better to define this here
UPD_PCP="/tmp/pcp_insitu_update"
#INSITU_DOWNLOAD=<----- defined in pcp-functions otherwise the beta testing does not work

#========================================================================================
# DEBUG info showing variables
#----------------------------------------------------------------------------------------
pcp_debug_info() {
	pcp_debug_variables "html" QUERY_STRING ACTION VERSION UPD_PCP INSITU_DOWNLOAD SPACE_REQUIRED
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
# Download a list of piCorePlayer versions that are available on pCP repo - insitu.cfg
#----------------------------------------------------------------------------------------
pcp_get_insitu_cfg() {
	if [ -d $UPD_PCP ]; then
		sudo rm -rf $UPD_PCP
		[ $? -ne 0 ] && FAIL_MSG="Can not remove directory $UPD_PCP"
	fi
	sudo mkdir -m 755 $UPD_PCP
	echo '[ INFO ] Step 1. - Downloading insitu.cfg...'
	$WGET_IUS1 ${INSITU_DOWNLOAD}/insitu.cfg -O ${UPD_PCP}/insitu.cfg
	if [ $? -eq 0 ]; then
		echo '[  OK  ] Successfully downloaded insitu.cfg'
	else
		echo '[ ERROR ] Error downloading insitu.cfg'
		FAIL_MSG="Error downloading insitu.cfg"
	fi
}

#========================================================================================
# Download the new update script from repo - insitu_update_stage2.cgi
#----------------------------------------------------------------------------------------
pcp_get_newinstaller() {
	echo '[ INFO ] Step 2A. - Removing the old update script...'
	sudo rm "${PCPHOME}/insitu_update_stage2.cgi"
	echo '[ INFO ] Step 2B. - Downloading the new update script for '$VERSION'...'

	# The web storage does not allow for cgi downloads.
	PACKAGE="insitu_update_stage2.gz"
	[ -e ${PCPHOME}/${PACKAGE} ] && rm -f ${PCPHOME}/${PACKAGE}
	$WGET_IUS1 ${INSITU_DOWNLOAD}/${VERSION}/${PACKAGE} -P ${PCPHOME} > /dev/null 2>&1
	if [ $? -eq 0 ]; then
		echo '[  OK  ] Successfully downloaded the new update script.'
		gunzip ${PCPHOME}/${PACKAGE}
		if [ $? -eq 0 ]; then
			mv -f ${PCPHOME}/insitu_update_stage2 ${PCPHOME}/insitu_update_stage2.cgi
			sudo chmod u=rwx,g=rx,o= "${PCPHOME}/insitu_update_stage2.cgi"
			sudo dos2unix "${PCPHOME}/insitu_update_stage2.cgi"
			sudo chown tc:staff "${PCPHOME}/insitu_update_stage2.cgi"
		else
			echo '[ ERROR ] Downloaded update script is corrupted.'
			FAIL_MSG="Downloaded update script is corrupted."
		fi
	else
		echo '[ ERROR ] Error downloading the update script.'
		FAIL_MSG="Error downloading the update script."
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
	echo '          <table class="bggrey percent100">'
	echo '            <tr class="warning">'
	echo '              <td>'
	echo '                <p><b>Warning:</b></p>'
	echo '                <ul>'
	echo '                  <li>Assume an insitu update will overwrite ALL the data on your SD card.</li>'
	echo '                  <li>Any user modified or added files may be lost or overwritten.</li>'
	echo '                  <li>An insitu update requires about 50% free space.</li>'
	echo '                  <li>Boot files config.txt and cmdline.txt will be overwritten.</li>'
	echo '                  <li>You may need to manually update your plugins, extensions, static IP etc.</li>'
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
		STEP="Step 1 - Checking network"
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
	echo '[ INFO ] You are currently using piCorePlayer v'$(pcp_picoreplayer_version)
	[ "$FAIL_MSG" = "ok" ] && pcp_get_insitu_cfg
fi
#----------------------------------------------------------------------------------------
if [ "$ACTION" = "download" ]; then
	echo '[ INFO ] You are downloading the update script.'
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
#========================================================================================
# Initial
#----------------------------------------------------------------------------------------
case $(uname -r) in
	*pcpAudioCore*) PCPAUDIOCOREyes="checked";PCPCOREyes="";;
	*) PCPCOREyes="checked";PCPAUDIOCORE="";;
esac
COL1=50
COL2=300
if [ "$ACTION" = "initial" ] && [ "$FAIL_MSG" = "ok" ] ; then
	pcp_incr_id
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>piCorePlayer insitu update: Select Kernel Type and Version</legend>'
	echo '          <form name="initial" action= "'$0'" method="get">'
	echo '            <table class="bggrey percent100">'
	pcp_start_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column'$COL1' center">'
	echo '                  <input class="small1" type="radio" name="CORE" value="pcpCore" '$PCPCOREyes'>'
	echo '                </td>'
	echo '                <td class="column'$COL2'">'
	echo '                  <p>Standard version [Recommended]</p>'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>pcpCore Kernel&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>This version is recommended for 99% of users.</p>'
	echo '                    <p>This version uses the kernel code and config from <a href="https://github.com/raspberrypi/linux">Raspberry Pi</a>.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column'$COL1' center">'
	echo '                  <input class="small1" type="radio" name="CORE" value="pcpAudioCore" '$PCPAUDIOCOREyes'>'
	echo '                </td>'
	echo '                <td class="column'$COL2'">'
	echo '                  <p>Audio enthusiast version [Experimental]</p>'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>pcpAudioCore Kernel&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>This version is recommended for experimenters only.</p>'
	echo '                    <p>This version starts with the same kernel code from <a href="https://github.com/raspberrypi/linux">Raspberry Pi</a>.</p>'
	echo '                    <p>The kernel is then patched with extra drivers and modifications to support additional custom DACs and higher sample rates.</p>'
	echo '                    <p>This version should not be used with WIFI.  Some wifi chips are known to not work with this version.</p>'
	echo '                    <p>This version should not be used for server applications such as LMS.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="large18 center">'
	echo '                  <select name="VERSION">'
	                          awk '{ print "<option value=\""$1"\">" $1"</option>" }' ${UPD_PCP}/insitu.cfg
	echo '                  </select>'
	echo '                </td>'
	echo '                <td colspan="2">'
	echo '                  <p>Select the update version of piCorePlayer required.</p>'
	echo '                </td>'
	echo '              </tr>'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="large18 center">'
	echo '                  <input class="large12" type="submit" value="Next >">'
	echo '                  <input type="hidden" name="ACTION" value="download">'
	echo '                </td>'
	echo '                <td colspan="2">'
	echo '                  <p>Press the [ Next > ] button to download version installer.</p>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </table>'
	echo '          </form>'
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
	echo '          <form name="download" action= "insitu_update_stage2.cgi">'
	echo '            <table class="bggrey percent100">'
	pcp_start_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="large18 center">'
	echo '                  <input type="submit" value="Next >">'
	echo '                  <input type="hidden" name="ACTION" value="download">'
	echo '                  <input type="hidden" name="CORE" value="'$CORE'">'
	echo '                  <input type="hidden" name="VERSION" value="'$VERSION'">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Press the [ Next > ] button to start the update process.</p>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </table>'
	echo '          </form>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
fi

#========================================================================================
pcp_html_end
