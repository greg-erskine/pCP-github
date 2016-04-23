#!/bin/sh

# Version 2.05 2016-04-17 SBP
#	Added popup menu to resize partition if too small

# Version: 0.03 2016-02-19 SBP
#	Added code to allow existing add-ons to remain functioning.
#	Fixed sourceforge redirection issue.

# Version: 0.02 2016-02-10 GE
#	Added warning on each page.
#	Added warnings for alsaequal and slimserver.

# version: 0.01 2016-02-03 GE
#	Original - Combined upd_picoreplayer.cgi, insitu.cgi and do_updatepicoreplayer.cgi

. pcp-functions
pcp_variables

pcp_html_head "Update pCP" "GE"

pcp_banner
pcp_navigation
pcp_running_script
pcp_httpd_query_string

WGET="/bin/busybox wget -T 30"
FAIL_MSG="ok"

# As all the insitu upgrade is done in one file, it may be better to define this here
UPD_PCP="/tmp/pcp_insitu_update"
#INSITU_DOWNLOAD="https://sourceforge.net/projects/picoreplayer/files/insitu"  #<----- defined in pcp-functions otherwise the beta testing does not work



#========================================================================================
#      382 - insitu.cfg
# 21044878 - piCorePlayer2.00_boot.tar.gz
# 14932349 - piCorePlayer2.00_tce.tar.gz
# --------
# 35977609 bytes
#----------------------------------------------------------------------------------------
#SPACE_REQUIRED=$((35977609 * 2 / 1000))
SPACE_REQUIRED=21044

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
# Check we have internet access - set FAIL_MSG if not accessible
#----------------------------------------------------------------------------------------
pcp_internet_indicator() {
	if [ $(pcp_internet_accessible) = 0 ]; then
		INTERNET_STATUS="Internet accessible."
	else
		INTERNET_STATUS="Internet not accessible!!"
		FAIL_MSG="Internet not accessible!!"
	fi
}

#========================================================================================
# Check we have sourceforge access - set FAIL_MSG if not accessible
#----------------------------------------------------------------------------------------
pcp_sourceforge_indicator() {
	if [ $(pcp_sourceforge_accessible) = 0 ]; then
		SOURCEFORGE_STATUS="Sourceforge repository accessible."
	else
		SOURCEFORGE_STATUS="Sourceforge repository not accessible!!"
		FAIL_MSG="Sourceforge not accessible!!"
	fi
}

#========================================================================================
# Check for extension - display reload extension warning message
#----------------------------------------------------------------------------------------
pcp_check_for_extension() {
	EXTENSION=$1
	if [ -f "/usr/local/tce.installed/${EXTENSION}" ]; then
		echo '[ WARN ] *** You may need to REINSTALL '$EXTENSION' ***'
	fi
}

pcp_check_for_all_extensions() {
	pcp_check_for_extension jivelite
	pcp_check_for_extension shairport-sync
	pcp_check_for_extension alsaequal
	pcp_check_for_extension slimserver
}

#========================================================================================
# Check for free space - set FAIL_MSG if insufficient space is available
#----------------------------------------------------------------------------------------
pcp_enough_free_space() {
	INITSPACE=0
	REQUIRED_SPACE=$1
	FREE_SPACE=$(pcp_free_space k)
	if [ $FREE_SPACE -gt $REQUIRED_SPACE ]; then
		echo '[  OK  ] Free space: '$FREE_SPACE'k - Required space: '$REQUIRED_SPACE'k'
	else
		echo '[ ERROR ] Free space: '$FREE_SPACE'k - Required space: '$REQUIRED_SPACE'k'
		echo '[ ERROR ] Not enough free space - try expanding your partition.'
		FAIL_MSG="Not enough free space - try expanding your partition."
		INITSPACE=1
	fi
}

#========================================================================================
# Prepare download directories - Do we really need boot and tce directory???
#----------------------------------------------------------------------------------------
pcp_create_download_directory() {
	if [ -d $UPD_PCP ]; then
		sudo rm -rf $UPD_PCP
		[ $? != 0 ] && FAIL_MSG="Can not remove directory $UPD_PCP"
	fi
	sudo mkdir -m 755 $UPD_PCP
	[ $? != 0 ] && FAIL_MSG="Can not make directory $UPD_PCP"
	sudo mkdir ${UPD_PCP}/boot
	[ $? != 0 ] && FAIL_MSG="Can not make directory ${UPD_PCP}/boot"
	sudo mkdir ${UPD_PCP}/tce
	[ $? != 0 ] && FAIL_MSG="Can not make directory ${UPD_PCP}/tce"
	sudo mkdir ${UPD_PCP}/mydata
	[ $? != 0 ] && FAIL_MSG="Can not make directory ${UPD_PCP}/mydata"
}

