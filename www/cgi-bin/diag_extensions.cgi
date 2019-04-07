#!/bin/sh

# Version: 5.0.0 2019-04-07

#========================================================================================
# This script checks for required extensions in repositories.
#----------------------------------------------------------------------------------------
. /etc/init.d/tc-functions
. pcp-functions
. pcp-lms-functions

pcp_html_head "Diagnostics extensions" "GE"

pcp_banner
pcp_navigation

#========================================================================================
# Set variables
#----------------------------------------------------------------------------------------
PCP_REPO=${PCP_REPO}/
KERNELVER=$(uname -r)
EXTENLIST="/tmp/pcp_extensions.lst"
WGET="/bin/busybox wget"
getMirror

#VERBOSE=TRUE

#ValidMajorVer="8.x 9.x 10.x"
#ValidBuild="ARM6 ARM7"

#========================================================================================
# Generate a list of REQUIRED DOWNLOADED EXTENSIONS (alphabetically sorted)
#
# NOTE: This list must be maintained MANUALLY.
#----------------------------------------------------------------------------------------
pcp_downloaded_extensions() {
	VERSION=$(echo ${KERNELVER} | awk -F"-" '{print $1}')
	echo alsa-modules-${VERSION}-pcpCore.tcz     > $EXTENLIST
	echo alsa-modules-${VERSION}-pcpCore_v7.tcz >> $EXTENLIST
	echo alsa-utils.tcz                         >> $EXTENLIST
	echo alsa.tcz                               >> $EXTENLIST
	echo ca-certificates.tcz                    >> $EXTENLIST
	echo crda.tcz                               >> $EXTENLIST
	echo dialog.tcz                             >> $EXTENLIST
	echo firmware-atheros.tcz                   >> $EXTENLIST
	echo firmware-brcmwifi.tcz                  >> $EXTENLIST
	echo firmware-ralinkwifi.tcz                >> $EXTENLIST
	echo firmware-rpi-wifi.tcz                  >> $EXTENLIST
	echo firmware-rtlwifi.tcz                   >> $EXTENLIST
	echo libasound.tcz                          >> $EXTENLIST
	echo libedit.tcz                            >> $EXTENLIST
	echo libiw.tcz                              >> $EXTENLIST
	echo libnl.tcz                              >> $EXTENLIST
	echo ncurses.tcz                            >> $EXTENLIST
	echo net-usb-${VERSION}-pcpCore.tcz         >> $EXTENLIST
	echo net-usb-${VERSION}-pcpCore_v7.tcz      >> $EXTENLIST
	echo never_remove.tcz                       >> $EXTENLIST
	echo openssh.tcz                            >> $EXTENLIST
	echo openssl.tcz                            >> $EXTENLIST
	echo pcp.tcz                                >> $EXTENLIST
	echo pcp-base.tcz                           >> $EXTENLIST
	echo pcp-libfaad2.tcz                       >> $EXTENLIST
	echo pcp-libflac.tcz                        >> $EXTENLIST
	echo pcp-libmad.tcz                         >> $EXTENLIST
	echo pcp-libmpg123.tcz                      >> $EXTENLIST
	echo pcp-libogg.tcz                         >> $EXTENLIST
	echo pcp-libsoxr.tcz                        >> $EXTENLIST
	echo pcp-libvorbis.tcz                      >> $EXTENLIST
	echo pcp-squeezelite.tcz                    >> $EXTENLIST
	echo readline.tcz                           >> $EXTENLIST
	echo wireless-${VERSION}-pcpCore.tcz        >> $EXTENLIST
	echo wireless-${VERSION}-pcpCore_v7.tcz     >> $EXTENLIST
	echo wireless_tools.tcz                     >> $EXTENLIST
	echo wiringpi.tcz                           >> $EXTENLIST
	echo wpa_supplicant.tcz                     >> $EXTENLIST
	unset VERSION
}

#========================================================================================
# Routines
#----------------------------------------------------------------------------------------
pcp_internet() {
	if [ $(pcp_internet_accessible) -eq 0 ]; then
		pcp_green_tick "Internet accessible."
		echo "[  OK  ] Internet accessible." >> $LOG
		INTERNET_ACCESSIBLE=TRUE
	else
		pcp_red_cross "Internet not accessible."
		echo "[ ERROR ] Internet not accessible." >> $LOG
		unset INTERNET_ACCESSIBLE
	fi
}

