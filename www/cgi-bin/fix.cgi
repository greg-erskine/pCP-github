#!/bin/sh

#========================================================================================
# This script is a little different from the normal piCorePlayer scripts.
#
# It uses a md5 checksum to determine if the latest version of the script is installed.
# If it finds a newer script is available it will download a new version.
#
# Generate new md5 file:
# - $ md5sum fix.cgi > fix.cgi.md5.txt
#----------------------------------------------------------------------------------------

# Version: 3.21 2017-05-20
#	Changed to allow booting from USB on RPI3. PH.

# Version: 3.20 2017-04-16
#	Fixed pcp-xxx-functions issues. GE.
#	Updated for 3.11 to be able to insitu update to 3.20. PH

# version: 3.11 2017-01-21
#	Updates for Hotfixes based on piversion.cfg. PH.
#	Added Hotfix3.11. PH.

# version: 0.01 2016-02-21 GE
#	Original.

. pcp-functions

pcp_html_head "Fix pCP" "GE"

pcp_banner
pcp_navigation
pcp_running_script
pcp_httpd_query_string

WGET="/bin/busybox wget -T 30"
FAIL_MSG="ok"
FIX_PCP="/tmp/pcp_fix"
FIX_DOWNLOAD="https://sourceforge.net/projects/picoreplayer/files"
#sourceforge won't let files download from the project-web with cgi in the name.  Leave fix.cgi downloaded from files area.
#FIX_DOWNLOAD="http://picoreplayer.sourceforge.net/insitu"
FIX_CGI="/home/tc/www/cgi-bin"
REBOOT_REQUIRED=0

#========================================================================================
# Fixes
#----------------------------------------------------------------------------------------
pcp_do_fix_1() {
	echo "[ INFO ] Applying fix_1"
	echo "[ INFO ] Adding oprnssl to onboot.lst"
	sudo sed -i '/openssl.tcz/d' $ONBOOTLST
	sudo echo 'openssl.tcz' >> $ONBOOTLST
}

pcp_do_fix_2() {
	# fix for piCorePlayer 2.01
	echo "[ INFO ] Applying fix_2"
	echo "[ INFO ] Fixing insitu_update.cgi"

	FILE="/home/tc/www/cgi-bin/insitu_update.cgi"
	FROM='$WGET -P $UPD_PCP ${INSITU_DOWNLOAD}/insitu.cfg'
	TO='$WGET -O ${UPD_PCP}/insitu.cfg ${INSITU_DOWNLOAD}/insitu.cfg/download'

	sudo sed -i 's@'"${FROM}"'@'"${TO}"'@' $FILE
}

pcp_do_fix_3() {
	# fix for piCorePlayer 2.00
	echo "[ INFO ] Applying fix_3"
	echo "[ INFO ] Fixing upd_picoreplayer.cgi"

	FILE="/home/tc/www/cgi-bin/upd_picoreplayer.cgi"
	FROM='sudo wget -P $UPD_PCP $INSITU_DOWNLOAD/insitu.cfg'
	TO='sudo wget -O ${UPD_PCP}/insitu.cfg ${INSITU_DOWNLOAD}/insitu.cfg/download'

	sudo sed -i 's@'"${FROM}"'@'"${TO}"'@' $FILE
}

pcp_do_fix_4() {
	echo "[ INFO ] Applying fix_4"
	echo "[ INFO ] Fixing writetoaudiotweak.cgi"

	FILE="/home/tc/www/cgi-bin/writetoaudiotweak.cgi"
	FROM='http://sourceforge.net/projects/picoreplayer/files/tce/7.x/ALSAequal/'
	TO='https://sourceforge.net/projects/picoreplayer/files/tce/7.x/ALSAequal/'

	sudo sed -i 's@'"${FROM}"'@'"${TO}"'@' $FILE
}

#we can delete this. Left here for reference right now.  PH.
pcp_do_fixes200() {
	pcp_do_fix_1
	pcp_do_fix_2
	pcp_do_fix_3
	pcp_do_fix_4
}