#========================================================================================
# Download the new update script from Sourceforge - insitu_update_second.cgi
#----------------------------------------------------------------------------------------

pcp_get_newinstaller() {
	echo '[ INFO ] Step 1. - Remove old Update script...'
	sudo rm "${PCPHOME}/insitu_update_second.cgi"
	echo '[ INFO ] Step 2. - Downloading new Update script...'
	$WGET ${INSITU_DOWNLOAD}/insitu_update_second.cgi/download -O ${PCPHOME}/insitu_update_second.cgi
	sudo chmod u=rwx,g=rx,o= "${PCPHOME}/insitu_update_second.cgi"
	
	sudo dos2unix "${PCPHOME}/insitu_update_second.cgi"
	sudo chown tc:staff "${PCPHOME}/insitu_update_second.cgi"
	if [ $? = 0 ]; then
		echo '[  OK  ] Successfully downloaded the new Update script'
	else
		echo '[ ERROR ] Error downloading Update script'
		FAIL_MSG="Error downloading Update script"
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
	echo '                <p style="color:white"><b>Warning:</b> An insitu upgrade will overwrite ALL data on your SD card.</p>'
	echo '                <ul>'
	echo '                  <li style="color:white">Any addtional extensions will need to be reinstalled i.e. jivelite, shairport-sync, alsaequal.</li>'
	echo '                  <li style="color:white">Any modified or additional files will be lost.</li>'
	echo '                  <li style="color:white">An insitu upgrade requires about 50% free space.</li>'
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
# Generate staus message and finish html page
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
case $ACTION in
	initial)
		STEP="Step 1 - Downloading available versions"
		pcp_warning_message
		pcp_internet_indicator
		[ $FAIL_MSG = "ok" ] || pcp_html_end
		pcp_sourceforge_indicator
		[ $FAIL_MSG = "ok" ] || pcp_html_end
		pcp_create_download_directory
		[ $FAIL_MSG = "ok" ] || pcp_html_end
		;;
	download)
		STEP="Step 2 - Downloading files"
		pcp_warning_message
		;;
	install)
		STEP="Step 3 - Installing files"
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
if [ $ACTION = "initial" ]; then
	echo '[ INFO ] '$INTERNET_STATUS
	echo '[ INFO ] '$SOURCEFORGE_STATUS
	echo '[ INFO ] You are currently using piCorePlayer'$(pcp_picoreplayer_version)
fi
#----------------------------------------------------------------------------------------
if [ $ACTION = "download" ]; then
	echo '[ INFO ] You are downloading Update script '
	[ $FAIL_MSG = "ok" ] && pcp_get_newinstaller
fi
#----------------------------------------------------------------------------------------
echo '                  </textarea>'
echo '                </td>'
echo '              </tr>'
#----------------------------------------------------------------------------------------
if [ $DEBUG = 1 ]; then
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
# initial
#----------------------------------------------------------------------------------------
if [ $ACTION = "initial" ] && [ $FAIL_MSG = "ok" ] ; then
	pcp_incr_id
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>piCorePlayer insitu upgrade</legend>'
	echo '          <table class="bggrey percent100">'
	echo '            <form name="initial" action= "'$0'" method="get">'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="large18 center">'
	echo '                  <input class="large12" type="submit" value="Next >">'
	echo '                  <input type="hidden" name="ACTION" value="download">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Press the [ Next ] button to download upgrade script.</p>'
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
# download
#----------------------------------------------------------------------------------------
if [ $ACTION = "download" ] && [ $FAIL_MSG = "ok" ] ; then
	pcp_incr_id
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>piCorePlayer insitu upgrade</legend>'
	echo '          <table class="bggrey percent100">'
	echo '            <form name="download" action= "insitu_update_second.cgi">'
	pcp_start_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="large18 center">'
	echo '                  <input type="submit" value="Next" />'
	echo '                  <input type="hidden" name="ACTION" value="initial" />'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Press the [ Next ] button to install start the upgrade process.</p>'
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