pcp_picore_repo_1() {
	if [ $(pcp_picore_repo_1_accessible) -eq 0 ]; then
		pcp_green_tick "Official piCore repository accessible ($PICORE_REPO_1)."
		echo "[  OK  ] Official piCore repository accessible. ($PICORE_REPO_1)" >> $LOG
		PICORE_REPO_1_ACCESSIBLE=TRUE
	else
		pcp_red_cross "Official piCore repository not accessible ($PICORE_REPO_1)."
		echo "[ ERROR ] Official piCore repository not accessible. ($PICORE_REPO_1)" >> $LOG
		unset PICORE_REPO_1_ACCESSIBLE
	fi
}

pcp_picore_repo_2() {
	if [ $(pcp_picore_repo_2_accessible) -eq 0 ]; then
		pcp_green_tick "Official piCore mirror repository accessible ($PICORE_REPO_2)."
		echo "[  OK  ] Official piCore mirror repository accessible. ($PICORE_REPO_2)" >> $LOG
		PICORE_REPO_2_ACCESSIBLE=TRUE
	else
		pcp_red_cross "Official piCore mirror repository not accessible ($PICORE_REPO_2)."
		echo "[ ERROR ] Official piCore mirror repository not accessible. ($PICORE_REPO_2)" >> $LOG
		unset PICORE_REPO_2_ACCESSIBLE
	fi
}

pcp_pcp_repo() {
	if [ $(pcp_pcp_repo_accessible) -eq 0 ]; then
		pcp_green_tick "piCorePlayer SourceForge repository accessible ($PCP_REPO)."
		echo "[  OK  ] piCorePlayer SourceForge repository accessible. ($PCP_REPO)" >> $LOG
		PCP_REPO_ACCESSIBLE=TRUE
	else
		pcp_red_cross "piCorePlayer SourceForge repository not accessible ($PCP_REPO)."
		echo "[ ERROR ] piCorePlayer SourceForge repository not accessible. ($PCP_REPO)" >> $LOG
		unset PCP_REPO_ACCESSIBLE
	fi
}

pcp_set_repo() {
	MIRROR="${1}/$(getMajorVer).x/$(getBuild)/tcz"
	echo "" | tee -a $LOG
	echo "[ INFO ] Set repository to ${MIRROR}" | tee -a $LOG
}

pcp_check_extension() {
	$WGET --spider "${MIRROR}/$1"
	if [ $? -eq 0 ]; then
		echo "[  OK  ] ${MIRROR}/$1" | tee -a $LOG
	else
		echo "[ FAIL ] ${MIRROR}/$1" | tee -a $LOG
	fi
}

pcp_extn_message() {
	echo "" | tee -a $LOG
	echo "[ INFO ] Checking extensions for ${1}..." | tee -a $LOG
}

#========================================================================================
# Display debug information
#----------------------------------------------------------------------------------------
pcp_debug_info() {
	if [ $DEBUG -eq 1 ]; then
		echo '<!-- Start of debug info -->'
		pcp_debug_variables "html" PICORE_REPO_1 PICORE_REPO_2 PCP_REPO LOG
		echo '<!-- End of debug info -->'
	fi
}

#========================================================================================
# Javascript - move to picoreplayer.js
#----------------------------------------------------------------------------------------
pcp_indicator_js() {
	echo '<script>'
	echo 'var theIndicator = document.querySelector("#indicator'$ID'");'
	echo '	theIndicator.classList.add("'$CLASS'");'
	echo '	document.getElementById("indicator'$ID'").innerHTML = "'$INDICATOR'";'
	echo '	document.getElementById("status'$ID'").innerHTML = "'$STATUS'";'
	echo '</script> '
}

#========================================================================================
# Main
#----------------------------------------------------------------------------------------
pcp_running_script
pcp_debug_info
pcp_log_header $0

#----------------------------------------------------------------------------------------
# Repository accessibility indicators.
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Checking repositories accessiblity. . . </legend>'
echo '          <table class="bggrey percent100">'
#--------------------------------------Internet accessible-------------------------------
pcp_start_row_shade
pcp_incr_id
echo '            <tr class="'$ROWSHADE'">'
echo '              <td class="column50 center">'
echo '                <p id="indicator'$ID'">?</p>'
echo '              </td>'
echo '              <td>'
echo '                <p id="status'$ID'">Checking internet...</p>'
echo '              </td>'
echo '            </tr>'
pcp_internet
pcp_indicator_js
#--------------------------------------Official piCore repository accessible-------------
pcp_toggle_row_shade
pcp_incr_id
echo '            <tr class="'$ROWSHADE'">'
echo '              <td class="column50 center">'
echo '                <p id="indicator'$ID'">?</p>'
echo '              </td>'
echo '              <td>'
echo '                <p id="status'$ID'">Checking piCore repository...</p>'
echo '              </td>'
echo '            </tr>'
pcp_picore_repo_1
pcp_indicator_js
#--------------------------------------Official piCore mirror repository accessible------
if [ $MODE -ge $MODE_DEVELOPER ]; then
	pcp_toggle_row_shade
	pcp_incr_id
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column50 center">'
	echo '                <p id="indicator'$ID'">?</p>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p id="status'$ID'">Checking piCore mirror repository...</p>'
	echo '              </td>'
	echo '            </tr>'
	pcp_picore_repo_2
	pcp_indicator_js