pcp_do_fixes_311() {
	#Leading / is removed
	#EXE files get set to root.staff mode 755
	HF_FILES_EXE="home/tc/www/cgi-bin/insitu_update_stage1.cgi"
	HFDIR="/tmp/hf"
	HOTFIX="hotfix311a.tgz"
	HOTFIXMD5="${HOTFIX}.md5.txt"
	echo "[ INFO ] Retreiving Hotfix 3.11a."
	rm -rf ${HFDIR}
	mkdir -p ${HFDIR}
	$WGET ${INSITU_DOWNLOAD}/piCorePlayer3.11/${HOTFIX} -O ${HFDIR}/${HOTFIX}
	if [ $? -eq 0 ]; then
		echo '[  OK  ] Successfully downloaded' ${HOTFIX}
	else
		echo '[ ERROR ] Error downloading '${HOTFIX}
		FAIL_MSG="Error downloading ${HOTFIX}"
	fi
	echo "[ INFO ] Retreiving Hotfix 3.11a md5sum"
	$WGET ${INSITU_DOWNLOAD}/piCorePlayer3.11/${HOTFIXMD5} -O ${HFDIR}/${HOTFIXMD5}
	if [ $? -eq 0 ]; then
		echo '[  OK  ] Successfully downloaded' ${HOTFIXMD5}
	else
		echo '[ ERROR ] Error downloading '${HOTFIXMD5}
		FAIL_MSG="Error downloading ${HOTFIX}"
	fi
	if [ "$FAIL_MSG" = "ok" ]; then
		echo "[ INFO ] Verifying Hotfix 3.11a"
		cd ${HFDIR}
		md5sum -sc ${HOTFIXMD5}
		if [ $? -eq 0 ]; then
			echo '[ INFO ] Hotfix Verified.'
		else
			echo '[ ERROR ] '$HOTFIX' verification failed.'
			FAIL_MSG="$HOTFIX verification failed."
		fi
	fi
#Apply the Fix
	if [ "$FAIL_MSG" = "ok" ]; then
		echo '[ INFO ] Extracting Hotfix 3.11a'
		tar xf ${HOTFIX}
		for EXE in ${HF_FILES_EXE}; do
			dos2unix $EXE
			chown tc:staff $EXE
			chmod 750 $EXE
			cp -fp $EXE /${EXE} 
		done
	fi
}

pcp_do_fixes_310() {
	#Leading / is removed
	#EXE files get set to root.staff mode 755
	HF_FILES_EXE="	home/tc/www/cgi-bin/about.cgi home/tc/www/cgi-bin/pcp-soundcard-functions \
		home/tc/www/cgi-bin/lms.cgi home/tc/www/cgi-bin/main.cgi home/tc/www/cgi-bin/writetoaudiotweak.cgi \
		home/tc/www/cgi-bin/writetosamba.cgi home/tc/www/cgi-bin/xtras_staticip.cgi"
	#CFG files get set to root.staff mode 664
	HF_FILES_CFG="usr/local/etc/pcp/cards/HDMI.conf usr/local/sbin/piversion.cfg"
	HFDIR="/tmp/hf"
	HOTFIX="hotfix311.tgz"
	HOTFIXMD5="${HOTFIX}.md5.txt"
	echo "[ INFO ] Retreiving Hotfix 3.11."
	rm -rf ${HFDIR}
	mkdir -p ${HFDIR}
	$WGET ${INSITU_DOWNLOAD}/piCorePlayer3.11/${HOTFIX} -O ${HFDIR}/${HOTFIX}
	if [ $? -eq 0 ]; then
		echo '[  OK  ] Successfully downloaded' ${HOTFIX}
	else
		echo '[ ERROR ] Error downloading '${HOTFIX}
		FAIL_MSG="Error downloading ${HOTFIX}"
	fi
	echo "[ INFO ] Retreiving Hotfix 3.11 md5sum"
	$WGET ${INSITU_DOWNLOAD}/piCorePlayer3.11/${HOTFIXMD5} -O ${HFDIR}/${HOTFIXMD5}
	if [ $? -eq 0 ]; then
		echo '[  OK  ] Successfully downloaded' ${HOTFIXMD5}
	else
		echo '[ ERROR ] Error downloading '${HOTFIXMD5}
		FAIL_MSG="Error downloading ${HOTFIX}"
	fi
	if [ "$FAIL_MSG" = "ok" ]; then
		echo "[ INFO ] Verifying Hotfix 3.11"
		cd ${HFDIR}
		md5sum -sc ${HOTFIXMD5}
		if [ $? -eq 0 ]; then
			echo '[ INFO ] Hotfix Verified.'
		else
			echo '[ ERROR ] '$HOTFIX' verification failed.'
			FAIL_MSG="$HOTFIX verification failed."
		fi
	fi
#Apply the Fix
	if [ "$FAIL_MSG" = "ok" ]; then
		echo '[ INFO ] Extracting Hotfix 3.11'
		tar xf ${HOTFIX}
		for EXE in ${HF_FILES_EXE}; do
			dos2unix $EXE
			chown tc:staff $EXE
			chmod 750 $EXE
			cp -fp $EXE /${EXE} 
		done
		for CFG in ${HF_FILES_CFG}; do
			dos2unix $CFG
			chown root:staff $CFG
			chmod 664 $CFG
			cp -fp $CFG /${CFG}
		done
	fi
	#Apply pcp-functions change with sed, as to not change user modes.
	if [ "$FAIL_MSG" = "ok" ]; then
		FILE="/home/tc/www/cgi-bin/pcp-functions"
		sed -i 's@OUTPUT=\"sysdefault:CARD=ALSA\"@OUTPUT=\"hw:CARD=ALSA\"@' $FILE
	fi
}

