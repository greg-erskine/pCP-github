#!/bin/sh

# Version: 7.0.0 2020-06-18

. pcp-functions

pcp_html_head "Update pCP" "GE"

pcp_navbar
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
	pcp_message INFO "Step 1. - Downloading insitu.cfg..." "text"
	$WGET_IUS1 ${INSITU_DOWNLOAD}/insitu.cfg -O ${UPD_PCP}/insitu.cfg
	if [ $? -eq 0 ]; then
		pcp_message OK "Successfully downloaded insitu.cfg" "text"
	else
		pcp_message ERROR "Error downloading insitu.cfg" "text"
		FAIL_MSG="Error downloading insitu.cfg"
	fi
}

#========================================================================================
# Download the new update script from repo - insitu_update_stage2.cgi
#----------------------------------------------------------------------------------------
pcp_get_newinstaller() {
	pcp_message INFO "Step 2A. - Removing the old update script..." "text"
	sudo rm "${PCPHOME}/insitu_update_stage2.cgi"
	pcp_message INFO "Step 2B. - Downloading the new update script for $VERSION..." "text"

	# The web storage does not allow for cgi downloads.
	PACKAGE="insitu_update_stage2.gz"
	[ -e ${PCPHOME}/${PACKAGE} ] && rm -f ${PCPHOME}/${PACKAGE}
	$WGET_IUS1 ${INSITU_DOWNLOAD}/${VERSION}/${PACKAGE} -P ${PCPHOME} > /dev/null 2>&1
	if [ $? -eq 0 ]; then
		pcp_message OK "Successfully downloaded the new update script." "text"
		gunzip ${PCPHOME}/${PACKAGE}
		if [ $? -eq 0 ]; then
			mv -f ${PCPHOME}/insitu_update_stage2 ${PCPHOME}/insitu_update_stage2.cgi
			sudo chmod u=rwx,g=rx,o= "${PCPHOME}/insitu_update_stage2.cgi"
			sudo dos2unix "${PCPHOME}/insitu_update_stage2.cgi"
			sudo chown tc:staff "${PCPHOME}/insitu_update_stage2.cgi"
		else
			pcp_message ERROR "Downloaded update script is corrupted." "text"
			FAIL_MSG="Downloaded update script is corrupted."
		fi
	else
		pcp_message ERROR "Error downloading the update script." "text"
		FAIL_MSG="Error downloading the update script."
	fi
}

#========================================================================================
# Generate warning message
#----------------------------------------------------------------------------------------
pcp_warning_message() {
	echo '    <div class="alert alert-primary" role="alert">'
	echo '      <b>Warning:</b>'
	echo '      <ul>'
	echo '        <li>Assume an insitu update will overwrite ALL the data on your SD card.</li>'
	echo '        <li>Any user modified or added files may be lost or overwritten.</li>'
	echo '        <li>An insitu update requires about 50% free space.</li>'
	echo '        <li>Boot files config.txt and cmdline.txt will be overwritten.</li>'
	echo '        <li>You may need to manually update your plugins, extensions, static IP etc.</li>'
	echo '      </ul>'
	echo '    </div>'
}

#========================================================================================
# Generate status message and finish html page
#----------------------------------------------------------------------------------------
pcp_upd_html_end() {
	pcp_heading5 "Status"
	pcp_border_begin
	echo '    <div class="row mx-1">'
	echo '      <div class="col">'
	echo '        <p>'$FAIL_MSG'</p>'
	echo '      </div>'
	echo '    </div>'
	pcp_border_end
	pcp_html_end
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
		[ "$FAIL_MSG" = "ok" ] || pcp_upd_html_end
		pcp_repo_indicator
		[ "$FAIL_MSG" = "ok" ] || pcp_upd_html_end
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

COLUMN3_1="col-sm-2"
COLUMN3_2="col-sm-4"
COLUMN3_3="col-sm"
#========================================================================================
# Main
#----------------------------------------------------------------------------------------
pcp_incr_id

pcp_heading5 "$STEP"
pcp_infobox_begin
#----------------------------------------------------------------------------------------
if [ "$ACTION" = "initial" ]; then
	pcp_message INFO "$INTERNET_STATUS" "text"
	pcp_message INFO "Checking $INSITU_DOWNLOAD:  $REPO_STATUS" "text"
	pcp_message INFO "You are currently using piCorePlayer v"$(pcp_picoreplayer_version) "text"
	[ "$FAIL_MSG" = "ok" ] && pcp_get_insitu_cfg
fi
#----------------------------------------------------------------------------------------
if [ "$ACTION" = "download" ]; then
	pcp_message INFO "You are downloading the update script." "text"
	[ "$FAIL_MSG" = "ok" ] && pcp_get_newinstaller
fi
#----------------------------------------------------------------------------------------
pcp_infobox_end

#----------------------------------------------------------------------------------------
if [ $DEBUG -eq 1 ]; then
	echo '              <div class="row">'
	echo '                <div>'
	                        pcp_debug_info
	echo '                </div>'
	echo '              </div>'
fi
#----------------------------------------------------------------------------------------

#========================================================================================
# Initial
#----------------------------------------------------------------------------------------
case $(uname -r) in
	*pcpAudioCore*) PCPAUDIOCOREyes="checked";PCPCOREyes="";;
	*) PCPCOREyes="checked";PCPAUDIOCORE="";;