fi
#--------------------------------------piCorePlayer SourceForge repository accessible----
pcp_toggle_row_shade
pcp_incr_id
echo '            <tr class="'$ROWSHADE'">'
echo '              <td class="column50 center">'
echo '                <p id="indicator'$ID'">?</p>'
echo '              </td>'
echo '              <td>'
echo '                <p id="status'$ID'">Checking piCorePlayer SourceForge repository...</p>'
echo '              </td>'
echo '            </tr>'
pcp_pcp_repo
pcp_indicator_js
#----------------------------------------------------------------------------------------
echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------

#========================================================================================
#  Check standard extensions are downloaded.
#  Check for extra extensions.
#----------------------------------------------------------------------------------------
echo "" >> $LOG 
echo "List of standard extensions" >> $LOG
echo "---------------------------" >> $LOG
echo "" >> $LOG

echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Checking the standard extensions are downloaded . . .</legend>'
echo '          <table class="bggrey percent100">'
pcp_start_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td>'
echo '                <textarea class="inform" style="height:300px">'

echo "[ INFO  ] The list of standard extensions must be maintained MANUALLY." | tee -a $LOG
pcp_downloaded_extensions
for i in $(cat $EXTENLIST)
do
	if [ -f /$TCEMNT/tce/optional/${i} ]; then
		[ $VERBOSE ] && echo "[ FOUND ] $i" | tee -a $LOG
	else
		echo "[ MISSING ] $i" | tee -a $LOG
	fi
done 

echo '                </textarea>'
echo '              </td>'
echo '            </tr>'
echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------
echo "" >> $LOG
echo "List of additional (non-standard) extensions" >> $LOG
echo "--------------------------------------------" >> $LOG
echo "" >> $LOG

echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Checking for extra extensions . . .</legend>'
echo '          <table class="bggrey percent100">'
pcp_start_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td>'
echo '                <textarea class="inform" style="height:300px">'