#========================================================================================
# DEBUG info showing variables
#----------------------------------------------------------------------------------------
pcp_debug_info() {
	echo '<p class="debug">[ DEBUG ] QUERY_STRING: '$QUERY_STRING'<br />'
	echo '                 [ DEBUG ] FIX_CGI: '$FIX_CGI'<br />'
	echo '                 [ DEBUG ] FIX_PCP: '$FIX_PCP'<br />'
	echo '                 [ DEBUG ] FIX_DOWNLOAD: '$FIX_DOWNLOAD'<br />'
	echo '                 [ DEBUG ] SPACE_REQUIRED: '$SPACE_REQUIRED'</p>'
}

#========================================================================================
# Space required
#
# 12393 fix.cgi
#    42 fix.cgi.md5.txt
# -----
# 12435 ~ 15
#----------------------------------------------------------------------------------------
SPACE_REQUIRED=15

#========================================================================================
# Check we have internet access - set FAIL_MSG if not accessible
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
# Check we have sourceforge access - set FAIL_MSG if not accessible
#----------------------------------------------------------------------------------------
pcp_sourceforge_indicator() {
	if [ $(pcp_sourceforge_accessible) -eq 0 ]; then
		SOURCEFORGE_STATUS="Sourceforge repository accessible."
	else
		SOURCEFORGE_STATUS="Sourceforge repository not accessible!!"
		FAIL_MSG="Sourceforge not accessible!!"
	fi
}

#========================================================================================
# Check for free space - set FAIL_MSG if insufficient space is available
#----------------------------------------------------------------------------------------
pcp_enough_free_space() {
	REQUIRED_SPACE=$1
	FREE_SPACE=$(pcp_free_space k)
	if [ $FREE_SPACE -gt $REQUIRED_SPACE ]; then
		echo '[  OK  ] Free space: '$FREE_SPACE'k - Required space: '$REQUIRED_SPACE'k'
	else
		echo '[ ERROR ] Free space: '$FREE_SPACE'k - Required space: '$REQUIRED_SPACE'k'
		echo '[ ERROR ] Not enough free space - try expanding your partition.'
		FAIL_MSG="Not enough free space - try expanding your partition."
	fi
}

#========================================================================================
# Prepare download directory
#----------------------------------------------------------------------------------------
pcp_create_download_directory() {
	if [ -d $FIX_PCP ]; then
		sudo rm -rf $FIX_PCP
		[ $? -ne 0 ] && FAIL_MSG="Cannot remove directory $FIX_PCP"
	fi
	sudo mkdir -m 755 $FIX_PCP
	[ $? -ne 0 ] && FAIL_MSG="Cannot make directory $FIX_PCP"
}

#========================================================================================
# Download fix.cgi.md5.txt
#----------------------------------------------------------------------------------------
pcp_get_fix_cgi_md5() {
	echo '[ INFO ] Downloading fix.cgi.md5.txt...'
	$WGET ${FIX_DOWNLOAD}/fix.cgi.md5.txt/download -O ${FIX_PCP}/fix.cgi.md5.txt
	if [ $? -eq 0 ]; then
		echo '[  OK  ] Successfully downloaded fix.cgi.md5.txt'
	else
		echo '[ ERROR ] Error downloading fix.cgi.md5.txt'
		FAIL_MSG="Error downloading fix.cgi.md5.txt"
	fi
	if [ "$FAIL_MSG" = "ok" ]
		then
		cp ${FIX_PCP}/fix.cgi.md5.txt ${FIX_CGI}
		if [ $? -eq 0 ]; then
			echo '[  OK  ] Successfully copied fix.cgi.md5.txt to cgi-bin'
		else
			echo '[ ERROR ] Error copying fix.cgi.md5.txt to cgi-bin'
			FAIL_MSG="Error downloading fix.cgi.md5.txt to cgi-bin"
		fi
		chown tc:staff ${FIX_CGI}/fix.cgi.md5.txt
		chmod 644 ${FIX_CGI}/fix.cgi.md5.txt
		fi
}