esac

if [ "$ACTION" = "initial" ] && [ "$FAIL_MSG" = "ok" ] ; then
	pcp_border_begin
	pcp_heading5 "Select Kernel Type and Version"
	echo '  <form name="initial" action= "'$0'" method="get">'
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN3_1' text-center">'
	echo '        <div class="form-check form-check-inline">'
	echo '          <input class="form-check-input" id="rad1" type="radio" name="CORE" value="pcpCore" '$PCPCOREyes'>'
	echo '        </div>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <p>Standard version [Recommended]</p>'
	echo '      </div>'
	pcp_incr_id
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <p>pcpCore Kernel&nbsp;&nbsp;'
	pcp_helpbadge
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>This version is recommended for 99% of users.</p>'
	echo '          <p>This version uses the kernel code and config from <a href="https://github.com/raspberrypi/linux">Raspberry Pi</a>.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN3_1' text-center">'
	echo '        <div class="form-check form-check-inline">'
	echo '          <input class="form-check-input" id="rad2" type="radio" name="CORE" value="pcpAudioCore" '$PCPAUDIOCOREyes'>'
	echo '        </div>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <p>Audio enthusiast version [Experimental]</p>'
	echo '      </div>'
	pcp_incr_id
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <p>pcpAudioCore Kernel&nbsp;&nbsp;'
	pcp_helpbadge
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>This version is recommended for experimenters only.</p>'
	echo '          <p>This version starts with the same kernel code from <a href="https://github.com/raspberrypi/linux">Raspberry Pi</a>.</p>'
	echo '          <p>The kernel is then patched with extra drivers and modifications to support additional custom DACs and higher sample rates.</p>'
	echo '          <p>This version should not be used with WIFI.  Some wifi chips are known to not work with this version.</p>'
	echo '          <p>This version should not be used for server applications such as LMS.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
	echo '    <div class="row mx-1">'
	echo '      <div class="input-group '$COLUMN3_1'">'
	echo '        <select class="custom-select custom-select-sm" name="VERSION">'
	                awk '{ print "<option value=\""$1"\">" $1"</option>" }' ${UPD_PCP}/insitu.cfg
	echo '        </select>'
	echo '      </div>'
	echo '      <div class="col">'
	echo '        <p>Select the update version of piCorePlayer required.</p>'
	echo '      </div>'
	echo '    </div>'
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN3_1' col-2">'
	echo '        <input class="'$BUTTON'" type="submit" value="Next >">'
	echo '        <input type="hidden" name="ACTION" value="download">'
	echo '      </div>'
	echo '      <div class="col">'
	echo '        <p>Press the [ Next > ] button to download version installer.</p>'
	echo '      </div>'
	echo '    </div>'
	echo '  </form>'
	pcp_border_end
fi
#========================================================================================
# Download
#----------------------------------------------------------------------------------------
if [ "$ACTION" = "download" ] && [ "$FAIL_MSG" = "ok" ]; then
	pcp_border_begin
	pcp_heading5 "piCorePlayer insitu update"
	echo '  <form name="download" action="insitu_update_stage2.cgi">'
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN3_1' col-2">'
	echo '        <input class="'$BUTTON'" type="submit" value="Next >">'
	echo '        <input type="hidden" name="ACTION" value="download">'
	echo '        <input type="hidden" name="CORE" value="'$CORE'">'
	echo '        <input type="hidden" name="VERSION" value="'$VERSION'">'
	echo '      </div>'
	echo '      <div class="col">'
	echo '        <p>Press the [ Next > ] button to start the update process.</p>'
	echo '      </div>'
	echo '    </div>'
	echo '  </form>'
	pcp_border_end
fi

#========================================================================================
pcp_html_end