EXTNS=$(ls $TCEMNT/tce/optional/*.tcz | awk -F 'optional/' '{print $2}')

for i in $EXTNS
do
	if grep $i $EXTENLIST >/dev/null 2>&1; then
		[ $VERBOSE ] && echo "[ OK ] $i"  | tee -a $LOG
	else
		echo "[ EXTRA ] $i" | tee -a $LOG
	fi
done 

echo '                </textarea>'
echo '              </td>'
echo '            </tr>'
echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------

echo "" >> $LOG
ls $TCEMNT/tce/optional/*.tcz | awk -F 'optional/' '{print $2}' > /tmp/downloadedextensions
pcp_write_to_log "Downloaded extensions" "cat /tmp/downloadedextensions"
pcp_write_to_log "Installed extensions" "tce-status -i"
pcp_write_to_log "Uninstalled extensions" "tce-status -u"

#--------------------------------------Warning message-----------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Warning</legend>'
echo '          <table class="bggrey percent100">'
echo '            <tr class="warning">'
echo '              <td>'
echo '                <p style="color:white">The checks below only refer to extensions for:</p>'
echo '                <ul>'
echo '                  <li style="color:white">Kernel: '${KERNELVER}'</li>'
echo '                  <li style="color:white">Major version: '$(getMajorVer)'.x</li>'
echo '                  <li style="color:white">Build version: '$(getBuild)'</li>'
echo '                </ul>'
echo '              </td>'
echo '            </tr>'
echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Checking extensions. . .</legend>'
echo '          <table class="bggrey percent100">'
pcp_start_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td>'
echo '                  <textarea class="inform" style="height:300px">'

echo "" >> $LOG
echo "Checking repositories for extensions" >> $LOG

#========================================================================================
pcp_set_repo ${PCP_REPO%/}
#========================================================================================
pcp_extn_message "LIRC"
#-----------------
pcp_check_extension pcp-lirc.tcz
pcp_check_extension libcofi.tcz
pcp_check_extension media-rc-${KERNELVER}.tcz
#----------------------------------------------------------------------------------------
pcp_extn_message "Raspberry Pi Touch Screen"
#--------------------------------------
pcp_check_extension touchscreen-${KERNELVER}.tcz
pcp_check_extension libts.tcz
#----------------------------------------------------------------------------------------
pcp_extn_message "Jivelite"
#---------------------
pcp_check_extension libts.tcz
pcp_check_extension libcofi.tcz
pcp_check_extension pcp-jivelite.tcz
pcp_check_extension pcp-jivelite_hdskins.tcz
pcp_check_extension VU_Meter_Kolossos_Oval.tcz
pcp_check_extension VU_Meter_Jstraw_Dark.tcz
pcp_check_extension VU_Meter_Jstraw_Dark_Peak.tcz
pcp_check_extension VU_Meter_Jstraw_Vintage.tcz
pcp_check_extension VU_Meter_Logitech_Black.tcz
pcp_check_extension VU_Meter_Logitech_White.tcz
#----------------------------------------------------------------------------------------
pcp_extn_message "Audiophonics"
#-------------------------
pcp_check_extension Audiophonics-powerscript.tcz
#----------------------------------------------------------------------------------------
pcp_extn_message "LMS"
#----------------
pcp_check_extension slimserver.tcz
pcp_check_extension slimserver-CPAN.tcz
pcp_check_extension perl5.tcz
pcp_check_extension gcc_libs.tcz
pcp_check_extension openssl.tcz
pcp_check_extension ca-certificates.tcz
pcp_check_extension perl_io_socket_ssl.tcz
pcp_check_extension perl_mozilla_ca.tcz
pcp_check_extension perl_net_ssleay.tcz
pcp_check_extension perl_crypt_openssl_rsa.tcz
pcp_check_extension perl_common_sense.tcz
pcp_check_extension perl_linux_inotify2.tcz
#----------------------------------------------------------------------------------------
pcp_extn_message "Broadcom USB wifi adaptor"
#--------------------------------------
pcp_check_extension firmware-brcmwifi.tcz
#----------------------------------------------------------------------------------------
pcp_extn_message "Shairport-sync"
#---------------------------
pcp_check_extension pcp-shairportsync.tcz
pcp_check_extension libcofi.tcz
#----------------------------------------------------------------------------------------
pcp_extn_message "ALSA equaliser"
#---------------------------
pcp_check_extension alsaequal.tcz
pcp_check_extension caps-0.4.5.tcz
#----------------------------------------------------------------------------------------
pcp_extn_message "networking"
#-----------------------
pcp_check_extension ntfs-3g.tcz
pcp_check_extension filesystems-${KERNELVER}.tcz
pcp_check_extension net-usb-${KERNELVER}.tcz
#----------------------------------------------------------------------------------------

#========================================================================================
pcp_set_repo ${PICORE_REPO_1%/}
#========================================================================================
pcp_extn_message "standard extensions"
#--------------------------------
pcp_check_extension alsa-modules-${KERNELVER}.tcz
pcp_check_extension alsa-utils.tcz
pcp_check_extension alsa.tcz
pcp_check_extension dialog.tcz
pcp_check_extension libasound.tcz
pcp_check_extension libedit.tcz
pcp_check_extension libiw.tcz
pcp_check_extension libnl.tcz
pcp_check_extension ncurses.tcz
pcp_check_extension openssh.tcz
pcp_check_extension openssl.tcz
pcp_check_extension readline.tcz
#----------------------------------------------------------------------------------------
pcp_extn_message "pastebin"
#---------------------
pcp_check_extension wget.tcz
#----------------------------------------------------------------------------------------
pcp_extn_message "wifi"
#-----------------
pcp_check_extension firmware-atheros.tcz
pcp_check_extension firmware-ralinkwifi.tcz
pcp_check_extension firmware-rpi-wifi.tcz
pcp_check_extension firmware-rtlwifi.tcz
pcp_check_extension wireless_tools.tcz
pcp_check_extension wpa_supplicant.tcz
#----------------------------------------------------------------------------------------
pcp_extn_message "wifi diagnositcs"
#-----------------------------
pcp_check_extension usbutils.tcz
#----------------------------------------------------------------------------------------
pcp_extn_message "Common extensions"
#------------------------------
pcp_check_extension nano.tcz
#----------------------------------------------------------------------------------------

echo "" | tee -a $LOG
echo "[ DONE ] Log report complete." | tee -a $LOG

echo '                </textarea>'
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
pcp_copyright

echo '</body>'
echo '</html>'