#========================================================================================
# Download fix.cgi
#----------------------------------------------------------------------------------------
pcp_get_fix_cgi() {
	echo '[ INFO ] Downloading fix.cgi...'
	$WGET ${FIX_DOWNLOAD}/fix.cgi/download -O ${FIX_PCP}/fix.cgi
	if [ $? -eq 0 ]; then
		echo '[  OK  ] Successfully downloaded fix.cgi'
	else
		echo '[ ERROR ] Error downloading fix.cgi'
		FAIL_MSG="Error downloading fix.cgi"
	fi
	if [ "$FAIL_MSG" = "ok" ]
		then
		cp ${FIX_PCP}/fix.cgi ${FIX_CGI}
		if [ $? -eq 0 ]; then
			echo '[  OK  ] Successfully copied fix.cgi to cgi-bin'
		else
			echo '[ ERROR ] Error copying fix.cgi to cgi-bin'
			FAIL_MSG="Error downloading fix.cgi to cgi-bin"
		fi
		chown tc:staff ${FIX_CGI}/fix.cgi
		chmod 750 ${FIX_CGI}/fix.cgi
	fi
}

#========================================================================================
# Check md5 of fix.cgi
#----------------------------------------------------------------------------------------
pcp_check_fix_md5() {
	cd ${FIX_CGI}
	md5sum -sc fix.cgi.md5.txt
	if [ $? -eq 0 ]; then
		echo '[  OK  ] fix.cgi is up-to-date.'
	else
		echo '[ WARN ] fix.cgi is not up-to-date.'
		pcp_get_fix_cgi
	fi
	cd /tmp
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
	echo '                <p style="color:white"><b>Warning:</b> You are about to apply a HotFix to pCP '$(pcp_picoreplayer_version)'.</p>'
	echo '                <ul>'
	echo '                  <li style="color:white">Yes really!!</li>'
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

	pcp_go_main_button
	pcp_footer
	pcp_copyright
	
	if [ "$ACTION" = "fix" ] && [ "$FAIL_MSG" = "ok" ] ; then
		sleep 1
		[ $REBOOT_REQUIRED -eq 1 ] && pcp_reboot_required
	fi
	
	echo '</body>'
	echo '</html>'
	exit
}

#========================================================================================
# Main routine - this is done before any tables are generated
#----------------------------------------------------------------------------------------
case "$ACTION" in
	fix)
		STEP="Step 2 - Do the fixes"
		pcp_warning_message
		;;
	*)
		ACTION="initial"
		STEP="Step 1 - Download latest fix.cgi"
		pcp_warning_message
		pcp_internet_indicator
		[ "$FAIL_MSG" = "ok" ] || pcp_html_end
#		pcp_sourceforge_indicator							#<--- Turn off atm as it may fail
#		[ "$FAIL_MSG" = "ok" ] || pcp_html_end
		pcp_create_download_directory
		[ "$FAIL_MSG" = "ok" ] || pcp_html_end
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
echo '                  <textarea class="inform" style="height:180px">'
#----------------------------------------------------------------------------------------
if [ "$ACTION" = "initial" ]; then
	echo '[ INFO ] '$INTERNET_STATUS
	#echo '[ INFO ] '$SOURCEFORGE_STATUS					#<--- Turn off atm as it may fail
	pcp_enough_free_space $SPACE_REQUIRED
	[ "$FAIL_MSG" = "ok" ] && pcp_get_fix_cgi_md5
	[ "$FAIL_MSG" = "ok" ] && pcp_check_fix_md5
fi
#----------------------------------------------------------------------------------------

if [ "$ACTION" = "fix" ]; then
	case $(pcp_picoreplayer_version) in
		3.10*)
			echo '[ INFO ] Hotfix for pCP 3.10 to address shairport sync issues.'
			[ "$FAIL_MSG" = "ok" ] && pcp_do_fixes_310
			[ "$FAIL_MSG" = "ok" ] && pcp_backup "nohtml"
			[ "$FAIL_MSG" = "ok" ] && echo '[ INFO ] Please Reselect sound card if using USB or HDMI.'
			[ "$FAIL_MSG" = "ok" ] && echo '[ INFO ] Please reinstall shairport-sync for final step.'
		;;
		3.11*)
			echo '[ INFO ] Hotfix for pCP 3.10 to allow insitu_update to 3.20.'
			[ "$FAIL_MSG" = "ok" ] && pcp_do_fixes_311
			[ "$FAIL_MSG" = "ok" ] && pcp_backup "nohtml"
		;;
		*)
			# No Fixes for this version
			echo '[ INFO ] There are no current fixes for '$(pcp_picoreplayer_version)'.'
		;;
	esac
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
# initial screen with [ Next > ] button
#----------------------------------------------------------------------------------------
if [ "$ACTION" = "initial" ] && [ "$FAIL_MSG" = "ok" ]; then
	pcp_incr_id
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Apply fixes</legend>'
	echo '          <table class="bggrey percent100">'
	echo '            <form name="initial" action= "'$0'" method="get">'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="large18 center">'
	echo '                  <input class="large12" type="submit" value="Next >">'
	echo '                  <input type="hidden" name="ACTION" value="fix">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Press the [ Next ] button to apply fix.</p>'
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

pcp_html_end
